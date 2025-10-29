import os, json, re
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.azure.openai_chat import AzureOpenAI
from agno.tools.pubmed import PubmedTools
from agno.tools.arxiv import ArxivTools
from agents.prompts import qalas_pub_prompt, arxiv_agent_prompt, qalas_analysis_prompt


# --- Ortam değişkenleri ---
load_dotenv()


pubmed_tool = PubmedTools()
arxiv_tool = ArxivTools()

your_api_key_here = os.getenv("OPENAI_API_KEY")
# --- PubMed Agent ---
qalas_pub_agent = Agent(
    name="PubMedQALASAgent",
    model=AzureOpenAI(
        "gpt-5-mini",
        api_key=your_api_key_here,
    ),
    reasoning=True,
    markdown=True,
    tools=[pubmed_tool],
    instructions=qalas_pub_prompt
)
arxiv_agent = Agent(
    name="ArxivQALASAgent",
    model=AzureOpenAI(
        "gpt-5-mini",
        api_key=your_api_key_here,

    ),
    reasoning=True,
    markdown=True,
    tools=[arxiv_tool],
    instructions= arxiv_agent_prompt
)


from agno.agent import Agent
from agno.models.azure.openai_chat import AzureOpenAI

qalas_analysis_agent = Agent(
    name="QALASAnalysisAgent",
    model=AzureOpenAI(
        "gpt-5-mini",
        api_key=your_api_key_here,
    ),
    reasoning=True,
    markdown=True,
    instructions=qalas_analysis_prompt
)
