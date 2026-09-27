from typing import Dict, Any
from app.mcp.tools import mcp_tools

class MCPServer:
    """Model Context Protocol (MCP) tool invocation server."""

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if not hasattr(mcp_tools, tool_name):
            return {"error": f"Tool '{tool_name}' not found on MCP server."}
        
        tool_func = getattr(mcp_tools, tool_name)
        try:
            result = await tool_func(**arguments)
            return {"status": "success", "tool": tool_name, "result": result}
        except Exception as e:
            return {"status": "error", "tool": tool_name, "error": str(e)}

mcp_server = MCPServer()
