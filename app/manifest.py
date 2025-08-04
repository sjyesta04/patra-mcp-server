from fastapi import APIRouter

router = APIRouter()

@router.get("/mcp/manifest")
def get_manifest():
    return {
        "tools": [
            {
                "name": "search_models_by_task",
                "description": "Returns model cards matching a given ML task",
                "endpoint": "/tool/search_models_by_task"
            }
        ],
        "resources": [
            {
                "name": "model_card",
                "description": "Returns metadata of a specific model card by ID",
                "endpoint": "/resource/model_card/{id}"
            }
        ],
        "prompts": []
    }
