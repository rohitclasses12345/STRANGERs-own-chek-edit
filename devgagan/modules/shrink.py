 
# ---------------------------------------------------
# File Name: shrink.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/Strangerboys24
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import requests
import string
import aiohttp
from devgagan import app
from devgagan.core.func import *
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB, WEBSITE_URL, AD_API, LOG_GROUP  
 
 
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]
 
 
async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)
 
 
 
Param = {}
 
 
async def generate_random_param(length=8):
    """Generate a random parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
 
 
async def get_shortened_url(deep_link):
    api_url = f"https://{WEBSITE_URL}/api?api={AD_API}&url={deep_link}"
 
     
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()   
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    return None
 
 
async def is_user_verified(user_id):
    """Check if a user has an active session."""
    session = await token.find_one({"user_id": user_id})
    return session is not None
 
 
@app.on_message(filters.command("start"))
async def token_handler(client, message):
    """Handle the /token command."""
    join = await subscribe(client, message)
    if join == 1:
        return
    chat_id = "save_restricted_content_bots"
    msg = await app.get_messages(chat_id, 796)
    user_id = message.chat.id
    if len(message.command) <= 1:
        # List of multiple starting images
        start_images = [
            "https://i.ibb.co/ZRvCxd5g/STRANGER-BOY.jpg",
            "https://www.freepik.com/free-ai-image/lifestyle-scene-with-people-doing-regular-tasks-anime-style_94952596.htm#fromView=keyword&page=2&position=20&uuid=df9b46bb-3e9a-43e9-b3bb-481ac83cbced&query=Sexy+anime+girl",
            "https://www.freepik.com/free-ai-image/anime-style-illustration-rose_206341678.htm#fromView=keyword&page=1&position=19&uuid=f5070f8a-bf67-4774-86c7-92067ce73da6&query=Sexy+anime+girl",
            "https://i.ibb.co/9HhNmHYg/STRANGER-BOY.jpg",
            "https://www.freepik.com/premium-ai-image/modern-spirit-fashion-forward-diva_358241706.htm#fromView=keyword&page=1&position=29&uuid=f5070f8a-bf67-4774-86c7-92067ce73da6&query=Sexy+anime+girl",
            "https://i.ibb.co/JwwmgFs6/STRANGER-BOY.jpg",
            "https://www.freepik.com/premium-ai-image/most-beautiful-woman-history-kawaii-soft-smile-anime_166751376.htm#fromView=keyword&page=2&position=14&uuid=df9b46bb-3e9a-43e9-b3bb-481ac83cbced&query=Sexy+anime+girl",
            "https://www.freepik.com/premium-ai-image/striking-anime-girl-with-fiery-red-hair-captivating-blue-eyes_339512292.htm#fromView=keyword&page=2&position=5&uuid=df9b46bb-3e9a-43e9-b3bb-481ac83cbced&query=Sexy+anime+girl",
            "https://www.freepik.com/free-ai-image/portrait-anime-character-doing-fitness-exercising_236197782.htm#fromView=search&page=2&position=22&uuid=7aca9fb5-c87b-4cce-a2bd-8a697e666bc0&query=Hot+girl+cute+animated",
            "https://www.freepik.com/premium-ai-image/stunning-digital-portrait-confident-female-with-expressive-blue-eyes-flowing-black-hair_292912268.htm#fromView=search&page=1&position=19&uuid=05f5aa6f-d09a-4578-9972-302056830492&query=Hot+girl+cute+animated",
            "https://i.ibb.co/ccV44ZRS/STRANGER-BOY.jpg",
            "https://www.freepik.com/premium-ai-image/anime-girl-sitting-window-sill-with-blue-eyes-black-dress_402567199.htm#fromView=keyword&page=1&position=14&uuid=f5070f8a-bf67-4774-86c7-92067ce73da6&query=Sexy+anime+girl",
            "https://i.ibb.co/7xm7cXyg/STRANGER-BOY.jpg",
            "https://www.freepik.com/premium-ai-image/anime-girl-sitting-desk-with-cell-phone-her-hand_313114443.htm#fromView=keyword&page=1&position=15&uuid=f5070f8a-bf67-4774-86c7-92067ce73da6&query=Sexy+anime+girl",
            "https://i.ibb.co/q3SX4gjQ/STRANGER-BOY.jpg",
            "https://www.freepik.com/premium-ai-image/drawing-woman-blue-dress_59951677.htm#fromView=keyword&page=1&position=17&uuid=f5070f8a-bf67-4774-86c7-92067ce73da6&query=Sexy+anime+girl",
            "https://i.ibb.co/0p3pmkwn/Angel.jpg",
            "https://www.freepik.com/free-ai-image/anime-like-illustration-girl-portrait_351801839.htm#fromView=keyword&page=1&position=16&uuid=f5070f8a-bf67-4774-86c7-92067ce73da6&query=Sexy+anime+girl",
         ]

        # Pick random image
        image_url = random.choice(start_images)
        join_button = InlineKeyboardButton("Join Channel", url="https://t.me/stangerboy")
        premium = InlineKeyboardButton("Get Premium", url="https://t.me/Strangerboys24")   
        keyboard = InlineKeyboardMarkup([
            [join_button],   
            [premium]    
        ])
         
        await message.reply_photo(
            msg.photo.file_id,
            caption=(
                "Hi 👋 Welcome, Wanna intro...?\n\n"
                "Welcome to [STRANGER SRC](https://i.ibb.co/PGkCBcMF/x.jpg) BOT!...\n\n"
                "╭━━━━━━━━━━━━━ ❀° ━━━━╮\n"
                "┣⪼•✅️ I can grab posts 🔒 from channels/groups where Forward is OFF 🚫\n"
                "┣⪼•🎬 I can fetch Videos/Audio from YT ▶️\n"
                "┣⪼•Insta 📸 & many more social hubs 🌐\n"
                "┣⪼•✳️ Simply send the post link of a public channel.\n"
                "┣⪼•For private channels, do /login.\n"
                "┣⪼•Send /help to know more."
                "╰━━━━━━━━━━━━━ ❀° ━━━╯シ\n"
            ),
            reply_markup=keyboard
        )
        return  
 
    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return
 
     
    if param:
        if user_id in Param and Param[user_id] == param:
             
            await token.insert_one({
                "user_id": user_id,
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=3),
            })
            del Param[user_id]   
            await message.reply("✅ You have been verified successfully! Enjoy your session for next 3 hours.")
            return
        else:
            await message.reply("❌ Invalid or expired verification link. Please generate a new token.")
            return
 
@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    user_id = message.chat.id
     
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return
    if await is_user_verified(user_id):
        await message.reply("✅ Your free session is already active enjoy!")
    else:
         
        param = await generate_random_param()
        Param[user_id] = param   
 
         
        deep_link = f"https://t.me/{client.me.username}?start={param}"
 
         
        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Failed to generate the token link. Please try again.")
            return
 
         
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Verify the token now...", url=shortened_url)]]
        )
        await message.reply("Click the button below to verify your free access token: \n\n> What will you get ? \n1. No time bound upto 3 hours \n2. Batch command limit will be FreeLimit + 20 \n3. All functions unlocked", reply_markup=button)
 
