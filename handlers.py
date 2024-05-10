from aiogram import types, Router, Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramBadRequest
import config
import os
import sys
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter


bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

def escape_markdown(text):
    special_characters = '\\`*_{}[]()#+-.!~><=|'
    for char in special_characters:
        text = text.replace(char, '\\' + char)
    return text

@router.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer("Бот для получения подписчиков/отписчиков")

@router.message(Command("restart"))
async def restart(msg: Message):
    await msg.answer("Перезапуск бота...\n")
    python = sys.executable
    os.execl(python, python, *sys.argv)

@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_leave(event: ChatMemberUpdatedFilter):
    full_name = escape_markdown(event.old_chat_member.user.full_name)
    username = escape_markdown(event.old_chat_member.user.username)
    url = escape_markdown(event.old_chat_member.user.url)
    id = event.new_chat_member.user.id
    for id in config.ADMINS_ID:
        try:
            await bot.send_message(id, f"Пользователь покинул канал\:\n[{full_name}]({url})\n\@{username}\n{id}")
        except TelegramBadRequest as e:
            print(str(e))
            continue

@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdatedFilter):
    full_name = escape_markdown(event.new_chat_member.user.full_name)
    username = escape_markdown(event.new_chat_member.user.username)
    url = escape_markdown(event.new_chat_member.user.url)
    id = event.new_chat_member.user.id
    for id in config.ADMINS_ID:
        try:
            await bot.send_message(id, f"Пользователь присоединился\:\n[{full_name}]({url})\n@{username}\n{id}")
        except TelegramBadRequest as e:
            print(str(e))
            continue
