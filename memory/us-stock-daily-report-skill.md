---
name: us-stock-daily-report-skill
title: 美股日报生成技能
description: 已安装美股收盘日报生成技能，需数据抓取来生成完整的16节日报
metadata:
  type: project
---

**美股收盘日报生成技能** 已安装。

- 技能名：`us-stock-daily-report`
- 调用方式：`run_skill({name: "us-stock-daily-report", arguments: "生成日报"})`
- 位于：`.reasonix/skills/us-stock-daily-report.md`
- 来源文件：桌面上的「你是一名专业的美股市场日报分析师...」模板

**关键要求：**
- 需要确认前一日是否为美股交易日
- 需要依次抓取 Yahoo Finance / Finviz / CNBC / FRED / CME FedWatch 等数据源
- 报告包含 16 个章节，涵盖大盘、宏观、板块、个股、技术面、财报、机构观点等
- 报告输出至 `reports/daily/{REPORT_DATE}.md`
- 数据缺失则写"暂无可靠数据"，不得编造
- 截断时优先保留第1-5节

**与 AI-Trader 的协同：**
AI-Trader 平台上可以获取实时的交易信号和市场情绪数据，可辅助日报的"板块轮动判断"和"重点个股异动"部分。
