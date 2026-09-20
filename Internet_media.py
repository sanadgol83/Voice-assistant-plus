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


load_dotenv()

LLM7_API_KEY = os.getenv("LLM7_API_KEY")

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")

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
        replacements = {'nola':'','enola':'','alex':'','translate':'','بارسا':'','پارسا': '','رویا': '', 'انگلیسی': '', "ترجمه": "", "ترنسلیت": ""}

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
    elif x == 5:
        translator(command,y)

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

def artificial(query, y):

    headers = {
        "Authorization": f"Bearer {LLM7_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {
            "role": "system",
            "content": """شما یک هوش مصنوعی کارآمد هستی هر کلمه ای که بهت دادم در رابطه باهاش تحقیق کن و خلاصه تحقیقت رو بدون توضیح اضافه
            بهم بده به همون زبونی که موضوع رو بهت دادم بهم خروجی بد مثلا اگه موضوع انگلیسی بود جوابش انگلیسی کن و اگه فارسی بود فارسی جوابش رو بده."""
        }
    ]

    user_input = query
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": "default",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(
            "https://api.llm7.io/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            ai_reply = data["choices"][0]["message"]["content"]

            if y == 1:
                print(": هوش مصنوعی", f"{ai_reply}\n")
                asyncio.run(stream_audio(ai_reply))
            else:
                print(": artificial ", f"{ai_reply}\n")
                speak(ai_reply)

            messages.append({
                "role": "assistant",
                "content": ai_reply
            })

        else:
            print(f"\nخطا: {response.status_code} - {response.text}\n")

    except Exception as e:
        print(f"\nخطا در ارتباط با سرور: {str(e)}\n")

def c_photo(
    query,
    y,
    model="lykon/dreamshaper-8-lcm",
    width=1024,
    height=1024,
    seed=None,
    enhance=True,
    logo=False
):
    encoded_prompt = urllib.parse.quote(query)

    api_url = f"https://gen.pollinations.ai/image/{encoded_prompt}"

    headers = {
        "Authorization": f"Bearer {POLLINATIONS_API_KEY}"
    }

    if seed is None:
        seed = random.randint(1, 500)

    params = {
        "model": model,
        "width": width,
        "height": height,
        "seed": seed,
        "enhance": enhance,
        "logo": logo
    }

    try:
        response = requests.get(
            api_url,
            headers=headers,
            params=params,
            stream=True
        )

        response.raise_for_status()

        image = Image.open(BytesIO(response.content))

        home_dir = os.path.expanduser("~")
        pictures_dir = os.path.join(
            home_dir,
            "Pictures",
            "p_ai_photo"
        )

        os.makedirs(pictures_dir, exist_ok=True)

        filename = f"screen_{time.strftime('%Y%m%d_%H%M%S')}.png"
        full_path = os.path.join(pictures_dir, filename)

        image.show(title="Generated Image")
        image.save(full_path)

        # خروجی متنی و صوتی
        if y == 1:
            result = f"عکس {query} با استفاده از هوش مصنوعی ساخته شد."
            print(": هوش مصنوعی", f"{result}\n")
            asyncio.run(stream_audio(result))

        else:
            result = f"I generated a photo of {query} with artificial intelligence."
            print(": artificial", f"{result}\n")
            speak(result)

        print(f"{full_path} : عکس ذخیره شد")

    except Exception as e:
        print(f"❌ خطا در تولید تصویر: {e}")

def translator(query,y):
    if y==1:
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
