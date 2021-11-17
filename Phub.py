import os
from aiohttp import ClientSession
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from Python_ARQ import ARQ 
from asyncio import get_running_loop
from wget import download
from config import OWNER, BOT_NAME, REPO_BOT, ARQ_API_KEY, UPDATES_CHANNEL, TOKEN


#------

# Config Check-----------------------------------------------------------------

# ARQ API and Bot Initialize---------------------------------------------------
session = ClientSession()


arq = ARQ("https://thearq.tech", ARQ_API_KEY, session)
pornhub = arq.pornhub

bot1 = Client(f"{BOT_NAME}", bot_token=f"{TOKEN}", api_id=6,
             api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")



db = {}

# Let's Go----------------------------------------------------------------------
@bot1.on_message(
    filters.command(["search"]) & ~filters.edited & ~filters.command("help") & ~filters.command("start") & ~filters.command("repo")
    )
async def sarch(_,message):
    m = await message.reply_text("finding your desirable video...")
    search = message.text.split(' ', 1)[1]
    try:
        resp = await pornhub(search,thumbsize="large_hd")
        res = resp.result
    except:
        await m.delete()
        pass
    if not resp.ok:
        await m.edit("error search or link detected.")
        return
    resolt = f"""
**➡️ TITLE:** {res[0].title}
**⏰ DURATION:** {res[0].duration}
**👁‍🗨 VIEWERS:** {res[0].views}
**🌟 RATING:** {res[0].rating}
"""
    await m.delete()
    m = await message.reply_photo(
        photo=res[0].thumbnails[0].src,
        caption=resolt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("NEXT",
                                         callback_data="next"),
                    InlineKeyboardButton("LINK",
                                         callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("SCREENSHOTS",
                                         callback_data="ss"),
                    InlineKeyboardButton("DOWNLOAD",
                                         callback_data="downbad"),
               
                ]               
            ]
        ),
        parse_mode="markdown",
    )
    new_db={"result":res,"curr_page":0}
    db[message.chat.id] = new_db
    
 # Next Button--------------------------------------------------------------------------
@bot1.on_callback_query(filters.regex("next"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page+1
    db[query.message.chat.id]['curr_page'] = cur_page
    if len(res) <= (cur_page+1):
        cbb = [
                [
                    InlineKeyboardButton("PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("SCREENSHOTS",
                                         callback_data="ss")
                    
                ],
                [
                    InlineKeyboardButton("LINK",
                                         callback_data="delete"),
                    InlineKeyboardButton("DOWNLOAD",
                                         callback_data="downbad")
              
                ]
              ]
    else:
        cbb = [
                [
                    InlineKeyboardButton("PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("NEXT",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("LINK",
                                         callback_data="delete"),
                    InlineKeyboardButton("SCREENSHOTS",
                                         callback_data="ss"),
                    InlineKeyboardButton("DOWNLOAD",
                                         callback_data="downbad"),
              
                    
                ]
              ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[cur_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}
"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )
 
# Previous Button-------------------------------------------------------------------------- 
@bot1.on_callback_query(filters.regex("previous"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    db[query.message.chat.id]['curr_page'] = cur_page
    if cur_page != 0:
        cbb=[
                [
                    InlineKeyboardButton("PREVIOUS",
                                         callback_data="previous"),
                    InlineKeyboardButton("NEXT",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("LINK",
                                         callback_data="delete"),
                    InlineKeyboardButton("SCREENSHOTS",
                                         callback_data="ss"),
                    InlineKeyboardButton("DOWNLOAD",
                                         callback_data="downbad")
              
                ]
            ]
    else:
        cbb=[
                [
                    InlineKeyboardButton("NEXT",
                                         callback_data="next"),
                    InlineKeyboardButton("LINK",
                                         callback_data="Delete"),
                ],
                [ 
                    InlineKeyboardButton("SCREENSHOTS",
                                         callback_data="ss"),
                    InlineKeyboardButton("DOWNLOAD",
                                         callback_data="downbad"),
              
                ]
                
            ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[cur_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}
"""
    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )


# Delete Button-------------------------------------------------------------------------- 
#@bot1.on_callback_query(filters.regex("delete"))
@bot1.on_callback_query(filters.regex("delete"))
def callback_query_delete(bot, query):
    #await query.message.delete()
     data = db[query.message.chat.id]
     res = data['result']
     curr_page = int(data['curr_page'])
     cur_page = curr_page-1
     db[query.message.chat.id]['curr_page'] = cur_page
     umrl = res[curr_page].url
     bot.send_message(text=umrl,chat_id=query.message.chat.id,disable_web_page_preview=True)



# SCREENSHOT BUTTON ---------------------------------------

@bot1.on_callback_query(filters.regex("ss"))
async def callback_query_delete(bot, query):
    data = db[query.message.chat.id]
    res = data['result']
    curr_page = int(data['curr_page'])
    ss = res[curr_page].thumbnails
    for src in ss:
      await bot.send_photo(photo=src.src,chat_id=query.message.chat.id)



# DOWNLOAD BUTTON ------------------------------------------

import requests, os, validators
import youtube_dl
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from pyrogram.types import  InlineKeyboardMarkup, InlineKeyboardButton





#=


import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import math
import os
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation


async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]



#=





def downloada(url, quality):
  
    if quality == "2":
        ydl_opts_start = {
            'format': 'best', #This Method Don't Need ffmpeg , if you don't have ffmpeg use This 
            'outtmpl': f'localhoct/%(id)s.%(ext)s',
            'no_warnings': False,
            'logtostderr': False,
            'ignoreerrors': False,
            'noplaylist': True,
            'http_chunk_size': 2097152,
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f'{title}'
    
@bot1.on_callback_query(filters.regex("downbad"))
def webpage(c, m): # c Mean Client | m Mean Message
    print(m.message.chat.id)
    data = db[m.message.chat.id]
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    url1 = res = data['result'][curr_page].url
    if validators.url(url1):
        sample_url = "https://da.gd/s?url={}".format(url1)
        url = requests.get(sample_url).text
    

"""    
    global check_current
    check_current = 0
    def progress(current, total): #Thanks to my dear friend Hassan Hoot for Progress Bar :)
        global check_current
        if ((current//1024//1024) % 50 )== 0 :
            if check_current != (current//1024//1024):
                check_current = (current//1024//1024)
                upmsg.edit(f"{current//1024//1024}MB / {total//1024//1024}MB Uploaded.")
        elif (current//1024//1024) == (total//1024//1024):
            upmsg.delete()
"""





   
    url1=f"{url} and 2"
    chat_id = m.message.chat.id
    data = url1
    url, quaitly = data.split(" and ")
    dlmsg = c.send_message(chat_id, '`downloading video..`')
    path = downloada(url, quaitly)
    upmsg = c.send_message(chat_id, '`uploading video..`')
    dlmsg.delete()
    thumb = path.replace('.mp4',".jpg",-1)
    if  os.path.isfile(thumb):
        thumb = open(thumb,"rb")
        path = open(path, 'rb')
        #c.send_photo(chat_id,thumb,caption=' ') #Edit it and add your Bot ID :)
        c.send_video(chat_id, path, thumb=thumb, caption=' ',
                    file_name=" ", supports_streaming=True, progress=progress_for_pyrogram) #Edit it and add your Bot ID :)
        upmsg.delete()
    else:
        path = open(path, 'rb')
        c.send_video(chat_id, path, caption=' ',
                    file_name=" ", supports_streaming=True, progress=progress)
        upmsg.delete()





bot1.run()
