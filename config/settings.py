
import os
from pathlib import Path

from dotenv import load_dotenv


# Get the root project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the root .env file
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)


# Application configuration
APP_NAME = "AI Chat Assistant"
APP_VERSION = "1.0.0"


# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Default model can be overridden through the .env file
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)


# Database configuration
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "chat_history.db"


# Create data directory if it does not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)


def validate_groq_config():
    """
    Validate the Groq API configuration.

    Returns:
        bool: True if the API key is available.
    """
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Please add your API key to the .env file."
        )

    return True
