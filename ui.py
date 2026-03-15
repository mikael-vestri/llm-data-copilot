import streamlit as st
from agents.sql_agent import agent_executor

st.set_page_config(page_title="LLM Data Copilot", page_icon="🧠")
st.title("🧠 LLM Data Copilot")
st.markdown("""
Ask natural language questions about your data. For example:
- *What are the tax savings for Texas in 2025?*
- *How many properties have missing jurisdictions this year?*
""")

# Input box
question = st.text_input("📌 Enter your data question:")

# Process input
if question:
    with st.spinner("🤖 Thinking..."):
        try:
            result = agent_executor.invoke({"input": question})
            sql_query = result.get("output", "No output returned.")
            st.success("✅ Query generated successfully!")
            st.code(sql_query, language="sql")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
