import random
import re
import time
from platform import python_version

from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import check_data_base_heal_th, codalive, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import StartTime, codex, codversion, mention

plugin_category = "utils"


@codex.cod_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "✧✧"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "✮ MY BOT IS RUNNING SUCCESSFULLY ✮"
    COD_IMG = gvarstatus("ALIVE_PIC")
    if COD_IMG:
        COD = [x for x in COD_IMG.split()]
        PIC = random.choice(COD)
        cod_caption = f"**{ALIVE_TEXT}**\n\n"
        cod_caption += f"**{EMOJI} Master : {mention}**\n"
        cod_caption += f"**{EMOJI} Uptime :** `{uptime}\n`"
        cod_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
        cod_caption += f"**{EMOJI} Codex Version :** `{codversion}`\n"
        cod_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
        cod_caption += f"**{EMOJI} Database :** `{check_sgnirts}`\n"
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=cod_caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(
            event,
            f"**{ALIVE_TEXT}**\n\n"
            f"**{EMOJI} Master : {mention}**\n"
            f"**{EMOJI} Uptime :** `{uptime}\n`"
            f"**{EMOJI} Telethon Version :** `{version.__version__}\n`"
            f"**{EMOJI} Codex Version :** `{codversion}`\n"
            f"**{EMOJI} Python Version :** `{python_version()}\n`"
            f"**{EMOJI} Database :** `{check_sgnirts}`\n",
        )


@codex.cod_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "✧✧"
    cod_caption = f"**Catuserbot is Up and Running**\n"
    cod_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    cod_caption += f"**{EMOJI} Codex Version :** `{codversion}`\n"
    cod_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    cod_caption += f"**{EMOJI} Master:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cod_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@codex.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await codalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
