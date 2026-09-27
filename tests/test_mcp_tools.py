import pytest
import asyncio
from app.mcp.tools import mcp_tools
from app.mcp.server import mcp_server

@pytest.mark.asyncio
async def test_search_nearby_veterinary_hospitals():
    results = await mcp_tools.search_nearby_veterinary_hospitals(17.3850, 78.4867, 10.0)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "place_id" in results[0]
    assert "source" in results[0]

@pytest.mark.asyncio
async def test_mcp_server_dispatch():
    res = await mcp_server.execute_tool("search_pet_pharmacies", {"lat": 17.3850, "lng": 78.4867, "radius_km": 10.0})
    assert res["status"] == "success"
    assert isinstance(res["result"], list)
