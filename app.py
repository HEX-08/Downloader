from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import uuid
import tempfile

app = Flask(__name__)

# إضافة مسار ffmpeg على macOS
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin"

# مجلد تحميل مؤقت (كل تحميل في ملف مؤقت)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# واجهة HTML فخمة
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>🎬 أداة التحميل الفخمة</title>
<style>
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #fff;
    text-align: center;
    margin: 0; padding: 0;
}
.container {
    margin-top: 100px;
    background: rgba(255,255,255,0.05);
    padding: 50px;
    border-radius: 25px;
    width: 450px;
    margin-left:auto; margin-right:auto;
    box-shadow: 0 8px 32px rgba(0,0,0,0.7);
    backdrop-filter: blur(10px);
}
h1 { margin-bottom: 30px; font-size: 28px; }
input[type="text"] {
    width: 85%; padding: 15px; border-radius: 12px; border:none; margin-bottom: 20px; font-size:16px;
}
button {
    padding: 14px 28px; background: #00c6ff; border: none; border-radius: 14px;
    font-size:16px; font-weight:bold; color:#fff; cursor:pointer; transition:0.3s;
}
button:hover { background:#0072ff; transform: scale(1.05); }
.footer { margin-top: 40px; font-size:14px; opacity:0.7; }
</style>
</head>
<body>
<div class="container">
<h1>🚀 تحميل الفيديو بجودة عالية</h1>
<form method="POST">
<input type="text" name="url" placeholder="ألصق رابط الفيديو هنا" required>
<br>
<button type="submit">تأكيد ✅</button>
</form>
</div>
<div class="footer">By Your Private Downloader ⚡</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["url"]
        try:
            # إنشاء ملف مؤقت لكل تحميل
            temp_dir = tempfile.mkdtemp()
            filename = f"{uuid.uuid4()}.mp4"
            filepath = os.path.join(temp_dir, filename)

            # إعدادات yt-dlp
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "outtmpl": filepath,
                "noplaylist": True,
                "quiet": True,               # يقلل الطلاسم في الترمنال
                "nocheckcertificate": True,  # لتجاوز مشاكل SSL
            }

            # تحميل الفيديو من أي موقع يدعمه yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            # إرسال الملف للتحميل المباشر في المتصفح
            return send_file(filepath, as_attachment=True, download_name="video.mp4")
        except Exception as e:
            return f"<h2>❌ خطأ: {str(e)}</h2>"

    return render_template_string(HTML_PAGE)

# التعديل الأساسي للرفع على Render
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # استخدام المنفذ الذي يعطيه Render
    app.run(host="0.0.0.0", port=port, debug=True)
