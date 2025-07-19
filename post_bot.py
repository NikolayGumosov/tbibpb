import datetime
import os
import requests

# Настройки
TOKEN = os.getenv("BOT_TOKEN")           # задается через GitHub Secrets
CHAT_ID = os.getenv("CHAT_ID")           # задается через GitHub Secrets

# Время запуска и тип публикации
now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # МСК = UTC+3
hour = now.hour
weekday = now.weekday()  # понедельник = 0, воскресенье = 6
week_number = now.isocalendar()[1]

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Ошибка:", response.text)
    else:
        print("Успешно отправлено")

# Стих дня (каждый день в 9:00)
def post_verse():
    with open("bible_verses.txt", "r", encoding="utf-8") as f:
        verses = [line.strip() for line in f if line.strip()]
    index = (now - datetime.datetime(2025, 1, 1)).days % len(verses)
    send_message(f"📖 <b>Стих дня</b>\n\n{verses[index]}")

# Молитва (каждый день в 20:00)
def post_prayer():
    with open("prayers.txt", "r", encoding="utf-8") as f:
        content = f.read()
    parts = content.split("=====")
    if 0 <= weekday < len(parts):
        send_message(f"🙏 <b>Молитва</b>\n\n{parts[weekday].strip()}")
    else:
        print("Не найдена молитва для дня недели.")

# История (воскресенье в 12:00)
def post_story():
    with open("bible_stories.txt", "r", encoding="utf-8") as f:
        content = f.read()
    stories = content.split("=====")
    story_index = (week_number - 1) % len(stories)
    send_message(f"📜 <b>Библейская история</b>\n\n{stories[story_index].strip()}")

# Запуск по расписанию
if hour == 9:
    post_verse()
elif hour == 20:
    post_prayer()
elif weekday == 6 and hour == 12:
    post_story()
else:
    print("Скрипт запущен вне расписания.")