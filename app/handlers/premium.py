from __future__ import annotations

from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.context import get_app
from app.keyboards import admin_premium_keyboard, main_menu_keyboard, premium_provider_keyboard
from app.locales import t
from app.states import PremiumState
from app.utils import text

router = Router(name="premium")


async def _start_premium(message: Message, user_id: int) -> None:
    app = get_app(message.bot)
    user = await app.users.get(user_id)
    if user is None:
        await message.answer("/start")
        return

    lang = user["language"] or app.settings.default_language
    if user["is_premium"]:
        await message.answer(
            t(lang, "already_premium"),
            reply_markup=main_menu_keyboard(lang, True),
        )
        return

    await message.answer(t(lang, "premium_intro"))
    await message.answer(t(lang, "premium_choose_provider"), reply_markup=premium_provider_keyboard(lang))


@router.message(Command("premium"))
async def cmd_premium(message: Message) -> None:
    if message.from_user is None:
        return
    await _start_premium(message, message.from_user.id)


@router.callback_query(F.data == "menu:premium")
async def menu_premium(query: CallbackQuery) -> None:
    if query.from_user is None or query.message is None:
        return
    await _start_premium(query.message, query.from_user.id)
    await query.answer()


@router.callback_query(F.data.startswith("premium_provider:"))
async def premium_provider(query: CallbackQuery, state: FSMContext) -> None:
    if query.data is None or query.from_user is None or query.message is None:
        return
    app = get_app(query.bot)
    user = await app.users.get(query.from_user.id)
    if user is None:
        await query.answer()
        return

    lang = user["language"] or app.settings.default_language
    provider = query.data.split(":", 1)[1]
    if provider == "cancel":
        await state.clear()
        await query.message.answer(
            t(lang, "menu_text"), reply_markup=main_menu_keyboard(lang, bool(user["is_premium"]))
        )
        await query.answer()
        return

    if provider not in {"kbzpay", "wavemoney"}:
        await query.answer()
        return

    await state.set_state(PremiumState.awaiting_screenshot)
    await state.update_data(provider=provider, language=lang)
    await query.message.answer(t(lang, "premium_send_receipt"))
    await query.answer()


@router.message(PremiumState.awaiting_screenshot, F.photo)
async def premium_screenshot(message: Message, state: FSMContext) -> None:
    if message.from_user is None or not message.photo:
        return

    app = get_app(message.bot)
    data = await state.get_data()
    provider = data.get("provider", "kbzpay")
    lang = data.get("language", app.settings.default_language)
    screenshot_file_id = message.photo[-1].file_id
    request_id = await app.premium_requests.create(message.from_user.id, provider, screenshot_file_id)
    await state.clear()

    user = await app.users.get(message.from_user.id)
    is_premium = bool(user and user["is_premium"])
    await message.answer(t(lang, "premium_submitted"))
    await message.answer(t(lang, "menu_text"), reply_markup=main_menu_keyboard(lang, is_premium))

    user_name = user["full_name"] if user else str(message.from_user.id)
    admin_caption = (
        f"Premium Request #{request_id}\n"
        f"User: {text(user_name)} ({message.from_user.id})\n"
        f"Provider: {text(provider)}\n"
        f"Status: pending"
    )
    for admin_id in app.settings.admin_ids:
        try:
            await message.bot.send_photo(
                admin_id,
                screenshot_file_id,
                caption=admin_caption,
                reply_markup=admin_premium_keyboard(request_id),
            )
        except TelegramAPIError:
            continue


@router.message(PremiumState.awaiting_screenshot)
async def premium_screenshot_invalid(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    await message.answer(t(lang, "invalid_photo"))
