import streamlit as st
import requests
import json
import time

BACKEND_URL = st.secrets["BACKEND_URL"]

st.set_page_config(
    page_title="HR Policy Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a professional look
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .reportview-container .main {
        color: #31333F;
        background-color: #F0F2F6;
    }
    h1 {
        color: #1E3A8A;
        font-family: 'Inter', sans-serif;
    }
    h2, h3 {
        color: #2563EB;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
    }
    .stTextArea>div>div>textarea {
        border-radius: 5px;
        border: 1px solid #D1D5DB;
    }
    .css-1d391kg {
        background-color: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=100)
    st.title("HR Policy AI")
    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "This tool uses an advanced Multi-Agent system to evaluate employee cases "
        "against company policies and generate structured decision summaries."
    )
    st.markdown("### Agents Active")
    st.success("✅ Document Retrieval Agent")
    st.success("✅ Case Evaluation Agent")
    st.success("✅ Decision Summary Agent")

# Main Content
st.title("⚖️ HR Policy Assistant")
st.markdown("Evaluate employee requests and cases seamlessly against company guidelines.")

case_details = st.text_area(
    "📝 Describe the Case Details:", 
    height=200, 
    placeholder="Example: John Doe from Engineering is requesting to work remotely for 3 weeks from Italy. He has been with the company for 8 months."
)

if st.button("Evaluate Case"):
    if not case_details.strip():
        st.warning("Please enter case details before evaluating.")
    else:
        with st.spinner("🤖 Analyzing case... Agents are actively reviewing policies..."):
            try:
                # Add a small delay for dramatic effect / realistic processing time feel
                time.sleep(1)
                
                response = requests.post(
                    f"{BACKEND_URL}/api/evaluate-case",
                    json={"case_details": case_details},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Evaluation Complete!")
                    st.markdown("---")
                    
                    # Create tabs for better organization
                    tab1, tab2, tab3 = st.tabs(["Decision Summary", "Evaluation Rationale", "Referenced Policies"])
                    
                    with tab1:
                        st.subheader("📋 Final Decision")
                        st.markdown(result.get("decision_summary", "No summary available."))
                    
                    with tab2:
                        st.subheader("🧠 Agent Evaluation")
                        st.info("The Case Evaluation Agent generated the following rationale based on retrieved documents:")
                        st.markdown(result.get("evaluation", "No evaluation available."))
                        
                    with tab3:
                        st.subheader("📄 Relevant Policy Excerpts")
                        st.caption("The Document Retrieval Agent found the following policy sections relevant to this case:")
                        docs = result.get("retrieved_docs", [])
                        if docs:
                            for idx, doc in enumerate(docs):
                                with st.expander(f"Reference {idx + 1}"):
                                    st.text(doc)
                        else:
                            st.write("No relevant documents found.")
                            
                else:
                    st.error(f"Failed to evaluate case. Status Code: {response.status_code}")
                    st.error(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Could not connect to the backend API. Please ensure the FastAPI server is running on http://localhost:8000")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
