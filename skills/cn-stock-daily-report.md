---
name: cn-stock-daily-report
description: 生成专业《A股收盘日报》— 16节结构，AKShare自动抓数，输出 reports/ashare-daily/{日期}/（md+pdf+jpg）
---

# A-Share Daily Report — A股收盘日报

## 角色
专业 A 股市场日报分析师。报告语言：中文。风格：数据驱动、适合复盘与次日计划。

## 数据源（A级）
- **AKShare** → 新浪指数日线、东财行业/涨停/北向、乐咕乐股宽度
- 宏观：LPR、美元人民币汇率（AKShare 宏观接口）
- **禁止编造**：缺数据写「暂无可靠数据」

## 报告结构（16节，与美股日报对齐）

1. 一句话总结 + 今日市场状态
2. 大盘表现（上证/深证/创业板/科创50/北证50/沪深300/中证500/1000）
3. 盘中走势复盘
4. 宏观环境（LPR、北向、政策事件）
5. 板块表现（东财行业涨跌榜）
6. 主题与风格（大盘 vs 小盘、成长 vs 价值）
7. 市场宽度（涨跌家数、涨停跌停、活跃度）
8. 技术面（沪深300/创业板/中证500/科创50 RSI/MACD）
9. 重点个股（涨幅榜、跌幅榜、涨停池）
10. 财报与事件
11. 机构观点与资金流
12. 板块轮动判断
13. 重点关注
14. 明日交易计划
15. 风险提示
16. 最终结论

## 发布

```bash
python scripts/publish_ashare_daily_report.py
python scripts/publish_ashare_daily_report.py 2026-06-19 --trade-date 2026-06-18
```

输出：`reports/ashare-daily/{YYYY-MM-DD}/`

排版规范：`reports/ashare-daily/PDF排版规范.md`

## 脚本地图

| 脚本 | 作用 |
|------|------|
| `ashare_market_data.py` | 抓数 + 技术指标 |
| `generate_ashare_daily_report.py` | 生成 16 节 MD |
| `publish_ashare_daily_report.py` | MD → PDF → JPG |
| `report_to_pdf.py` | 共用 PDF 引擎（`cover_title=A股收盘日报`） |

## 日期约定

- 文件夹日期 = **发布日早晨**（与美股日报一致）
- 正文标题日期 = **上一 A 股交易日收盘**
- `--trade-date` 可显式指定交易日
