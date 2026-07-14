# -*- coding: utf-8 -*-
"""诊断睡眠数据的实际格式 - 只看2026年的"""
import os, sys
import xml.etree.ElementTree as ET
from datetime import datetime

d = r"D:\wechat\xwechat_files\wxid_7msi24mq8wso12_7744\msg\file\2026-07\导出\apple_health_export"
xml_files = [f for f in os.listdir(d) if f.endswith('.xml')]
target = None
for f in xml_files:
    fp = os.path.join(d, f)
    if os.path.getsize(fp) > 500 * 1024 * 1024:
        target = fp
        break

print(f"读取: {os.path.basename(target)}")

context = ET.iterparse(target, events=("end",))
sleep_samples = []
hr_samples = []
for event, elem in context:
    rtype = elem.get("type", "")
    sdate = elem.get("startDate", "")
    if rtype == "HKCategoryTypeIdentifierSleepAnalysis" and "2026-07" in sdate:
        sleep_samples.append({
            "value": elem.get("value"),
            "startDate": sdate,
            "endDate": elem.get("endDate"),
            "sourceName": elem.get("sourceName"),
        })
        if len(sleep_samples) >= 30:
            break
    elem.clear()

print(f"\n2026年7月睡眠样本 ({len(sleep_samples)} 条):")
seen_vals = set()
for s in sleep_samples:
    v = s["value"]
    seen_vals.add(v)
    print(f"  value={v!r}  start={s['startDate'][:19]}  end={s['endDate'][:19]}  source={s['sourceName']}")

print(f"\n出现的价值类型: {seen_vals}")

