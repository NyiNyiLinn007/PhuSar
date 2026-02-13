from __future__ import annotations

from datetime import timedelta

from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.context import get_app
from app.locales import t
from app.utils import now_utc, text

router = Router(name="admin")


def _is_admin(admin_ids: set[int], user_id: int) -> bool:
    return user_id in admin_ids


async def _apply_premium_days(user_id: int, days: int, actor_bot, app) -> None:
    user = await app.users.get(user_id)
    base = now_utc()
    if user is not None and user["premium_until"] is not None and user["premium_until"] > base:
        base = user["premium_until"]
    premium_until = base + timedelta(days=days)
    await app.users.set_premium_until(user_id, premium_until)

    user_lang = (user["language"] if user else app.settings.default_language) or app.settings.default_language
    try:
        await actor_bot.send_message(user_id, t(user_lang, "premium_welcome"))
    except TelegramAPIError:
        pass


@router.message(Command("ban"))
async def cmd_ban(message: Message) -> None:
    if message.from_user is None:
        return
    app = get_app(message.bot)
    lang = await app.users.get_language(message.from_user.id, app.settings.default_language)
    if not _is_admin(app.settings.admin_ids, message.from_user.id):
        await message.answer(t(lang, "admin_only"))
        return

    if message.text is None:
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Usage: /ban <user_id>")
        return

    target_id = int(parts[1])
    await app.users.set_banned(target_id, True)
    await message.answer(t(lang, "user_banned"))
    try:
        await message.bot.send_message(target_id, t("en", "banned"))
    except TelegramAPIError:
        pass


@router.message(Command("unban"))
async def cmd_unban(message: Message) -> None:
    if message.from_user is None:
        return
    app = get_app(message.bot)
    lang = await app.users.get_language(message.from_user.id, app.settings.default_language)
    if not _is_admin(app.settings.admin_ids, message.from_user.id):
        await message.answer(t(lang, "admin_only"))
        return

    if message.text is None:
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Usage: /unban <user_id>")
        return

    target_id = int(parts[1])
    await app.users.set_banned(target_id, False)
    await message.answer(t(lang, "user_unbanned"))


@router.message(Command("whereami"))
async def cmd_whereami(message: Message) -> None:
    if message.from_user is None:
        return
    app = get_app(message.bot)
    lang = await app.users.get_language(message.from_user.id, app.settings.default_language)
    if not _is_admin(app.settings.admin_ids, message.from_user.id):
        await message.answer(t(lang, "admin_only"))
        return

    user = await app.users.get(message.from_user.id)
    if user is None:
        await message.answer("/start")
        return

    region = text(user["location_region"] or "-")
    township = text(user["township"] or "-")
    lat = user["latitude"]
    lon = user["longitude"]
    if lat is None or lon is None:
        await message.answer(t(lang, "whereami_empty", region=region, township=township))
        return

    await message.answer(
        t(
            lang,
            "whereami_value",
            lat=f"{float(lat):.6f}",
            lon=f"{float(lon):.6f}",
            region=region,
            township=township,
        )
    )


@router.message(Command("approve"))
async def cmd_approve(message: Message) -> None:
    if message.from_user is None:
        return
    app = get_app(message.bot)
    lang = await app.users.get_language(message.from_user.id, app.settings.default_language)
    if not _is_admin(app.settings.admin_ids, message.from_user.id):
        await message.answer(t(lang, "admin_only"))
        return
    if not app.settings.premium_enabled:
        await message.answer(t(lang, "premium_disabled"))
        return

    if message.text is None:
        return
    parts = message.text.split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
        await message.answer(t(lang, "admin_approve_usage"))
        return

    user_id = int(parts[1])
    days = int(parts[2])
    if days <= 0 or days > 365:
        await message.answer(t(lang, "admin_approve_usage"))
        return

    pending = await app.premium_requests.resolve_latest_pending_for_user(
        user_id=user_id,
        status="approved",
        reviewed_by=message.from_user.id,
    )
    if pending is None:
        await message.answer(t(lang, "premium_no_pending"))
        return

    await _apply_premium_days(user_id=user_id, days=days, actor_bot=message.bot, app=app)
    await message.answer(t(lang, "admin_premium_done", days=days))


@router.message(Command("reject"))
async def cmd_reject(message: Message) -> None:
    if message.from_user is None:
        return
    app = get_app(message.bot)
    lang = await app.users.get_language(message.from_user.id, app.settings.default_language)
    if not _is_admin(app.settings.admin_ids, message.from_user.id):
        await message.answer(t(lang, "admin_only"))
        return
    if not app.settings.premium_enabled:
        await message.answer(t(lang, "premium_disabled"))
        return

    if message.text is None:
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer(t(lang, "admin_reject_usage"))
        return

    user_id = int(parts[1])
    pending = await app.premium_requests.resolve_latest_pending_for_user(
        user_id=user_id,
        status="rejected",
        reviewed_by=message.from_user.id,
    )
    if pending is None:
        await message.answer(t(lang, "premium_no_pending"))
        return

    user = await app.users.get(user_id)
    user_lang = (user["language"] if user else app.settings.default_language) or app.settings.default_language
    try:
        await message.bot.send_message(user_id, t(user_lang, "premium_rejected"))
    except TelegramAPIError:
        pass
    await message.answer(t(lang, "admin_reject_done"))


@router.callback_query(F.data.startswith("premium_decision:"))
async def premium_decision(query: CallbackQuery) -> None:
    if query.data is None or query.from_user is None:
        return
    app = get_app(query.bot)
    if not _is_admin(app.settings.admin_ids, query.from_user.id):
        await query.answer(t(app.settings.default_language, "admin_only"), show_alert=True)
        return
    if not app.settings.premium_enabled:
        await query.answer(t(app.settings.default_language, "premium_disabled"), show_alert=True)
        return

    parts = query.data.split(":")
    if len(parts) != 3:
        await query.answer()
        return
    try:
        request_id = int(parts[1])
    except ValueError:
        await query.answer()
        return
    decision = parts[2]
    if decision not in {"approved", "rejected"}:
        await query.answer()
        return

    request = await app.premium_requests.get(request_id)
    if request is None:
        await query.answer("Request not found.", show_alert=True)
        return
    if request["status"] != "pending":
        await query.answer("Already reviewed.", show_alert=True)
        return

    await app.premium_requests.set_status(request_id, decision, query.from_user.id)
    if decision == "approved":
        await _apply_premium_days(
            user_id=int(request["user_id"]),
            days=int(request["duration_days"] or 7),
            actor_bot=query.bot,
            app=app,
        )
    else:
        user = await app.users.get(int(request["user_id"]))
        user_lang = (user["language"] if user else app.settings.default_language) or app.settings.default_language
        try:
            await query.bot.send_message(int(request["user_id"]), t(user_lang, "premium_rejected"))
        except TelegramAPIError:
            pass

    if query.message is not None:
        try:
            await query.message.edit_reply_markup(reply_markup=None)
        except TelegramAPIError:
            pass
    await query.answer("Reviewed.")


@router.callback_query(F.data.startswith("report_admin:"))
async def report_admin_decision(query: CallbackQuery) -> None:
    if query.data is None or query.from_user is None:
        return
    app = get_app(query.bot)
    if not _is_admin(app.settings.admin_ids, query.from_user.id):
        await query.answer(t(app.settings.default_language, "admin_only"), show_alert=True)
        return

    parts = query.data.split(":")
    if len(parts) != 3:
        await query.answer()
        return
    try:
        report_id = int(parts[1])
    except ValueError:
        await query.answer()
        return
    decision = parts[2]
    if decision not in {"ban", "dismiss"}:
        await query.answer()
        return

    report = await app.reports.get(report_id)
    if report is None:
        await query.answer("Report not found.", show_alert=True)
        return
    if report["status"] != "pending":
        await query.answer("Already reviewed.", show_alert=True)
        return

    if decision == "ban":
        await app.users.set_banned(int(report["target_id"]), True)
        await app.reports.set_status(report_id, "banned", query.from_user.id)
        try:
            await query.bot.send_message(int(report["target_id"]), t("en", "banned"))
        except TelegramAPIError:
            pass
    else:
        await app.reports.set_status(report_id, "dismissed", query.from_user.id)

    if query.message is not None:
        try:
            await query.message.edit_reply_markup(reply_markup=None)
        except TelegramAPIError:
            pass
    await query.answer("Updated.")
