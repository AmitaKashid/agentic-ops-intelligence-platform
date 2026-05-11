import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1/evaluation", tags=["Evaluation"])

RESULTS_PATH = Path("evaluation/results.csv")
SUMMARY_PATH = Path("evaluation/metrics_summary.json")
ERROR_ANALYSIS_PATH = Path("evaluation/error_analysis.md")


@router.post("/run")
def run_evaluation():
    completed = subprocess.run(
        [sys.executable, "-m", "evaluation.run_evaluation"],
        capture_output=True,
        text=True,
    )

    if completed.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Evaluation failed.",
                "stderr": completed.stderr,
                "stdout": completed.stdout,
            },
        )

    return {
        "status": "completed",
        "stdout": completed.stdout,
    }


@router.get("/results")
def get_evaluation_results():
    if not RESULTS_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Evaluation results not found. Run POST /api/v1/evaluation/run first.",
        )

    df = pd.read_csv(RESULTS_PATH)

    return {
        "total_rows": len(df),
        "results": df.to_dict(orient="records"),
    }


@router.get("/summary")
def get_evaluation_summary():
    if not SUMMARY_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Evaluation summary not found. Run POST /api/v1/evaluation/run first.",
        )

    return json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))


@router.get("/error-analysis")
def get_error_analysis():
    if not ERROR_ANALYSIS_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Error analysis not found. Run POST /api/v1/evaluation/run first.",
        )

    return {
        "content": ERROR_ANALYSIS_PATH.read_text(encoding="utf-8")
    }