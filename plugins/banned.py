from pyrogram import Client, filters
from utils import temp
from pyrogram.types import Message
from database.users_chats_db import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import SUPPORT_CHAT
async def banned_users(_, client, message: Message):
    return (
        message.from_user is not None or not message.sender_chat
    ) and message.from_user.id in temp.BANNED_USERS

banned_user = filters.create(banned_users)

async def disabled_chat(_, client, message: Message):
    return message.chat.id in temp.BANNED_CHATS

disabled_group=filters.create(disabled_chat)


@Client.on_message(filters.private & banned_user & filters.incoming)
async def ban_reply(bot, message):
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply(f'𝑆𝑜𝑟𝑟𝑦 𝐷𝑢𝑑𝑒, 𝑌𝑜𝑢 𝑎𝑟𝑒 𝐵𝑎𝑛𝑛𝑒𝑑 𝑡𝑜 𝑢𝑠𝑒 𝑀𝑒. 𝑇𝑜 𝑢𝑠𝑒 𝑚𝑒 𝐴𝑠𝑘 𝐴𝑑𝑚𝑖𝑛 𝑜𝑟 𝑆𝑒𝑒 𝑡𝒉𝑒 𝑅𝑒𝑎𝑠𝑜𝑛,𝑊𝒉𝑦 𝑦𝑜𝑢 𝑏𝑎𝑛𝑛𝑒𝑑 \nBan 𝑅𝑒𝑎𝑠𝑜𝑛: {ban["ban_reason"]}')

@Client.on_message(filters.group & disabled_group & filters.incoming)
async def grp_bd(bot, message):
    buttons = [[
        InlineKeyboardButton('Support', url=f'https://t.me/HeavenBotSupport')
    ]]
    reply_markup=InlineKeyboardMarkup(buttons)
    vazha = await db.get_chat(message.chat.id)
    k = await message.reply(
        text=f"𝐶𝒉𝑎𝑡 𝐼𝑠 𝑁𝑜𝑡 𝐴𝑙𝑙𝑜𝑤𝑒𝑑 𝐵𝑟𝑜 🐞\n\n𝑀𝑦 𝑎𝑑𝑚𝑖𝑛𝑠 𝒉𝑎𝑠 𝑟𝑒𝑠𝑡𝑟𝑖𝑐𝑡𝑒𝑑 𝑚𝑒 𝑓𝑟𝑜𝑚 𝑤𝑜𝑟𝑘𝑖𝑛𝑔 𝒉𝑒𝑟𝑒 ! 𝐼𝑓 𝑦𝑜𝑢 𝑤𝑎𝑛𝑡 𝑡𝑜 𝑘𝑛𝑜𝑤 𝑚𝑜𝑟𝑒 𝑎𝑏𝑜𝑢𝑡 𝑖𝑡 𝑐𝑜𝑛𝑡𝑎𝑐𝑡 𝑠𝑢𝑝𝑝𝑜𝑟𝑡..\nReason : <code>{vazha['reason']}</code>.",
        reply_markup=reply_markup)
    try:
        await k.pin()
    except:
        pass
    await bot.leave_chat(message.chat.id)
