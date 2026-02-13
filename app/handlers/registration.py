from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from app.context import get_app
from app.keyboards import (
    gender_keyboard,
    language_keyboard,
    location_keyboard,
    main_menu_keyboard,
    region_keyboard,
    seeking_keyboard,
)
from app.locales import REGION_LABELS, t
from app.states import RegistrationState
from app.utils import is_premium_active, is_profile_complete

router = Router(name="registration")


async def begin_registration(message: Message, state: FSMContext, language_hint: str) -> None:
    await state.clear()
    await state.set_state(RegistrationState.language)
    await state.update_data(language=language_hint)
    await message.answer(t(language_hint, "choose_language"), reply_markup=language_keyboard())


@router.callback_query(RegistrationState.language, F.data.startswith("lang:"))
async def registration_language(query: CallbackQuery, state: FSMContext) -> None:
    if query.data is None or query.from_user is None or query.message is None:
        return

    language = query.data.split(":", 1)[1]
    if language not in {"en", "my"}:
        language = "en"

    app = get_app(query.bot)
    await app.users.set_language(query.from_user.id, language)
    await state.update_data(language=language)
    await state.set_state(RegistrationState.full_name)
    await query.message.answer(t(language, "ask_name"))
    await query.answer()


@router.message(RegistrationState.full_name)
async def registration_name(message: Message, state: FSMContext) -> None:
    if message.text is None:
        data = await state.get_data()
        lang = data.get("language", "en")
        await message.answer(t(lang, "invalid_text"))
        return

    display_name = message.text.strip()
    data = await state.get_data()
    lang = data.get("language", "en")
    if not display_name:
        await message.answer(t(lang, "invalid_text"))
        return

    await state.update_data(full_name=display_name[:100])
    await state.set_state(RegistrationState.gender)
    await message.answer(t(lang, "ask_gender"), reply_markup=gender_keyboard(lang))


@router.callback_query(RegistrationState.gender, F.data.startswith("gender:"))
async def registration_gender(query: CallbackQuery, state: FSMContext) -> None:
    if query.data is None or query.message is None:
        return

    gender = query.data.split(":", 1)[1]
    if gender not in {"male", "female"}:
        await query.answer()
        return

    data = await state.get_data()
    lang = data.get("language", "en")
    await state.update_data(gender=gender)
    await state.set_state(RegistrationState.seeking)
    await query.message.answer(t(lang, "ask_seeking"), reply_markup=seeking_keyboard(lang))
    await query.answer()


@router.callback_query(RegistrationState.seeking, F.data.startswith("seek:"))
async def registration_seeking(query: CallbackQuery, state: FSMContext) -> None:
    if query.data is None or query.message is None:
        return

    seeking = query.data.split(":", 1)[1]
    if seeking not in {"male", "female", "both"}:
        await query.answer()
        return

    data = await state.get_data()
    lang = data.get("language", "en")
    await state.update_data(seeking=seeking)
    await state.set_state(RegistrationState.region)
    await query.message.answer(t(lang, "ask_region"), reply_markup=region_keyboard(lang))
    await query.answer()


@router.callback_query(RegistrationState.region, F.data.startswith("region:"))
async def registration_region(query: CallbackQuery, state: FSMContext) -> None:
    if query.data is None or query.message is None:
        return

    region_code = query.data.split(":", 1)[1]
    if region_code not in REGION_LABELS:
        await query.answer()
        return

    data = await state.get_data()
    lang = data.get("language", "en")
    await state.update_data(region_code=region_code, location_mode="registration")
    await state.set_state(RegistrationState.ask_location)
    await query.message.answer(t(lang, "ask_location"), reply_markup=location_keyboard(lang))
    await query.answer()


@router.message(RegistrationState.ask_location, F.location)
async def registration_location(message: Message, state: FSMContext) -> None:
    if message.from_user is None or message.location is None:
        return

    app = get_app(message.bot)
    data = await state.get_data()
    lang = data.get("language", app.settings.default_language)
    latitude = float(message.location.latitude)
    longitude = float(message.location.longitude)
    mode = data.get("location_mode", "registration")

    if mode == "update":
        await app.users.update_coordinates(message.from_user.id, latitude, longitude)
        await app.discovery.clear_queue(message.from_user.id)
        updated_user = await app.users.get(message.from_user.id)
        await state.clear()
        is_premium = bool(updated_user and is_premium_active(updated_user))
        await message.answer(t(lang, "location_updated"), reply_markup=ReplyKeyboardRemove())
        await message.answer(
            t(lang, "menu_text"),
            reply_markup=main_menu_keyboard(lang, is_premium, app.settings.premium_enabled),
        )
        return

    await state.update_data(
        latitude=latitude,
        longitude=longitude,
        township=t(lang, "township_from_gps"),
    )
    await state.set_state(RegistrationState.age)
    await message.answer(t(lang, "location_received"), reply_markup=ReplyKeyboardRemove())
    await message.answer(t(lang, "ask_age"))


@router.message(RegistrationState.ask_location)
async def registration_location_fallback(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    mode = data.get("location_mode", "registration")
    text_value = (message.text or "").strip()

    if mode == "registration" and text_value == t(lang, "btn_township_manual"):
        await state.update_data(latitude=None, longitude=None)
        await state.set_state(RegistrationState.township)
        await message.answer(t(lang, "ask_township"), reply_markup=ReplyKeyboardRemove())
        return

    await message.answer(t(lang, "location_share_required"), reply_markup=location_keyboard(lang))


@router.message(RegistrationState.township)
async def registration_township(message: Message, state: FSMContext) -> None:
    if message.text is None:
        data = await state.get_data()
        lang = data.get("language", "en")
        await message.answer(t(lang, "invalid_text"))
        return

    township = message.text.strip()
    data = await state.get_data()
    lang = data.get("language", "en")
    if not township:
        await message.answer(t(lang, "invalid_text"))
        return

    await state.update_data(township=township[:50])
    await state.set_state(RegistrationState.age)
    await message.answer(t(lang, "ask_age"))


@router.message(RegistrationState.age)
async def registration_age(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    if message.text is None:
        await message.answer(t(lang, "invalid_age"))
        return

    raw_age = message.text.strip()
    if not raw_age.isdigit():
        await message.answer(t(lang, "invalid_age"))
        return

    age = int(raw_age)
    if age < 18 or age > 99:
        await message.answer(t(lang, "invalid_age"))
        return

    await state.update_data(age=age)
    await state.set_state(RegistrationState.bio)
    await message.answer(t(lang, "ask_bio"))


@router.message(RegistrationState.bio)
async def registration_bio(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    if message.text is None:
        await message.answer(t(lang, "invalid_text"))
        return

    bio = message.text.strip()
    if not bio:
        await message.answer(t(lang, "invalid_text"))
        return

    await state.update_data(bio=bio[:500])
    await state.set_state(RegistrationState.photo)
    await message.answer(t(lang, "ask_photo"))


@router.message(RegistrationState.photo, F.photo)
async def registration_photo(message: Message, state: FSMContext) -> None:
    if message.from_user is None or not message.photo:
        return

    app = get_app(message.bot)
    data = await state.get_data()
    language = data.get("language", app.settings.default_language)
    region_code = data.get("region_code", "other")
    region_name = REGION_LABELS.get(region_code, REGION_LABELS["other"])["en"]
    photo_id = message.photo[-1].file_id

    await app.users.save_registration(
        user_id=message.from_user.id,
        full_name=data.get("full_name", message.from_user.full_name or "User"),
        language=language,
        gender=data["gender"],
        seeking=data["seeking"],
        location_region=region_name,
        township=data["township"],
        age=int(data["age"]),
        bio=data["bio"],
        photo_id=photo_id,
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
    )
    await app.discovery.clear_queue(message.from_user.id)
    updated_user = await app.users.get(message.from_user.id)
    await state.clear()
    is_premium = bool(updated_user and is_premium_active(updated_user))
    await message.answer(t(language, "profile_saved"))
    await message.answer(
        t(language, "menu_text"),
        reply_markup=main_menu_keyboard(language, is_premium, app.settings.premium_enabled),
    )


@router.message(RegistrationState.photo)
async def registration_photo_invalid(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "en")
    await message.answer(t(lang, "invalid_photo"))


@router.message(Command("location"))
async def cmd_location(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    app = get_app(message.bot)
    user = await app.users.get(message.from_user.id)
    if user is None:
        await message.answer("/start")
        return

    lang = user["language"] or app.settings.default_language
    if user["is_banned"]:
        await message.answer(t(lang, "banned"))
        return
    if not is_profile_complete(user):
        await message.answer(t(lang, "profile_incomplete"))
        return

    await state.clear()
    await state.set_state(RegistrationState.ask_location)
    await state.update_data(language=lang, location_mode="update")
    await message.answer(t(lang, "ask_location_update"), reply_markup=location_keyboard(lang))


@router.message(Command("cancel"))
async def cancel_state(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    app = get_app(message.bot)
    lang = app.settings.default_language
    if message.from_user is not None:
        lang = await app.users.get_language(message.from_user.id, app.settings.default_language)

    await state.clear()
    user = await app.users.get(message.from_user.id) if message.from_user is not None else None
    is_premium = bool(user and is_premium_active(user))
    await message.answer(t(lang, "registration_cancelled"), reply_markup=ReplyKeyboardRemove())
    await message.answer(t(lang, "menu_text"), reply_markup=main_menu_keyboard(lang, is_premium, app.settings.premium_enabled))
