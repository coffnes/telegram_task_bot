import logging
import os
import shutil

import voice_converter
import photo_checking
import read_from_database
import save_to_database
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Данный бот создан для тестового задания на позицию Data Collection Specialist компании ID R&D\n"
                                    "Доступные команды:\n"
                                    "/start - показать список команд \n"
                                    "/photo - показать актуальное фото \n"
                                    "/voices - показать все сохраненные голосовые")


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    message = "Ошибка!"
    if photo_checking.check(user.id, "user_photo.jpg"):
        message = "Фото успешно сохранено, /photo - посмотреть фото"
    else:
        message = "На данном фото нет лица"
    await update.message.reply_text(message)


async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    voice_file = await update.message.voice.get_file()
    await voice_file.download_to_drive("temp_voice.oga")
    voice_converter.convert(user.id, "temp_voice.oga")
    await update.message.reply_text("Файл успешно конвертирован и сохранен, /voices - посмотреть голосовые")


async def show_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваше фото:")
    user = update.message.from_user
    file_name = read_from_database.photo_from_db(user.id)
    if file_name:
        await update.message.reply_photo(file_name)
        os.remove(file_name)
    else:
        await update.message.reply_text("У вас не добавлено фото")



async def show_voices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваши голосовые:")
    user = update.message.from_user
    voices = read_from_database.voices_from_db(user.id)
    if len(voices) == 0:
        await update.message.reply_text("У вас не добавлено голосовых")
    for voice in voices:
        await update.message.reply_document(voice)
    shutil.rmtree("temp_voices", ignore_errors=True)


def main():
    save_to_database.db_init()
    application = Application.builder().token("token").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, photo))
    application.add_handler(MessageHandler(filters.VOICE, voice))
    application.add_handler(CommandHandler("photo", show_photo))
    application.add_handler(CommandHandler("voices", show_voices))
    application.run_polling()


if __name__ == '__main__':
    main()

