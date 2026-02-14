from __future__ import annotations

from collections.abc import Mapping

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.context import get_app
from app.handlers.registration import begin_registration
from app.keyboards import language_settings_keyboard, main_menu_keyboard, profile_keyboard
from app.locales import gender_label, seeking_label, t
from app.states import ProfileEditState
from app.utils import escape_html, is_premium_active, is_profile_complete, text

router = Router(name="start")


def _profile_text(lang: str, user: Mapping[str, object]) -> str:
    return (
        f"<b>{t(lang, 'profile_title')}</b>\n"
        f"{escape_html(user.get('full_name') or '-')}\n"
        f"{t(lang, 'label_age')}: {text(user.get('age') or '-')}\n"
        f"{t(lang, 'label_gender')}: {text(gender_label(lang, str(user.get('gender') or '-')))}\n"
        f"{t(lang, 'label_seeking')}: {text(seeking_label(lang, str(user.get('seeking') or '-')))}\n"
        f"{t(lang, 'label_location')}: "
        f"{text(user.get('location_region') or '-')}, {text(user.get('township') or '-')}\n\n"
        f"{escape_html(user.get('bio') or '-')}"
    )


async def _show_home(message: Message, lang: str, is_premium: bool) -> None:
    app = get_app(message.bot)
    await message.answer(t(lang, "welcome"))
    await message.answer(
        t(lang, "menu_text"),
        reply_markup=main_menu_keyboard(lang, is_premium, app.settings.premium_enabled),
    )


async def _show_profile(message: Message, user: Mapping[str, object], lang: str) -> None:
    payload = dict(user)
    if user.get("photo_id"):
        await message.answer_photo(
            photo=str(user["photo_id"]),
            caption=_profile_text(lang, payload),
            reply_markup=profile_keyboard(lang),
        )
        return
    await message.answer(_profile_text(lang, payload), reply_markup=profile_keyboard(lang))


async def _load_user_or_start(message: Message) -> tuple[Mapping[str, object] | None, str]:
    app = get_app(message.bot)
    if message.from_user is None:
        return None, app.settings.default_language

    user = await app.users.get(message.from_user.id)
    if user is None:
        await message.answer("/start")
        return None, app.settings.default_language
    lang = user["language"] or app.settings.default_language
    return user, str(lang)


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
    user, lang = await _load_user_or_start(message)
    if user is None:
        return
    app = get_app(message.bot)
    await message.answer(
        t(lang, "menu_text"),
        reply_markup=main_menu_keyboard(lang, is_premium_active(user), app.settings.premium_enabled),
    )


@router.message(Command("profile"))
async def cmd_profile(message: Message) -> None:
    user, lang = await _load_user_or_start(message)
    if user is None:
        return
    if user["is_banned"]:
        await message.answer(t(lang, "banned"))
        return
    if not is_profile_complete(user):
        await message.answer(t(lang, "profile_incomplete"))
        return
    await _show_profile(message, user, lang)


@router.message(Command("edit_bio"))
async def cmd_edit_bio(message: Message, state: FSMContext) -> None:
    user, lang = await _load_user_or_start(message)
    if user is None:
        return
    if user["is_banned"]:
        await message.answer(t(lang, "banned"))
        return
    if not is_profile_complete(user):
        await message.answer(t(lang, "profile_incomplete"))
        return

    await state.clear()
    await state.set_state(ProfileEditState.bio)
    await message.answer(t(lang, "ask_edit_bio"))


@router.message(Command("edit_photo"))
async def cmd_edit_photo(message: Message, state: FSMContext) -> None:
    user, lang = await _load_user_or_start(message)
    if user is None:
        return
    if user["is_banned"]:
        await message.answer(t(lang, "banned"))
        return
    if not is_profile_complete(user):
        await message.answer(t(lang, "profile_incomplete"))
        return

    await state.clear()
    await state.set_state(ProfileEditState.photo)
    await message.answer(t(lang, "ask_edit_photo"))


@router.message(Command("language"))
async def cmd_language(message: Message, state: FSMContext) -> None:
    user, lang = await _load_user_or_start(message)
    if user is None:
        return
    if user["is_banned"]:
        await message.answer(t(lang, "banned"))
        return

    await state.clear()
    await message.answer(t(lang, "language_choose"), reply_markup=language_settings_keyboard())


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


@router.message(ProfileEditState.bio)
async def save_bio(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    app = get_app(message.bot)
    user = await app.users.get(message.from_user.id)
    if user is None:
        await state.clear()
        await message.answer("/start")
        return
    lang = user["language"] or app.settings.default_language
    if message.text is None:
        await message.answer(t(lang, "invalid_text"))
        return

    bio = message.text.strip()
    if not bio:
        await message.answer(t(lang, "invalid_text"))
        return

    await app.users.update_bio(message.from_user.id, bio[:500])
    await state.clear()
    updated_user = await app.users.get(message.from_user.id)
    is_premium = bool(updated_user and is_premium_active(updated_user))
    await message.answer(t(lang, "edit_bio_saved"))
    await message.answer(
        t(lang, "menu_text"),
        reply_markup=main_menu_keyboard(lang, is_premium, app.settings.premium_enabled),
    )


@router.message(ProfileEditState.photo, F.photo)
async def save_photo(message: Message, state: FSMContext) -> None:
    if message.from_user is None or not message.photo:
        return
    app = get_app(message.bot)
    user = await app.users.get(message.from_user.id)
    if user is None:
        await state.clear()
        await message.answer("/start")
        return
    lang = user["language"] or app.settings.default_language

    await app.users.update_photo(message.from_user.id, message.photo[-1].file_id)
    await state.clear()
    updated_user = await app.users.get(message.from_user.id)
    is_premium = bool(updated_user and is_premium_active(updated_user))
    await message.answer(t(lang, "edit_photo_saved"))
    await message.answer(
        t(lang, "menu_text"),
        reply_markup=main_menu_keyboard(lang, is_premium, app.settings.premium_enabled),
    )


@router.message(ProfileEditState.photo)
async def save_photo_invalid(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    app = get_app(message.bot)
    lang = await app.users.get_language(message.from_user.id, app.settings.default_language)
    await message.answer(t(lang, "invalid_photo"))


@router.callback_query(F.data.startswith("langset:"))
async def language_settings_save(query: CallbackQuery, state: FSMContext) -> None:
    if query.from_user is None or query.data is None or query.message is None:
        return
    app = get_app(query.bot)
    user = await app.users.get(query.from_user.id)
    if user is None:
        await query.message.answer("/start")
        await query.answer()
        return

    language = query.data.split(":", 1)[1]
    if language not in {"en", "my"}:
        language = "en"

    await app.users.set_language(query.from_user.id, language)
    await state.clear()
    updated_user = await app.users.get(query.from_user.id)
    is_premium = bool(updated_user and is_premium_active(updated_user))
    await query.message.answer(t(language, "language_saved"))
    await query.message.answer(
        t(language, "menu_text"),
        reply_markup=main_menu_keyboard(language, is_premium, app.settings.premium_enabled),
    )
    await query.answer()


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
    await _show_profile(query.message, user, str(lang))
    await query.answer()


@router.callback_query(F.data == "profile:edit")
async def profile_edit(query: CallbackQuery, state: FSMContext) -> None:
    if query.from_user is None or query.message is None:
        return
    app = get_app(query.bot)
    lang = await app.users.get_language(query.from_user.id, app.settings.default_language)
    await begin_registration(query.message, state, lang)
    await query.answer()
