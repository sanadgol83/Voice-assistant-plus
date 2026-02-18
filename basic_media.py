import screen_brightness_control as sbc
from datetime import datetime
from PIL import ImageGrab
from utils import *
import pygetwindow as gw
import pyautogui
import ctypes
from ctypes import wintypes
import time
import os
import asyncio



def chrome(x):
    os.startfile("Chrome")
    if x==1:
        print('...💻کروم باز کردم...')
        asyncio.run(stream_audio("برنامه کروم رو باز کردم"))
    else:
        print('...💻i opened the chrome expelor...')
        speak("i opened the chrome expelor")

def firefox(x):
    os.startfile("Firefox")
    if x==1:
        print('...🦊فایرفاکس باز کردم...')
        asyncio.run(stream_audio("برنامه فایرفاکس رو باز کردم"))
    else:
        print('...🦊i opened the firefox expelor...')
        speak("i opened the firefox expelor")

def word(x):
    os.startfile("winword")
    if x==1:
        print('...🧩ورد باز کردم...')
        asyncio.run(stream_audio("برنامه ورد رو باز کردم"))
    else:
        print('...🧩i opened the word office...')
        speak("i opened the word office")
    
def point(x):
    os.startfile("powerpnt")
    if x==1:
        print('...🧩پاور پوینت باز کردم...')
        asyncio.run(stream_audio("برنامه پاورپوینت رو باز کردم"))
    else:
        print('...🧩i opened the power point office...')
        speak("i opened the power point office")
    
def excel(x):
    os.startfile("excel")
    if x==1:
        print('...🧩اکسل باز کردم...')
        asyncio.run(stream_audio("برنامه اکسل رو باز کردم"))
    else:
        print('...🧩i opened the excel office...')
        speak("i opened the excel office")
    
    

def notebook(command,x):
    replacements = {'nola':'','enola':'','alex':'','text':'', 'notepad':'', 'note':'', 'notebook':'', 'write':'',
                    'بارسا':'','پارسا': '','رویا': '', 'متن': '', 'یادداشت': '', "یاداشت": "", "دفترچه": ""}
    for old, new in replacements.items():
        command = command.replace(old, new)

    home_dir = os.path.expanduser("~")
    notebook_dir = os.path.join(home_dir, "Documents", "p_notebook")
    
    # ایجاد پوشه در صورت عدم وجود
    os.makedirs(notebook_dir, exist_ok=True)
    
    # ایجاد نام فایل با زمان
    filename = f"note_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    file_path = os.path.join(notebook_dir, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(command)
    if x==1:
        print(f"{file_path} : یاد داشت ذخیره شد")
        asyncio.run(stream_audio("یادداشتتو ذخیره کردم برات"))
    else:
        print(f"{file_path} : your note saved in")
        speak("i saved the note for you")

def this_pc(x):
    os.startfile("::{20D04FE0-3AEA-1069-A2D8-08002B30309D}")
    if x == 1:
        print('...🧷 دیس پی سی باز کردم...')
        asyncio.run(stream_audio("دیس پی سی رو باز کردم"))
    else:
        print('...🧷 i opened the this pc...')
        speak("i opened the this pc")

def settings(x):
    os.startfile("ms-settings:")
    if x == 1:
        print('...⚙️ تنظیمات باز کردم...')
        asyncio.run(stream_audio("تنظیمات رو باز کردم"))
    else:
        print('...⚙️ i opened the settings...')
        speak("i opened the settings")

def off(x):
    if x == 1:
        print('...خداحافظی...')
        asyncio.run(stream_audio("خداحافظ رفیق"))
    else:
        print('...Goodbye...')
        speak("Goodbye bro")
    os.system("shutdown /s /t 1")

def rest(x):
    if x == 1:
        print('...ریستارت کردم...')
        asyncio.run(stream_audio("دوباره برمیگردم"))
    else:
        print('...Restarting...')
        speak("I am come back now")
    os.system("shutdown /r /t 1")

def timex(x):
    time = datetime.now().strftime("%H:%M")
    if x == 1:
        print(f'🕰 زمان: {time}')
        asyncio.run(stream_audio(time))
    else:
        print(f'🕰 Time: {time}')
        speak(str(time))

def play(x):
    pyautogui.press('playpause')
    if x == 1:
        print('...▶ پخش کردم...')
        asyncio.run(stream_audio("پخش رو شروع کردم"))
    else:
        print('...▶ playback started...')
        speak("i started the case")

def stop(x):
    pyautogui.press('playpause')
    if x == 1:
        print('...⏸ توقف کردم...')
        asyncio.run(stream_audio("توقف کردم"))
    else:
        print('...⏸ playback stopped...')
        speak("i stopped the playback")

def gl(x):
    pyautogui.press('prevtrack')
    if x == 1:
        print('...⏮ قبلی رو زدم...')
        asyncio.run(stream_audio("مدیای قبلی"))
    else:
        print('...⏮ previous track...')
        speak("i clicked on the previous item")

def bl(x):
    pyautogui.press('nexttrack')
    if x == 1:
        print('...⏭ بعدی رو زدم...')
        asyncio.run(stream_audio("مدیای بعدی"))
    else:
        print('...⏭ next track...')
        speak("i clicked to go to next item")

def unmute(x):
    pyautogui.press('volumemute')
    if x == 1:
        print('...🎶 صدا رو باز کردم...')
        asyncio.run(stream_audio("صدا رو فعال کردم"))
    else:
        print('...🎶 unmuted...')
        speak("i unmuted the volume")

def mute(x):
    pyautogui.press('volumemute')
    if x == 1:
        print('...🔈 صدا رو قطع کردم...')
        asyncio.run(stream_audio("صدا رو قطع کردم"))
    else:
        print('...🔈 muted...')
        speak("i muted the volume")

def kam(x):
    for _ in range(10):
        pyautogui.press('volumedown')
    if x == 1:
        print('...🔉 صدا رو کم کردم...')
        asyncio.run(stream_audio("صدا رو کم کردم"))
    else:
        print('...🔉 volume decreased...')
        speak("i turned down the volume")

def ziad(x):
    for _ in range(10):
        pyautogui.press('volumeup')
    if x == 1:
        print('...🔊 صدا رو زیاد کردم...')
        asyncio.run(stream_audio("صدا رو زیاد کردم"))
    else:
        print('...🔊 volume increased...')
        speak("i turned up the volume")

def n_kam(x):
    current_list = sbc.get_brightness()
    current = current_list[0]
    new_brightness = max(0, current - 10)
    sbc.set_brightness(new_brightness)
    if x == 1:
        print('...🔆 روشنایی کم کردم...')
        asyncio.run(stream_audio(f"روشنایی رو کم کردم به {new_brightness} درصد"))
    else:
        print('...🔆 i dimmed the brightness...')
        speak(f"i dimmed the brightness to {new_brightness} percent")

def n_ziad(x):
    current_list = sbc.get_brightness()
    current = current_list[0]
    new_brightness = min(current + 10, 100)
    sbc.set_brightness(new_brightness)
    if x == 1:
        print('...🌟 روشنایی زیاد کردم...')
        asyncio.run(stream_audio(f"روشنایی رو زیاد کردم به {new_brightness} درصد"))
    else:
        print('...🌟 i increased the brightness...')
        speak(f"i increased the brightness to {new_brightness} percent")

def maximize_current_window(x):
    try:
        active_window = gw.getActiveWindow()
        
        if (active_window and 
            active_window.title.strip() != "" and 
            "Program Manager" not in active_window.title):
            active_window.maximize()
            if x == 1:
                print('...👀 پنجره بزرگ کردم...')
                asyncio.run(stream_audio("پنجره رو بزرگ کردم"))
            else:
                print('...👀 window maximized...')
                speak("i enlarged the window")
        else:
            if x == 1:
                print('...پنجره ای پیدا نشد...')
                asyncio.run(stream_audio("پنجره ای برای بزرگ کردن پیدا نکردم"))
            else:
                print('...no window found...')
                speak("i did not find a window to enlarge")

    except Exception as e:
        if x == 1:
            return f"خطا: {e}"
        else:
            return f"Error: {e}"

def minimize_current_window(x):
    try:
        active_window = gw.getActiveWindow()
        
        if (active_window and 
            active_window.title.strip() != "" and 
            "Program Manager" not in active_window.title):
            active_window.minimize()
            if x == 1:
                print('...🐜 پنجره کوچیک کردم...')
                asyncio.run(stream_audio("پنجره رو کوچک کردم"))
            else:
                print('...🐜 window minimized...')
                speak("i minimized the window")
        else:
            if x == 1:
                print('...پنجره ای پیدا نشد...')
                asyncio.run(stream_audio("پنجره ای برای کوچک کردن پیدا نکردم"))
            else:
                print('...no window found...')
                speak("i did not find a window to minimize")

    except Exception as e:
        if x == 1:
            return f"خطا: {e}"
        else:
            return f"Error: {e}"

def close_current_window(x):
    try:
        pyautogui.hotkey('alt', 'f4')
        if x == 1:
            print('...🤐 پنجره برات بستم...')
            asyncio.run(stream_audio("پنجره رو بستم"))
        else:
            print('...🤐 window closed...')
            speak("i closed the window")
    except Exception as e:
        if x == 1:
            return f"خطا: {e}"
        else:
            return f"Error: {e}"

def restore_window(x):
    """آخرین پنجره مینیمایز شده را بازیابی می‌کند"""
    try:
        # گرفتن تمام پنجره‌ها
        all_windows = gw.getAllWindows()
        
        # فیلتر کردن پنجره‌های مینیمایز شده و معتبر
        minimized_windows = []
        for w in all_windows:
            if (w.isMinimized and 
                w.title.strip() != "" and 
                "Program Manager" not in w.title):
                minimized_windows.append(w)
        
        if minimized_windows:
            target_window = minimized_windows[-1]  # آخرین پنجره مینیمایز شده
            
            # بازیابی و فعال کردن پنجره
            target_window.restore()
            time.sleep(0.2)  # تاخیر کوتاه
            target_window.activate()
            time.sleep(0.3)
            
            if x == 1:
                print(f'...🔄 پنجره بازیابی شد: {target_window.title} ...')
                asyncio.run(stream_audio("پنجره بازیابی شد"))
            else:
                print(f'...🔄 window restored: {target_window.title} ...')
                speak(f"window {target_window.title} restored")
        else:
            if x == 1:
                print('...پنجره مینیمایز شده‌ای پیدا نشد...')
                asyncio.run(stream_audio("پنجره کوچک شده ای پیدا نکردم"))
            else:
                print('...no minimized window found...')
                speak("no minimized window found")
            
    except Exception as e:
        if x == 1:
            print(f"خطا در بازیابی پنجره: {e}")
        else:
            print(f"Error restoring window: {e}")

def screen(x):
    if x == 1:
        print('...📷 اسکرین شات گرفتم...')
        asyncio.run(stream_audio("از صفحه عکس گرفتم"))
    else:
        print('...📷 screenshot taken...')
        speak("i took a screenshot")
    
    # مسیر پوشه Pictures کاربر
    home_dir = os.path.expanduser("~")
    pictures_dir = os.path.join(home_dir, "Pictures", "p_screen")
    
    # ایجاد پوشه در صورت عدم وجود
    os.makedirs(pictures_dir, exist_ok=True)
    
    # ایجاد نام فایل با زمان
    filename = f"screen_{time.strftime('%Y%m%d_%H%M%S')}.png"
    full_path = os.path.join(pictures_dir, filename)
    
    if x == 1:
        print(f"{full_path} : عکس ذخیره شد")
    else:
        print(f"{full_path} : image saved")

    # گرفتن و ذخیره اسکرین‌شات
    screenshot = ImageGrab.grab()
    screenshot.show()
    screenshot.save(full_path)

