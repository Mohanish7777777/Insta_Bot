from pyrogram import filters, Client as Mbot
from os import mkdir, environ 
from random import randint
from bot import LOG_GROUP, DUMP_GROUP
from shutil import rmtree 
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from requests import get
import traceback, os

FIXIE_SOCKS_HOST = environ.get('FIXIE_SOCKS_HOST')

async def thumb_down(videoId):
    with open(f"/tmp/{videoId}.jpg", "wb") as file:
        file.write(get(f"https://img.youtube.com/vi/{videoId}/default.jpg").content)
    return f"/tmp/{videoId}.jpg"

async def ytdl_video(path, video_url, id):
    print(video_url)
    qa = "mp4"  # Set to MP4 format
    file = f"{path}/%(title)s.%(ext)s"
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": file,
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "cache-dir": "/tmp/",
        "nocheckcertificate": True,
        # "proxy": f"socks5://{FIXIE_SOCKS_HOST}",
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(video)
            print(filename)
            return filename
        except (IOError, BrokenPipeError):
            pass
            video = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(video)
            print(filename)
            return filename
        except Exception as e:
            if FIXIE_SOCKS_HOST:
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'default_search': 'ytsearch',
                    'noplaylist': True,
                    "nocheckcertificate": True,
                    "outtmpl": file,
                    "quiet": True,
                    "addmetadata": True,
                    "prefer_ffmpeg": True,
                    "geo_bypass": True,
                    "cache-dir": "/tmp/",
                    "nocheckcertificate": True,
                    "proxy": f"socks5://{FIXIE_SOCKS_HOST}"
                }
                with YoutubeDL(ydl_opts) as ydl:
                    try:
                        video = ydl.extract_info(video_url, download=True)
                        filename = ydl.prepare_filename(video)
                        print(filename)
                        return filename
                    except Exception as e:
                        print(e)

async def ytdl_down(path, video_url, id):
    print(video_url)
    qa = "mp3"
    file = f"{path}/%(title)s"
    ydl_opts = {
        'format': "bestaudio",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": file,
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "cache-dir": "/tmp/",
        "nocheckcertificate": True,
        # "proxy": f"socks5://{FIXIE_SOCKS_HOST}",
        "postprocessors": [{'key': 'FFmpegExtractAudio', 'preferredcodec': qa, 'preferredquality': '320'}],
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(video)
            return f"{filename}.{qa}"
        except (IOError, BrokenPipeError):
            pass
            video = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(video)
            print(filename)
            return f"{filename}.{qa}"
        except Exception as e:
            pass
            try:
                ydl_opts = {
                    'format': "bestaudio",
                    'default_search': 'ytsearch',
                    'noplaylist': True,
                    "nocheckcertificate": True,
                    "outtmpl": file,
                    "quiet": True,
                    "addmetadata": True,
                    "prefer_ffmpeg": True,
                    "geo_bypass": True,
                    "cache-dir": "/tmp/",
                    "nocheckcertificate": True,
                    "proxy": f"socks5://{FIXIE_SOCKS_HOST}",
                    "postprocessors": [{'key': 'FFmpegExtractAudio', 'preferredcodec': qa, 'preferredquality': '320'}],
                }
                with YoutubeDL(ydl_opts) as ydl:
                    video = ydl.extract_info(video_url, download=True)
                    filename = ydl.prepare_filename(video)
                    return f"{filename}.{qa}"
            except Exception as e:
                print(e)

async def getIds(video):
    ids = []
    with YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(video, download=False)
        try:
            info_dict = info_dict['entries']
            ids.extend([x.get('id'), x.get('playlist_index'), x.get('creator') or x.get('uploader'), x.get('title'), x.get('duration'), x.get('thumbnail')] for x in info_dict)
        except:
            ids.append([info_dict.get('id'), info_dict.get('playlist_index'), info_dict.get('creator') or info_dict.get('uploader'), info_dict.get('title'), info_dict.get('duration'), info_dict.get('thumbnail')])
    return ids

@Mbot.on_message(filters.regex(r'https?://.*youtube[^\s]+') & filters.incoming |
                 filters.regex(r'(https?:\/\/(?:www\.)?youtu\.?be(?:\.com)?\/.*)') & filters.incoming)
async def handle_youtube_links(Mbot, message):
    try:
        m = await message.reply_sticker("CAACAgIAAxkBATWhF2Qz1Y-FKIKqlw88oYgN8N82FtC8AAJnAAPb234AAT3fFO9hR5GfHgQ")
    except:
        pass
    link = message.matches[0].group(0)
    if "channel" in link or "/c/" in link:
        return await m.edit_text("**Channel** Download Not Available.")
    if "shorts" in link:
        try:
            randomdir = "/tmp/" + str(randint(1, 100000000))
            mkdir(randomdir)
            fileLink = await ytdl_video(randomdir, link, message.from_user.id)
            AForCopy = await message.reply_video(fileLink)
            if os.path.exists(randomdir):
                rmtree(randomdir)
            await m.delete()
            if DUMP_GROUP:
                await AForCopy.copy(DUMP_GROUP)
        except Exception as e:
            await m.delete()
            if LOG_GROUP:
                await Mbot.send_message(LOG_GROUP, f"YouTube Shorts {e} {link}")
            await message.reply(f"400: Sorry, unable to find it. Try another or report it to @SupportUser.")
            print(traceback.format_exc())
            await Mbot.send_message(LOG_GROUP, traceback.format_exc())
        return await message.reply("Check out @xadmin_instabot(music) @MohanishX(Channel)\nPlease support us by maintaining this project.")

    try:
        if "music.youtube.com" in link:
            link = link.replace("music.youtube.com", "youtube.com")
        ids = await getIds(link)
        videoInPlaylist = len(ids)
        randomdir = "/tmp/" + str(randint(1, 100000000))
        mkdir(randomdir)
        for id in ids:
            print(id)
            link = f"https://youtu.be/{id[0]}"
            PForCopy = await message.reply_photo(f"https://i.ytimg.com/vi/{id[0]}/hqdefault.jpg", caption=f"🎧 Title : `{id[3]}`\n🎤 Artist : `{id[2]}`\n💽 Track No : `{id[1]}`\n💽 Total Track : `{videoInPlaylist}`")
            fileLink = await ytdl_down(randomdir, link, message.from_user.id)
            print("down completely")
            thumbnail = await thumb_down(id[0])
            AForCopy = await message.reply_audio(fileLink, caption=f"[{id[3]}](https://youtu.be/{id[0]}) - {id[2]} Thank you for using - @xadmin_instabot", title=id[3].replace("_", " "), performer=id[2], thumb=thumbnail, duration=id[4])
            if DUMP_GROUP:
                await PForCopy.copy(DUMP_GROUP)
                await AForCopy.copy(DUMP_GROUP)
        await m.delete()
        if os.path.exists(randomdir):
            rmtree(randomdir)
        await message.reply("Check out @MohanishX(Channel)\nPlease support us to maintain this project.")
    except Exception as e:
        print(e)
        if LOG_GROUP:
            await Mbot.send_message(LOG_GROUP, f"Youtube {e} {link}")
        await message.reply(f"400: Sorry, unable to find it. Try another or report it to @SupportUser.")
        await Mbot.send_message(LOG_GROUP, traceback.format_exc())

@Mbot.on_message(filters.regex(r'https?://.*instagram[^\s]+') & filters.incoming | 
                 filters.regex(r'https?://.*tiktok[^\s]+') & filters.incoming | 
                 filters.regex(r'https?://.*twitter[^\s]+') & filters.incoming | 
                 filters.regex(r'https?://.*facebook[^\s]+') & filters.incoming)
async def handle_social_media_links(Mbot, message):
    try:
        await message.reply(f"Hello 👋👋 {message.from_user.mention()} \nI am a Telegram Bot that can download from multiple social media platforms. Currently, I support Instagram, TikTok, Twitter, Facebook, and YouTube!")
    except Exception as e:
        await Mbot.send_message(LOG_GROUP, f"Error handling link: {e}")
        await message.reply(f"400: Sorry, unable to process the request. Please try another link or report it to @SupportUser.")
        print(traceback.format_exc())

if __name__ == "__main__":
    Mbot.run()
