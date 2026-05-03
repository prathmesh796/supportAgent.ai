import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "support_tickets"
SUPPORT_TICKETS_CSV = PROJECT_ROOT / "support_tickets" / "support_tickets.csv"

# Output files
PREDICTIONS_CSV = OUTPUT_DIR / "output.csv"

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# models
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
GROQ_MODEL = os.getenv("GROQ_MODEL")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your .env file.")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set. Please set it in your .env file.")

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
