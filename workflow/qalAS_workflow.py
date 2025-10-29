"""
QALAS Research Workflow
Author: Esma
Description:
Automated multi-agent workflow that searches PubMed and Arxiv for
QALAS-related MRI studies, summarizes them in Turkish, and can also
explain imaging terms when needed.
"""

import os, json, re
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.azure.openai_chat import AzureOpenAI
from agno.tools.pubmed import PubmedTools
from agno.tools.arxiv import ArxivTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.workflow.workflow import Workflow
from agno.workflow.step import Step
from agno.workflow.condition import Condition
from agno.workflow.types import StepInput, StepOutput
from agents.agents import qalas_pub_agent, arxiv_agent, qalas_analysis_agent

# --- Kaynak seçici ---
# workflow/qalAS_workflow.py

import re

def _has(text, terms):
    q = text.lower()
    return any(t in q for t in terms)

def choose_sources(query: str) -> dict:
    q = (query or "").lower()

    # MRI/QALAS geniş tetikleyiciler (EN/TR + common typos)
    mri_terms = [
        "mri", "quantitative mri", "quantitative-mri", "quantitve mri", "quantitiv mri",
        "quantititve mri", "qalas", "3d-qalas", "relaxometry", "t1", "t2", "pd mapping",
        "manyetik rezonans", "kantitatif mr", "kantitatif mri"
    ]

    pubmed_triggers = [
        "pubmed", "klinik", "validation", "validasyon", "reproducibility",
        "tekrarlanabilirlik", "cross-vendor", "multi-center", "çok merkezli",
        "comparison", "karşılaştırma"
    ]

    arxiv_triggers = ["arxiv", "preprint", "latest", "state-of-the-art", "sota", "en yeni"]


    pubmed = _has(q, pubmed_triggers) or _has(q, mri_terms)
    arxiv  = _has(q, arxiv_triggers)  or _has(q, mri_terms)

    # Güvenli varsayılan: hiçbir şey yakalanmadıysa PubMed + Arxiv aç
    if not (pubmed or arxiv):
        pubmed, arxiv = True, True

    return {"pubmed": pubmed, "arxiv": arxiv}

def source_selector(step_input: StepInput) -> StepOutput:
    query = step_input.input or step_input.previous_step_content or ""
    selection = choose_sources(query)
    print(f"[Router] Selected sources for '{query}': {selection}")  # ✅ Debug çıktısını buradan al
    return StepOutput(content=json.dumps(selection, ensure_ascii=False))  # ✅ log parametresini kaldır


def _read_selector(step_input: StepInput):
    """Always read router ('select_sources') output safely."""
    # Router adımının (select_sources) sonucunu al
    router_output = step_input.get_step_output("select_sources")
    if router_output:
        raw = getattr(router_output, "content", router_output)
    else:
        raw = None

    # JSON parse etmeyi dene
    if isinstance(raw, str):
        raw = raw.strip()
        if raw:
            try:
                data = json.loads(raw)
                print(f"[Selector Reader] Parsed router JSON: {data}")
                return data
            except Exception:
                print(f"[Selector Reader] Router JSON decode failed: {raw}")
                return {}
        else:
            print("[Selector Reader] Router output empty.")
            return {}

    if isinstance(raw, dict):
        print(f"[Selector Reader] Got router dict: {raw}")
        return raw

    print("[Selector Reader] No router output found.")
    return {}


def should_use_pubmed(step_input: StepInput) -> bool:
    d = _read_selector(step_input)
    print(f"[Condition] PUBMED={d.get('pubmed')}")
    return bool(d.get("pubmed", False))

def should_use_arxiv(step_input: StepInput) -> bool:
    d = _read_selector(step_input)
    print(f"[Condition] ARXIV={d.get('arxiv')}")
    return bool(d.get("arxiv", False))


# --- Workflow tanımı ---from agents.agents import qalas_pub_agent, arxiv_agent, qalas_analysis_agent

def qalas_research_workflow(query: str) -> Workflow:
    step_source = Step(name="select_sources", executor=source_selector)
    step_pubmed = Step(name="pubmed_search", agent=qalas_pub_agent)
    step_arxiv = Step(name="arxiv_search", agent=arxiv_agent)

    # 🧩 Yeni adım: sonuçları birleştirip analiz eden agent
    def merge_and_analyze(step_input: StepInput) -> StepOutput:
        pubmed_out = step_input.get_step_output("pubmed_search")
        arxiv_out = step_input.get_step_output("arxiv_search")
        query_text = step_input.input or ""

        combined_text = ""
        if pubmed_out and getattr(pubmed_out, "content", None):
            combined_text += f"\n\n[PubMed Çıktısı]\n{pubmed_out.content}"
        if arxiv_out and getattr(arxiv_out, "content", None):
            combined_text += f"\n\n[Arxiv Çıktısı]\n{arxiv_out.content}"

        if not combined_text.strip():
            combined_text = "Hiç sonuç bulunamadı."

        prompt = f"""
Soru: {query_text}
Aşağıda PubMed ve Arxiv ajanlarının teknik çıktılarını göreceksin.
Bu bilgileri sentezleyerek, soruya akademik düzeyde, Türkçe bir yanıt hazırla.

{combined_text}
"""

        response = qalas_analysis_agent.run(prompt)
        return StepOutput(content=response.content)

    step_analysis = Step(name="analysis_synthesis", executor=merge_and_analyze)

    return Workflow(
        name="QALAS_Research_Workflow",
        description="Automated multi-agent pipeline for QALAS research (PubMed + Arxiv + Analysis).",
        steps=[
            step_source,
            Condition(name="PubMed", evaluator=should_use_pubmed, steps=[step_pubmed]),
            Condition(name="Arxiv", evaluator=should_use_arxiv, steps=[step_arxiv]),
            step_analysis,  # 
        ],
    )
