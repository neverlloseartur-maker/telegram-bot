from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, CHANNEL_ID

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# ---- Функция проверки подписки ----
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ---- Команда /start ----
@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    is_subscribed = await check_subscription(message.from_user.id)

    if not is_subscribed:
        keyboard = types.InlineKeyboardMarkup()
        btn_sub = types.InlineKeyboardButton(
            "📢 Перейти к каналу", 
            url=f"https://t.me/{CHANNEL_ID.replace('@', '')}"
        )
        btn_check = types.InlineKeyboardButton(
            "🔄 Проверить подписку", 
            callback_data="check_sub"
        )
        keyboard.add(btn_sub)
        keyboard.add(btn_check)

        await message.answer(
            "🎉 <b>Добро пожаловать!</b>\n\n"
            "Наш канал — это место, где каждый день выходят лучшие:\n"
            "✨ Промокоды\n"
            "💸 Скидки\n"
            "🎁 Акции и бонусы\n\n"
            "Чтобы продолжить — подпишитесь на наш канал 👇",
            parse_mode="HTML",
            reply_markup=keyboard
        )
        return

    # Если уже подписан
    await message.answer(
        "🔥 <b>Отлично!</b> Вы уже подписаны.\n"
        "Готов получать самые свежие промокоды? 😉",
        parse_mode="HTML"
    )


# ---- Обработка кнопки «Проверить подписку» ----
@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def check_sub_handler(callback: types.CallbackQuery):

    is_subscribed = await check_subscription(callback.from_user.id)

    if is_subscribed:
        await callback.message.edit_text(
            "✔ <b>Подписка подтверждена!</b>\n\n"
            "Теперь вы будете получать только самые горячие промокоды 🔥\n\n"
            "<b>Быстрее нажимай Меню и забирай промокод!</b>",
            parse_mode="HTML"
        )
    else:
        await callback.answer("❗ Вы всё ещё не подписаны!", show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

