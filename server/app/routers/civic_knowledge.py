import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from app.services.civic_graph_service import (
    get_civic_knowledge_graph,
    get_entity_connections,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/civic-knowledge", tags=["Civic Knowledge Graph"])

@router.get("/graph")
async def get_graph(node_type: Optional[str] = Query(None)):
    """
    Returns the live national civic & legal knowledge graph connecting
    the Constitution of India, Nyaykosh codified statutes, ministries, and welfare schemes.
    """
    graph = get_civic_knowledge_graph()
    nodes = graph["nodes"]
    
    if node_type and node_type != "all":
        nodes = [n for n in nodes if n["type"].lower() == node_type.lower() or n.get("category", "").lower() == node_type.lower()]
        node_ids = {n["id"] for n in nodes}
        links = [l for l in graph["links"] if l["source"] in node_ids and l["target"] in node_ids]
    else:
        links = graph["links"]

    return {
        "status": "success",
        "metadata": graph["metadata"],
        "nodesCount": len(nodes),
        "linksCount": len(links),
        "nodes": nodes,
        "links": links
    }

@router.get("/entities/{entity_id}")
async def get_entity(entity_id: str):
    """
    Retrieves full contextual connections, rights, and parent laws for a specific entity node.
    """
    details = get_entity_connections(entity_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity '{entity_id}' not found in civic knowledge graph."
        )
    return {
        "status": "success",
        "entity": details
    }

