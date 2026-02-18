import sounddevice as sd
from basic_media import *
from Internet_media import *
from utils import update_choice
import queue
import time
import json
import vosk
import tkinter as tk
import ttkbootstrap as ttk
import threading
import sys
import os
from pygame import mixer
import shutil
from webcam_media import *
mixer.init()

def resource_path(relative_path):
    """برای دسترسی به فایل‌ها در حالت --onefile"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# مسیرهای مدل Vosk
model_path_fa = resource_path("vosk-model-small-fa-0.5")
model_path_en = resource_path("vosk-model-small-en-us-0.15")

# بارگذاری مدل‌ها
try:
    model_fa = vosk.Model(model_path_fa)
    model_en = vosk.Model(model_path_en)
    current_model = model_fa  # مدل پیش‌فرض
    current_language = "fa"   # زبان پیش‌فرض
except Exception as e:
    print(f"خطا در بارگذاری مدل‌ها: {e}")

q = queue.Queue()

# متغیرهای جهانی
stream = None
assistant_active = False
assistant_thread = None

# فایل تنظیمات
def get_config_path():
    """مسیر دائمی برای ذخیره `config.json`"""
    appdata_path = os.path.join(os.getenv("APPDATA"), "Parsino")
    os.makedirs(appdata_path, exist_ok=True)
    return os.path.join(appdata_path, "config.json")

# مسیر دائمی config.json
CONFIG_FILE = get_config_path()

# بارگذاری تنظیمات قبلی
def load_settings():
    """بارگذاری تنظیمات از فایل دائمی"""
    if not os.path.exists(CONFIG_FILE):
        default_config_path = resource_path("config.json")
        if os.path.exists(default_config_path):
            shutil.copy(default_config_path, CONFIG_FILE)
        else:
            save_settings(0, "minty", "fa")
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
        return (config.get("gender", 0), 
                config.get("theme", "minty"), 
                config.get("language", "fa"))

# ذخیره تنظیمات در فایل
def save_settings(gender, theme, language):
    """ذخیره تنظیمات در فایل"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"gender": gender, "theme": theme, "language": language}, 
                 f, ensure_ascii=False, indent=4)

# سیستم مدیریت متن چندزبانه
class TextManager:
    def __init__(self):
        self.texts = {
            "fa": {
                "window_title": "دستیار صوتی هوشمند پارسینو",
                "start_btn": "شروع",
                "stop_btn": "توقف",
                "exit_btn": "خروج",
                "settings_btn": "⚙️ تنظیمات",
                "back_btn": "← بازگشت",
                "status_ready": "وضعیت: آماده به کار",
                "status_active": "وضعیت: فعال - در حال گوش دادن",
                "status_stopped": "وضعیت: متوقف شده",
                "language_label": "زبان: فارسی",
                "console_title": "نمایش فعالیت های سیستم",
                "settings_title": "تنظیمات",
                "theme_title": "تغییر تم",
                "language_selection": "انتخاب زبان و گوینده",
                "language_text": "زبان",
                "voice_text": "گوینده",
                "male_voice": "پارسا",
                "female_voice": "رویا",
                "theme_btn": "تغییر تم",
                "assistant_ready": "<<< سیستم آماده است برای شروع دکمه 'شروع' را فشار دهید",
                "assistant_activated": "<<< ... دستیار فعال شد آماده دریافت دستورات",
                "assistant_stopped": "<<< دستیار متوقف شد برای شروع مجدد دکمه شروع را بزنید",
                "voice_selected": "گوینده انتخاب شده: {}",
                "language_selected": "زبان انتخاب شده: {}",
                "theme_changed": "...✨تغییر کرد {} تم برنامه به...",
                "help_title": "اطلاعات پروژه و راهنمای استفاده"
            },
            "en": {
                "window_title": "Parsino Intelligent Voice Assistant",
                "start_btn": "Start",
                "stop_btn": "Stop",
                "exit_btn": "Exit",
                "settings_btn": "⚙️ Settings",
                "back_btn": "← Back",
                "status_ready": "Status: Ready",
                "status_active": "Status: Active - Listening",
                "status_stopped": "Status: Stopped",
                "language_label": "Language: English",
                "console_title": "System Activity Display",
                "settings_title": "Settings",
                "theme_title": "Change Theme",
                "language_selection": "Language and Voice Selection",
                "language_text": "Language",
                "voice_text": "Voice",
                "male_voice": "Alex",
                "female_voice": "Enola",
                "theme_btn": "Change Theme",
                "assistant_ready": "<<< System is ready. Press the 'Start' button to begin",
                "assistant_activated": "<<< ... Assistant activated, ready to receive commands",
                "assistant_stopped": "<<< Assistant stopped. Press Start to resume.",
                "voice_selected": "Voice selected: {}",
                "language_selected": "Language selected: {}",
                "theme_changed": "...✨Theme changed to {}...",
                "help_title": "Project Information and User Guide"
            }
        }
    
    def get_text(self, key, language):
        """دریافت متن بر اساس کلید و زبان"""
        return self.texts.get(language, {}).get(key, key)

# ایجاد مدیر متن
text_manager = TextManager()

# واژگان دستوری فارسی
wakeUpCall_fa = ['بارسا','پارسا']
wakeUpCall_en = ['alex']

app_commands = ['برنامه', 'اپ']
chrome_command = ['کروم', 'گوگل']
firefox_command = ['فایر', 'فاکس']
word_command = ['برد','ورلد','ورد']
point_command = ['پوینت','پاور', 'پاورپوینت']
excel_command = ['اکسل']

notebook_command = ['تکست','متن','دفترچه‌یاداشت','دفترچه‌یادداشت','یاداشت','یادداشت','دفترچه']

system_commands = ['کامپیوتر', 'سیستم']
off_command = ['خاموش']
rest_command = ['ریست']

webcam_commands = ['وبکم','وب']
photo_command = ['عکس']
video_command = ['فیلم','ویدیو']

wiki_command = ['ریکی', 'پدیا', 'ویکی', 'ویکی‌پدیا']
browser_command = ['جستجو','تحقیق']
ai_command = ['هوش‌مصنوعی','مصنوعی','هوش']
text_to_photo_command = ['عکس','تولید‌عکس','تولید']
Translator_command = ['انگلیسی','ترنسلیت','ترجمه']

pc_command = ['مای', 'دیس', 'پی سی']
settings_command = ['تنظیمات']
time_command = ['زمان', 'ساعت']

play_command = ['پخش', 'پلی']
stop_command = ['متوقف', 'قطع', 'استاپ']
prev_command = ['قبلی', 'قبلیه']
next_command = ['بعدی', 'بعديه']

sound_commands = ['صدا']
sound_mute_command = ['ند','به', 'ميوت']
sound_unmute_command = ['باز']
sound_vol_down = ['خم', 'کم', 'کاهش']
sound_vol_up = ['زیاد', 'افزايش']

bright_commands = ['نور', 'روشنایی']
bright_vol_down = ['خم', 'کم', 'کاهش']
bright_vol_up = ['زیاد', 'افزايش']

windowes_commands = ['پنجره']
max_command = ['بزرگ']
min_command = ['کوچک','کوچیک']
restore_command = ['باز']
close_command = ['بستن','ند','به']

screen_command = ['اسکرین', 'صفحه']

mony_command = ['اقتصاد', 'دلار', 'طلا']

internet_command = ['آنلاین','سرعت','اتصال','اینترنت']

# واژگان دستوری انگلیسی
app_commands_en = ['app', 'application', 'program', 'open']
chrome_command_en = ['chrome', 'browser', 'google']
firefox_command_en = ['firefox', 'fox']
word_command_en = ['word', 'document']
point_command_en = ['powerpoint', 'presentation', 'slides']
excel_command_en = ['excel', 'spreadsheet']

notebook_command_en = ['text', 'notepad', 'note', 'notebook', 'write']

system_commands_en = ['computer', 'system']
off_command_en = ['shutdown', 'turn off', 'power off']
rest_command_en = ['restart', 'reboot']

webcam_commands_en = ['webcam', 'camera']
photo_command_en = ['photo', 'picture', 'take photo']
video_command_en = ['video', 'record video', 'record']

wiki_command_en = ['article']
browser_command_en = ['search', 'research']
ai_command_en = ['ai', 'artificial', 'intelligence']
text_to_photo_command_en = ['generate', 'image', 'create', 'photo', 'picture']
Translator_command_en = ['translate', 'english', 'translation']

pc_command_en = ['pc', 'this']
settings_command_en = ['settings', 'control panel']
time_command_en = ['time', 'clock']

play_command_en = ['play', 'start']
stop_command_en = ['stop', 'pause']
prev_command_en = ['previous', 'back']
next_command_en = ['next', 'skip']

sound_commands_en = ['volume', 'sound']
sound_mute_command_en = ['mute', 'silence']
sound_unmute_command_en = ['unmute', 'sound on']
sound_vol_down_en = ['down']
sound_vol_up_en = ['up']

bright_commands_en = ['brightness', 'light']
bright_vol_down_en = ['down']
bright_vol_up_en = ['up']

windowes_commands_en = ['window']
max_command_en = ['maximize', 'fullscreen']
min_command_en = ['minimize', 'small']
restore_command_en = ['restore', 'normal']
close_command_en = ['close', 'exit']

screen_command_en = ['screenshot', 'screen']

mony_command_en = ['economy', 'dollar', 'gold', 'currency']

internet_command_en = ['internet', 'speed', 'connection', 'online']


# تابع‌های صوت - ساختار اصلی
def start_recording():
    global stream
    if stream is None:
        stream = sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=callback)
        stream.start()

def stop_recording():
    global stream
    if stream:
        stream.stop()
        stream.close()
        stream = None

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))


def execute_command(command, language):
    """انتخاب تابع اجرای دستور بر اساس زبان"""
    if language == "fa":
        execute_command_fa(command)
    else:
        execute_command_en(command)


def execute_command_fa(command):
    """اجرای دستورات فارسی"""
    command = command.lower()
    if any(item in command for item in wakeUpCall_fa):
        print(f"تشخیص دادم: {command}")
        
        if any(item in command for item in app_commands):
            if any(item in command for item in chrome_command):
                chrome(1)
            elif any(item in command for item in firefox_command):
                firefox(1)
            elif any(item in command for item in word_command):
                word(1)
            elif any(item in command for item in point_command):
                point(1)
            elif any(item in command for item in excel_command):
                excel(1)

        elif any(item in command for item in notebook_command):
            notebook(command,1)

        elif any(item in command for item in system_commands):
            if any(item in command for item in off_command):
                off(1)
            elif any(item in command for item in rest_command):
                rest(1)
        
        elif any(item in command for item in webcam_commands):
            if any(item in command for item in photo_command):
                take_photo(1)
            elif any(item in command for item in video_command):
                record_video(1)

        elif any(item in command for item in wiki_command):
            internet(command, 1,1)
        elif any(item in command for item in browser_command):
            internet(command, 2,1)
        elif any(item in command for item in ai_command):
            internet(command, 3,1)
        elif any(item in command for item in text_to_photo_command):
            internet(command, 4,1)
        elif any(item in command for item in Translator_command):
            internet(command, 5,1)

        elif any(item in command for item in pc_command):
            this_pc(1)
        elif any(item in command for item in settings_command):
            settings(1)    
        elif any(item in command for item in time_command):
            timex(1)

        elif any(item in command for item in play_command):
            play(1)
        elif any(item in command for item in stop_command):
            stop(1)
        elif any(item in command for item in prev_command):
            gl(1)
        elif any(item in command for item in next_command):
            bl(1)

        elif any(item in command for item in sound_commands):
            if any(item in command for item in sound_mute_command):
                mute(1)
            elif any(item in command for item in sound_unmute_command):
                unmute(1)
            elif any(item in command for item in sound_vol_down):
                kam(1)
            elif any(item in command for item in sound_vol_up):
                ziad(1)

        elif any(item in command for item in bright_commands):
            if any(item in command for item in bright_vol_down):
                n_kam(1)
            elif any(item in command for item in bright_vol_up):
                n_ziad(1)
        
        elif any(item in command for item in windowes_commands):
            if any(item in command for item in max_command):
                maximize_current_window(1)
            elif any(item in command for item in min_command):
                minimize_current_window(1)
            elif any(item in command for item in restore_command):
                restore_window(1)
            elif any(item in command for item in close_command):
                close_current_window(1)
            
        elif any(item in command for item in screen_command):
            screen(1)

        elif any(item in command for item in mony_command):
            mony(1)

        elif any(item in command for item in internet_command):
            check_internet(1)

def execute_command_en(command):
    """اجرای دستورات انگلیسی"""
    command = command.lower()
    if any(item in command for item in wakeUpCall_en):
        print(f"Detected: {command}")
        
        if any(item in command for item in app_commands_en):
            if any(item in command for item in chrome_command_en):
                chrome(2)
            elif any(item in command for item in firefox_command_en):
                firefox(2)
            elif any(item in command for item in word_command_en):
                word(2)
            elif any(item in command for item in point_command_en):
                point(2)
            elif any(item in command for item in excel_command_en):
                excel(2)

        elif any(item in command for item in notebook_command_en):
            notebook(command,2)

        elif any(item in command for item in system_commands_en):
            if any(item in command for item in off_command_en):
                off(2)
            elif any(item in command for item in rest_command_en):
                rest(2)
        
        elif any(item in command for item in webcam_commands_en):
            if any(item in command for item in photo_command_en):
                take_photo(2)
            elif any(item in command for item in video_command_en):
                record_video(2)

        elif any(item in command for item in wiki_command_en):
            internet(command, 1,2)
        elif any(item in command for item in browser_command_en):
            internet(command, 2,2)
        elif any(item in command for item in ai_command_en):
            internet(command, 3,2)
        elif any(item in command for item in text_to_photo_command_en):
            internet(command, 4,2)
        elif any(item in command for item in Translator_command_en):
            internet(command, 5,2)

        elif any(item in command for item in pc_command_en):
            this_pc(2)
        elif any(item in command for item in settings_command_en):
            settings(2)    
        elif any(item in command for item in time_command_en):
            timex(2)

        elif any(item in command for item in play_command_en):
            play(2)
        elif any(item in command for item in stop_command_en):
            stop(2)
        elif any(item in command for item in prev_command_en):
            gl(2)
        elif any(item in command for item in next_command_en):
            bl(2)

        elif any(item in command for item in sound_commands_en):
            if any(item in command for item in sound_mute_command_en):
                mute(2)
            elif any(item in command for item in sound_unmute_command_en):
                unmute(2)
            elif any(item in command for item in sound_vol_down_en):
                kam(2)
            elif any(item in command for item in sound_vol_up_en):
                ziad(2)

        elif any(item in command for item in bright_commands_en):
            if any(item in command for item in bright_vol_down_en):
                n_kam(2)
            elif any(item in command for item in bright_vol_up_en):
                n_ziad(2)
        
        elif any(item in command for item in windowes_commands_en):
            if any(item in command for item in max_command_en):
                maximize_current_window(2)
            elif any(item in command for item in min_command_en):
                minimize_current_window(2)
            elif any(item in command for item in restore_command_en):
                restore_window(2)
            elif any(item in command for item in close_command_en):
                close_current_window(2)
            
        elif any(item in command for item in screen_command_en):
            screen(2)

        elif any(item in command for item in mony_command_en):
            mony(2)

        elif any(item in command for item in internet_command_en):
            check_internet(2)


class RedirectStdout:
    """هدایت خروجی پرینت به پنجره متن با راست‌چین کردن"""

    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.tag_configure('right', justify='right', font=("Tahoma", 9))

    def write(self, string):
        lines = string.split('\n')
        for line in lines:
            if line.strip():
                self.text_widget.insert(tk.END, line + '\n', 'right')
            else:
                self.text_widget.insert(tk.END, '\n')
        self.text_widget.see(tk.END)
        self.text_widget.update_idletasks()

    def flush(self):
        pass

class AssistantGUI:
    def __init__(self):
        
        # بارگذاری تنظیمات قبلی
        gender_var, theme_var, language_var = load_settings()
        self.gender_var = gender_var
        self.theme_var = theme_var
        self.language_var = language_var

        # تنظیم مدل و کلمات唤醒 بر اساس زبان
        self.update_language_models()

        # ایجاد پنجره اصلی
        self.root = ttk.Window(themename=self.theme_var)
        self.update_window_title()
        self.root.geometry("600x400")
        self.root.minsize(400, 300)
        self.root.resizable(True, True)

        self.title_text = tk.StringVar()
        self.update_title()

        # ایجاد پشته برای مدیریت پنل‌ها
        self.panel_stack = []

        # ایجاد فریم اصلی برای پنل‌ها
        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ایجاد پنل اصلی
        self.main_panel = self.create_main_panel()
        self.settings_panel = self.create_settings_panel()
        self.theme_panel = self.create_theme_panel()

        # نمایش پنل اصلی
        self.show_panel(self.main_panel)

        # تنظیم خروجی کنسول
        sys.stdout = RedirectStdout(self.console)

        # مدیریت رویداد بستن پنجره
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # متغیرهای دستیار
        self.assistant_active = False
        self.assistant_thread = None

        print(text_manager.get_text("assistant_ready", self.language_var))
        self.root.mainloop()

    def update_language_models(self):
        """به‌روزرسانی مدل و کلمات唤醒 بر اساس زبان انتخاب شده"""
        global current_model, current_language, wakeUpCall_fa, wakeUpCall_en
        
        if self.language_var == "fa":
            current_model = model_fa
            current_language = "fa"
            # به‌روزرسانی لیست اصلی بر اساس جنسیت
            if self.gender_var == 0:
                wakeUpCall_fa[:] = ['بارسا','پارسا']
            else:
                wakeUpCall_fa[:] = ['یا','رو','رویا']
        else:
            current_model = model_en
            current_language = "en"
            if self.gender_var == 0:
                wakeUpCall_en[:] = ['alex']
            else:
                wakeUpCall_en[:] = ['enola','nola']

    def update_title(self):
        """به‌روزرسانی عنوان بر اساس زبان و جنسیت"""
        if self.language_var == "fa":
            if self.gender_var == 0:
                self.title_text.set("پارسا")
            else:
                self.title_text.set("رویا")
        else:
            if self.gender_var == 0:
                self.title_text.set("Alex")
            else:
                self.title_text.set("Enola")
    
    def update_window_title(self):
        """به‌روزرسانی عنوان پنجره بر اساس زبان"""
        self.root.title(text_manager.get_text("window_title", self.language_var))

    def create_main_panel(self):
        """ایجاد پنل اصلی"""
        panel = ttk.Frame(self.container)
        panel.grid_rowconfigure(1, weight=1)
        panel.grid_columnconfigure(0, weight=1)

        header_frame = ttk.Frame(panel)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        title = ttk.Label(
            header_frame,
            textvariable=self.title_text,
            font=("Tahoma", 15, "bold"),
            bootstyle="inverse-primary",
            anchor="center"
        )
        title.pack(fill=tk.X, pady=5)

        # استفاده از text به جای textvariable برای LabelFrame
        self.console_frame = ttk.LabelFrame(
            panel, 
            text=text_manager.get_text("console_title", self.language_var)
        )
        self.console_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.console = tk.Text(
            self.console_frame,
            height=8,
            bg="#2e2e2e",
            fg="white",
            font=("Tahoma", 9),
            wrap=tk.WORD
        )
        self.console.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            self.console_frame,
            command=self.console.yview,
            bootstyle="round"
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.console.config(yscrollcommand=scrollbar.set)
        self.console_frame.grid_rowconfigure(0, weight=1)
        self.console_frame.grid_columnconfigure(0, weight=1)

        button_frame = ttk.Frame(panel)
        button_frame.grid(row=2, column=0, sticky="ew", pady=(10, 5))
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.start_btn = ttk.Button(
            button_frame,
            text=text_manager.get_text("start_btn", self.language_var),
            command=self.start_assistant,
            bootstyle="success",
            width=8
        )
        self.start_btn.grid(row=0, column=0, sticky="ew", padx=2)

        self.stop_btn = ttk.Button(
            button_frame,
            text=text_manager.get_text("stop_btn", self.language_var),
            command=self.stop_assistant,
            bootstyle="danger",
            width=8,
            state=tk.DISABLED
        )
        self.stop_btn.grid(row=0, column=1, sticky="ew", padx=2)

        self.exit_btn = ttk.Button(
            button_frame,
            text=text_manager.get_text("exit_btn", self.language_var),
            command=self.on_close,
            bootstyle="warning",
            width=8
        )
        self.exit_btn.grid(row=0, column=2, sticky="ew", padx=2)

        self.settings_btn = ttk.Button(
            button_frame,
            text=text_manager.get_text("settings_btn", self.language_var),
            command=lambda: self.show_panel(self.settings_panel),
            bootstyle="info",
            width=8
        )
        self.settings_btn.grid(row=0, column=3, sticky="ew", padx=2)

        status_bar = ttk.Frame(panel, padding=(5, 2))
        status_bar.grid(row=3, column=0, sticky="ew")
        
        # وضعیت سمت چپ
        self.status_var = tk.StringVar(value=text_manager.get_text("status_ready", self.language_var))
        status_label = ttk.Label(
            status_bar,
            textvariable=self.status_var,
            bootstyle="inverse-dark",
            font=("Tahoma", 8)
        )
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # زبان سمت راست
        self.lang_status_var = tk.StringVar(value=text_manager.get_text("language_label", self.language_var))
        lang_status_label = ttk.Label(
            status_bar,
            textvariable=self.lang_status_var,
            bootstyle="inverse-info",
            font=("Tahoma", 8)
        )
        lang_status_label.pack(side=tk.RIGHT, padx=5)

        return panel

    def create_settings_panel(self):
        """ایجاد پنل تنظیمات"""
        panel = ttk.Frame(self.container)

        # عنوان و دکمه بازگشت
        header = ttk.Frame(panel)
        header.pack(fill=tk.X, pady=(0, 10))

        self.back_btn_settings = ttk.Button(
            header,
            text=text_manager.get_text("back_btn", self.language_var),
            command=lambda: self.show_panel(self.main_panel),
            bootstyle="secondary",
            width=8
        )
        self.back_btn_settings.pack(side=tk.RIGHT, padx=5)

        self.settings_title = ttk.Label(
            header,
            text=text_manager.get_text("settings_title", self.language_var),
            font=("Tahoma", 15, "bold"),
            bootstyle="inverse-primary",
            anchor="center"
        )
        self.settings_title.pack(fill=tk.X, expand=True, pady=2)

        # استفاده از text به جای textvariable برای LabelFrame
        self.settings_console_frame = ttk.LabelFrame(
            panel, 
            text=text_manager.get_text("help_title", self.language_var)
        )
        # توجه: pack این فریم بعداً انجام می‌شود تا کنترل‌های پایین صفحه همیشه دیده شوند

        scrollbar = ttk.Scrollbar(self.settings_console_frame, bootstyle="round")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.settings_console = tk.Text(
            self.settings_console_frame,
            height=8,
            bg="#2e2e2e",
            fg="white",
            font=("Tahoma", 10),
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        self.settings_console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.settings_console.yview)
        self.settings_console.tag_configure('right', justify='right', font=("Tahoma", 10))

        # بارگذاری محتوای راهنما
        self.update_help_text()

        # نوار کنترل‌های پایین (همیشه قابل مشاهده)
        bottom_controls = ttk.Frame(panel)
        bottom_controls.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 5))

        # بخش انتخاب زبان و گوینده
        self.selection_frame = ttk.LabelFrame(
            bottom_controls, 
            text=text_manager.get_text("language_selection", self.language_var)
        )
        self.selection_frame.pack(fill=tk.X, pady=(0, 6))
        
        # تغییر: selection_inner را در وسط قرار می‌دهیم
        selection_inner = ttk.Frame(self.selection_frame)
        selection_inner.pack(padx=5, pady=5, anchor='center')  # <-- anchor=center
        
        # تنظیم وزن ستون‌ها برای مرکز قرار دادن
        selection_inner.grid_columnconfigure(0, weight=1)
        selection_inner.grid_columnconfigure(1, weight=1)
        
        # ستون زبان
        lang_frame = ttk.Frame(selection_inner)
        lang_frame.grid(row=0, column=0, sticky="ew", padx=(0, 20))  # <-- sticky="ew"
        
        self.lang_label = ttk.Label(
            lang_frame, 
            text=" : "+text_manager.get_text("language_text", self.language_var), 
            font=("Tahoma", 9)
        )
        self.lang_label.grid(row=1, column=3, sticky="w")  # اگر می‌خواهید این هم وسط باشد، sticky="" بگذارید
        
        self.current_language = tk.StringVar(value=self.language_var)
        
        lang_btn_frame = ttk.Frame(lang_frame)
        lang_btn_frame.grid(row=1, column=0, sticky="w", pady=2)
        
        fa_btn = ttk.Radiobutton(
            lang_btn_frame,
            text="فارسی",
            variable=self.current_language,
            value="fa",
            command=lambda: self.update_language("fa"),
            bootstyle="primary-toolbutton"
        )
        fa_btn.pack(side=tk.LEFT)
        
        en_btn = ttk.Radiobutton(
            lang_btn_frame,
            text="English",
            variable=self.current_language,
            value="en",
            command=lambda: self.update_language("en"),
            bootstyle="primary-toolbutton"
        )
        en_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # ستون گوینده
        gender_frame = ttk.Frame(selection_inner)
        gender_frame.grid(row=0, column=1, sticky="ew")  # <-- sticky="ew"
        
        self.voice_label = ttk.Label(
            gender_frame, 
            text=" : "+text_manager.get_text("voice_text", self.language_var), 
            font=("Tahoma", 9)
        )
        self.voice_label.grid(row=1, column=3, sticky="w")
        
        self.current_gender = tk.IntVar(value=self.gender_var)
        
        gender_btn_frame = ttk.Frame(gender_frame)
        gender_btn_frame.grid(row=1, column=0, sticky="w", pady=2)
        
        self.male_btn = ttk.Radiobutton(
            gender_btn_frame,
            text=text_manager.get_text("male_voice", self.language_var),
            variable=self.current_gender,
            value=0,
            command=lambda: self.update_gender(0),
            bootstyle="primary-toolbutton"
        )
        self.male_btn.pack(side=tk.LEFT)
        
        self.female_btn = ttk.Radiobutton(
            gender_btn_frame,
            text=text_manager.get_text("female_voice", self.language_var),
            variable=self.current_gender,
            value=1,
            command=lambda: self.update_gender(1),
            bootstyle="primary-toolbutton"
        )
        self.female_btn.pack(side=tk.LEFT, padx=(10, 0))

        # دکمه تغییر تم
        self.theme_btn = ttk.Button(
            bottom_controls,
            text=text_manager.get_text("theme_btn", self.language_var),
            command=lambda: self.show_panel(self.theme_panel),
            bootstyle="primary",
            width=80
        )
        self.theme_btn.pack(fill=tk.X)

        # فریم راهنما باید فضای باقی‌مانده را بگیرد
        self.settings_console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        return panel

    def update_help_text(self):
        """به‌روزرسانی متن راهنما بر اساس زبان فعلی"""
        self.settings_console.config(state=tk.NORMAL)
        self.settings_console.delete("1.0", tk.END)
        
        if self.language_var == "fa":
            help_text = """📋 اطلاعات پروژه و راهنمای کامل دستیار صوتی پارسینو

👨‍💻 اطلاعات توسعه:
• برنامه‌نویس و سازنده: محمد سندگل
• ورژن فعلی نرم‌افزار: 3.2.5
• سال شروع ساخت: 2025
• تکنولوژی‌های استفاده شده: Python, Vosk, Tkinter, ttkbootstrap

🎯 روش استفاده از دستیار:

۱. ابتدا باید نام دستیار را صدا بزنید:
   • برای پارسا: پارسا
   • برای رویا: رویا

۲. سپس دستور مورد نظر را بیان کنید

📝 دستورات اصلی دستیار:

🎵 دستورات کنترل رسانه:
• "پارسا پخش کن" - پخش موسیقی/ویدیو
• "پارسا متوقف کن" - توقف پخش
• "پارسا قبلی" - بازگشت به آهنگ قبلی
• "پارسا بعدی" - رفتن به آهنگ بعدی

🔊 دستورات کنترل صدا:
• "پارسا صدا کم کن" - کاهش حجم صدا
• "پارسا صدا زیاد کن" - افزایش حجم صدا
• "پارسا صدا قطع کن" - بی‌صدا کردن
• "پارسا صدا روشن کن" - فعال کردن صدا

💻 دستورات برنامه‌ها:
• "پارسا کروم باز کن" - اجرای مرورگر کروم
• "پارسا فایرفاکس باز کن" - اجرای فایرفاکس
• "پارسا ورد باز کن" - اجرای Microsoft Word
• "پارسا پاورپوینت باز کن" - اجرای PowerPoint
• "پارسا اکسل باز کن" - اجرای Excel

📓 دستورات دفترچه یادداشت:
• "پارسا دفترچه باز کن" - ایجاد یادداشت جدید
• "پارسا متن بنویس [متن مورد نظر]" - نوشتن متن

🌐 دستورات اینترنت و جستجو:
• "پارسا ویکی پدیا [موضوع]" - جستجو در ویکی‌پدیا
• "پارسا جستجو کن [عبارت]" - جستجو در اینترنت
• "پارسا هوش مصنوعی [سوال]" - پرسش از هوش مصنوعی
• "پارسا عکس تولید کن [توضیحات]" - تولید عکس با هوش مصنوعی
• "پارسا ترجمه کن [متن]" - ترجمه متن به انگلیسی

🖥️ دستورات سیستم:
• "پارسا کامپیوتر خاموش کن" - خاموش کردن سیستم
• "پارسا کامپیوتر ریستارت کن" - راه‌اندازی مجدد
• "پارسا مای کامپیوتر باز کن" - باز کردن This PC
• "پارسا تنظیمات باز کن" - باز کردن تنظیمات ویندوز

📷 دستورات وبکم:
• "پارسا عکس بگیر" - عکس‌برداری با وبکم
• "پارسا فیلم بگیر" - ضبط ویدیو با وبکم

🪟 دستورات مدیریت پنجره‌ها:
• "پارسا پنجره بزرگ کن" - بزرگ کردن پنجره جاری
• "پارسا پنجره کوچک کن" - کوچک کردن پنجره
• "پارسا پنجره ببند" - بستن پنجره جاری
• "پارسا پنجره باز کن" - بازگرداندن پنجره

🖼️ دستورات صفحه‌نمایش:
• "پارسا اسکرین شات بگیر" - عکس‌برداری از صفحه

💰 دستورات اقتصادی:
• "پارسا قیمت دلار" - نمایش قیمت ارز
• "پارسا قیمت طلا" - نمایش قیمت طلا

📡 دستورات اینترنت:
• "پارسا وضعیت اینترنت" - بررسی سرعت اینترنت

⏰ دستورات زمان:
• "پارسا ساعت چند است" - نمایش زمان فعلی

🔧 نکات مهم:
• دستورات باید به صورت طبیعی و روان بیان شوند
• پس از گفتن نام دستیار، کمی مکث کنید سپس دستور را بگویید
• محیط را ساکت نگه دارید برای تشخیص بهتر صدا
• از میکروفون با کیفیت استفاده کنید

⚙️ تنظیمات قابل تغییر:
• انتخاب بین دو گوینده (پارسا/رویا)
• انتخاب زبان (فارسی/انگلیسی)
• تغییر تم رابط کاربری
• تنظیم جنسیت صدا

برای شروع، دکمه "شروع" را فشار داده و دستورات خود را آزمایش کنید!"""
        else:
            help_text = """📋 Project Information and Complete Guide for Parsino Voice Assistant

👨‍💻 Development Information:
• Developer: Mohammad Sandgol
• Current Version: 3.2.5
• Start Year: 2025
• Technologies Used: Python, Vosk, Tkinter, ttkbootstrap

🎯 How to Use the Assistant:

1. First, call the assistant's name:
   • For Alex: "Alex"
   • For Enola: "Enola"

2. Then say your command

📝 Main Commands:

🎵 Media Control Commands:
• "Alex play" - Play music/video
• "Alex stop" - Stop playback
• "Alex previous" - Previous track
• "Alex next" - Next track

🔊 Volume Control Commands:
• "Alex volume down" - Decrease volume
• "Alex volume up" - Increase volume
• "Alex mute" - Mute sound
• "Alex unmute" - Unmute sound

💻 Application Commands:
• "Alex open chrome" - Launch Chrome browser
• "Alex open firefox" - Launch Firefox
• "Alex open word" - Launch Microsoft Word
• "Alex open powerpoint" - Launch PowerPoint
• "Alex open excel" - Launch Excel

📓 Notepad Commands:
• "Alex open notepad" - Create new note
• "Alex write text [text]" - Write text

🌐 Internet and Search Commands:
• "Alex wikipedia [topic]" - Search Wikipedia
• "Alex search [query]" - Internet search
• "Alex ai [question]" - Ask AI question
• "Alex generate image [description]" - Generate AI image
• "Alex translate [text]" - Translate to English

🖥️ System Commands:
• "Alex shutdown computer" - Shutdown system
• "Alex restart computer" - Restart system
• "Alex open my computer" - Open This PC
• "Alex open settings" - Open Windows settings

📷 Webcam Commands:
• "Alex take photo" - Capture photo with webcam
• "Alex record video" - Record video with webcam

🪟 Window Management Commands:
• "Alex maximize window" - Maximize current window
• "Alex minimize window" - Minimize window
• "Alex close window" - Close current window
• "Alex restore window" - Restore window

🖼️ Screen Commands:
• "Alex take screenshot" - Capture screen

💰 Economy Commands:
• "Alex dollar price" - Show currency rates
• "Alex gold price" - Show gold price

📡 Internet Commands:
• "Alex internet status" - Check internet speed

⏰ Time Commands:
• "Alex what time is it" - Show current time

🔧 Important Tips:
• Commands should be spoken naturally and clearly
• Pause briefly after saying the assistant's name
• Keep the environment quiet for better voice recognition
• Use a quality microphone for best results

⚙️ Customizable Settings:
• Choose between two voices (Alex/Enola)
• Select language (Persian/English)
• Change user interface theme
• Adjust voice gender settings

Press the "Start" button to begin and test your commands!"""
        
        self.settings_console.insert(tk.END, help_text, 'right')
        self.settings_console.config(state=tk.DISABLED)

    def create_theme_panel(self):
        """ایجاد پنل تغییر تم"""
        panel = ttk.Frame(self.container)

        # عنوان و دکمه بازگشت
        header = ttk.Frame(panel)
        header.pack(fill=tk.X, pady=(0, 10))

        self.back_btn_theme = ttk.Button(
            header,
            text=text_manager.get_text("back_btn", self.language_var),
            command=lambda: self.show_panel(self.settings_panel),
            bootstyle="secondary",
            width=8
        )
        self.back_btn_theme.pack(side=tk.RIGHT, padx=5)

        self.theme_title = ttk.Label(
            header,
            text=text_manager.get_text("theme_title", self.language_var),
            font=("Tahoma", 15, "bold"),
            bootstyle="inverse-primary",
            anchor="center"
        )
        self.theme_title.pack(fill=tk.X, expand=True, pady=5)

        themes = [
            "cosmo", "flatly", "litera", "minty", "lumen",
            "sandstone", "yeti", "pulse", "united", "morph",
            "journal", "darkly", "superhero", "solar", "cyborg",
            "vapor", "simplex", "cerculean"
        ]

        # ایجاد فریم اصلی برای ستون‌ها
        columns_frame = ttk.Frame(panel)
        columns_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ایجاد سه ستون
        col1 = ttk.Frame(columns_frame)
        col2 = ttk.Frame(columns_frame)
        col3 = ttk.Frame(columns_frame)

        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        col3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # تقسیم تم‌ها به سه بخش مساوی
        chunk_size = len(themes) // 3
        themes1 = themes[:chunk_size]
        themes2 = themes[chunk_size:2 * chunk_size]
        themes3 = themes[2 * chunk_size:]

        # ایجاد دکمه‌ها برای ستون اول
        for theme in themes1:
            btn = ttk.Button(
                col1,
                text=theme,
                command=lambda t=theme: self.change_theme(t),
                bootstyle="light",
                width=12
            )
            btn.pack(pady=7, padx=3, fill=tk.X)

        # ایجاد دکمه‌ها برای ستون دوم
        for theme in themes2:
            btn = ttk.Button(
                col2,
                text=theme,
                command=lambda t=theme: self.change_theme(t),
                bootstyle="light",
                width=12
            )
            btn.pack(pady=7, padx=3, fill=tk.X)

        # ایجاد دکمه‌ها برای ستون سوم
        for theme in themes3:
            btn = ttk.Button(
                col3,
                text=theme,
                command=lambda t=theme: self.change_theme(t),
                bootstyle="light",
                width=12
            )
            btn.pack(pady=7 , padx=3, fill=tk.X)

        return panel

    def show_panel(self, panel):
        """نمایش پنل مورد نظر در container"""
        for widget in self.container.winfo_children():
            widget.pack_forget()

        panel.pack(fill=tk.BOTH, expand=True)
        self.panel_stack.append(panel)

    def change_theme(self, theme):
        """تغییر تم برنامه"""
        self.root.style.theme_use(theme)
        self.theme_var = theme
        print(text_manager.get_text("theme_changed", self.language_var).format(theme))
        self.show_panel(self.settings_panel)

    def update_gender(self, value):
        """به‌روزرسانی جنسیت"""
        self.gender_var = value
        self.update_language_models()
        self.update_title()
        update_choice(value)
        
        voice_name = text_manager.get_text("male_voice", self.language_var) if value == 0 else text_manager.get_text("female_voice", self.language_var)
        print(text_manager.get_text("voice_selected", self.language_var).format(voice_name))

    def update_language(self, language):
        """به‌روزرسانی زبان"""
        self.language_var = language
        self.update_language_models()
        self.update_title()
        self.update_window_title()
        
        # به‌روزرسانی تمام عناصر UI
        self.update_all_ui_text()
        
        lang_name = "فارسی" if language == "fa" else "English"
        print(text_manager.get_text("language_selected", self.language_var).format(lang_name))

    def update_all_ui_text(self):
        """به‌روزرسانی تمام عناصر UI در همه پنل‌ها"""
        # به‌روزرسانی پنل اصلی
        self.start_btn.config(text=text_manager.get_text("start_btn", self.language_var))
        self.stop_btn.config(text=text_manager.get_text("stop_btn", self.language_var))
        self.exit_btn.config(text=text_manager.get_text("exit_btn", self.language_var))
        self.settings_btn.config(text=text_manager.get_text("settings_btn", self.language_var))
        
        # به‌روزرسانی وضعیت
        if self.assistant_active:
            self.status_var.set(text_manager.get_text("status_active", self.language_var))
        else:
            self.status_var.set(text_manager.get_text("status_ready", self.language_var))
        
        self.lang_status_var.set(text_manager.get_text("language_label", self.language_var))
        
        # به‌روزرسانی LabelFrame‌ها با استفاده از config
        self.console_frame.config(text=text_manager.get_text("console_title", self.language_var))
        
        # به‌روزرسانی پنل تنظیمات
        self.back_btn_settings.config(text=text_manager.get_text("back_btn", self.language_var))
        self.settings_title.config(text=text_manager.get_text("settings_title", self.language_var))
        self.settings_console_frame.config(text=text_manager.get_text("help_title", self.language_var))
        self.selection_frame.config(text=text_manager.get_text("language_selection", self.language_var))
        self.lang_label.config(text=" : "+text_manager.get_text("language_text", self.language_var))
        self.voice_label.config(text=" : "+text_manager.get_text("voice_text", self.language_var))
        self.male_btn.config(text=text_manager.get_text("male_voice", self.language_var))
        self.female_btn.config(text=text_manager.get_text("female_voice", self.language_var))
        self.theme_btn.config(text=text_manager.get_text("theme_btn", self.language_var))
        
        # به‌روزرسانی پنل تم
        self.back_btn_theme.config(text=text_manager.get_text("back_btn", self.language_var))
        self.theme_title.config(text=text_manager.get_text("theme_title", self.language_var))
        
        # به‌روزرسانی راهنما
        self.update_help_text()

    def start_assistant(self):
        """شروع دستیار - ساختار اصلی"""
        if not self.assistant_active:
            self.assistant_active = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.status_var.set(text_manager.get_text("status_active", self.language_var))
                
            self.assistant_thread = threading.Thread(target=self.run_assistant, daemon=True)
            self.assistant_thread.start()
            
            print(text_manager.get_text("assistant_activated", self.language_var))

    def stop_assistant(self):
        """توقف دستیار - ساختار اصلی"""
        if self.assistant_active:
            self.assistant_active = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            
            self.status_var.set(text_manager.get_text("status_stopped", self.language_var))
            print(text_manager.get_text("assistant_stopped", self.language_var))

    def run_assistant(self):
        """اجرای دستیار - ساختار اصلی و کارآمد"""
        start_recording()
        rec = None
        last_model = None  # برای تشخیص تغییر مدل

        while self.assistant_active:
            try:
                # 🔁 اگر مدل تغییر کرده، recognizer را دوباره بساز
                if last_model != current_model:
                    rec = vosk.KaldiRecognizer(current_model, 16000)
                    last_model = current_model

                data = q.get(timeout=1.0)
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    text = json.loads(result)["text"]
                    if text.strip():  # جلوگیری از رشته‌های خالی
                        stop_recording()
                        execute_command(text, self.language_var)
                        if self.assistant_active:
                            time.sleep(1)
                            start_recording()
            except queue.Empty:
                continue
            except Exception as e:
                if self.language_var == "fa":
                    print(f"خطا در پردازش صدا: {str(e)}")
                else:
                    print(f"Error in voice processing: {str(e)}")
                if self.assistant_active:
                    time.sleep(1)
                    start_recording()

        stop_recording()

    def on_close(self):
        """ذخیره تنظیمات قبل از خروج"""
        self.assistant_active = False

        if hasattr(self, "assistant_thread") and self.assistant_thread and self.assistant_thread.is_alive():
            self.assistant_thread.join(timeout=1.0)

        save_settings(self.gender_var, self.theme_var, self.language_var)
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = AssistantGUI()