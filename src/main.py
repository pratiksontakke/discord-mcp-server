# src/main.py

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastmcp import FastMCP

from .discord_bot import discord_bot_manager
    
# 1. Define the lifespan manager
@asynccontextmanager
async def lifespan(app: FastMCP):
    """
    Handles application startup events.
    In this case, it starts the Discord bot.
    """
    print("Application startup: Starting Discord bot...")
    await discord_bot_manager.start()
    yield
    # Code here would run on shutdown, e.g., await discord_bot_manager.stop()
    print("Application shutdown.")


# 2. Initialize FastMCP and pass the lifespan manager to it
mcp = FastMCP(
    "Discord MCP Server",
    lifespan=lifespan
)

# --- All your tools remain the same ---

@mcp.tool()
async def send_message(channel_id: str, message: str) -> Dict[str, Any]:
    """Send a message to a specific Discord channel."""
    return await discord_bot_manager.send_message(channel_id, message)

@mcp.tool()
async def get_messages(channel_id: str, limit: int = 10) -> Dict[str, Any]:
    """Get the last N messages from a Discord channel."""
    return await discord_bot_manager.get_messages(channel_id, limit)

@mcp.tool()
async def get_channel_info(channel_id: str) -> Dict[str, Any]:
    """Get metadata about a specific Discord channel."""
    return await discord_bot_manager.get_channel_info(channel_id)

@mcp.tool()
async def search_messages(channel_id: str, query: str, limit: int = 50) -> Dict[str, Any]:
    """Search for messages containing a query within a channel."""
    return await discord_bot_manager.search_messages(channel_id, query, limit)

@mcp.tool()
async def moderate_content(channel_id: str, message_id: str, action: str = "delete") -> Dict[str, Any]:
    """Moderate content in a channel. Currently supports deleting messages."""
    return await discord_bot_manager.moderate_content(channel_id, message_id, action)


# 3. The old on_event decorator is now GONE. The lifespan manager handles it.
# @mcp.on_event("startup")  <-- DELETE THIS
# async def startup_event():
#     """On server startup, start the Discord bot."""
#     await discord_bot_manager.start()


def main():
    """Main function to run the MCP server."""
    print("Initializing Discord MCP Server...")
    print("Authentication is disabled. The server is open to all clients.")
    print("Connect to this server using the MCP Inspector for debugging.")
    mcp.run()

if __name__ == "__main__":
    main()