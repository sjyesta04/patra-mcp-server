from fastapi import APIRouter, HTTPException
from app.db import get_db_driver
from neo4j.exceptions import Neo4jError

router = APIRouter()

@router.get("/resource/model_card/{model_id}")
def get_model_card_by_id(model_id: str):
    driver = get_db_driver()

    try:
        model_id_int = int(model_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Model ID must be an integer")

    query = """
MATCH (m:ModelCard)
WHERE id(m) = $model_id
RETURN m
"""

    # Enforce READ-ONLY
    forbidden_keywords = ["CREATE", "DELETE", "MERGE", "SET"]
    if any(kw in query.upper() for kw in forbidden_keywords):
        raise HTTPException(status_code=400, detail="Write operations are not allowed.")

    try:
        with driver.session() as session:
            result = session.run(query, model_id=model_id_int)
            record = result.single()
            if record:
                return record["m"]._properties
            else:
                raise HTTPException(status_code=404, detail="ModelCard not found")
    except Neo4jError as e:
        raise HTTPException(status_code=500, detail=str(e))
