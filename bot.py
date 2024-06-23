# (c) @LazyDeveloperr

import os
import asyncio
import traceback
lazy_pic = os.environ.get("LAZY_PIC","")
from binascii import (
    Error
)
from pyrogram import (
    Client,
    enums,
    filters
)
from pyrogram.errors import (
    UserNotParticipant,
    FloodWait,
    QueryIdInvalid
)
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message
)
from configs import Config
from configs import *
from handlers.database import db
from handlers.add_user_to_db import add_user_to_database
from handlers.send_file import send_media_and_reply
from handlers.helpers import b64_to_str, str_to_b64
from handlers.check_user_status import handle_user_status
from handlers.force_sub_handler import (
    handle_force_sub,
    get_invite_link
)
import logging
import logging.config
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

from handlers.broadcast_handlers import main_broadcast_handler
from handlers.save_media import (
    save_media_in_channel,
    save_batch_media_in_channel
)
from util.human_readable import humanbytes
from urllib.parse import quote_plus
from util.file_properties import get_name, get_hash, get_media_file_size
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from handlers.send_file import media_forward
from pyrogram import idle
from lazybot import Bot
from util.keepalive import ping_server
from lazybot.clients import initialize_clients
from aiohttp import web
from handlers import web_server
from pyrogram import Client, __version__
from handlers.helpers import  decode, get_messages
from pyrogram.enums import ParseMode
import sys


MediaList = {}
Bot.start()
loop = asyncio.get_event_loop()

PORT = "8080"

async def Lazy_start():
    print('\n')
    print(' Initalizing clients ')
    await initialize_clients()
    try:
        db_channel = await Bot.get_chat(Config.DB_CHANNEL)
        Bot.db_channel = db_channel
        test = await Bot.send_message(chat_id=db_channel.id, text="TEST")
        await test.delete()
        print("Bot is admin in db channel")

    except Exception as e:
        # Handle the exception, log it, and optionally take other actions
        print(e)  # Print the error for debugging
        print(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
        print("\nBot Stopped bYE")
        sys.exit()
    @Bot.on_message(filters.private)
    async def _(bot: Client, cmd: Message):
        await handle_user_status(bot, cmd)


    @Bot.on_message(filters.command("start") & filters.private)
    async def start(bot: Client, cmd: Message):

        if cmd.from_user.id in Config.BANNED_USERS:
            await cmd.reply_text("ꜱᴏʀʀʏ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ.")
            return
        if Config.UPDATES_CHANNEL is not None:
            back = await handle_force_sub(bot, cmd)
            if back == 400:
                return
        usr_cmd = cmd.text.split("_", 1)[-1]
        if usr_cmd == "/start":
            await add_user_to_database(bot, cmd)
            if(Config.LAZY_MODE == True):
                await cmd.reply_photo(photo=lazy_pic,
                caption=Config.LAZY_HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🍿suppor† group", url="https://t.me/codeconvo"),
                            InlineKeyboardButton("🔊Books channel", url="https://t.me/books_groupp")
                        ],
                        [
                            InlineKeyboardButton("About Bot", callback_data="aboutbot"),
                            InlineKeyboardButton("About Dev", callback_data="aboutdevs")
                        ],
                        [
                            InlineKeyboardButton("Courses Channel", url="https://t.me/course_guy")
                        ]]))
            else :
                await cmd.reply_photo(photo=lazy_pic,
                caption=Config.HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🍿suppor† group", url="https://t.me/codeconvo"),
                            InlineKeyboardButton("🔊Books channel", url="https://t.me/books_groupp")
                        ],
                        [
                            InlineKeyboardButton("About Bot", callback_data="aboutbot"),
                            InlineKeyboardButton("About Dev", callback_data="aboutdevs")
                        ],
                        [
                            InlineKeyboardButton("Courses Channel", url="https://t.me/course_guy")
                        ]]))
            
        else:
            try:
                try:
                    file_id = int(b64_to_str(usr_cmd).split("_")[-1])
                except (Error, UnicodeDecodeError):
                    file_id = int(usr_cmd.split("_")[-1])
                GetMessage = await bot.get_messages(chat_id=Config.DB_CHANNEL, message_ids=file_id)
                message_ids = []
                if GetMessage.text:
                    message_ids = GetMessage.text.split(" ")
                    _response_msg = await cmd.reply_text(
                        text=f"**Total Files:** `{len(message_ids)}`",
                        quote=True,
                        disable_web_page_preview=True
                    )
                else:
                    message_ids.append(int(GetMessage.id))

                for i in range(len(message_ids)):
                    await send_media_and_reply(bot, user_id=cmd.from_user.id, file_id=int(message_ids[i]))

            except Exception as err:
                print(err)
                await cmd.reply_text(f"ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.!\n\n**Error:** `{err}`")
        

    @Bot.on_message((filters.document | filters.video | filters.audio) & ~filters.chat(Config.DB_CHANNEL))
    async def main(bot: Client, message: Message):

        if message.chat.type == enums.ChatType.PRIVATE:

            await add_user_to_database(bot, message)

            if Config.UPDATES_CHANNEL is not None:
                back = await handle_force_sub(bot, message)
                if back == 400:
                    return

            if message.from_user.id in Config.BANNED_USERS:
                await message.reply_text("ꜱᴏʀʀʏ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!\n\nContact [Support Group](https://t.me/codeconvo)",
                                        disable_web_page_preview=True)
                return

            if Config.OTHER_USERS_CAN_SAVE_FILE is False:
                return

            await message.reply_text(
                text="ᴄʜᴏᴏꜱᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ꜰʀᴏᴍ ʙᴇʟᴏᴡ:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Save in Batch", callback_data="addToBatchTrue")],
                    [InlineKeyboardButton("Get File Link", callback_data="addToBatchFalse")]
                ]),
                quote=True,
                disable_web_page_preview=True
            )
        elif message.chat.type == enums.ChatType.CHANNEL:
            if (message.chat.id == int(Config.LOG_CHANNEL)) or (message.chat.id == int(Config.UPDATES_CHANNEL)) or message.forward_from_chat or message.forward_from:
                return
            elif int(message.chat.id) in Config.BANNED_CHAT_IDS:
                await bot.leave_chat(message.chat.id)
                return
            else:
                pass

            try:
                forwarded_msg = await message.forward(Config.DB_CHANNEL)
                file_er_id = str(forwarded_msg.id)
                share_link = f"https://t.me/{Config.BOT_USERNAME}?start=Books_groupp_{str_to_b64(file_er_id)}"
                CH_edit = await bot.edit_message_reply_markup(message.chat.id, message.id,
                                                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                                                "Get File Link", url=share_link)]]))
                if message.chat.username:
                    await forwarded_msg.reply_text(
                        f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/{message.chat.username}/{CH_edit.id}) Channel's Broadcasted File's Button Added!")
                else:
                    private_ch = str(message.chat.id)[4:]
                    await forwarded_msg.reply_text(
                        f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/c/{private_ch}/{CH_edit.id}) Channel's Broadcasted File's Button Added!")
            except FloodWait as sl:
                await asyncio.sleep(sl.value)
                await bot.send_message(
                    chat_id=int(Config.LOG_CHANNEL),
                    text=f"#FloodWait:\nGot FloodWait of `{str(sl.value)}s` from `{str(message.chat.id)}` !!",
                    disable_web_page_preview=True
                )
            except Exception as err:
                await bot.leave_chat(message.chat.id)
                await bot.send_message(
                    chat_id=int(Config.LOG_CHANNEL),
                    text=f"#ERROR_TRACEBACK:\nGot Error from `{str(message.chat.id)}` !!\n\n**Traceback:** `{err}`",
                    disable_web_page_preview=True
                )


    @Bot.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER) & filters.reply)
    async def broadcast_handler_open(_, m: Message):
        await main_broadcast_handler(m, db)


    @Bot.on_message(filters.private & filters.command("status") & filters.user(Config.BOT_OWNER))
    async def sts(_, m: Message):
        total_users = await db.total_users_count()
        await m.reply_text(
            text=f"Total Users:  `{total_users}`",
            quote=True
        )


    @Bot.on_message(filters.private & filters.command("ban_user") & filters.user(Config.BOT_OWNER))
    async def ban(c: Client, m: Message):
        
        if len(m.command) == 1:
            await m.reply_text(
                f"ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ʙᴀɴ ᴀɴʏ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.\n\n"
                f"Usage:\n\n"
                f"`/ban_user user_id ban_duration ban_reason`\n\n"
                f"Eg: `/ban_user 1234567 28 You misused me.`\n"
                f"This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
                quote=True
            )
            return

        try:
            user_id = int(m.command[1])
            ban_duration = int(m.command[2])
            ban_reason = ' '.join(m.command[3:])
            ban_log_text = f"BΔnninǤ user {user_id} FФЯ {ban_duration} ᴅᴀʏꜱ ꜰᴏʀ ᴛʜᴇ ʀᴇᴀꜱᴏɴ {ban_reason}."
            try:
                await c.send_message(
                    user_id,
                    f"ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ ꜰᴏʀ **{ban_duration}** ᴅᴀʏ(ꜱ) ꜰᴏʀ ᴛʜᴇ ʀᴇᴀꜱᴏɴ __{ban_reason}__ \n\n"
                    f"**Message from the admin**"
                )
                ban_log_text += '\n\nᴜꜱᴇʀ ɴᴏᴛɪꜰɪᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!'
            except:
                traceback.print_exc()
                ban_log_text += f"\n\nᴜꜱᴇʀ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴ ꜰᴀɪʟᴇᴅ! \n\n`{traceback.format_exc()}`"

            await db.ban_user(user_id, ban_duration, ban_reason)
            print(ban_log_text)
            await m.reply_text(
                ban_log_text,
                quote=True
            )
        except:
            traceback.print_exc()
            await m.reply_text(
                f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
                quote=True
            )

    @Bot.on_message(filters.private & filters.command("unban_user") & filters.user(Config.BOT_OWNER))
    async def unban(c: Client, m: Message):

        if len(m.command) == 1:
            await m.reply_text(
                f"ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴜɴʙᴀɴ ᴀɴʏ ᴜꜱᴇʀ.\n\n"
                f"Usage:\n\n`/unban_user user_id`\n\n"
                f"Eg: `/unban_user 1234567`\n"
                f"ᴛʜɪꜱ ᴡɪʟʟ ᴜɴʙᴀɴ ᴜꜱᴇʀ ᴡɪᴛʜ ɪᴅ `1234567`.",
                quote=True
            )
            return

        try:
            user_id = int(m.command[1])
            unban_log_text = f"ᴜɴʙᴀɴɴɪɴɢ ᴜꜱᴇʀ {user_id}"
            try:
                await c.send_message(
                    user_id,
                    f"ʏᴏᴜʀ ʙᴀɴ ᴡᴀꜱ ʟɪꜰᴛᴇᴅ!"
                )
                unban_log_text += '\n\nᴜꜱᴇʀ ɴᴏᴛɪꜰɪᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!'
            except:
                traceback.print_exc()
                unban_log_text += f"\n\nᴜꜱᴇʀ ɴᴏᴛɪꜰɪᴄᴀᴛɪᴏɴ ꜰᴀɪʟᴇᴅ! \n\n`{traceback.format_exc()}`"
            await db.remove_ban(user_id)
            print(unban_log_text)
            await m.reply_text(
                unban_log_text,
                quote=True
            )
        except:
            traceback.print_exc()
            await m.reply_text(
                f"Error occurred! Traceback given below\n\n`{traceback.format_exc()}`",
                quote=True
            )


    @Bot.on_message(filters.private & filters.command("banned_users") & filters.user(Config.BOT_OWNER))
    async def _banned_users(_, m: Message):
        
        all_banned_users = await db.get_all_banned_users()
        banned_usr_count = 0
        text = ''

        async for banned_user in all_banned_users:
            user_id = banned_user['id']
            ban_duration = banned_user['ban_status']['ban_duration']
            banned_on = banned_user['ban_status']['banned_on']
            ban_reason = banned_user['ban_status']['ban_reason']
            banned_usr_count += 1
            text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, " \
                    f"**Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
        reply_text = f"Total banned user(s): `{banned_usr_count}`\n\n{text}"
        if len(reply_text) > 4096:
            with open('banned-users.txt', 'w') as f:
                f.write(reply_text)
            await m.reply_document('banned-users.txt', True)
            os.remove('banned-users.txt')
            return
        await m.reply_text(reply_text, True)


    @Bot.on_message(filters.private & filters.command("clear_batch"))
    async def clear_user_batch(bot: Client, m: Message):
        MediaList[f"{str(m.from_user.id)}"] = []
        await m.reply_text("ᴄʟᴇᴀʀᴇᴅ ʏᴏᴜʀ ʙᴀᴛᴄʜ ꜰɪʟᴇꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!")


    @Bot.on_callback_query()
    async def button(bot: Client, cmd: CallbackQuery):

        cb_data = cmd.data
        if "aboutbot" in cb_data:
            await cmd.message.edit(
                Config.ABOUT_BOT_TEXT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Courses Channel",
                                                url="https://t.me/course_guy")
                        ],
                        [
                            InlineKeyboardButton("Go Home", callback_data="gotohome"),
                            InlineKeyboardButton("About Dev", callback_data="aboutdevs")
                        ]
                    ]
                )
            )

        elif "aboutdevs" in cb_data:
            await cmd.message.edit(
                Config.ABOUT_DEV_TEXT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Courses Channel",
                                                url="https://t.me/course_guy")
                        ],
                        [
                            InlineKeyboardButton("About Bot", callback_data="aboutbot"),
                            InlineKeyboardButton("Go Home", callback_data="gotohome")
                        ]
                    ]
                )
            )

        elif "gotohome" in cb_data:
            if(Config.LAZY_MODE == True):
                await cmd.message.edit(
                Config.LAZY_HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🍿suppor† group", url="https://t.me/codeconvo"),
                            InlineKeyboardButton("🔊Books channel", url="https://t.me/books_groupp")
                        ],
                        [
                            InlineKeyboardButton("About bot", callback_data="aboutbot"),
                            InlineKeyboardButton("About Dev", callback_data="aboutdevs")
                        ],
                        [
                            InlineKeyboardButton("Courses Channel", url="https://t.me/course_guy")
                        ]
                    ]
                )
            )
            else :
                await cmd.message.edit(
                Config.HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🍿suppor† group", url="https://t.me/codeconvo"),
                            InlineKeyboardButton("🔊Books channel", url="https://t.me/books_groupp")
                        ],
                        [
                            InlineKeyboardButton("About Dev", callback_data="aboutbot"),
                            InlineKeyboardButton("About Bot", callback_data="aboutdevs")
                        ],
                        [
                            InlineKeyboardButton("Courses Channel", url="https://t.me/course_guy")
                        ]
                    ]
                )
            )

        elif "refreshForceSub" in cb_data:
            if Config.UPDATES_CHANNEL:
                if Config.UPDATES_CHANNEL.startswith("-100"):
                    channel_chat_id = int(Config.UPDATES_CHANNEL)
                else:
                    channel_chat_id = Config.UPDATES_CHANNEL
                try:
                    user = await bot.get_chat_member(channel_chat_id, cmd.message.chat.id)
                    if user.status == "kicked":
                        await cmd.message.edit(
                            text="ꜱᴏʀʀʏ ꜱɪʀ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜꜱᴇ ᴍᴇ. ᴄᴏɴᴛᴀᴄᴛ ᴍʏ [Support Group](https://t.me/codeconvo).",
                            disable_web_page_preview=True
                        )
                        return
                except UserNotParticipant:
                    invite_link = await get_invite_link(channel_chat_id)
                    await cmd.message.edit(
                        text="**Join our main channel to Use the bot\n\n"
                            "Only channel subscriber will get the book",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("Join Books Channel", url=invite_link.invite_link)
                                ],
                                [
                                    InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
                                ]
                            ]
                        )
                    )
                    return
                except Exception:
                    await cmd.message.edit(
                        text="ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. ᴄᴏɴᴛᴀᴄᴛ ᴍʏ [Support Group](https://t.me/codeconvo).",
                        disable_web_page_preview=True
                    )
                    return
            if(Config.LAZY_MODE == True):
                await cmd.message.edit(
                Config.LAZY_HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🍿suppor† group", url="https://t.me/codeconvo"),
                            InlineKeyboardButton("🔊Books channel", url="https://t.me/books_groupp")
                        ],
                        [
                            InlineKeyboardButton("About Bot", callback_data="aboutbot"),
                            InlineKeyboardButton("About Bot", callback_data="aboutdevs")
                        ],
                        [
                            InlineKeyboardButton("Courses Channel", url="https://t.me/course_guy")
                        ]
                    ]
                )
            )
            else :
                await cmd.message.edit(
                Config.HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🍿suppor† group", url="https://t.me/codeconvo"),
                            InlineKeyboardButton("🔊Books channel", url="https://t.me/books_groupp")
                        ],
                        [
                            InlineKeyboardButton("About Bot", callback_data="aboutbot"),
                            InlineKeyboardButton("About Dev", callback_data="aboutdevs")
                        ],
                        [
                            InlineKeyboardButton("Courses Channel", url="https://t.me/course_guy")
                        ]
                    ]
                )
            )

        elif cb_data.startswith("ban_user_"):
            user_id = cb_data.split("_", 2)[-1]
            if Config.UPDATES_CHANNEL is None:
                await cmd.answer("ꜱᴏʀʀʏ ꜱɪʀ, ʏᴏᴜ ᴅɪᴅɴ'ᴛ ꜱᴇᴛ ᴀɴʏ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ!", show_alert=True)
                return
            if not int(cmd.from_user.id) == Config.BOT_OWNER:
                await cmd.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!", show_alert=True)
                return
            try:
                await bot.kick_chat_member(chat_id=int(Config.UPDATES_CHANNEL), user_id=int(user_id))
                await cmd.answer("USEƦ BANNED FƦOM UPDATES CHANNEL!", show_alert=True)
            except Exception as e:
                await cmd.answer(f"ᴄᴀɴ'ᴛ ʙᴀɴ ʜɪᴍ!\n\nError: {e}", show_alert=True)

        elif cb_data.startswith("generate_stream_link"):
            _, file_id = cb_data.split(":")
            try:
                user_id = cmd.from_user.id
                username =  cmd.from_user.mention

                lazy_file = await media_forward(bot, user_id=STREAM_LOGS, file_id=file_id)
 
                
                fileName = {quote_plus(get_name(lazy_file))}
                lazy_stream = f"{URL}watch/{str(lazy_file.id)}/{quote_plus(get_name(lazy_file))}?hash={get_hash(lazy_file)}"
                lazy_download = f"{URL}{str(lazy_file.id)}/{quote_plus(get_name(lazy_file))}?hash={get_hash(lazy_file)}"

                xo = await cmd.message.reply_text(f'🔐')
                await asyncio.sleep(1)
                await xo.delete()

                await lazy_file.reply_text(
                    text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
                    quote=True,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("web Download", url=lazy_download),  # we download Link
                                                        InlineKeyboardButton('▶Stream online', url=lazy_stream)]])  # web stream Link
                )
                await cmd.message.edit(
                    text="•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ☠︎⚔",
                    quote=True,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("web Download", url=lazy_download),  # we download Link
                                                        InlineKeyboardButton('▶Stream online', url=lazy_stream)]])  # web stream Link
                )
            except Exception as e:
                print(e)  # print the error message
                await cmd.answer(f"☣something went wrong sweetheart\n\n{e}", show_alert=True)
                return


        elif "addToBatchTrue" in cb_data:
            if MediaList.get(f"{str(cmd.from_user.id)}", None) is None:
                MediaList[f"{str(cmd.from_user.id)}"] = []
            file_id = cmd.message.reply_to_message.id
            MediaList[f"{str(cmd.from_user.id)}"].append(file_id)
            await cmd.message.edit("ꜰɪʟᴇ ꜱᴀᴠᴇᴅ ɪɴ ʙᴀᴛᴄʜ!\n\n"
                                "ᴘʀᴇꜱꜱ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʙᴀᴛᴄʜ ʟɪɴᴋ.",
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton("⚡️ ɢᴇᴛ ʙᴀᴛᴄʜ & ᴘᴏꜱᴛ ⚡️", callback_data="getBatchLink")],
                                    [InlineKeyboardButton("Close Message", callback_data="closeMessage")]
                                ]))

        elif "addToBatchFalse" in cb_data:
            await save_media_in_channel(bot, editable=cmd.message, message=cmd.message.reply_to_message)

        elif "getBatchLink" in cb_data:
            message_ids = MediaList.get(f"{str(cmd.from_user.id)}", None)
            if message_ids is None:
                await cmd.answer("ʙᴀᴛᴄʜ ʟɪꜱᴛ ᴇᴍᴘᴛʏ!", show_alert=True)
                return
            await cmd.message.edit("ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ, ɢᴇɴᴇʀᴀᴛɪɴɢ ʙᴀᴛᴄʜ ʟɪɴᴋ...")
            await save_batch_media_in_channel(bot=bot, editable=cmd.message, message_ids=message_ids)
            MediaList[f"{str(cmd.from_user.id)}"] = []

        elif "closeMessage" in cb_data:
            await cmd.message.delete(True)

        try:
            await cmd.answer()
        except QueryIdInvalid: pass

    if ON_HEROKU:
        asyncio.create_task(ping_server())
    me = await Bot.get_me()
    Bot.username = '@' + me.username
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0" if ON_HEROKU else BIND_ADRESS
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()


if __name__ == '__main__':
    try:
        loop.run_until_complete(Lazy_start())
    except KeyboardInterrupt:
        logging.info(' Service Stopped ')

