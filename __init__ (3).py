from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.ext.asyncio import AsyncSession
from database.crud import (
    get_or_create_user, get_or_create_direct_chat, get_direct_chat_history,
    add_direct_message, update_direct_chat
)
from services.llm import get_llm
from services.prompt_builder import PromptBuilder
from settings import settings


async def handle_direct_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик прямых сообщений пользователю боту (не Business)"""

    if not settings.ENABLE_DIRECT_MODE:
        return

    # Пропускаем команды и callback
    if update.message and update.message.text and update.message.text.startswith("/"):
        return

    # Пропускаем сообщения из Business Connection
    if update.business_message:
        return

    # Работаем только в личных чатах
    if update.effective_chat.type != "private":
        return

    session: AsyncSession = context.bot_data["db_session"]

    # Получаем или создаём пользователя
    user = await get_or_create_user(
        session,
        telegram_id=update.effective_user.id,
        username=update.effective_user.username,
        first_name=update.effective_user.first_name,
        last_name=update.effective_user.last_name
    )

    # Проверяем, включён ли Direct Mode
    if not user.direct_mode_enabled:
        return

    # Получаем или создаём direct чат
    chat = await get_or_create_direct_chat(session, user.id)

    # Сохраняем сообщение пользователя
    await add_direct_message(
        session,
        chat_id=chat.id,
        sender_type="user",
        text=update.message.text or ""
    )

    # Показываем typing
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    # Получаем историю
    history = await get_direct_chat_history(session, chat.id, limit=settings.MAX_CONTEXT_MESSAGES)
    history_dicts = [{"sender_type": h.sender_type, "text": h.text} for h in history]

    # Строим промпт
    system_prompt = PromptBuilder.build_direct_prompt(
        user=user,
        chat=chat,
        prompt=user.prompt
    )
    messages = PromptBuilder.build_messages(history_dicts, update.message.text or "")

    # Генерируем ответ
    llm = get_llm(user.llm_provider, user.llm_api_key)

    try:
        response_text = await llm.generate(
            system_prompt,
            messages,
            mode="direct",
            user_settings={"user_id": user.id, "chat_id": chat.id}
        )

        # Отправляем ответ
        await update.message.reply_text(response_text)

        # Сохраняем ответ бота
        await add_direct_message(
            session,
            chat_id=chat.id,
            sender_type="bot",
            text=response_text,
            llm_model=user.llm_provider
        )

    except Exception as e:
        print(f"Direct LLM Error: {e}")
        await update.message.reply_text(
            "⚠️ Произошла ошибка при генерации ответа. Попробуйте позже."
        )


async def direct_mode_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Информация о Direct Mode"""

    query = update.callback_query
    await query.answer()

    text = """🤖 Direct Mode — общение с ботом

В этом режиме вы просто общаетесь со мной как с AI-ассистентом.

💡 Возможности:
• Задавайте любые вопросы
• Просите помочь с задачами
• Обсуждайте идеи
• Практикуйте языки
• Получайте советы

⚙️ Настройки:
• Выберите стиль общения
• Настройте свою персону
• Укажите интересы для персонализации

💼 Также доступен Business Mode — бот будет отвечать от вашего имени в личных чатах через Telegram Business."""

    from keyboards.inline import main_menu_keyboard
    await query.edit_message_text(text, reply_markup=main_menu_keyboard())
