from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from app.locales import REGION_LABELS, report_reason_label, t


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("my", "lang_name"), callback_data="lang:my"),
                InlineKeyboardButton(text=t("en", "lang_name"), callback_data="lang:en"),
            ]
        ]
    )


def gender_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "btn_male"), callback_data="gender:male"),
                InlineKeyboardButton(text=t(lang, "btn_female"), callback_data="gender:female"),
            ]
        ]
    )


def seeking_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "btn_male"), callback_data="seek:male"),
                InlineKeyboardButton(text=t(lang, "btn_female"), callback_data="seek:female"),
                InlineKeyboardButton(text=t(lang, "btn_both"), callback_data="seek:both"),
            ]
        ]
    )


def region_keyboard(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=label.get(lang, label["en"]), callback_data=f"region:{code}")
        for code, label in REGION_LABELS.items()
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            buttons[0:2],
            buttons[2:4],
            buttons[4:6],
        ]
    )


def location_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "btn_share_location"), request_location=True)],
            [KeyboardButton(text=t(lang, "btn_township_manual"))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def main_menu_keyboard(lang: str, is_premium: bool, premium_enabled: bool) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=f"\U0001F50E {t(lang, 'btn_discover')}", callback_data="menu:discover")],
        [InlineKeyboardButton(text=f"\U0001F464 {t(lang, 'btn_profile')}", callback_data="menu:profile")],
    ]
    if premium_enabled:
        premium_label = f"\u2705 {t(lang, 'btn_premium')}" if is_premium else f"\U0001F31F {t(lang, 'btn_premium')}"
        liked_you_label = t(lang, "btn_liked_you") if is_premium else f"\U0001F512 {t(lang, 'btn_liked_you')}"
        boost_label = f"\U0001F680 {t(lang, 'btn_boost')}" if is_premium else f"\U0001F512 {t(lang, 'btn_boost')}"
        rows = [
            [InlineKeyboardButton(text=f"\U0001F50E {t(lang, 'btn_discover')}", callback_data="menu:discover")],
            [InlineKeyboardButton(text=liked_you_label, callback_data="menu:liked_you")],
            [InlineKeyboardButton(text=boost_label, callback_data="menu:boost")],
            [InlineKeyboardButton(text=premium_label, callback_data="menu:premium")],
            [InlineKeyboardButton(text=f"\U0001F464 {t(lang, 'btn_profile')}", callback_data="menu:profile")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def profile_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"\u270F\ufe0f {t(lang, 'btn_edit')}", callback_data="profile:edit")],
            [InlineKeyboardButton(text=f"\U0001F50E {t(lang, 'btn_discover')}", callback_data="menu:discover")],
        ]
    )


def discovery_keyboard(lang: str, target_id: int, premium_enabled: bool) -> InlineKeyboardMarkup:
    first_row = [
        InlineKeyboardButton(text=t(lang, "btn_like"), callback_data=f"act:{target_id}:like"),
        InlineKeyboardButton(text=t(lang, "btn_pass"), callback_data=f"act:{target_id}:dislike"),
    ]
    rows: list[list[InlineKeyboardButton]] = [
        first_row,
        [InlineKeyboardButton(text=t(lang, "btn_report"), callback_data=f"report:{target_id}")],
    ]
    if premium_enabled:
        first_row.append(InlineKeyboardButton(text=t(lang, "btn_superlike"), callback_data=f"act:{target_id}:superlike"))
        rows.insert(1, [InlineKeyboardButton(text=t(lang, "btn_rewind"), callback_data="act:rewind")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def like_back_keyboard(lang: str, target_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "btn_like_back"), callback_data=f"act:{target_id}:like"),
                InlineKeyboardButton(text=t(lang, "btn_pass"), callback_data=f"act:{target_id}:dislike"),
            ],
            [InlineKeyboardButton(text=t(lang, "btn_report"), callback_data=f"report:{target_id}")],
        ]
    )


def report_reason_keyboard(lang: str, target_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=report_reason_label(lang, "fake"),
                    callback_data=f"report_reason:{target_id}:fake",
                ),
                InlineKeyboardButton(
                    text=report_reason_label(lang, "spam"),
                    callback_data=f"report_reason:{target_id}:spam",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=report_reason_label(lang, "inappropriate"),
                    callback_data=f"report_reason:{target_id}:inappropriate",
                ),
                InlineKeyboardButton(
                    text=report_reason_label(lang, "abusive"),
                    callback_data=f"report_reason:{target_id}:abusive",
                ),
            ],
            [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="report_cancel")],
        ]
    )


def premium_plan_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "premium_plan_weekly"), callback_data="premium_plan:weekly")],
            [InlineKeyboardButton(text=t(lang, "premium_plan_monthly"), callback_data="premium_plan:monthly")],
            [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="premium_plan:cancel")],
        ]
    )


def premium_provider_keyboard(lang: str, plan_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "btn_kbz"), callback_data=f"premium_provider:{plan_code}:kbzpay"),
                InlineKeyboardButton(
                    text=t(lang, "btn_wave"),
                    callback_data=f"premium_provider:{plan_code}:wavemoney",
                ),
            ],
            [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="premium_provider:cancel")],
        ]
    )


def admin_premium_keyboard(request_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\u2705 Approve",
                    callback_data=f"premium_decision:{request_id}:approved",
                ),
                InlineKeyboardButton(
                    text="\u274C Reject",
                    callback_data=f"premium_decision:{request_id}:rejected",
                ),
            ]
        ]
    )


def admin_report_keyboard(report_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="\U0001F6AB Ban User",
                    callback_data=f"report_admin:{report_id}:ban",
                ),
                InlineKeyboardButton(text="Dismiss", callback_data=f"report_admin:{report_id}:dismiss"),
            ]
        ]
    )
