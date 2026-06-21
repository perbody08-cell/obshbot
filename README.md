# 🤖 Telegram AI Bot — Business + Direct Mode

Бот с двумя режимами работы:
- **Business Mode** — отвечает от имени пользователя через Telegram Business
- **Direct Mode** — общение с ботом напрямую как с AI-ассистентом

## 🚀 Деплой на Railway

### Шаг 1: Подготовка

1. Форкни или загрузи этот репозиторий на GitHub
2. Зарегистрируйся на [Railway](https://railway.app) (если еще нет)

### Шаг 2: Создание проекта

1. В Railway нажми **"New Project"**
2. Выбери **"Deploy from GitHub repo"**
3. Выбери свой репозиторий

### Шаг 3: Добавление PostgreSQL

1. Нажми **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway автоматически создаст переменную `DATABASE_URL`

### Шаг 4: Переменные окружения

Перейди в **Variables** и добавь:

| Переменная | Значение | Описание |
|-----------|----------|----------|
| `BOT_TOKEN` | `123456:ABC-DEF...` | Токен от [@BotFather](https://t.me/BotFather) |
| `ADMIN_IDS` | `123456789` | Твой Telegram ID (через запятую если несколько) |
| `LLM_PROVIDER` | `mock` | Пока mock, потом `anthropic` / `openai` / `local` |
| `LLM_API_KEY` | *(пусто)* | API ключ (когда подключишь LLM) |

`DATABASE_URL` создается автоматически при добавлении PostgreSQL.

### Шаг 5: Деплой

1. Нажми **"Deploy"**
2. Дождись сборки (1-2 минуты)
3. Перейди в **Logs** — увидишь `🚀 Бот запущен!`

## 🛠️ Локальный запуск

```bash
# 1. Клонировать репозиторий
git clone <repo-url>
cd telegram_bot

# 2. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# 3. Установить зависимости
pip install -r bot/requirements.txt

# 4. Настроить переменные
cp bot/.env.example bot/.env
# Отредактируй bot/.env

# 5. Запустить БД (через Docker)
docker-compose up -d db

# 6. Запустить бота
python bot/main.py
```

## 📁 Структура проекта

```
telegram_bot/
├── bot/
│   ├── main.py              # Точка входа
│   ├── config.py            # Конфигурация
│   ├── requirements.txt     # Зависимости
│   ├── database/            # Модели и CRUD
│   ├── handlers/            # Обработчики
│   ├── services/            # LLM, промпты
│   └── keyboards/           # Клавиатуры
├── Procfile                 # Railway процесс
├── railway.json             # Railway конфиг
├── nixpacks.toml            # Nixpacks конфиг
├── Dockerfile               # Docker образ
└── docker-compose.yml       # Локальная БД
```

## 🎯 Использование

### Direct Mode (сразу работает)
1. Найди бота в Telegram
2. Напиши `/start`
3. Просто общайся — бот отвечает как AI-ассистент

### Business Mode
1. Нужен Telegram Business (платная подписка)
2. Настройки → Автоматизация чатов → Добавить бота
3. Введи @username бота
4. Настрой стиль в меню бота

## ⚙️ Настройки

| Команда | Описание |
|---------|----------|
| `/start` | Главное меню |
| `/settings` | Настройки |
| `/help` | Инструкция |
| `/admin` | Админ-панель |

## 🔗 Полезные ссылки

- [Railway Docs](https://docs.railway.app/)
- [python-telegram-bot](https://docs.python-telegram-bot.org/)
- [Telegram Business](https://telegram.org/blog/ultimate-privacy-topics-2-0/ru#automatizatsiya-chatov)
