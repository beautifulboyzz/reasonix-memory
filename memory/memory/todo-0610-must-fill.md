---
name: todo-0610-must-fill
title: 0610待办：改回must_fill + 今晚夜盘
description: 今晚夜盘跑 --once，明天改回 must_fill=true
metadata:
  type: project
---

## 待办提醒：2026-06-10

### ⏰ 明天白天 14:00 前要做
**把 `bot_config.json` 的 `must_fill` 改回 `true`**
路径：`D:\ALL\ctp_simnow\bot_config.json`
```json
"must_fill": true,
```
否则明天 14:58 定时调仓没有追单保护。

### 🌙 今晚夜盘要做
跑 `python run_ctp_bot.py --once` 真下单（已改为 `must_fill: false`，不会卡截止时间）

### 已完成的修改
- `contract_specs.py` → 加了 TICK_SIZE_MAP（tick修复）
- `aggressive_executor.py` → 改用查表
- `bot_config.json` → `must_fill: false`（夜盘用），`scrape_sources` 改为 `['sina']`（关掉东财爬虫）
