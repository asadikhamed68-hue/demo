import os
import secrets
from pathlib import Path

import httpx
from dotenv import load_dotenv


APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
load_dotenv(PROJECT_ROOT / ".env", encoding="utf-8-sig")
load_dotenv(APP_DIR / ".env", override=True, encoding="utf-8-sig")

# Environment variables
OCLC_CLIENT_ID = os.getenv("OCLC_CLIENT_ID")
OCLC_CLIENT_SECRET = os.getenv("OCLC_CLIENT_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",") if origin.strip()]
ALLOWED_HOSTS = [host.strip() for host in os.getenv(
    "ALLOWED_HOSTS", "uaeu.ac.ae,*.uaeu.ac.ae,localhost,127.0.0.1"
).split(",") if host.strip()]
SECRET_KEY = os.getenv("SECRET_KEY", "")
ADMIN_KEY = os.getenv("ADMIN_KEY", "")

# Optional API keys for expanded article search
CORE_API_KEY = os.getenv("CORE_API_KEY", "")
SEMANTIC_SCHOLAR_KEY = os.getenv("S2_API_KEY", "")
NCBI_API_KEY = os.getenv("NCBI_API_KEY", "")

if not all([OCLC_CLIENT_ID, OCLC_CLIENT_SECRET]):
    raise ValueError("Missing required OCLC credentials in environment variables")

if ENVIRONMENT not in {"development", "production"}:
    raise ValueError("ENVIRONMENT must be 'development' or 'production'")

if ENVIRONMENT == "production" and (not SECRET_KEY or len(SECRET_KEY) < 32):
    raise ValueError("SECRET_KEY must be set to at least 32 characters in production")

if ENVIRONMENT != "production" and not SECRET_KEY:
    SECRET_KEY = secrets.token_urlsafe(32)

if ENVIRONMENT == "production" and ("*" in ALLOWED_ORIGINS or not ALLOWED_ORIGINS):
    raise ValueError("ALLOWED_ORIGINS must list exact frontend origins in production")

# OCLC Configuration
OCLC_SYMBOL = "UAE"
BASE_URL_CI = "https://discovery.api.oclc.org/worldcat-org-ci/search"
OCLC_TOKEN_URL = "https://oauth.oclc.org/token"

# HTTP Client Configuration
HTTP_TIMEOUT = 15.0
MAX_RETRIES = 3
HTTP_LIMITS = httpx.Limits(max_connections=50, max_keepalive_connections=20)

# Security Configuration
MAX_QUERY_LENGTH = 500
MAX_RESULTS_LIMIT = 50
OCLC_FILTERED_MAX_PAGES = max(1, min(int(os.getenv("OCLC_FILTERED_MAX_PAGES", "4")), 8))
RATE_LIMIT_REQUESTS = "15/minute"
RATE_LIMIT_STORAGE_URI = os.getenv("RATE_LIMIT_STORAGE_URI", "memory://")
SESSION_TTL_SECONDS = int(os.getenv("SESSION_TTL_SECONDS", "3600"))
CSRF_HEADER_NAME = "X-CSRF-Token"
GEMINI_MAX_CONCURRENCY = int(os.getenv("GEMINI_MAX_CONCURRENCY", "4"))

# Search Configuration
SEARCH_LIMIT = 35
FINAL_RECOMMENDATIONS = 7
ENABLE_SEMANTIC_EMBEDDINGS = os.getenv("ENABLE_SEMANTIC_EMBEDDINGS", "true").lower() in {"1", "true", "yes", "on"}
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/text-embedding-004")
MAX_EMBEDDING_CANDIDATES = int(os.getenv("MAX_EMBEDDING_CANDIDATES", "24"))
ENABLE_AI_QUERY_EXPANSION = os.getenv("ENABLE_AI_QUERY_EXPANSION", "true").lower() in {"1", "true", "yes", "on"}
MAX_AI_EXPANDED_QUERIES = int(os.getenv("MAX_AI_EXPANDED_QUERIES", "3"))
AI_QUERY_EXPANSION_TIMEOUT_SECONDS = float(os.getenv("AI_QUERY_EXPANSION_TIMEOUT_SECONDS", "4.0"))

# Cache Configuration
CACHE_TTL_SECONDS = 300
MAX_CACHE_SIZE = 100
ARTICLE_CACHE_TTL_SECONDS = int(os.getenv("ARTICLE_CACHE_TTL_SECONDS", "900"))
ARTICLE_CACHE_MAX_SIZE = int(os.getenv("ARTICLE_CACHE_MAX_SIZE", "200"))

# Conversation Memory Configuration
MAX_CONVERSATION_HISTORY = 10
CONVERSATION_TTL_SECONDS = 1920
MAX_CONVERSATIONS = 1000