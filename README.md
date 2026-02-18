# 🎤 Parsino - Intelligent Voice Assistant

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=flat-square&logo=github)](https://github.com/sanadgol83/Voice-assistant-plus)
[![Python](https://img.shields.io/badge/Python-3.10.11-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
# English

## 🎤 Parsino - Intelligent Voice Assistant

A powerful, bilingual (Persian/English) voice-controlled desktop assistant built with Python. Control your computer, applications, media, and more using natural voice commands.

---

## ✨ Features

### 🎯 Core Capabilities

- **🎤 Voice Recognition**: Advanced speech recognition using Vosk models
- **🌐 Bilingual Support**: Full support for Persian (Farsi) and English
- **🎨 Modern UI**: Beautiful, customizable interface with multiple themes
- **🔊 Text-to-Speech**: Natural-sounding voice responses using Edge TTS
- **⚙️ System Control**: Control applications, media, system settings, and more

### 📋 Command Categories

- **💻 Application Control**: Launch Chrome, Firefox, Word, PowerPoint, Excel
- **🎵 Media Control**: Play, pause, next, previous track
- **🔊 Volume & Brightness**: Adjust system volume and screen brightness
- **🌐 Internet & AI**: Wikipedia search, web search, AI chat, image generation
- **📷 Webcam**: Take photos and record videos with audio
- **🪟 Window Management**: Maximize, minimize, close, restore windows
- **📝 Notepad**: Create and save text notes
- **💰 Economy**: Check gold and currency prices
- **⏰ System**: Time display, shutdown, restart, settings

---

## 📋 Requirements

### ⚠️ Important

**This project requires Python 3.10.11 specifically.**

All dependencies have been tested and verified to work correctly with Python 3.10.11. Using a different Python version may cause compatibility issues.

### System Requirements

- **Python**: 3.10.11 (Required)
- **OS**: Windows 10/11
- **RAM**: Minimum 2GB
- **Microphone**: Required for voice commands
- **Internet**: Required for AI features, web search, and updates

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/sanadgol83/Voice-assistant-plus.git
cd Voice-assistant-plus
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Vosk Models

The application requires Vosk speech recognition models. Place them in the project root:

- `vosk-model-small-fa-0.5` - Persian model
- `vosk-model-small-en-us-0.15` - English model

Download from: [Vosk Models](https://alphacephei.com/vosk/models)

---

## 🎮 Usage

### Starting the Application

```bash
python Parsino.py
```

### Using Voice Commands

1. **Click "Start"** button to activate the assistant
2. **Say the wake word**:
   - For Persian: "پارسا" (Parsa) or "رویا" (Roya)
   - For English: "Alex" or "Enola"
3. **Speak your command** after the wake word

### Example Commands

**English:**
- "Alex open chrome" - Open Chrome
- "Alex volume up" - Increase volume
- "Alex wikipedia python" - Search Wikipedia for Python
- "Alex take photo" - Take a photo

**Persian:**
- "پارسا کروم باز کن" - Open Chrome
- "پارسا صدا زیاد کن" - Increase volume
- "پارسا ویکی پدیا پایتون" - Search Wikipedia for Python
- "پارسا عکس بگیر" - Take a photo

---

## 📁 Project Structure

```
Parsino/
│
├── Parsino.py              # Main application file
├── basic_media.py           # System and media control functions
├── Internet_media.py        # Internet, AI, and web functions
├── webcam_media.py          # Webcam photo and video functions
├── utils.py                 # Utility functions (TTS, settings)
├── requirements.txt         # Python dependencies
├── README.md               # This file
│
└── vosk-model-small-fa-0.5/    # Persian Vosk model (download separately)
└── vosk-model-small-en-us-0.15/ # English Vosk model (download separately)
```

---

## 🛠️ Technologies Used

- **Python 3.10.11** - Core programming language
- **Vosk** - Speech recognition engine
- **Tkinter** - GUI framework
- **ttkbootstrap** - Modern UI themes
- **Edge TTS** - Text-to-speech synthesis
- **OpenCV** - Computer vision (webcam)
- **MoviePy** - Video processing
- **BeautifulSoup** - Web scraping
- **Requests** - HTTP library
- **PyAutoGUI** - GUI automation
- **And more...**

---

## ⚙️ Configuration

The application saves settings in:

```
%APPDATA%\Parsino\config.json
```

You can customize:
- Language (Persian/English)
- Voice gender (Male/Female)
- UI Theme (18 available themes)

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Microphone not detected

- Check microphone permissions in Windows settings
- Ensure microphone is connected and working

**Issue**: Vosk models not found

- Download models from [Vosk Models](https://alphacephei.com/vosk/models)
- Place them in the project root directory

**Issue**: Import errors

- Ensure you're using Python 3.10.11
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

---

## 👨‍💻 Developer

**Mohammad Sanadgol**

- **Version**: 3.2.5
- **Start Year**: 2025
- **GitHub**: [@sanadgol83](https://github.com/sanadgol83)
- **Repository**: [Voice-assistant-plus](https://github.com/sanadgol83/Voice-assistant-plus)

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request to the [repository](https://github.com/sanadgol83/Voice-assistant-plus).

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on [GitHub](https://github.com/sanadgol83/Voice-assistant-plus/issues).

---

## 🙏 Acknowledgments

- [Vosk](https://alphacephei.com/vosk/) - Speech recognition
- [Edge TTS](https://github.com/rany2/edge-tts) - Text-to-speech
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) - Modern UI themes
- All open-source libraries used in this project

---

## 📊 Version History

- **v3.2.5** (2025) - Current version
  - Bilingual support (Persian/English)
  - Multiple UI themes
  - Enhanced voice recognition
  - Webcam video recording with audio
  - AI integration

---

**Made with ❤️ by Mohammad Sanadgol**

---

<div dir="rtl">

<a name="فارسی"></a>
# فارسی

## 🎤 پارسینو - دستیار صوتی هوشمند

دستیار دسکتاپ قدرتمند و دو زبانه (فارسی/انگلیسی) که با پایتون ساخته شده است. کامپیوتر، برنامه‌ها، رسانه و موارد دیگر را با دستورات صوتی طبیعی کنترل کنید.

---

## ✨ ویژگی‌ها

### 🎯 قابلیت‌های اصلی

- **🎤 تشخیص صدا**: تشخیص گفتار پیشرفته با استفاده از مدل‌های Vosk
- **🌐 پشتیبانی دو زبانه**: پشتیبانی کامل از فارسی و انگلیسی
- **🎨 رابط کاربری مدرن**: رابط کاربری زیبا و قابل تنظیم با تم‌های متعدد
- **🔊 تبدیل متن به گفتار**: پاسخ‌های صوتی طبیعی با استفاده از Edge TTS
- **⚙️ کنترل سیستم**: کنترل برنامه‌ها، رسانه، تنظیمات سیستم و موارد بیشتر

### 📋 دسته‌بندی دستورات

- **💻 کنترل برنامه‌ها**: اجرای Chrome، Firefox، Word، PowerPoint، Excel
- **🎵 کنترل رسانه**: پخش، توقف، بعدی، قبلی
- **🔊 صدا و روشنایی**: تنظیم صدا و روشنایی صفحه نمایش
- **🌐 اینترنت و هوش مصنوعی**: جستجوی ویکی‌پدیا، جستجوی وب، چت هوش مصنوعی، تولید تصویر
- **📷 وبکم**: گرفتن عکس و ضبط ویدیو با صدا
- **🪟 مدیریت پنجره‌ها**: بزرگ کردن، کوچک کردن، بستن، بازگرداندن پنجره‌ها
- **📝 دفترچه یادداشت**: ایجاد و ذخیره یادداشت‌های متنی
- **💰 اقتصاد**: بررسی قیمت طلا و ارز
- **⏰ سیستم**: نمایش زمان، خاموش کردن، راه‌اندازی مجدد، تنظیمات

---

## 📋 نیازمندی‌ها

### ⚠️ مهم

**این پروژه به طور خاص به Python 3.10.11 نیاز دارد.**

همه وابستگی‌ها با Python 3.10.11 تست و تأیید شده‌اند. استفاده از نسخه دیگری از Python ممکن است باعث مشکلات سازگاری شود.

### نیازمندی‌های سیستم

- **Python**: 3.10.11 (الزامی)
- **سیستم عامل**: Windows 10/11
- **RAM**: حداقل 2 گیگابایت
- **میکروفون**: برای دستورات صوتی الزامی است
- **اینترنت**: برای ویژگی‌های هوش مصنوعی، جستجوی وب و به‌روزرسانی‌ها الزامی است

---

## 🚀 نصب

### مرحله 1: کلون کردن مخزن

```bash
git clone https://github.com/sanadgol83/Voice-assistant-plus.git
cd Voice-assistant-plus
```

### مرحله 2: ایجاد محیط مجازی

```bash
# ایجاد محیط مجازی
python -m venv venv

# فعال کردن محیط مجازی
# در Windows:
venv\Scripts\activate
# در Linux/Mac:
source venv/bin/activate
```

### مرحله 3: نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### مرحله 4: دانلود مدل‌های Vosk

برنامه به مدل‌های تشخیص گفتار Vosk نیاز دارد. آن‌ها را در ریشه پروژه قرار دهید:

- `vosk-model-small-fa-0.5` - مدل فارسی
- `vosk-model-small-en-us-0.15` - مدل انگلیسی

دانلود از: [Vosk Models](https://alphacephei.com/vosk/models)

---

## 🎮 نحوه استفاده

### شروع برنامه

```bash
python Parsino.py
```

### استفاده از دستورات صوتی

1. **دکمه "شروع" را فشار دهید** تا دستیار فعال شود
2. **کلمه بیدارکننده را بگویید**:
   - برای فارسی: "پارسا" یا "رویا"
   - برای انگلیسی: "Alex" یا "Enola"
3. **دستور خود را بعد از کلمه بیدارکننده بگویید**

### مثال دستورات

**فارسی:**
- "پارسا کروم باز کن" - باز کردن Chrome
- "پارسا صدا زیاد کن" - افزایش صدا
- "پارسا ویکی پدیا پایتون" - جستجوی ویکی‌پدیا برای Python
- "پارسا عکس بگیر" - گرفتن عکس

**انگلیسی:**
- "Alex open chrome" - باز کردن Chrome
- "Alex volume up" - افزایش صدا
- "Alex wikipedia python" - جستجوی ویکی‌پدیا برای Python
- "Alex take photo" - گرفتن عکس

---

## 📁 ساختار پروژه

```
Parsino/
│
├── Parsino.py              # فایل اصلی برنامه
├── basic_media.py           # توابع کنترل سیستم و رسانه
├── Internet_media.py        # توابع اینترنت، هوش مصنوعی و وب
├── webcam_media.py          # توابع عکس و ویدیو وبکم
├── utils.py                 # توابع کمکی (TTS، تنظیمات)
├── requirements.txt         # وابستگی‌های پایتون
├── README.md               # این فایل
│
└── vosk-model-small-fa-0.5/    # مدل فارسی Vosk (به صورت جداگانه دانلود کنید)
└── vosk-model-small-en-us-0.15/ # مدل انگلیسی Vosk (به صورت جداگانه دانلود کنید)
```

---

## 🛠️ تکنولوژی‌های استفاده شده

- **Python 3.10.11** - زبان برنامه‌نویسی اصلی
- **Vosk** - موتور تشخیص گفتار
- **Tkinter** - فریمورک رابط کاربری
- **ttkbootstrap** - تم‌های مدرن رابط کاربری
- **Edge TTS** - تبدیل متن به گفتار
- **OpenCV** - بینایی کامپیوتر (وبکم)
- **MoviePy** - پردازش ویدیو
- **BeautifulSoup** - استخراج داده از وب
- **Requests** - کتابخانه HTTP
- **PyAutoGUI** - خودکارسازی رابط کاربری
- **و موارد بیشتر...**

---

## ⚙️ تنظیمات

برنامه تنظیمات را در این مسیر ذخیره می‌کند:

```
%APPDATA%\Parsino\config.json
```

می‌توانید تنظیم کنید:
- زبان (فارسی/انگلیسی)
- جنسیت صدا (مرد/زن)
- تم رابط کاربری (18 تم موجود)

---

## 🐛 عیب‌یابی

### مشکلات رایج

**مشکل**: میکروفون تشخیص داده نمی‌شود

- مجوزهای میکروفون را در تنظیمات Windows بررسی کنید
- اطمینان حاصل کنید که میکروفون متصل است و کار می‌کند

**مشکل**: مدل‌های Vosk پیدا نمی‌شوند

- مدل‌ها را از [Vosk Models](https://alphacephei.com/vosk/models) دانلود کنید
- آن‌ها را در دایرکتوری ریشه پروژه قرار دهید

**مشکل**: خطاهای import

- اطمینان حاصل کنید که از Python 3.10.11 استفاده می‌کنید
- وابستگی‌ها را دوباره نصب کنید: `pip install -r requirements.txt --force-reinstall`

---

## 👨‍💻 توسعه‌دهنده

**محمد سندگل**

- **نسخه**: 3.2.5
- **سال شروع**: 2025
- **GitHub**: [@sanadgol83](https://github.com/sanadgol83)
- **مخزن**: [Voice-assistant-plus](https://github.com/sanadgol83/Voice-assistant-plus)

---

## 📝 مجوز

این پروژه تحت مجوز MIT است - برای جزئیات فایل LICENSE را ببینید.

---

## 🤝 مشارکت

مشارکت‌ها خوش‌آمد هستند! لطفاً Pull Request به [مخزن](https://github.com/sanadgol83/Voice-assistant-plus) ارسال کنید.

---

## 📧 پشتیبانی

برای مشکلات، سوالات یا پیشنهادات، لطفاً یک issue در [GitHub](https://github.com/sanadgol83/Voice-assistant-plus/issues) باز کنید.

---

## 🙏 تشکر

- [Vosk](https://alphacephei.com/vosk/) - تشخیص گفتار
- [Edge TTS](https://github.com/rany2/edge-tts) - تبدیل متن به گفتار
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) - تم‌های مدرن رابط کاربری
- همه کتابخانه‌های متن‌باز استفاده شده در این پروژه

---

## 📊 تاریخچه نسخه

- **v3.2.5** (2025) - نسخه فعلی
  - پشتیبانی دو زبانه (فارسی/انگلیسی)
  - تم‌های متعدد رابط کاربری
  - تشخیص صدا بهبود یافته
  - ضبط ویدیو وبکم با صدا
  - یکپارچه‌سازی هوش مصنوعی

---

**ساخته شده با ❤️ توسط محمد سندگل**

</div>
