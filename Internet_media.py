from googletrans import Translator
import wikipedia
import webbrowser
from utils import *
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import urllib.parse
import time
import random
import platform
import speedtest
import asyncio
from dotenv import load_dotenv


def internet(command,x,y):
    if x == 1 :
        replacements = {'nola':'','enola':'','alex':'','article':'','of':'','بارسا':'','پارسا': '','رویا': '','ریکی':'', 'پدیا': '', 'ویکی': '', 'ویکی‌پدیا': ''}
    elif x == 2 :
        replacements = {'nola':'','enola':'','alex':'','search':'','research':'','بارسا':'','پارسا': '','رویا': '', 'جستجو': '', 'تحقیق': ''}
    elif x == 3 :
        replacements = {'nola':'','enola':'','alex':'','بارسا':'','پارسا': '','رویا': '','هوش':'','مصنوعی': '', "هوش مصنوعی": "", "هوش‌مصنوعی": ""}
    elif x == 4 :
        replacements = {'nola':'','enola':'','alex':'','generate':'', 'image':'', 'create':'', 'photo':'', 'picture':'','بارسا':'','پارسا': '','رویا': '', 'عکس': '', 'تولید': '', "تولید‌عکس": ""}
    elif x == 5 :
        replacements = {'nola':'','enola':'','alex':'','بارسا':'','پارسا': '','رویا': '', 'انگلیسی': '', "ترجمه": "", "ترنسلیت": ""}

    for old, new in replacements.items():
        command = command.replace(old, new)
    if x == 1:
        search_wikipedia(command,y)
    elif x == 2:
        search_browser(command,y)
    elif x == 3:
        artificial(command,y)
    elif x == 4:
        c_photo(command,y)
    #elif x == 5:
    #    translator(command,y)

wikipedia.set_lang("fa")

def search_wikipedia(query,y):
    try:
        # دریافت خلاصه مقاله
        summary = wikipedia.summary(query, sentences=4)
        page = wikipedia.page(query)
        if y==1:
            print(f"خلاصه مقاله '{query}':\n{summary}\n")
            print(f"لینک کامل مقاله: {page.url}")
            asyncio.run(stream_audio(summary))
        else:
            translator = Translator()
            text_fa = summary
            translation = translator.translate(text_fa, src='fa', dest='en')
            print(translation.text)
            print(f"url link : {page.url}")
            speak(translation.text)

    except wikipedia.exceptions.DisambiguationError as e:
        print(f"چندین معنی ممکن دارد: {e.options}")
    except wikipedia.exceptions.PageError:
        print("مقاله‌ای با این عنوان یافت نشد.")
    except Exception as e:
        print(f"خطا: {str(e)}")

def search_browser(query,y):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    if y==1:
        print(f"...جستجو کردم درمورد {query} در جستجوگر...")
        asyncio.run(stream_audio(f"در جستجوگر جستجو کردم در رابطه با {query}"))
    else:
        print(f"...i search about {query} in browser...")    
        speak(f"i search about {query} in browser")

def artificial(query,y):
    load_dotenv()
    api_key = os.getenv("API_KEY", "")
    model = os.getenv("MODEL", "google/gemma-3-27b-it")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "content":""" شما یک هوش مصنوعی کار آمد هستی هر کلمه ای که بهت دادم در رابطه باهاش تحقیق کن و خلاصه تحقیقت رو بدون توضیح اضافه 
         بهم بده به همون زبونی که موضوع رو بهت دادم بهم خروجی بد مثلا اگه موض.ع انگلیسی جوابش انگیسی کن."""}
    ]
    user_input = query
    messages.append({"role": "user", "content": user_input})
    payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }
    
    try:
        # ارسال درخواست به OpenRouter API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
            
        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            data = response.json()
            ai_reply = data['choices'][0]['message']['content']
            if y==1:
                print(": هوش مصنوعی",f"{ai_reply}\n")
                asyncio.run(stream_audio(ai_reply))
            else:
                print(": artificial ",f"{ai_reply}\n")
                speak(ai_reply)
            # افزودن پاسخ به تاریخچه
            messages.append({"role": "assistant", "content": ai_reply})
        else:
            print(f"\nخطا: {response.status_code} - {response.text}\n")
        
    except Exception as e:
        print(f"\nخطا در ارتباط با سرور: {str(e)}\n")

def c_photo(
    query,
    model="turbo",
    width=1024,
    height=1024,
    seed=random.randint(1, 500),
    enhance=True,
    logo=False
):
    encoded_prompt = urllib.parse.quote(query)
    api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?" \
          f"model={model}&width={width}&height={height}&seed={seed}&enhance={enhance}&logo={logo}"
    try:
        # ارسال درخواست GET
        response = requests.get(api_url, stream=True)
        response.raise_for_status()  # بررسی خطاهای HTTP
        
        # تبدیل پاسخ به تصویر
        image = Image.open(BytesIO(response.content))
        
        home_dir = os.path.expanduser("~")
        pictures_dir = os.path.join(home_dir, "Pictures", "p_ai_photo")
    
    # ایجاد پوشه در صورت عدم وجود
        os.makedirs(pictures_dir, exist_ok=True)
    
    # ایجاد نام فایل با زمان
        filename = f"screen_{time.strftime('%Y%m%d_%H%M%S')}.png"
        full_path = os.path.join(pictures_dir, filename)

        # نمایش تصویر
        image.show(title="Generated Image")
        
        # ذخیره تصویر (اختیاری)
        image.save(full_path)
        print(f"{full_path} : عکس ذخیره شد")
        
        translator = Translator()
        text_fa = query
        translation = translator.translate(text_fa, src='fa', dest='en')
        speak(f"I generated a photo of a {translation.text} with artificial intelligence")

    except Exception as e:
        print(f"❌ خطا در تولید تصویر: {e}")

def translator(query,x):
    if x==1:
        translator = Translator()
        translation = translator.translate(query, src='fa', dest='en')
        print(translation.text)
        speak(translation.text)
    else:
        translator = Translator()
        translation = translator.translate(query, src='en', dest='fa')
        print(translation.text)
        asyncio.run(stream_audio(translation.text))

def mony(x):
    url1 = 'https://www.tgju.org/profile/geram18'
    response1 = requests.get(url1)

    soup = BeautifulSoup(response1.text, 'html.parser')
    for h3 in soup.find_all('h3'):
        if 'نرخ فعلی' in h3.get_text():
            text1 = h3.get_text()

    url2 = 'https://www.tgju.org/profile/price_dollar_rl'
    response2 = requests.get(url2)

    soup = BeautifulSoup(response2.text, 'html.parser')
    for h3 in soup.find_all('h3'):
        if 'نرخ فعلی' in h3.get_text():
            text2 = h3.get_text()

    replacements1 = {'نرخ فعلی: :':': قیمت روز طلا ۱۸ عیار'}
    replacements2 = {'نرخ فعلی: :': ': قیمت روز دلار'}
    for old, new in replacements1.items():
        command1 = text1.replace(old, new)
        break
    for old, new in replacements2.items():
        command2 = text2.replace(old, new)
        break
    index1 , index2 = 35 , 27
    result1 = command1[:index1]
    result2 = command2[:index2]
    if x==1:
        print(result1,result2)
        asyncio.run(stream_audio(result1+result2))
    else:
        result = result1+result2
        translator = Translator()
        text_fa = result
        translation = translator.translate(text_fa, src='fa', dest='en')
        print(translation.text)
        speak(translation.text)

def check_internet(x):
   # بررسی همزمان اتصال و سرعت اینترنت و گزارش نتیجه
    if x==1:
        print("...🚦در حال بررسی کمی صبر کنید...")
    else:
        print("...🚦Please wait while checking...")
    # بررسی اتصال
    try:
        if platform.system().lower() == "windows":
            response = os.system("ping -n 1 8.8.8.8 > nul 2>&1")
        else:
            response = os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1")
        
        is_connected = response == 0
    except:
        is_connected = False

    # بررسی سرعت اگر اتصال برقرار باشد
    speed_result = {'success': False}
    if is_connected:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            
            download = round(st.download() / 1_000_000, 2)
            upload = round(st.upload() / 1_000_000, 2)
            ping = round(st.results.ping, 2)
            
            speed_result = {
                'download': download, 
                'upload': upload, 
                'ping': ping, 
                'success': True
            }
        except:
            speed_result = {'success': False}

    # گزارش نتیجه
    if is_connected:
        if speed_result['success']:
            if x==1:
                print(f"{speed_result['ping']}ms آنلاین هستید و پینگ شما")
                print(f"{speed_result['download']}Mbps سرعت دانلود")
                print(f"{speed_result['upload']}Mbps سرعت آپلود")
                asyncio.run(stream_audio(f"پینگ شما {speed_result['ping']} میلی‌ثانیه، سرعت دانلود {speed_result['download']} مگابیت بر ثانیه، سرعت آپلود {speed_result['upload']} مگابیت بر ثانیه است"))
            else:
                print(f"You are online with {speed_result['ping']}ms ping")
                print(f"{speed_result['download']}Mbps download speed")
                print(f"{speed_result['upload']}Mbps upload speed")
                speak(f"You are online Ping {speed_result['ping']} milliseconds, Download {speed_result['download']} megabits per second, Upload {speed_result['upload']} megabits per second")
        else:
            print("✅ آنلاین هستید! (سرعت اینترنت قابل اندازه‌گیری نبود)")
            speak("You are online but internet speed could not be measured")
    else:
        print("❌ آنلاین نیستید! اتصال اینترنت قطع است.")
        speak("You are offline No internet connection")
