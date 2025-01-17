from pyrogram import filters, Client as Mbot
import bs4, requests
from bot import DUMP_GROUP
from apscheduler.schedulers.background import BackgroundScheduler
from sys import executable
from os import sys , execl , environ 
# if you are using service like heroku after restart it changes ip which avoid Ip Blocking Also Restart When Unknown Error occurred and bot is idle 
RESTART_ON = environ.get('RESTART_ON')
def restart():
     execl(executable, executable, "bot.py")
if RESTART_ON:
   scheduler = BackgroundScheduler()
   scheduler.add_job(restart, "interval", hours=6)
   scheduler.start()
@Mbot.on_message(filters.incoming & filters.private,group=-1)
async def monitor(Mbot, message):
           if DUMP_GROUP:
              await message.forward(DUMP_GROUP)
          
@Mbot.on_message(filters.command("start") & filters.incoming)
async def start(Mbot, message):
          await message.reply(f"Hello 👋👋 {message.from_user.mention()} \nI am a Telegram Bot that can download from multiple social media platforms. Currently, I support Instagram, TikTok, Twitter, and Facebook!\n Powered By MohanishX ⚡")
          
@Mbot.on_message(filters.command("help") & filters.incoming)
async def help(Mbot, message):
          await message.reply("This is user friendly bot so you can simple send your Instagram reel and post links here:) \n eg: `https://www.instagram.com/reel/CZqWDGODoov/?igshid=MzRlODBiNWFlZA==`\n `post:` `https://www.instagram.com/reel/CuCTtORJbDj/?igshid=MzRlODBiNWFlZA==`")
@Mbot.on_message(filters.command("donate") & filters.command("Donate") & filters.incoming )
async def donate(_, message):
       await message.reply_text(f"Donate 🍪 **$** https://buymeacoffee.com/mohanish \n**UPI**`arunrnadh2002@okhdfcbank` \nMade with ❤️ Mohanish")
