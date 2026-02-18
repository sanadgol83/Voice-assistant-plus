import json
import os
import pyttsx3
import shutil
import sys
import asyncio
import edge_tts
import pygame
from io import BytesIO


def resource_path(relative_path):
    """برای دسترسی به فایل‌ها در حالت --onefile"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# مسیر فایل تنظیمات
def get_config_path():
    """مسیر دائمی برای ذخیره `config.json`"""
    appdata_path = os.path.join(os.getenv("APPDATA"), "Parsino")
    os.makedirs(appdata_path, exist_ok=True)
    return os.path.join(appdata_path, "config.json")

# مسیر دائمی config.json
CONFIG_FILE = get_config_path()

# بارگذاری تنظیمات
def load_settings():
    """بارگذاری تنظیمات از فایل دائمی"""
    if not os.path.exists(CONFIG_FILE):
        # کپی فایل اولیه از مسیر منبع به AppData
        default_config_path = resource_path("config.json")
        if os.path.exists(default_config_path):
            shutil.copy(default_config_path, CONFIG_FILE)
        else:
            # ایجاد فایل پیش‌فرض اگر منبع وجود نداشت
            save_settings(0, "minty")
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
        return config.get("gender", 0), config.get("theme", "minty")

def save_settings(gender, theme):
    """ذخیره تنظیمات در فایل دائمی"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"gender": gender, "theme": theme}, f, ensure_ascii=False, indent=4)

# مقدار اولیه choice
gender_var, _ = load_settings()
choice = gender_var  # 0 برای مرد، 1 برای زن

# تنظیمات صوت
engine = pyttsx3.init()
engine.setProperty('rate', 115)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')

# تعیین صدای اولیه
if choice == 0:
    engine.setProperty('voice', voices[0].id)  # مرد
else:
    engine.setProperty('voice', voices[1].id)  # زن


def update_choice(gender=None):
    """به‌روزرسانی choice و صدای دستیار با مقدار لحظه‌ای جنسیت"""
    global choice, engine, voices

    # اگر مقدار جنسیت مستقیماً داده شده باشد (بدون خواندن از فایل)
    if gender is not None:
        choice = gender
    else:
        # در حالت عادی، از فایل تنظیمات بارگذاری کن
        gender_var, _ = load_settings()
        choice = gender_var

    # تعیین صدای مرد یا زن
    if choice == 0:
        engine.setProperty('voice', voices[0].id)  # مرد
    else:
        engine.setProperty('voice', voices[1].id)  # زن

def speak(text):
    engine.say(text)
    engine.startLoop(False)  # False = غیر مسدودکننده
    # پردازش رویدادها تا پایان پخش
    while engine.isBusy():
        engine.iterate()
    engine.endLoop()



async def stream_audio(text, gender=None):
    # اگر جنسیت مشخص نشده، از تنظیمات ذخیره شده استفاده کن
    if gender is None:
        gender = choice
    
    # انتخاب صدا بر اساس جنسیت (0 برای مرد، 1 برای زن)
    if gender == 0:
        voice = "fa-IR-FaridNeural"  # صدای مرد
    else:
        voice = "fa-IR-DilaraNeural"  # صدای زن
    
    communicate = edge_tts.Communicate(text, voice)
    
    # راه اندازی pygame برای پخش صدا
    pygame.mixer.init()
    pygame.init()
    
    # جمع‌آوری تمام داده‌های صوتی در حافظه
    audio_data = bytearray()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
    
    # ایجاد فایل صوتی مجازی در حافظه
    audio_buffer = BytesIO(audio_data)
    
    # پخش فایل صوتی
    pygame.mixer.music.load(audio_buffer, "mp3")
    pygame.mixer.music.play()
    
    # منتظر ماندن تا پخش تمام شود
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)
    
    pygame.quit()
