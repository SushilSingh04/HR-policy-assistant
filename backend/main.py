from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agents import run_hr_assistant

app = FastAPI(title="HR Policy Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CaseRequest(BaseModel):
    case_details: str

@app.post("/api/evaluate-case")
def evaluate_case(request: CaseRequest):
    result = run_hr_assistant(request.case_details)
    return {
        "decision_summary": result.get("decision_summary", ""),
        "evaluation": result.get("evaluation", ""),
        "retrieved_docs": result.get("retrieved_docs", [])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
