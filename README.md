# Discord MCP Server

This project implements a Model Context Protocol (MCP) server that allows AI models like Claude to interact directly with Discord. It provides a suite of tools for sending messages, reading channel history, searching, and moderation, all accessible through natural language prompts to an AI.

The server is built using Python with `fastmcp` and `discord.py` and is designed to run within a WSL (Windows Subsystem for Linux) environment while being controlled by a native Windows MCP client.

## Features ::

-   **AI-Powered Actions**: Enables an AI to perform actions in a Discord server on your behalf.
-   **Comprehensive Toolset**:
    -   `send_message`: Post messages to any channel.
    -   `get_messages`: Read recent message history.
    -   `get_channel_info`: Fetch metadata about a channel.
    -   `search_messages`: Find messages containing specific keywords.
    -   `moderate_content`: Delete messages by their ID.
-   **Asynchronous**: Built on `asyncio` to handle operations efficiently without blocking.
-   **Secure Secrets**: Manages the Discord Bot Token securely using a `.env` file.

## Project Structure

```
discord-mcp-server/
├── .env
├── README.md
├── requirements.txt
└── src/
    ├── __init__.py
    ├── config.py           # Configuration and secrets management
    ├── discord_bot.py      # Core Discord bot logic and MCP tools
    └── main.py             # MCP server entry point
```

## Setup and Installation

### Prerequisites

-   Windows 10 or 11 with **WSL 2** installed.
-   Python 3.8+ installed within your WSL distribution.
-   A Discord account and a server where you have admin privileges.
-   An MCP Client (like MCP Inspector or the Claude app).

### Step 1: Create the Discord Bot

1.  Navigate to the [Discord Developer Portal](https://discord.com/developers/applications).
2.  Click **"New Application"** and give it a name.
3.  Go to the **"Bot"** tab.
4.  Click **"Add Bot"** and confirm.
5.  Under the bot's username, click **"Reset Token"** to get your bot token. **Copy and save this token.** This is your `DISCORD_BOT_TOKEN`.
6.  Enable **Privileged Gateway Intents**:
    -   Toggle on **SERVER MEMBERS INTENT**.
    -   Toggle on **MESSAGE CONTENT INTENT**.
7.  Invite the bot to your server:
    -   Go to the **"OAuth2" -> "URL Generator"** tab.
    -   Select the `bot` and `applications.commands` scopes.
    -   Under "Bot Permissions", grant `Send Messages`, `Read Message History`, and `Manage Messages`.
    -   Copy the generated URL, paste it into your browser, and add the bot to your server.

### Step 2: Clone and Set Up the Project

1.  Open your WSL terminal.
2.  Clone the repository into your WSL filesystem (e.g., in your home directory).
    ```bash
    git clone <your-github-repository-link>
    cd discord-mcp-server
    ```
3.  Create a Python virtual environment.
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4.  Install the required dependencies.
    ```bash
    pip install -r requirements.txt
    ```
5.  Create the environment file.
    ```bash
    cp .env.example .env
    ```
6.  Edit the `.env` file and add your Discord bot token.
    ```env
    # .env
    DISCORD_BOT_TOKEN="YourDiscordBotTokenGoesHere"
    ```

## Running the Server with an MCP Client (Windows + WSL)

This server is designed to be launched and managed by an external MCP client running on Windows. You **do not** run the `python -m src.main` command manually in your terminal.

Instead, you must configure your MCP client to start the server using the `wsl.exe` bridge.

### Client Configuration

In your MCP client's server configuration file (e.g., for MCP Inspector or the Claude App), add the following entry:

```json
{
  "mcpServers": {
    "discord_mcp_server": {
      "command": "wsl.exe",
      "args": [
        "bash",
        "-c",
        "cd /home/pratik/misogiai/discord-mcp-server/ && /home/pratik/misogiai/discord-mcp-server/.venv/bin/python -m src.main"
      ],
      "cwd": "/home/pratik/misogiai/discord-mcp-server/"
    }
  }
}
```
**Note:** Make sure the paths like `/home/pratik/...` exactly match the location of your project inside WSL.

### Configuration Breakdown

-   `"command": "wsl.exe"`: Tells the Windows client to use the WSL command-line tool as the entry point.
-   `"args": [...]`: The arguments passed to `wsl.exe`.
    -   `"bash", "-c"`: We run the `bash` shell and use the `-c` flag to pass it a single command string to execute.
    -   `"cd ... && ... python -m src.main"`: This is the crucial command string.
        -   `cd /path/to/your/project/`: It **first** changes the directory to your project's root inside WSL. This is essential for Python to find the `src` module.
        -   `&&`: If the `cd` command is successful, it then proceeds.
        -   `/path/to/.venv/bin/python -m src.main`: It runs the server using the correct virtual environment's Python interpreter.

### How to Use with an AI Model (like Claude)

Once the server is connected to your client, you can prompt the AI using natural language. To get the `channel_id` for your prompts, turn on **Developer Mode** in Discord's "Advanced" settings, then right-click a channel and select **"Copy Channel ID"**.

**Example Prompts:**

-   **Sending a message:**
    > "Post a message to Discord channel `1405137114743570502` saying: 'Hello World! The AI is now online.'"

-   **Reading recent messages:**
    > "Can you show me the last 3 messages from channel `1405137114743570502`?"

-   **Searching for a conversation:**
    > "Search for the term 'project deadline' in channel `1405137114743570502`."

-   **Deleting a message (requires a message ID):**
    > "Please delete the spam message with ID `1405194830121140224` in channel `1405137114743570502`."
