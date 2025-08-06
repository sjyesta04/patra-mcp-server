# app/routes/search.py

from fastapi import APIRouter, HTTPException
from app.db import get_db_driver
from app.routes.model_card import get_model_card_by_id
from neo4j.exceptions import Neo4jError

router = APIRouter()

@router.post("/tool/search_models_by_task")
async def search_models_by_task(payload: dict):
    task = payload.get("task")
    if not task:
        raise HTTPException(status_code=400, detail="Missing 'task' in request payload")

    query = """
    MATCH (m:ModelCard)
    WHERE $task IN m.categories
    RETURN m
    """

    forbidden_keywords = ["CREATE", "DELETE", "MERGE", "SET"]
    if any(kw in query.upper() for kw in forbidden_keywords):
        raise HTTPException(status_code=400, detail="Write operations are not allowed.")

    driver = get_db_driver()
    try:
        with driver.session() as session:
            result = session.run(query, task=task)
            models = [record["m"]._properties for record in result]
            return {"results": models}
    except Neo4jError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tool/summarize_model_purpose")
async def summarize_model_purpose(payload: dict):
    model_id = payload.get("model_id")
    if model_id is None:
        raise HTTPException(status_code=400, detail="Missing 'model_id' in request payload")

    try:
        model_card = get_model_card_by_id(model_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving model: {e}")

    if not model_card:
        raise HTTPException(status_code=404, detail=f"Model with ID {model_id} not found")

    name = model_card.get("name", "This model")
    task = model_card.get("categories", "an ML task")
    desc = model_card.get("short_description", "")

    summary = f"{name} is used for {task}. {desc}"
    return {"summary": summary}
