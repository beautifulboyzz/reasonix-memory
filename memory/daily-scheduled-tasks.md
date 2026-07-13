---
name: daily-scheduled-tasks
title: 本机定时任务一览
description: 两台本机定时任务：15:00 换月提醒 / 17:00 天勤数据入库
metadata:
  type: project
---

## 任务一：换月提醒（15:00）

- **脚本**: `D:\换月提醒系统\换月+持仓量每日监控.py`
- **系统任务**: `RollMonitor_Daily1500` ✅ 已配置
- **时间**: 每天 15:00，去年 5/28 开始启用
- **上次执行**: 2026-06-10 15:00:01（正常）
- **执行命令**: `powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "D:\换月提醒系统\run_roll_monitor_1500.ps1"`
- **输出**: 推送飞书，日志保留在 `logs\\roll_monitor_YYYYMMDD.log`
- **本机模式**: 仅用新浪/东财 API，不碰 200 tick / Mongo

## 任务二：天勤数据入库（17:00）

- **脚本**: `D:\fu_db\auto_run_daily.py`
- **系统任务**: `FuDB_AutoRun_1700` ✅ 已配置（2026-06-11 创建）
- **时间**: 每天 17:00，首次计划 2026-06-11 17:00
- **执行命令**: `C:\Users\22633\AppData\Local\Programs\Python\Python311\python.exe D:\fu_db\auto_run_daily.py --now`
- **工作目录**: `D:\fu_db`
- **工作内容**: 分两阶段 —— ① 天勤引擎拉取交易日历/合约基础信息/日线/主力映射（粘性换月，不走TqApi避免卡死）；② 调用 `export_my_data.py` 生成全品种复权 CSV
- **手动命令**: `python auto_run_daily.py --now`（立即执行一次），`python auto_run_daily.py --now --full`（全量重建）

## 为什么重要

这两条任务每天固定跑，是数据管线的两个环节。在讨论夜盘、修改脚本或排查数据问题时，需要确认什么时间段在跑什么，以协调停机/改参/热更新。

## 注意

- 换月提醒 `--loop` 常驻模式已改用系统计划任务触发，不再用脚本内 loop（`--loop` 参数保留但未被使用）
- 天勤任务使用 `--now` 参数避免卡在交互输入，跑完即退出不占内存
