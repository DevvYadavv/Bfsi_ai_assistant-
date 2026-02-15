import streamlit as st
import sys
import os

st.set_page_config(page_title="BFSI Call Center Assistant", page_icon="🏦")

# Add current directory to path so we can import src
sys.path.append(os.getcwd())

from src.rag_engine import RAGEngine
from src.slm_interface import SLMInterface

# Initialize engines
@st.cache_resource
def load_engines():
    rag = RAGEngine()
    slm = SLMInterface()
    # Uncomment to load the actual model (warning: large download)
    # slm.load_model() 
    return rag, slm

rag_engine, slm_interface = load_engines()

st.title("🏦 BFSI Call Center AI Assistant")
st.markdown("---")

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    use_rag = st.checkbox("Enable RAG", value=True)
    use_slm = st.checkbox("Enable SLM Fallback", value=True)
    
    if st.button("Reload Knowledge Base"):
        st.cache_resource.clear()
        st.success("Reloaded!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = ""
        
        # 1. Dataset Match (Tier 1)
        dataset_match, similarity = rag_engine.retrieve(prompt)
        
        # Debug info
        st.write(f"DEBUG: Similarity: {similarity:.2f}")

        if dataset_match and similarity > 0.7: # Threshold
             response = f"**[Dataset Match]**\n{dataset_match['output']}"
        
        # 2 using SLM (Tier 2/3)
        elif use_slm:
             if use_rag:
                 # In a real scenario, we'd retrieve context chunks here
                 # context = rag_engine.retrieve_context(prompt) 
                 context = "Loan interest rates are 10.5% for personal loans." # Mock context
                 response = f"**[SLM Match]**\n" + slm_interface.generate_response(prompt, context)
             else:
                 response = f"**[SLM Match]**\n" + slm_interface.generate_response(prompt)
        else:
             response = "I'm sorry, I couldn't find an answer to your query."

        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
