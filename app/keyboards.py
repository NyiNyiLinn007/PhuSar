from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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


def main_menu_keyboard(lang: str, is_premium: bool) -> InlineKeyboardMarkup:
    premium_label = f"\u2705 {t(lang, 'btn_premium')}" if is_premium else f"\U0001F31F {t(lang, 'btn_premium')}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"\U0001F50E {t(lang, 'btn_discover')}", callback_data="menu:discover")],
            [InlineKeyboardButton(text=premium_label, callback_data="menu:premium")],
            [InlineKeyboardButton(text=f"\U0001F464 {t(lang, 'btn_profile')}", callback_data="menu:profile")],
        ]
    )


def profile_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"\u270F\ufe0f {t(lang, 'btn_edit')}", callback_data="profile:edit")],
            [InlineKeyboardButton(text=f"\U0001F50E {t(lang, 'btn_discover')}", callback_data="menu:discover")],
        ]
    )


def discovery_keyboard(lang: str, target_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "btn_like"), callback_data=f"act:{target_id}:like"),
                InlineKeyboardButton(text=t(lang, "btn_pass"), callback_data=f"act:{target_id}:dislike"),
            ],
            [
                InlineKeyboardButton(text=t(lang, "btn_superlike"), callback_data=f"act:{target_id}:superlike"),
            ],
            [
                InlineKeyboardButton(text=t(lang, "btn_report"), callback_data=f"report:{target_id}"),
            ],
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
            [
                InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="report_cancel"),
            ],
        ]
    )


def premium_provider_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "btn_kbz"), callback_data="premium_provider:kbzpay"),
                InlineKeyboardButton(text=t(lang, "btn_wave"), callback_data="premium_provider:wavemoney"),
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
