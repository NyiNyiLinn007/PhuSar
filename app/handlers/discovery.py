from __future__ import annotations

from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.context import get_app
from app.keyboards import admin_report_keyboard, discovery_keyboard, main_menu_keyboard, report_reason_keyboard
from app.locales import gender_label, report_reason_label, t
from app.utils import distance_between_users_km, is_premium_active, is_profile_complete, text

router = Router(name="discovery")


def _candidate_caption(lang: str, profile: dict[str, object], distance_km: float | None = None) -> str:
    location_line = (
        f"{t(lang, 'label_location')}: "
        f"{text(profile.get('location_region') or '-')}, {text(profile.get('township') or '-')}"
    )
    if distance_km is not None:
        location_line += f"\n{t(lang, 'distance_away', km=f'{distance_km:.1f}')}"

    return (
        f"<b>{text(profile.get('full_name') or 'Unknown')}</b>, {text(profile.get('age') or '-')}\n"
        f"{t(lang, 'label_gender')}: {text(gender_label(lang, str(profile.get('gender') or '-')))}\n"
        f"{location_line}\n\n"
        f"{text(profile.get('bio') or '-')}"
    )


async def _show_profile_card(
    message: Message,
    lang: str,
    candidate: dict[str, object],
    viewer: dict[str, object] | None = None,
) -> None:
    app = get_app(message.bot)
    distance_km = distance_between_users_km(viewer, candidate) if viewer is not None else None
    await message.answer_photo(
        photo=candidate["photo_id"],  # type: ignore[arg-type]
        caption=_candidate_caption(lang, candidate, distance_km),
        reply_markup=discovery_keyboard(lang, int(candidate["user_id"]), app.settings.premium_enabled),
    )


async def _send_next_profile(message: Message, viewer_id: int) -> None:
    app = get_app(message.bot)
    viewer = await app.users.get(viewer_id)
    if viewer is None:
        await message.answer("/start")
        return

    lang = viewer["language"] or app.settings.default_language
    premium = is_premium_active(viewer)
    if viewer["is_banned"]:
        await message.answer(t(lang, "banned"))
        return

    if not is_profile_complete(viewer):
        await message.answer(t(lang, "profile_incomplete"))
        return

    candidate_id = await app.discovery.next_candidate_id(viewer)
    if candidate_id is None:
        await message.answer(
            t(lang, "no_profiles"),
            reply_markup=main_menu_keyboard(lang, premium, app.settings.premium_enabled),
        )
        return

    candidate = await app.users.get(candidate_id)
    if candidate is None:
        await app.discovery.clear_queue(viewer_id)
        await message.answer(
            t(lang, "no_profiles"),
            reply_markup=main_menu_keyboard(lang, premium, app.settings.premium_enabled),
        )
        return

    await _show_profile_card(message, lang, dict(candidate), dict(viewer))


@router.message(Command("discover"))
async def cmd_discover(message: Message) -> None:
    if message.from_user is None:
        return
    await _send_next_profile(message, message.from_user.id)


@router.message(Command("liked"))
async def cmd_liked_you(message: Message) -> None:
    if message.from_user is None:
        return
    app = get_app(message.bot)
    user = await app.users.get(message.from_user.id)
    if user is None:
        await message.answer("/start")
        return
    lang = user["language"] or app.settings.default_language
    if not app.settings.premium_enabled:
        await message.answer(t(lang, "premium_disabled"))
        return
    if not is_premium_active(user):
        await message.answer(t(lang, "liked_you_locked"))
        return

    likers = await app.actions.list_incoming_likes(message.from_user.id, limit=20)
    if not likers:
        await message.answer(t(lang, "liked_you_empty"))
        return
    await message.answer(t(lang, "liked_you_intro"))
    for liker in likers:
        await _show_profile_card(message, lang, dict(liker), dict(user))


@router.message(Command("boost"))
async def cmd_boost(message: Message) -> None:
    if message.from_user is None:
        return
    app = get_app(message.bot)
    actor = await app.users.get(message.from_user.id)
    if actor is None:
        await message.answer("/start")
        return
    lang = actor["language"] or app.settings.default_language
    if not app.settings.premium_enabled:
        await message.answer(t(lang, "premium_disabled"))
        return
    if not is_premium_active(actor):
        await message.answer(t(lang, "boost_locked"))
        return

    viewer_ids = await app.users.list_boost_viewer_ids(
        actor_id=message.from_user.id,
        actor_gender=actor["gender"],
        actor_seeking=actor["seeking"],
        actor_region=actor["location_region"],
        limit=100,
    )
    await app.discovery.push_candidate_to_viewers(message.from_user.id, viewer_ids)
    await message.answer(t(lang, "boost_done"))


@router.callback_query(F.data == "menu:discover")
async def menu_discover(query: CallbackQuery) -> None:
    if query.from_user is None or query.message is None:
        return
    await _send_next_profile(query.message, query.from_user.id)
    await query.answer()


@router.callback_query(F.data == "menu:liked_you")
async def menu_liked_you(query: CallbackQuery) -> None:
    if query.from_user is None or query.message is None:
        return
    app = get_app(query.bot)
    user = await app.users.get(query.from_user.id)
    if user is None:
        await query.answer()
        return
    lang = user["language"] or app.settings.default_language
    if not app.settings.premium_enabled:
        await query.message.answer(t(lang, "premium_disabled"))
        await query.answer()
        return
    if not is_premium_active(user):
        await query.message.answer(t(lang, "liked_you_locked"))
        await query.answer()
        return

    likers = await app.actions.list_incoming_likes(query.from_user.id, limit=20)
    if not likers:
        await query.message.answer(t(lang, "liked_you_empty"))
        await query.answer()
        return
    await query.message.answer(t(lang, "liked_you_intro"))
    for liker in likers:
        await _show_profile_card(query.message, lang, dict(liker), dict(user))
    await query.answer()


@router.callback_query(F.data == "menu:boost")
async def menu_boost(query: CallbackQuery) -> None:
    if query.from_user is None or query.message is None:
        return
    app = get_app(query.bot)
    actor = await app.users.get(query.from_user.id)
    if actor is None:
        await query.answer()
        return
    lang = actor["language"] or app.settings.default_language
    if not app.settings.premium_enabled:
        await query.message.answer(t(lang, "premium_disabled"))
        await query.answer()
        return
    if not is_premium_active(actor):
        await query.message.answer(t(lang, "boost_locked"))
        await query.answer()
        return

    viewer_ids = await app.users.list_boost_viewer_ids(
        actor_id=query.from_user.id,
        actor_gender=actor["gender"],
        actor_seeking=actor["seeking"],
        actor_region=actor["location_region"],
        limit=100,
    )
    await app.discovery.push_candidate_to_viewers(query.from_user.id, viewer_ids)
    await query.message.answer(t(lang, "boost_done"))
    await query.answer()


@router.callback_query(F.data == "act:rewind")
async def rewind_last_pass(query: CallbackQuery) -> None:
    if query.from_user is None or query.message is None:
        return
    app = get_app(query.bot)
    actor = await app.users.get(query.from_user.id)
    if actor is None:
        await query.answer()
        return
    lang = actor["language"] or app.settings.default_language
    if not app.settings.premium_enabled:
        await query.message.answer(t(lang, "premium_disabled"))
        await query.answer()
        return

    target_id = await app.discovery.pop_last_disliked(query.from_user.id)
    if target_id is None:
        await query.message.answer(t(lang, "rewind_missing"))
        await query.answer()
        return

    await app.actions.delete_action(query.from_user.id, target_id)
    target = await app.users.get(target_id)
    if target is None:
        await query.message.answer(t(lang, "rewind_missing"))
        await query.answer()
        return

    await query.message.answer(t(lang, "rewind_done"))
    await _show_profile_card(query.message, lang, dict(target), dict(actor))
    await query.answer()


@router.callback_query(F.data.startswith("act:"))
async def profile_action(query: CallbackQuery) -> None:
    if query.data is None or query.from_user is None or query.message is None:
        return

    parts = query.data.split(":")
    if len(parts) != 3:
        await query.answer()
        return

    try:
        target_id = int(parts[1])
    except ValueError:
        await query.answer()
        return
    action = parts[2]
    app = get_app(query.bot)
    allowed_actions = {"like", "dislike", "superlike"} if app.settings.premium_enabled else {"like", "dislike"}
    if action not in allowed_actions:
        await query.answer()
        return

    actor_id = query.from_user.id
    target_user = await app.users.get(target_id)
    if target_user is None:
        await query.answer()
        await _send_next_profile(query.message, actor_id)
        return

    await app.actions.save_action(actor_id, target_id, action)
    actor = await app.users.get(actor_id)
    if action == "dislike":
        await app.discovery.set_last_disliked(actor_id, target_id)

    try:
        await query.message.edit_reply_markup(reply_markup=None)
    except TelegramAPIError:
        pass

    if action == "superlike":
        actor = actor or await app.users.get(actor_id)
        if actor is not None:
            target_lang = target_user["language"] or app.settings.default_language
            actor_name = actor["full_name"] or "Someone"
            try:
                await query.bot.send_message(target_id, t(target_lang, "superlike_received", name=text(actor_name)))
            except TelegramAPIError:
                pass

    if action in {"like", "superlike"} and await app.actions.has_positive_action(target_id, actor_id):
        actor = await app.users.get(actor_id)
        target = target_user
        if actor and target:
            actor_lang = actor["language"] or app.settings.default_language
            target_lang = target["language"] or app.settings.default_language
            actor_name = actor["full_name"] or "Someone"
            target_name = target["full_name"] or "Someone"

            await query.message.answer(t(actor_lang, "match", name=text(target_name)))
            try:
                await query.bot.send_message(target_id, t(target_lang, "match", name=text(actor_name)))
            except TelegramAPIError:
                pass

    await query.answer()
    await _send_next_profile(query.message, actor_id)


@router.callback_query(F.data.startswith("report:"))
async def report_prompt(query: CallbackQuery) -> None:
    if query.data is None or query.message is None or query.from_user is None:
        return
    parts = query.data.split(":")
    if len(parts) != 2:
        await query.answer()
        return
    try:
        target_id = int(parts[1])
    except ValueError:
        await query.answer()
        return

    app = get_app(query.bot)
    lang = await app.users.get_language(query.from_user.id, app.settings.default_language)
    await query.message.answer(t(lang, "report_prompt"), reply_markup=report_reason_keyboard(lang, target_id))
    await query.answer()


@router.callback_query(F.data == "report_cancel")
async def report_cancel(query: CallbackQuery) -> None:
    await query.answer()
    if query.message is not None:
        try:
            await query.message.edit_reply_markup(reply_markup=None)
        except TelegramAPIError:
            pass


@router.callback_query(F.data.startswith("report_reason:"))
async def report_submit(query: CallbackQuery) -> None:
    if query.data is None or query.message is None or query.from_user is None:
        return
    parts = query.data.split(":")
    if len(parts) != 3:
        await query.answer()
        return

    try:
        target_id = int(parts[1])
    except ValueError:
        await query.answer()
        return
    reason = parts[2]
    if reason not in {"fake", "spam", "inappropriate", "abusive"}:
        await query.answer()
        return

    app = get_app(query.bot)
    reporter = await app.users.get(query.from_user.id)
    lang = (reporter["language"] if reporter else app.settings.default_language) or app.settings.default_language
    report_id = await app.reports.create(query.from_user.id, target_id, reason)

    target_user = await app.users.get(target_id)
    reason_en = report_reason_label("en", reason)
    reporter_name = reporter["full_name"] if reporter else str(query.from_user.id)
    target_name = target_user["full_name"] if target_user else str(target_id)
    admin_text = (
        f"Report #{report_id}\n"
        f"Reporter: {text(reporter_name)} ({query.from_user.id})\n"
        f"Target: {text(target_name)} ({target_id})\n"
        f"Reason: {text(reason_en)}"
    )
    for admin_id in app.settings.admin_ids:
        try:
            await query.bot.send_message(
                admin_id,
                admin_text,
                reply_markup=admin_report_keyboard(report_id),
            )
        except TelegramAPIError:
            continue

    await query.message.answer(t(lang, "report_submitted"))
    try:
        await query.message.edit_reply_markup(reply_markup=None)
    except TelegramAPIError:
        pass
    await query.answer()
