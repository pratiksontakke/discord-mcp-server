import asyncio
from typing import Dict, Any
import discord
from discord.ext import commands

from src.config import settings

class DiscordBotManager:
    """
    Manages the Discord bot's connection, events, and interactions.
    """
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self._is_ready = asyncio.Event()

        @self.bot.event
        async def on_ready():
            print(f"{self.bot.user} has connected to Discord!")
            print(f"Bot is in {len(self.bot.guilds)} servers.")
            for guild in self.bot.guilds:
                print(f"  - {guild.name} (ID: {guild.id})")
            self._is_ready.set() # Signal that the bot is ready

    async def start(self):
        """Starts the bot in a background task."""
        if not self.bot.is_ready():
            print("Starting Discord bot...")
            asyncio.create_task(self.bot.start(settings.DISCORD_BOT_TOKEN))
            await self._is_ready.wait() # Wait until on_ready event is fired
            print("Bot is now ready.")

    async def get_channel(self, channel_id: str) -> discord.TextChannel:
        """Helper to get a channel and handle errors."""
        await self._is_ready.wait()
        channel = self.bot.get_channel(int(channel_id))
        if not channel or not isinstance(channel, discord.TextChannel):
            raise ValueError(f"Channel {channel_id} not found or is not a text channel.")
        return channel

    async def send_message(self, channel_id: str, message: str) -> Dict[str, Any]:
        """Send message to a Discord channel."""
        try:
            channel = await self.get_channel(channel_id)
            sent_message = await channel.send(message)
            return {"success": True, "message_id": str(sent_message.id)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_messages(self, channel_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get recent messages from a Discord channel."""
        try:
            channel = await self.get_channel(channel_id)
            messages_data = []
            async for msg in channel.history(limit=limit):
                messages_data.append({
                    "id": str(msg.id),
                    "author": msg.author.name,
                    "content": msg.content,
                    "timestamp": msg.created_at.isoformat(),
                })
            return {"success": True, "messages": messages_data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """Get information about a Discord channel."""
        try:
            channel = await self.get_channel(channel_id)
            info = {
                "id": str(channel.id),
                "name": channel.name,
                "topic": channel.topic,
                "guild": channel.guild.name,
                "member_count": getattr(channel, 'members', None) and len(channel.members)
            }
            return {"success": True, "data": info}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def search_messages(self, channel_id: str, query: str, limit: int = 50) -> Dict[str, Any]:
        """Search for messages containing a query in a channel."""
        try:
            channel = await self.get_channel(channel_id)
            matches = []
            async for msg in channel.history(limit=limit):
                if query.lower() in msg.content.lower():
                    matches.append({"id": str(msg.id), "content": msg.content, "author": msg.author.name})
            return {"success": True, "matches": matches}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def moderate_content(self, channel_id: str, message_id: str, action: str = "delete") -> Dict[str, Any]:
        """Deletes a specific message."""
        if action != "delete":
            return {"success": False, "error": "Unsupported action. Only 'delete' is available."}
        try:
            channel = await self.get_channel(channel_id)
            message = await channel.fetch_message(int(message_id))
            await message.delete()
            return {"success": True, "message": f"Message {message_id} deleted."}
        except discord.NotFound:
            return {"success": False, "error": "Message not found."}
        except discord.Forbidden:
            return {"success": False, "error": "Bot lacks permissions to delete this message."}
        except Exception as e:
            return {"success": False, "error": str(e)}


discord_bot_manager = DiscordBotManager()