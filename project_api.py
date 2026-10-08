from pathlib import Path
import json

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Interview Project Context API",
    description="Small read-only API used by an ElevenLabs interview-practice agent.",
)

DATA_FILE = Path(__file__).with_name("projects.json")


def load_projects():
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/projects")
def list_projects():
    projects = load_projects()
    return {
        "projects": [
            {
                "id": project_id,
                "title": data["title"],
                "company": data["company"],
            }
            for project_id, data in projects.items()
        ]
    }


@app.get("/projects/{project_id}")
def get_project(project_id: str):
    projects = load_projects()

    if project_id not in projects:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Unknown project_id",
                "available_project_ids": list(projects.keys()),
            },
        )

    return {
        "project_id": project_id,
        **projects[project_id],
    }
