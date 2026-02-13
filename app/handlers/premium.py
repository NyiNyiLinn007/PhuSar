from __future__ import annotations

from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.context import get_app
from app.keyboards import (
    main_menu_keyboard,
    premium_plan_keyboard,
    premium_provider_keyboard,
)
from app.locales import t
from app.states import PremiumState
from app.utils import is_premium_active, text

router = Router(name="premium")

PLAN_CONFIG = {
    "weekly": {"days": 7, "price": 1500},
    "monthly": {"days": 30, "price": 3000},
}


def _plan_label(lang: str, plan_code: str) -> str:
    if plan_code == "monthly":
        return t(lang, "premium_plan_monthly")
    return t(lang, "premium_plan_weekly")


async def _start_premium(message: Message, user_id: int) -> None:
    app = get_app(message.bot)
    user = await app.users.get(user_id)
    if user is None:
        await message.answer("/start")
        return

    lang = user["language"] or app.settings.default_language
    if not app.settings.premium_enabled:
        await message.answer(t(lang, "premium_disabled"))
        await message.answer(
            t(lang, "menu_text"),
            reply_markup=main_menu_keyboard(lang, is_premium_active(user), app.settings.premium_enabled),
        )
        return
    if is_premium_active(user):
        await message.answer(
            t(lang, "already_premium"),
            reply_markup=main_menu_keyboard(lang, True, app.settings.premium_enabled),
        )
        return

    await message.answer(t(lang, "premium_intro"))
    await message.answer(t(lang, "premium_choose_plan"), reply_markup=premium_plan_keyboard(lang))


@router.message(Command("premium"))
async def cmd_premium(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    await state.clear()
    await _start_premium(message, message.from_user.id)


@router.callback_query(F.data == "menu:premium")
async def menu_premium(query: CallbackQuery, state: FSMContext) -> None:
    if query.from_user is None or query.message is None:
        return
    await state.clear()
    await _start_premium(query.message, query.from_user.id)
    await query.answer()


@router.callback_query(F.data.startswith("premium_plan:"))
async def premium_plan(query: CallbackQuery, state: FSMContext) -> None:
    if query.data is None or query.from_user is None or query.message is None:
        return
    app = get_app(query.bot)
    user = await app.users.get(query.from_user.id)
    if user is None:
        await query.answer()
        return
    lang = user["language"] or app.settings.default_language
    if not app.settings.premium_enabled:
        await state.clear()
        await query.message.answer(t(lang, "premium_disabled"))
        await query.answer()
        return

    plan_code = query.data.split(":", 1)[1]
    if plan_code == "cancel":
        await state.clear()
        await query.message.answer(
            t(lang, "menu_text"),
            reply_markup=main_menu_keyboard(lang, is_premium_active(user), app.settings.premium_enabled),
        )
        await query.answer()
        return
    if plan_code not in PLAN_CONFIG:
        await query.answer()
        return

    await state.set_state(PremiumState.choosing_provider)
    await state.update_data(
        language=lang,
        plan_code=plan_code,
        duration_days=PLAN_CONFIG[plan_code]["days"],
        price_mmk=PLAN_CONFIG[plan_code]["price"],
    )
    await query.message.answer(t(lang, "premium_plan_selected", plan=_plan_label(lang, plan_code)))
    await query.message.answer(t(lang, "premium_choose_provider"), reply_markup=premium_provider_keyboard(lang, plan_code))
    await query.answer()


@router.callback_query(PremiumState.choosing_provider, F.data.startswith("premium_provider:"))
async def premium_provider(query: CallbackQuery, state: FSMContext) -> None:
    if query.data is None or query.from_user is None or query.message is None:
        return
    app = get_app(query.bot)
    user = await app.users.get(query.from_user.id)
    if user is None:
        await query.answer()
        return
    lang = user["language"] or app.settings.default_language
    if not app.settings.premium_enabled:
        await state.clear()
        await query.message.answer(t(lang, "premium_disabled"))
        await query.answer()
        return

    if query.data == "premium_provider:cancel":
        await state.clear()
        await query.message.answer(
            t(lang, "menu_text"),
            reply_markup=main_menu_keyboard(lang, is_premium_active(user), app.settings.premium_enabled),
        )
        await query.answer()
        return

    parts = query.data.split(":")
    if len(parts) != 3:
        await query.answer()
        return
    plan_code = parts[1]
    provider = parts[2]
    if plan_code not in PLAN_CONFIG or provider not in {"kbzpay", "wavemoney"}:
        await query.answer()
        return

    await state.set_state(PremiumState.awaiting_screenshot)
    await state.update_data(
        language=lang,
        plan_code=plan_code,
        provider=provider,
        duration_days=PLAN_CONFIG[plan_code]["days"],
        price_mmk=PLAN_CONFIG[plan_code]["price"],
    )

    payment_phone = app.settings.payment_phone or "-"
    await query.message.answer(t(lang, "premium_payment_details", phone=payment_phone))
    qr_id = app.settings.kbzpay_qr_file_id if provider == "kbzpay" else app.settings.wavemoney_qr_file_id
    if qr_id:
        try:
            await query.message.answer_photo(qr_id)
        except TelegramAPIError:
            pass
    await query.message.answer(t(lang, "premium_send_receipt"))
    await query.answer()


@router.message(PremiumState.awaiting_screenshot, F.photo)
async def premium_screenshot(message: Message, state: FSMContext) -> None:
    if message.from_user is None or not message.photo:
        return

    app = get_app(message.bot)
    data = await state.get_data()
    provider = data.get("provider", "kbzpay")
    plan_code = data.get("plan_code", "weekly")
    duration_days = int(data.get("duration_days", PLAN_CONFIG["weekly"]["days"]))
    price_mmk = int(data.get("price_mmk", PLAN_CONFIG["weekly"]["price"]))
    lang = data.get("language", app.settings.default_language)
    screenshot_file_id = message.photo[-1].file_id
    request_id = await app.premium_requests.create(
        user_id=message.from_user.id,
        provider=provider,
        plan_code=plan_code,
        duration_days=duration_days,
        price_mmk=price_mmk,
        screenshot_file_id=screenshot_file_id,
    )
    await state.clear()

    user = await app.users.get(message.from_user.id)
    is_premium = bool(user and is_premium_active(user))
    await message.answer(t(lang, "premium_submitted"))
    await message.answer(
        t(lang, "menu_text"),
        reply_markup=main_menu_keyboard(lang, is_premium, app.settings.premium_enabled),
    )

    user_name = user["full_name"] if user else str(message.from_user.id)
    admin_caption = (
        f"Premium Request #{request_id}\n"
        f"User: {text(user_name)} ({message.from_user.id})\n"
        f"Provider: {text(provider)}\n"
        f"Plan: {text(plan_code)}\n"
        f"Price: {price_mmk} MMK\n"
        f"Approve: /approve {message.from_user.id} {duration_days}\n"
        f"Reject: /reject {message.from_user.id}"
    )
    for target_id in sorted(app.settings.admin_ids):
        try:
            await message.bot.send_photo(
                target_id,
                screenshot_file_id,
                caption=admin_caption,
            )
        except TelegramAPIError:
            continue


@router.message(PremiumState.awaiting_screenshot)
async def premium_screenshot_invalid(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    await message.answer(t(lang, "invalid_photo"))
