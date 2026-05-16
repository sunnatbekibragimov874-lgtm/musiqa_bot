import telebot
import os
import subprocess
import time

TOKEN = "8968218318:AAG3nh4svS5zB3gZrmS9nrLKyZAyrwLiORo"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
                     "🎵 *Musiqa Chiqaruvchi Bot*\n\n"
                     "Har qanday videoni yuboring.\n"
                     "Men undan musiqani chiqarib beraman.",
                     parse_mode="Markdown")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        msg = bot.reply_to(message, "🔥 *Video qabul qilindi!*")

        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        video_path = f"video_{message.chat.id}.mp4"
        audio_path = f"audio_{message.chat.id}.mp3"

        with open(video_path, 'wb') as f:
            f.write(downloaded_file)

        bot.edit_message_text("🎧 *Musiqa tayyorlanmoqda...*\n❤️ Biz bilan bo‘lganingiz uchun mamnunmiz!", 
                            message.chat.id, msg.message_id)

        command = [
            'ffmpeg', '-i', video_path,
            '-vn', '-acodec', 'libmp3lame',
            '-b:a', '96k', '-ac', '2', '-ar', '44100',
            '-af', 'bass=10',
            '-y', audio_path
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(audio_path):
            audio_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
            with open(audio_path, 'rb') as audio:
                bot.send_audio(message.chat.id, audio, 
                             caption=f"✅ *Musiqa Tayyor!* 🎶\n📁 Hajmi: {audio_size_mb:.1f} MB",
                             reply_to_message_id=message.message_id)
        
        time.sleep(1.5)
        if os.path.exists(video_path): os.remove(video_path)
        if os.path.exists(audio_path): os.remove(audio_path)

    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik: {str(e)}")


print("🎵 Bot ishga tushdi...")
bot.infinity_polling()
