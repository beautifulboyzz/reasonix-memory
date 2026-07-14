# -*- coding: utf-8 -*-
import os, asyncio, sys
import winsdk.windows.graphics.imaging as wi
import winsdk.windows.media.ocr as wocr
import winsdk.windows.storage as ws
sys.stdout.reconfigure(encoding='utf-8')

async def ocr(img_path):
    file = await ws.StorageFile.get_file_from_path_async(os.path.abspath(img_path))
    stream = await file.open_async(0)
    decoder = await wi.BitmapDecoder.create_async(stream)
    sb = await decoder.get_software_bitmap_async()
    engine = wocr.OcrEngine.try_create_from_user_profile_languages()
    result = await engine.recognize_async(sb)
    return [line.text for line in result.lines]

fp = r'D:\reasonix-memory\health\screenshots\b768ef3fb221fbaf82fee4ef88b121af.jpg'
texts = asyncio.run(ocr(fp))
for t in texts:
    if len(t.strip()) > 1:
        print(t)
