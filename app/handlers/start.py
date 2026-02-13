from __future__ import annotations

from collections.abc import Mapping

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.context import get_app
from app.handlers.registration import begin_registration
from app.keyboards import main_menu_keyboard, profile_keyboard
from app.locales import gender_label, seeking_label, t
from app.utils import is_premium_active, is_profile_complete, text

router = Router(name="start")


def _profile_text(lang: str, user: Mapping[str, object]) -> str:
    return (
        f"<b>{t(lang, 'profile_title')}</b>\n"
        f"{text(user.get('full_name') or '-')}\n"
        f"{t(lang, 'label_age')}: {text(user.get('age') or '-')}\n"
        f"{t(lang, 'label_gender')}: {text(gender_label(lang, str(user.get('gender') or '-')))}\n"
        f"{t(lang, 'label_seeking')}: {text(seeking_label(lang, str(user.get('seeking') or '-')))}\n"
        f"{t(lang, 'label_location')}: "
        f"{text(user.get('location_region') or '-')}, {text(user.get('township') or '-')}\n\n"
        f"{text(user.get('bio') or '-')}"
    )


async def _show_home(message: Message, lang: str, is_premium: bool) -> None:
    app = get_app(message.bot)
    await message.answer(t(lang, "welcome"))
    await message.answer(
        t(lang, "menu_text"),
        reply_markup=main_menu_keyboard(lang, is_premium, app.settings.premium_enabled),
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    app = get_app(message.bot)
    full_name = message.from_user.full_name.strip()[:100] if message.from_user.full_name else "User"
    user = await app.users.ensure_user(message.from_user.id, full_name, message.from_user.username)
    lang = user["language"] or app.settings.default_language

    if user["is_banned"]:
        await message.answer(t(lang, "banned"))
        return

    if is_profile_complete(user):
        await _show_home(message, lang, is_premium_active(user))
        return

    await begin_registration(message, state, lang)


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    if message.from_user is None:
        return
    app = get_app(message.bot)
    user = await app.users.get(message.from_user.id)
    if user is None:
        await message.answer("/start")
        return
    lang = user["language"] or app.settings.default_language
    await message.answer(
        t(lang, "menu_text"),
        reply_markup=main_menu_keyboard(lang, is_premium_active(user), app.settings.premium_enabled),
    )


@router.message(Command("delete_account"))
async def cmd_delete_account(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    app = get_app(message.bot)
    user = await app.users.get(message.from_user.id)
    if user is None:
        await message.answer("/start")
        return

    lang = user["language"] or app.settings.default_language
    await state.clear()
    await app.users.delete_account(message.from_user.id)
    await app.discovery.clear_queue(message.from_user.id)
    await app.redis.delete(f"rewind_last_dislike:{message.from_user.id}")
    await message.answer(t(lang, "delete_account_done"))


@router.callback_query(F.data == "menu:profile")
async def profile_menu(query: CallbackQuery) -> None:
    if query.from_user is None or query.message is None:
        return
    app = get_app(query.bot)
    user = await app.users.get(query.from_user.id)
    if user is None:
        await query.message.answer("/start")
        await query.answer()
        return
    lang = user["language"] or app.settings.default_language
    payload = dict(user)
    if user["photo_id"]:
        await query.message.answer_photo(
            photo=user["photo_id"],
            caption=_profile_text(lang, payload),
            reply_markup=profile_keyboard(lang),
        )
    else:
        await query.message.answer(_profile_text(lang, payload), reply_markup=profile_keyboard(lang))
    await query.answer()


@router.callback_query(F.data == "profile:edit")
async def profile_edit(query: CallbackQuery, state: FSMContext) -> None:
    if query.from_user is None or query.message is None:
        return
    app = get_app(query.bot)
    lang = await app.users.get_language(query.from_user.id, app.settings.default_language)
    await begin_registration(query.message, state, lang)
    await query.answer()
