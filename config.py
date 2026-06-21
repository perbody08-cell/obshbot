BOT_TOKEN=your_bot_token_here

# Railway автоматически создает переменную DATABASE_URL
# Если деплоишь локально — укажи свою БД
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/bot

# Админы (через запятую)
ADMIN_IDS=123456789

# LLM Settings
LLM_PROVIDER=mock
LLM_API_KEY=
LLM_MODEL=claude-sonnet-4.6
LLM_BASE_URL=

# Modes
ENABLE_BUSINESS_MODE=true
ENABLE_DIRECT_MODE=true

# Settings
MAX_CONTEXT_MESSAGES=20
DEFAULT_PROMPT_ID=1
