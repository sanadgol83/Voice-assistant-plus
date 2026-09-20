# 🎤 Parsino — Intelligent Bilingual Voice Assistant

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=flat-square&logo=github)](https://github.com/sanadgol83/Voice-assistant-plus)
[![Python](https://img.shields.io/badge/Python-3.10.11-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**Parsino** is a bilingual Persian/English desktop voice assistant built with Python. It combines speech recognition, text-to-speech, system automation, web services, AI, image generation, webcam features, and a customizable graphical interface in a single application.

[English](#english) · [فارسی](#فارسی)

---

<a name="english"></a>

# 🇬🇧 English

## 🎤 About Parsino

Parsino is a Windows-focused voice assistant designed to control everyday computer tasks through natural Persian or English voice commands.

The project supports:

- 🎤 Persian and English speech recognition
- 🔊 Bilingual voice responses
- 🤖 AI-powered text responses
- 🎨 AI image generation
- 💻 Application and system control
- 🌐 Web and Wikipedia search
- 📷 Webcam photo and video features
- 🎵 Media control
- 🪟 Window management
- 📝 Text notes
- 💰 Gold and currency information
- 🎨 A customizable GUI with multiple themes

---

## ✨ Features

### 🎤 Voice & Language

- Persian and English voice commands
- Multiple wake words:
  - Persian: `پارسا`, `رویا`
  - English: `Alex`, `Enola`
- Vosk-based speech recognition
- Bilingual text-to-speech responses
- Different response paths for Persian and English commands

### 🤖 AI Features

Parsino can communicate with an AI model through the **LLM7 OpenAI-compatible API**.

The AI integration can:

- Answer questions and provide short explanations
- Respond in Persian or English according to the input language
- Produce both written and spoken responses
- Use the `default` LLM7 model configuration

### 🎨 AI Image Generation

Parsino can generate images from voice commands through the **Pollinations image API**.

Generated images can be:

- Displayed immediately
- Saved automatically in the user's Pictures directory
- Accompanied by a Persian or English spoken/text response according to the command language

### 💻 Computer Control

Examples include:

- Open applications such as Chrome, Firefox, Word, PowerPoint, and Excel
- Control system volume
- Adjust screen brightness
- Manage application windows
- Shutdown and restart the system
- Open system settings

### 🌐 Internet Features

- Wikipedia search
- Web search
- AI requests
- AI image generation
- Translation

### 📷 Webcam

- Take photos
- Record videos
- Record video with audio

### 📝 Productivity

- Create and save text notes
- Read system information
- Display time and other system information

---

## 🧠 Architecture Overview

Parsino is organized around several functional modules:

```text
Voice Command
     │
     ▼
Speech Recognition (Vosk)
     │
     ▼
Command Detection & Language Detection
     │
     ├── System / Application Control
     ├── Media Control
     ├── Web / Wikipedia
     ├── AI → LLM7 API
     ├── Image Generation → Pollinations API
     ├── Webcam
     └── Other Utilities
              │
              ▼
       Text + Voice Response
```

---

## 📋 Requirements

### ⚠️ Python Version

**Python 3.10.11 is the recommended and tested Python version for this project.**

The project's dependencies and current implementation are based on Python 3.10.11. Other Python versions may require dependency or code adjustments.

### System Requirements

| Requirement | Details |
|---|---|
| OS | Windows 10 / Windows 11 |
| Python | **3.10.11** |
| RAM | 2 GB minimum; more is recommended |
| Microphone | Required for voice commands |
| Internet | Required for AI, web search, translation, image generation, and other online services |
| Webcam | Optional; required only for webcam features |

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sanadgol83/Voice-assistant-plus.git
cd Voice-assistant-plus
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

It is recommended to verify the Python version after activating the environment:

```bash
python --version
```

Expected:

```text
Python 3.10.11
```

---

## 🎙️ 4. Install Vosk Models

Parsino uses Vosk for speech recognition.

Download the required models from:

[Vosk Models](https://alphacephei.com/vosk/models)

Place the required model folders in the project root:

```text
vosk-model-small-fa-0.5/
vosk-model-small-en-us-0.15/
```

The Persian model is used for Persian speech recognition and the English model is used for English speech recognition.

---

## 🔐 5. Configure API Keys

Some Parsino features use external APIs. **API keys should never be hard-coded into Python files or committed to GitHub.**

Create a file named:

```text
.env
```

in the project root.

Example:

```env
LLM7_API_KEY=your_llm7_api_key_here
POLLINATIONS_API_KEY=your_pollinations_api_key_here
```

### LLM7 API

The AI assistant uses the LLM7 OpenAI-compatible chat completion endpoint:

```text
https://api.llm7.io/v1/chat/completions
```

The current implementation uses:

```text
model = default
```

The `LLM7_API_KEY` variable is read from `.env`.

### Pollinations API

AI image generation uses the Pollinations image endpoint:

```text
https://gen.pollinations.ai/image/
```

The `POLLINATIONS_API_KEY` variable is read from `.env`.

### Important Security Note

Do **not** upload `.env` to GitHub.

Add these entries to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

If an API key is accidentally exposed publicly, revoke/rotate it from the corresponding service as soon as possible.

---

## ▶️ Running Parsino

After activating the virtual environment:

```bash
python Parsino.py
```

Start the assistant from the application interface and use one of the supported wake words.

---

## 🗣️ Voice Commands

### English

```text
Alex open chrome
Alex volume up
Alex wikipedia python
Alex generate an image of a cat on the moon
Alex take photo
```

### Persian

```text
پارسا کروم باز کن
پارسا صدا زیاد کن
پارسا ویکی پدیا پایتون
پارسا عکس یک گربه روی ماه تولید کن
پارسا عکس بگیر
```

The exact available commands depend on the command definitions implemented in the project.

---

## 🖼️ AI Image Generation

The image-generation function accepts a language/output parameter so that the response can be returned in the appropriate language.

Conceptually:

```text
Persian command
     │
     ▼
Image generation
     │
     ├── Generated image
     ├── Written response
     └── Persian voice response
```

and:

```text
English command
     │
     ▼
Image generation
     │
     ├── Generated image
     ├── Written response
     └── English voice response
```

Generated images are saved under:

```text
%USERPROFILE%\Pictures\p_ai_photo\
```

---

## 🤖 AI Response Flow

Parsino sends the user's request to LLM7 and receives the generated response.

The response is then handled according to the selected language/output path:

```text
User command
     │
     ▼
LLM7 API
     │
     ▼
AI response
     │
     ├── Printed text
     └── Voice output
```

The AI system prompt instructs the model to respond in the same language as the user's request.

---

## 📁 Project Structure

```text
Parsino/
│
├── Parsino.py                  # Main application
├── basic_media.py              # System and media controls
├── Internet_media.py            # Internet, AI, search, translation, image generation
├── webcam_media.py              # Webcam photo/video functionality
├── utils.py                     # Utility functions, TTS, settings, etc.
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── LICENSE                      # MIT License
├── .env                         # Local API keys (DO NOT COMMIT)
│
├── vosk-model-small-fa-0.5/     # Persian Vosk model
└── vosk-model-small-en-us-0.15/ # English Vosk model
```

---

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python 3.10.11 | Main programming language |
| Vosk | Speech recognition |
| Tkinter | Graphical user interface |
| ttkbootstrap | UI themes |
| Edge TTS | Text-to-speech |
| OpenCV | Webcam and computer vision |
| MoviePy | Video processing |
| BeautifulSoup | Web data extraction |
| Requests | HTTP/API communication |
| PyAutoGUI | Desktop automation |
| LLM7 | AI text generation |
| Pollinations | AI image generation |

---

## ⚙️ Configuration

Parsino stores application settings in:

```text
%APPDATA%\Parsino\config.json
```

Depending on the current implementation, configurable options include:

- Language
- Voice gender
- UI theme
- Other application preferences

The project currently includes multiple UI themes.

---

## 🐛 Troubleshooting

### Microphone is not detected

- Check Windows microphone permissions.
- Make sure the correct microphone is selected.
- Check that the microphone works in another application.

### Vosk model not found

Make sure the model folders are located in the project root:

```text
vosk-model-small-fa-0.5
vosk-model-small-en-us-0.15
```

You can download them from:

[Vosk Models](https://alphacephei.com/vosk/models)

### API request fails

Check:

1. Your internet connection.
2. The API key in `.env`.
3. That the `.env` file is located in the project root.
4. That the environment variable name is exactly:

```text
LLM7_API_KEY
POLLINATIONS_API_KEY
```

Do not add quotation marks unless your configuration specifically requires them.

### Import / dependency errors

Make sure the virtual environment is active and reinstall dependencies:

```bash
python -m pip install -r requirements.txt --force-reinstall
```

Then verify:

```bash
python --version
```

---

## 🔒 Security

Parsino uses API credentials for external services.

For safe GitHub usage:

- Never commit `.env`
- Never place API keys directly in `.py` files
- Never publish screenshots containing active API keys
- Rotate an exposed key immediately
- Keep private credentials outside the repository

A safe repository should contain a template such as:

```env
LLM7_API_KEY=
POLLINATIONS_API_KEY=
```

for example in `.env.example`, while the real `.env` remains local.

---

## 👨‍💻 Developer

**Mohammad Sanadgol**

- GitHub: [@sanadgol83](https://github.com/sanadgol83)
- Repository: [Voice-assistant-plus](https://github.com/sanadgol83/Voice-assistant-plus)
- Project start: 2025
- Current documented version: **3.2.7**

---

## 📝 License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) for the complete license text.

---

## 🤝 Contributing

Contributions are welcome.

You can:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the project
5. Open a Pull Request

For bugs and feature requests, open an Issue on GitHub.

---

## 📧 Support

For bugs, questions, and suggestions:

[Open an Issue](https://github.com/sanadgol83/Voice-assistant-plus/issues)

---

## 🙏 Acknowledgments

- [Vosk](https://alphacephei.com/vosk/) — Speech recognition
- [Edge TTS](https://github.com/rany2/edge-tts) — Text-to-speech
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) — UI themes
- [LLM7](https://llm7.io/) — AI API
- [Pollinations](https://pollinations.ai/) — AI image generation
- All open-source libraries used by the project

---

## 📊 Version History

### v3.2.7

- Persian/English bilingual support
- Multiple UI themes
- Voice recognition
- Webcam photo and video recording
- AI integration
- Web and Wikipedia features
- AI image generation

---

<div align="center">

**Made with ❤️ by Mohammad Sanadgol**

</div>

---

<div dir="rtl">

<a name="فارسی"></a>

# 🇮🇷 فارسی

## 🎤 درباره Parsino

**Parsino** یک دستیار صوتی دسکتاپ دو زبانه (فارسی/انگلیسی) است که با Python ساخته شده و برای اجرای دستورات روزمره کامپیوتر از طریق صدا طراحی شده است.

این پروژه امکاناتی مانند تشخیص گفتار، تبدیل متن به گفتار، کنترل سیستم، جستجوی اینترنتی، هوش مصنوعی، تولید تصویر، وبکم و رابط گرافیکی قابل تنظیم را در یک برنامه ترکیب می‌کند.

---

## ✨ قابلیت‌ها

### 🎤 صدا و زبان

- تشخیص گفتار فارسی و انگلیسی
- کلمات بیدارکننده فارسی:
  - `پارسا`
  - `رویا`
- کلمات بیدارکننده انگلیسی:
  - `Alex`
  - `Enola`
- استفاده از Vosk برای تشخیص گفتار
- پاسخ صوتی دو زبانه
- پشتیبانی از مسیرهای خروجی متفاوت برای دستورات فارسی و انگلیسی

### 🤖 هوش مصنوعی

Parsino از API سازگار با OpenAI سرویس **LLM7** برای پاسخ‌های هوش مصنوعی استفاده می‌کند.

قابلیت‌های بخش AI:

- پاسخ به سوالات
- ارائه توضیحات کوتاه
- پاسخ به فارسی یا انگلیسی متناسب با زبان درخواست
- نمایش پاسخ به صورت متنی
- پخش پاسخ به صورت صوتی
- استفاده از مدل `default`

### 🎨 تولید تصویر با هوش مصنوعی

Parsino امکان تولید تصویر با استفاده از API سرویس **Pollinations** را دارد.

تصویر تولیدشده:

- نمایش داده می‌شود
- به صورت خودکار ذخیره می‌شود
- دارای پیام متنی و صوتی متناسب با زبان دستور است

مسیر ذخیره تصاویر:

```text
%USERPROFILE%\Pictures\p_ai_photo\
```

### 💻 کنترل کامپیوتر

از جمله:

- اجرای Chrome، Firefox، Word، PowerPoint و Excel
- کنترل صدا
- تنظیم روشنایی
- مدیریت پنجره‌ها
- خاموش کردن سیستم
- Restart
- دسترسی به برخی تنظیمات سیستم

### 🌐 امکانات اینترنتی

- جستجوی Wikipedia
- جستجوی وب
- درخواست از هوش مصنوعی
- تولید تصویر با هوش مصنوعی
- ترجمه

### 📷 وبکم

- گرفتن عکس
- ضبط ویدیو
- ضبط ویدیو همراه با صدا

### 📝 امکانات کاربردی

- ایجاد و ذخیره یادداشت
- نمایش ساعت و اطلاعات سیستم
- اجرای دستورات مختلف سیستم

---

## 🧠 ساختار کلی برنامه

```text
دستور صوتی
    │
    ▼
تشخیص گفتار با Vosk
    │
    ▼
تشخیص دستور و زبان
    │
    ├── کنترل سیستم و برنامه‌ها
    ├── کنترل رسانه
    ├── جستجوی وب / Wikipedia
    ├── هوش مصنوعی → LLM7
    ├── تولید تصویر → Pollinations
    ├── وبکم
    └── سایر امکانات
             │
             ▼
       خروجی متنی + صوتی
```

---

## 📋 نیازمندی‌ها

### ⚠️ نسخه Python

**نسخه پیشنهادی و تست‌شده این پروژه Python 3.10.11 است.**

وابستگی‌ها و کد فعلی پروژه بر اساس Python 3.10.11 توسعه و تست شده‌اند. استفاده از نسخه‌های دیگر Python ممکن است به تغییر در وابستگی‌ها یا کد نیاز داشته باشد.

### نیازمندی‌های سیستم

| مورد | نیاز |
|---|---|
| سیستم‌عامل | Windows 10 / Windows 11 |
| Python | **3.10.11** |
| RAM | حداقل 2GB؛ مقدار بیشتر پیشنهاد می‌شود |
| میکروفون | برای دستورات صوتی الزامی |
| اینترنت | برای AI، جستجو، ترجمه، تولید تصویر و سرویس‌های آنلاین |
| وبکم | اختیاری؛ فقط برای قابلیت‌های وبکم |

---

## 🚀 نصب

### مرحله 1 — کلون کردن پروژه

```bash
git clone https://github.com/sanadgol83/Voice-assistant-plus.git
cd Voice-assistant-plus
```

### مرحله 2 — ساخت Virtual Environment

```bash
python -m venv venv
```

فعال‌سازی در Windows:

```bash
venv\Scripts\activate
```

### مرحله 3 — نصب وابستگی‌ها

```bash
python -m pip install -r requirements.txt
```

بررسی نسخه Python:

```bash
python --version
```

باید نسخه زیر نمایش داده شود:

```text
Python 3.10.11
```

---

## 🎙️ مرحله 4 — نصب مدل‌های Vosk

Parsino برای تشخیص گفتار به مدل‌های Vosk نیاز دارد.

مدل‌ها را از لینک زیر دانلود کنید:

[Vosk Models](https://alphacephei.com/vosk/models)

سپس پوشه‌های موردنیاز را در ریشه پروژه قرار دهید:

```text
vosk-model-small-fa-0.5/
vosk-model-small-en-us-0.15/
```

مدل فارسی برای تشخیص گفتار فارسی و مدل انگلیسی برای تشخیص گفتار انگلیسی استفاده می‌شود.

---

## 🔐 مرحله 5 — تنظیم API Keyها

برخی قابلیت‌های Parsino از سرویس‌های آنلاین استفاده می‌کنند.

**API Keyها را هرگز داخل فایل‌های Python قرار ندهید و آن‌ها را در GitHub منتشر نکنید.**

در ریشه پروژه یک فایل با نام زیر ایجاد کنید:

```text
.env
```

نمونه:

```env
LLM7_API_KEY=your_llm7_api_key_here
POLLINATIONS_API_KEY=your_pollinations_api_key_here
```

### LLM7

بخش هوش مصنوعی از endpoint زیر استفاده می‌کند:

```text
https://api.llm7.io/v1/chat/completions
```

در پیاده‌سازی فعلی مدل به شکل زیر تنظیم شده است:

```text
default
```

کلید API از متغیر زیر خوانده می‌شود:

```text
LLM7_API_KEY
```

### Pollinations

تولید تصویر از endpoint زیر استفاده می‌کند:

```text
https://gen.pollinations.ai/image/
```

کلید API از متغیر زیر خوانده می‌شود:

```text
POLLINATIONS_API_KEY
```

### ⚠️ نکته امنیتی مهم

فایل `.env` نباید وارد GitHub شود.

در `.gitignore` قرار دهید:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

اگر یک API Key به صورت عمومی منتشر شد، آن را از سرویس مربوطه باطل و یک کلید جدید ایجاد کنید.

---

## ▶️ اجرای برنامه

بعد از فعال کردن محیط مجازی:

```bash
python Parsino.py
```

سپس از رابط برنامه دستیار را فعال کرده و یکی از کلمات بیدارکننده را استفاده کنید.

---

## 🗣️ نمونه دستورات

### فارسی

```text
پارسا کروم باز کن
پارسا صدا زیاد کن
پارسا ویکی پدیا پایتون
پارسا عکس یک گربه روی ماه تولید کن
پارسا عکس بگیر
```

### انگلیسی

```text
Alex open chrome
Alex volume up
Alex wikipedia python
Alex generate an image of a cat on the moon
Alex take photo
```

دستورات دقیق قابل استفاده به commandهایی بستگی دارد که در نسخه فعلی پروژه تعریف شده‌اند.

---

## 🎨 تولید تصویر و خروجی دو زبانه

بخش تولید تصویر علاوه بر ساخت تصویر، خروجی متنی و صوتی متناسب با زبان دستور را نیز ارائه می‌کند.

برای مثال:

```text
دستور فارسی
    │
    ▼
تولید تصویر
    │
    ├── تصویر تولیدشده
    ├── پیام متنی فارسی
    └── پاسخ صوتی فارسی
```

و:

```text
English command
    │
    ▼
Image generation
    │
    ├── Generated image
    ├── English text response
    └── English voice response
```

---

## 🤖 خروجی هوش مصنوعی

در بخش AI، درخواست کاربر به LLM7 ارسال می‌شود و پاسخ دریافت‌شده سپس به دو شکل استفاده می‌شود:

```text
دستور کاربر
    │
    ▼
LLM7 API
    │
    ▼
پاسخ AI
    │
    ├── خروجی متنی
    └── خروجی صوتی
```

System Prompt فعلی نیز مدل را هدایت می‌کند تا پاسخ را متناسب با زبان درخواست کاربر ارائه کند.

---

## 📁 ساختار پروژه

```text
Parsino/
│
├── Parsino.py                  # فایل اصلی برنامه
├── basic_media.py              # کنترل سیستم و رسانه
├── Internet_media.py           # اینترنت، AI، جستجو، ترجمه و تولید تصویر
├── webcam_media.py             # قابلیت‌های عکس و ویدیو وبکم
├── utils.py                    # توابع کمکی، TTS، تنظیمات و ...
├── requirements.txt            # وابستگی‌های Python
├── README.md                   # مستندات پروژه
├── LICENSE                     # مجوز MIT
├── .env                        # کلیدهای API (نباید منتشر شود)
│
├── vosk-model-small-fa-0.5/    # مدل فارسی Vosk
└── vosk-model-small-en-us-0.15/ # مدل انگلیسی Vosk
```

---

## 🛠️ تکنولوژی‌های استفاده‌شده

| تکنولوژی | کاربرد |
|---|---|
| Python 3.10.11 | زبان اصلی |
| Vosk | تشخیص گفتار |
| Tkinter | رابط گرافیکی |
| ttkbootstrap | تم‌های رابط کاربری |
| Edge TTS | تبدیل متن به گفتار |
| OpenCV | وبکم و پردازش تصویر |
| MoviePy | پردازش ویدیو |
| BeautifulSoup | استخراج داده از وب |
| Requests | ارتباط HTTP و API |
| PyAutoGUI | خودکارسازی دسکتاپ |
| LLM7 | تولید متن با هوش مصنوعی |
| Pollinations | تولید تصویر با هوش مصنوعی |

---

## ⚙️ تنظیمات

تنظیمات برنامه در مسیر زیر ذخیره می‌شوند:

```text
%APPDATA%\Parsino\config.json
```

تنظیمات قابل شخصی‌سازی شامل مواردی مانند:

- زبان
- جنسیت صدا
- تم رابط کاربری
- سایر تنظیمات برنامه

---

## 🐛 عیب‌یابی

### میکروفون شناسایی نمی‌شود

- دسترسی میکروفون را در Windows بررسی کنید.
- میکروفون صحیح را به عنوان ورودی انتخاب کنید.
- عملکرد میکروفون را در یک برنامه دیگر بررسی کنید.

### مدل Vosk پیدا نمی‌شود

مطمئن شوید پوشه‌های زیر در ریشه پروژه قرار دارند:

```text
vosk-model-small-fa-0.5
vosk-model-small-en-us-0.15
```

### خطای API

موارد زیر را بررسی کنید:

1. اتصال اینترنت
2. صحیح بودن API Key
3. قرار داشتن `.env` در ریشه پروژه
4. صحیح بودن نام متغیرها:

```text
LLM7_API_KEY
POLLINATIONS_API_KEY
```

### خطای Import یا Dependency

ابتدا Virtual Environment را فعال کنید:

```bash
venv\Scripts\activate
```

سپس:

```bash
python -m pip install -r requirements.txt --force-reinstall
```

و نسخه Python را بررسی کنید:

```bash
python --version
```

---

## 🔒 امنیت API Keyها

برای انتشار پروژه در GitHub:

- `.env` را commit نکنید.
- API Key را داخل فایل `.py` قرار ندهید.
- API Key را در README یا Screenshot منتشر نکنید.
- در صورت افشای کلید، آن را فوراً باطل/تعویض کنید.
- اطلاعات محرمانه را خارج از Repository نگه دارید.

برای کمک به کاربران جدید می‌توانید فایل زیر را در پروژه قرار دهید:

```text
.env.example
```

با محتوای:

```env
LLM7_API_KEY=
POLLINATIONS_API_KEY=
```

فایل واقعی `.env` باید فقط روی سیستم کاربر باقی بماند.

---

## 👨‍💻 توسعه‌دهنده

**محمد سندگل**

- GitHub: [@sanadgol83](https://github.com/sanadgol83)
- Repository: [Voice-assistant-plus](https://github.com/sanadgol83/Voice-assistant-plus)
- شروع پروژه: 2025
- نسخه مستندشده فعلی: **3.2.7**

---

## 📝 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است.

برای جزئیات کامل به فایل [LICENSE](LICENSE) مراجعه کنید.

---

## 🤝 مشارکت

مشارکت در توسعه پروژه آزاد است.

برای مشارکت:

1. Repository را Fork کنید.
2. یک Branch جدید ایجاد کنید.
3. تغییرات خود را اعمال کنید.
4. پروژه را تست کنید.
5. Pull Request ایجاد کنید.

برای گزارش باگ یا پیشنهاد قابلیت جدید نیز می‌توانید Issue ایجاد کنید.

---

## 📧 پشتیبانی

برای گزارش مشکلات، سوالات یا پیشنهادها:

[ایجاد Issue در GitHub](https://github.com/sanadgol83/Voice-assistant-plus/issues)

---

## 🙏 تشکر

- [Vosk](https://alphacephei.com/vosk/) — تشخیص گفتار
- [Edge TTS](https://github.com/rany2/edge-tts) — تبدیل متن به گفتار
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) — تم‌های رابط کاربری
- [LLM7](https://llm7.io/) — API هوش مصنوعی
- [Pollinations](https://pollinations.ai/) — تولید تصویر با هوش مصنوعی
- تمام کتابخانه‌های متن‌باز استفاده‌شده در پروژه

---

## 📊 تاریخچه نسخه

### v3.2.7

- پشتیبانی دو زبانه فارسی/انگلیسی
- چندین تم رابط کاربری
- تشخیص گفتار
- ضبط عکس و ویدیو با وبکم
- یکپارچه‌سازی هوش مصنوعی
- جستجوی وب و Wikipedia
- تولید تصویر با هوش مصنوعی
- خروجی متنی و صوتی دو زبانه

---

<div align="center">

**ساخته‌شده با ❤️ توسط محمد سندگل**

</div>

</div>
