from workflow.qalAS_workflow import qalas_research_workflow
import os

if __name__ == "__main__":
    query = input("Araştırma konusu: ")
    wf = qalas_research_workflow(query)
    result = wf.run(query)

    print("\n=== QALAS RESEARCH RESULT ===\n")
    print(result.content)

    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/qalas_summary_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Sorgu: {query}\n\n")
        f.write(result.content)

    print(f"\n📝 Arxiv özetleri {filename} dosyasına kaydedildi!")
