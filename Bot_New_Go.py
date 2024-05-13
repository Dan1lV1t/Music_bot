import os
import telebot
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio


bot = telebot.TeleBot('6474964281:AAHM6tZJYceMQh6qfsk-oV4zBWpZ-t7A6Uo')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Салам! Отправь мне ссылку на видео с YouTube.")


@bot.message_handler(func=lambda message: True)
def download_video(message):
    try:
        video_url = message.text
        youtube = YouTube(video_url)

        video_stream = youtube.streams.filter(only_audio=True).first()

        if video_stream:
            video_stream.download()
            video_title = youtube.title
            new_filename = f'{video_title}.mp4'
            new_mp3_filename = f'{video_title}.mp3'

            os.rename(video_stream.default_filename, new_filename)

            ffmpeg_extract_audio(new_filename, new_mp3_filename)

            audio_file = open(new_mp3_filename, 'rb')
            bot.send_audio(message.chat.id, audio_file)

            audio_file.close()
            os.remove(new_filename)
            os.remove(new_mp3_filename)

        else:
            bot.reply_to(message, "Не удалось найти аудио в формате MP3.")

    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при скачивании аудио.")


bot.polling()

