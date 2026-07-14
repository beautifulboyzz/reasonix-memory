import os
import sys
import platform
import shutil
import subprocess
from datetime import datetime

# ================= 配置区 =================
# 基础目录（脚本所在目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 截图存放目录
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
# 归档目录（识别完的图片放这里）
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
# 数据保存的 Markdown 文件路径
RECORD_FILE = os.path.join(BASE_DIR, "sleep_records.md")
# ==========================================

# 确保必要的文件夹存在
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

def ocr_mac(img_path):
    """macOS 原生 Vision 框架 OCR"""
    swift_code = f"""
    import Vision
    import Cocoa

    let imageUrl = URL(fileURLWithPath: "{img_path}")
    guard let ciImage = CIImage(contentsOf: imageUrl) else {{
        print("Error: Could not load image")
        exit(1)
    }}

    let handler = VNImageRequestHandler(ciImage: ciImage, options: [:])
    let request = VNRecognizeTextRequest {{ request, error in
        guard let observations = request.results as? [VNRecognizedTextObservation] else {{ return }}
        let recognizedStrings = observations.compactMap {{ $0.topCandidates(1).first?.string }}
        print(recognizedStrings.joined(separator: "\\n"))
    }}
    request.recognitionLanguages = ["zh-Hans", "en-US"]
    try? handler.perform([request])
    """
    
    temp_swift = os.path.join(BASE_DIR, "temp_ocr.swift")
    with open(temp_swift, "w", encoding="utf-8") as f:
        f.write(swift_code)
    
    try:
        result = subprocess.run(["swift", temp_swift], capture_output=True, text=True, encoding="utf-8")
        return result.stdout.strip()
    finally:
        if os.path.exists(temp_swift):
            os.remove(temp_swift)

def ocr_windows(img_path):
    """Windows 10/11 原生 WinRT OCR"""
    try:
        import asyncio
        from winsdk.windows.graphics.imaging import BitmapDecoder
        from winsdk.windows.media.ocr import OcrEngine
        from winsdk.windows.storage import StorageFile

        async def win_ocr():
            file = await StorageFile.get_file_from_path_async(os.path.abspath(img_path))
            stream = await file.open_async(0)
            decoder = await BitmapDecoder.create_async(stream)
            software_bitmap = await decoder.get_software_bitmap_async()
            
            engine = OcrEngine.try_create_from_user_profile_languages()
            result = await engine.recognize_async(software_bitmap)
            return "\n".join([line.text for line in result.lines])

        return asyncio.run(win_ocr())
    except ImportError:
        return "Windows 运行此脚本需要先安装 winsdk: pip install winsdk"
    except Exception as e:
        return f"Windows OCR 失败: {str(e)}"

def run_ocr(img_path):
    """根据系统自动选择 OCR 引擎"""
    system_name = platform.system()
    if system_name == "Darwin":
        return ocr_mac(img_path)
    elif system_name == "Windows":
        return ocr_windows(img_path)
    else:
        raise NotImplementedError("目前仅支持 macOS 和 Windows 系统")

def git_sync():
    """Git 自动提交与同步"""
    print("[*] 正在同步到 Git 仓库...")
    try:
        # 切换到脚本所在目录执行 git
        os.chdir(BASE_DIR)
        subprocess.run(["git", "add", "."], check=True)
        commit_msg = f"chore: update health records {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("[+] Git 同步成功！")
    except Exception as e:
        print(f"[-] Git 同步失败 (可能无更新内容或网络问题): {e}")

def get_image_date(file_path):
    """获取图片的创建/修改日期，格式化为 YYYY-MM-DD"""
    # 优先获取创建时间（Windows下为ctime，Mac下ctime为元数据修改时间，birthtime为创建时间）
    stat = os.stat(file_path)
    try:
        timestamp = stat.st_birthtime
    except AttributeError:
        # Windows 或部分 Linux 系统没有 st_birthtime，取修改时间或创建时间中较早的一个
        timestamp = min(stat.st_mtime, stat.st_ctime)
    
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

def process_screenshots():
    # 支持的图片格式
    valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
    files = [f for f in os.listdir(SCREENSHOTS_DIR) if os.path.splitext(f)[1].lower() in valid_extensions]
    
    if not files:
        print(f"[!] 没有在 '{SCREENSHOTS_DIR}' 文件夹中发现新截图。")
        return

    print(f"[*] 发现 {len(files)} 张新截图，准备开始处理...")
    
    # 用来按日期暂存 OCR 结果的字典 { "2026-03-27": ["文本1", "文本2"] }
    daily_results = {}

    for file_name in files:
        src_path = os.path.join(SCREENSHOTS_DIR, file_name)
        
        # 1. 自动识别截图日期
        img_date = get_image_date(src_path)
        print(f"\n[*] 正在处理: {file_name} (识别到文件日期: {img_date})")
        
        # 2. 运行 OCR 识别
        raw_text = run_ocr(src_path)
        if raw_text.strip():
            if img_date not in daily_results:
                daily_results[img_date] = []
            daily_results[img_date].append(raw_text)
            print(f"[+] OCR 识别成功！")
        else:
            print(f"[-] 图片 {file_name} 未识别到任何文字。")

        # 3. 自动分类并重命名移动到 archive 归档夹
        # 避免重名，加一个时间戳微秒后缀
        timestamp_suffix = datetime.now().strftime("%H%M%S_%f")[:10]
        dest_file_name = f"{img_date}_{timestamp_suffix}{os.path.splitext(file_name)[1]}"
        dest_path = os.path.join(ARCHIVE_DIR, dest_file_name)
        
        shutil.move(src_path, dest_path)
        print(f"[->] 已重命名并归档至: archive/{dest_file_name}")

    # 4. 将提取出的文本结构化写入本地 Markdown 记录
    if daily_results:
        with open(RECORD_FILE, "a", encoding="utf-8") as f:
            for date_str, texts in sorted(daily_results.items()):
                f.write(f"\n\n## 日期: {date_str} (自动分类导入)\n")
                for i, text in enumerate(texts, 1):
                    f.write(f"### 截图数据分段 - {i}\n")
                    f.write("```text\n")
                    f.write(text)
                    f.write("\n```\n")
        
        print(f"\n[+] 所有数据已成功追加写入: {RECORD_FILE}")
        
        # 5. Git 自动同步
        git_sync()

def main():
    process_screenshots()

if __name__ == "__main__":
    main()