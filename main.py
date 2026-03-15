"""CLI entry point for LLM Data Copilot.

Run the agent in interactive mode:
    python main.py

For the web UI instead:
    streamlit run ui.py
"""
from agents.sql_agent import agent_executor, is_safe_query_llm

if __name__ == "__main__":
    print("🧠 LLM Data Copilot — CLI mode")
    print("   (Web UI: streamlit run ui.py)\n")
    while True:
        question = (
            input("""📌 Enter your question (or 'exit' to quit)\n>> 
                Examples:
                - How many properties do we have per client for the current tax year?
                - What are the total taxable values and tax amounts by client for 2025?
                - Which properties have missing tax values for 2025?
                - Show tax savings (difference between initial and revised tax) by client for 2025.
                - List the top 10 clients by total tax due in 2025.
                >> """).strip()
        )
        if question.lower() in ("exit", "quit"):
            break
        if not question:
            continue
        result = agent_executor.invoke({"input": question})
        output = result.get("output", "")
        print("\n🎯 Generated SQL:\n")
        print(output)
        if output and is_safe_query_llm(output):
            print("\n✅ Query validated as read-only.")
        elif output:
            print("\n⚠️  Only read-only queries are allowed.")
        print()
