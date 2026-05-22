import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from backend.document_loader import get_vector_store
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    case_details: str
    retrieved_docs: List[str]
    evaluation: str
    decision_summary: str

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def retrieve_node(state: AgentState):
    print("Agent: Document Retrieval Agent")
    case_details = state["case_details"]
    vectorstore = get_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(case_details)
    
    # Format docs with source tracking
    formatted_docs = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown Source")
        formatted_docs.append(f"Source: {os.path.basename(source)}\nContent: {doc.page_content}")
        
    return {"retrieved_docs": formatted_docs}

def evaluate_node(state: AgentState):
    print("Agent: Case Evaluation Agent")
    case_details = state["case_details"]
    docs_text = "\n\n".join(state["retrieved_docs"])
    
    system_prompt = (
        "You are an expert HR Policy Case Evaluation Agent. "
        "Your task is to evaluate the provided case details against the provided HR policies. "
        "Determine if the case complies with the policies, violates them, or if more information is needed. "
        "Provide a detailed rationale referencing the provided policies."
    )
    
    human_prompt = f"Case Details:\n{case_details}\n\nRelevant Policies:\n{docs_text}"
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    
    response = llm.invoke(messages)
    return {"evaluation": response.content}

def summarize_node(state: AgentState):
    print("Agent: Decision Summary Agent")
    case_details = state["case_details"]
    evaluation = state["evaluation"]
    docs_text = "\n\n".join(state["retrieved_docs"])
    
    system_prompt = (
        "You are an expert HR Decision Summary Agent. "
        "Your task is to take an HR evaluation and synthesize it into a professional, structured decision summary. "
        "Include the following sections:\n"
        "1. Executive Summary\n"
        "2. Decision (Approved, Denied, Needs Review)\n"
        "3. Rationale & Citations (Explicitly name the sources referenced from the policies)\n"
        "Output ONLY the markdown formatted summary."
    )
    
    human_prompt = f"Case Details:\n{case_details}\n\nEvaluation:\n{evaluation}\n\nAvailable Policy Context:\n{docs_text}"
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    
    response = llm.invoke(messages)
    return {"decision_summary": response.content}

# Define Graph
workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("evaluate", evaluate_node)
workflow.add_node("summarize", summarize_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "evaluate")
workflow.add_edge("evaluate", "summarize")
workflow.add_edge("summarize", END)

app = workflow.compile()

def run_hr_assistant(case_details: str):
    initial_state = {"case_details": case_details}
    result = app.invoke(initial_state)
    return result
