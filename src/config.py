import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Application settings loaded from environment variables.
    """
    DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN")

    def __init__(self):
        if not self.DISCORD_BOT_TOKEN:
            raise ValueError("DISCORD_BOT_TOKEN environment variable not set.")

settings = Settings()