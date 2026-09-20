import cv2
import datetime
import os
import numpy as np
import threading
import pyaudio
import wave
from moviepy import VideoFileClip, AudioFileClip
import time
from utils import *

def take_photo(x):
    if x==1:
        print('...📷عکس گرفتم...')
    else:
        print('...📷take photo...')
    # تعیین مسیر ذخیره‌سازی
    home_dir = os.path.expanduser("~")
    pictures_dir = os.path.join(home_dir, "Pictures", "p_webcam")
    
    # ایجاد پوشه در صورت عدم وجود
    os.makedirs(pictures_dir, exist_ok=True)
    
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("❌ وبکم پیدا نشد!")
        return
    
    success, frame = camera.read()
    
    if success:
        # ایجاد نام فایل با زمان
        filename = f"webcam_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        full_path = os.path.join(pictures_dir, filename)
        
        cv2.imwrite(full_path, frame)
     
        # نمایش عکس گرفته شده برای 3 ثانیه
        cv2.imshow('show picture', frame)
        cv2.waitKey(3000)
        cv2.destroyWindow('show picture')
        if x==1:
            print(f"{full_path} : عکس ذخیره شد")
            asyncio.run(stream_audio("با استفاده از وبکم عکس گرفتم"))
        else:
            print(f"{full_path} :save picture")
            speak("i took a picture with a webcam")

    else:
        print("❌ خطا در گرفتن عکس!")

    camera.release()

def record_video(x):
    if x==1:
        print('...ویدیو گرفتم...')
    else:
        print('...📷take video...')
    # تعیین مسیر ذخیره‌سازی
    home_dir = os.path.expanduser("~")
    videos_dir = os.path.join(home_dir, "Videos", "v_webcam")
    os.makedirs(videos_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_video = os.path.join(videos_dir, f"temp_video_{timestamp}.mp4")
    temp_audio = os.path.join(videos_dir, f"temp_audio_{timestamp}.wav")
    final_output = os.path.join(videos_dir, f"video_with_audio_{timestamp}.mp4")
    
    # پارامترهای ضبط
    VIDEO_FPS = 30
    AUDIO_RATE = 44100
    CHUNK = 1024
    
    # متغیرهای اشتراکی
    audio_frames = []
    audio_recording = False
    video_recording = False
    
    # تابع ضبط صدا
    def record_audio():
        nonlocal audio_frames
        
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=2,
                        rate=AUDIO_RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        while audio_recording:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                audio_frames.append(data)
            except Exception as e:
                if x==1:
                    print(f"خطا در ضبط صدا: {e}")
                else:
                    print(f"Audio recording error: {e}")
                break
        
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    # شروع ضبط
    if x==1:
        print("...⏱️در حال ضبط ویدیو...")
    else:
        print("...⏱️Recording video...")
    # شروع ضبط صدا
    audio_recording = True
    audio_thread = threading.Thread(target=record_audio)
    audio_thread.start()
    
    # ضبط ویدیو
    video_recording = True
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        if x==1:
            print("❌ وبکم پیدا نشد!")
        else:
            print("❌ Webcam not found!")
        audio_recording = False
        audio_thread.join()
        return
    
    # تنظیمات دوربین
    cap.set(cv2.CAP_PROP_FPS, VIDEO_FPS)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # گرفتن اندازه فریم
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # ایجاد VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, VIDEO_FPS, (frame_width, frame_height))
    
    start_time = time.time()
    
    try:
        while video_recording:
            ret, frame = cap.read()
            if not ret:
                if x==1:
                    print("❌ خطا در خواندن فریم از دوربین")
                else:
                    print("❌ Error reading frame from camera")
                break
            frame = cv2.flip(frame, 1)
            # ذخیره فریم
            out.write(frame)
            
            # نمایش ویدیوی زنده
            elapsed_time = time.time() - start_time
            cv2.putText(frame, f"Time record : {elapsed_time:.1f}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, "Press the 'Esc' button to stop", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.imshow('Parsino Video Recorder', frame)
            
            if cv2.waitKey(1) & 0xFF == 27:
                break
                
    except Exception as e:
        if x==1:
            print(f"❌ خطا در ضبط ویدیو: {e}")
        else:
            print(f"❌ Error recording video : {e}")
    
    finally:
        # توقف ضبط
        video_recording = False
        audio_recording = False
        
        # آزاد کردن منابع ویدیو
        out.release()
        cap.release()
        cv2.destroyAllWindows()
        
        # منتظر ماندن برای پایان thread صدا
        audio_thread.join()
                
        # ذخیره فایل صوتی
        if audio_frames:
            try:
                wf = wave.open(temp_audio, 'wb')
                wf.setnchannels(2)
                wf.setsampwidth(2)
                wf.setframerate(AUDIO_RATE)
                wf.writeframes(b''.join(audio_frames))
                wf.close()
            except Exception as e:
                if x==1:
                    print(f"❌ خطا در ذخیره فایل صوتی: {e}")
                else:
                    print(f"❌ Error saving audio file: {e}")
                return
        
        # بررسی وجود فایل‌ها
        if not os.path.exists(temp_video):
            if x==1:
                print("❌ فایل ویدیویی ایجاد نشد")
            else:
                print("❌ Video file could not be created")
            return
        
        if not os.path.exists(temp_audio):
            if x==1:
                print("❌ فایل صوتی ایجاد نشد")
            else:
                print("❌ The audio file could not be created")
            return
        
        # ادغام ویدیو و صدا
        try:
            if x==1:
                print("🔗در حال ادغام ویدیو و صدا")
            else:
                print("🔗Merging video and audio")

            video_clip = VideoFileClip(temp_video)
            audio_clip = AudioFileClip(temp_audio)
            
            # هماهنگ کردن طول ویدیو و صدا
            video_duration = video_clip.duration
            audio_duration = audio_clip.duration
            
            # استفاده از مدت زمان کوتاه‌تر
            final_duration = min(video_duration, audio_duration)
            
            if final_duration < 1.0:
                if x==1:
                    print("❌ مدت زمان ضبط بسیار کوتاه است")
                else:
                    print("❌ The recording time is very short")
                return
            
            video_clip = video_clip.subclipped(0, final_duration)
            audio_clip = audio_clip.subclipped(0, final_duration)
            
            final_clip = video_clip.with_audio(audio_clip)            
            # ذخیره فایل نهایی
            final_clip.write_videofile(
                final_output, 
                codec='libx264', 
                audio_codec='aac', 
                fps=VIDEO_FPS,
                logger=None
            )
            
            # بستن کلیپ‌ها
            video_clip.close()
            audio_clip.close()
            final_clip.close()
            
            # حذف فایل‌های موقت
            try:
                os.remove(temp_video)
                os.remove(temp_audio)
            except:
                if x==1:
                    print("⚠️ نتوانستم فایل‌های موقت را حذف کنم")
                else:
                    print("⚠️ Could not delete temporary files")
            if x==1:
                print(f"🎬 مدت زمان نهایی: {final_duration:.2f} ثانیه")
                print(f"{final_output} : فیلم ذخیره شد")
                asyncio.run(stream_audio(f"مدت زمان نهایی: {final_duration:.2f} ثانیه"))
            else:
                print(f"🎬 Final duration: {final_duration:.2f} seconds")
                print(f"Video saved: {final_output}")
                speak(f"Final duration: {final_duration:.2f} seconds")
        except Exception as e:
            if x==1:
                print(f"❌ خطا در ادغام ویدیو و صدا: {e}")
                print(f"📹 ویدیو بدون صدا: {temp_video}")
                print(f"🎵 صدا: {temp_audio}")
            else:
                print(f"❌ Error merging video and audio: {e}")
                print(f"📹 Video without audio: {temp_video}")
                print(f"🎵 Audio: {temp_audio}")
