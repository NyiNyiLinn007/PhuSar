from __future__ import annotations

from aiogram import Bot
from aiogram.types import BotCommand


DEFAULT_COMMANDS = [
    BotCommand(command="profile", description="My Profile (ငါ့ရဲ့ Profile)"),
    BotCommand(command="edit_photo", description="Change my photo (ပုံပြောင်းမည်)"),
    BotCommand(command="edit_bio", description="Change my bio text (Bio ပြင်မည်)"),
    BotCommand(command="language", description="Change Language (ဘာသာစကား)"),
]


async def setup_default_commands(bot: Bot) -> None:
    await bot.set_my_commands(DEFAULT_COMMANDS)
