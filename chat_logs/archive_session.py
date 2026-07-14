# -*- coding: utf-8 -*-
"""
对话归档脚本 — 每次对话结束时运行
"""
import os, sys, json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE = r"D:\reasonix-memory"
LOG_DIR = os.path.join(BASE, "chat_logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 生成本次记录文件
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H%M%S")
filepath = os.path.join(LOG_DIR, f"{date_str}_{time_str}_存档.md")

content = f"""# 对话记录 {date_str} {now.strftime('%H:%M')}

## 本次涉及的话题

[Reasonix 自动记录]

## 关键信息变更

- （待 Reasonix 填写）

## 补剂/饮食/健康更新

- （待 Reasonix 填写）

---

*由 Reasonix 自动生成*
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"存档文件已创建: {filepath}")
