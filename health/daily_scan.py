# -*- coding: utf-8 -*-
"""
每日扫图：扫描 screenshots/ 里所有新图片 → OCR 提取文字 → 保存供 Reasonix 读取
"""
import os, sys, asyncio, json, shutil
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

import winsdk.windows.graphics.imaging as wi
import winsdk.windows.media.ocr as wocr
import winsdk.windows.storage as ws

BASE = r"D:\reasonix-memory\health"
SCREENSHOTS = os.path.join(BASE, "screenshots")
ARCHIVE = os.path.join(BASE, "archive")
RAW_DIR = os.path.join(BASE, "_ocr_raw")
os.makedirs(ARCHIVE, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

async def ocr_image(img_path):
    file = await ws.StorageFile.get_file_from_path_async(os.path.abspath(img_path))
    stream = await file.open_async(0)
    decoder = await wi.BitmapDecoder.create_async(stream)
    sb = await decoder.get_software_bitmap_async()
    engine = wocr.OcrEngine.try_create_from_user_profile_languages()
    result = await engine.recognize_async(sb)
    return [line.text for line in result.lines]

# 扫描新图片
exts = ('.png', '.jpg', '.jpeg', '.bmp')
files = sorted([f for f in os.listdir(SCREENSHOTS) if f.lower().endswith(exts)])
if not files:
    print("[-] screenshots/ 暂无新图片")
    sys.exit(0)

print(f"[*] 发现 {len(files)} 张新截图，正在 OCR...")

today = datetime.now().strftime("%Y%m%d_%H%M%S")
all_texts = []

for fname in files:
    fp = os.path.join(SCREENSHOTS, fname)
    print(f"  -> {fname}")
    try:
        texts = asyncio.run(ocr_image(fp))
    except Exception as e:
        texts = [f"[OCR ERROR] {e}"]
    
    all_texts.append({"file": fname, "texts": texts})
    
    # 归档图片
    ts = datetime.now().strftime("%H%M%S")
    shutil.move(fp, os.path.join(ARCHIVE, f"{today}_{ts}_{fname}"))

# 保存 OCR 原始文本
out_file = os.path.join(RAW_DIR, f"scan_{today}.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(all_texts, f, ensure_ascii=False, indent=2)

print(f"\n[+] OCR 完成，共 {sum(len(a['texts']) for a in all_texts)} 行文字")
print(f"[+] 原始数据保存至: {out_file}")
print(f"[*] 请在 Reasonix 中说「读取今日截图」，我来整理归档。")
