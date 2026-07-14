# -*- coding: utf-8 -*-
"""
解析 export_cda.xml → 提取 Grow + Apple 系统数据
用文本分割方式，兼容多根元素
"""
import os, sys, re, json
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

BASE = r"D:\wechat\xwechat_files\wxid_7msi24mq8wso12_7744\msg\file\2026-07\导出\apple_health_export"
OUT = r"D:\reasonix-memory\health"
CDA_FILE = os.path.join(BASE, "export_cda.xml")

CUTOFF = "2000-01-01"  # 全量
ALLOWED_SOURCES = ["黎程进", "Grow", "健康"]

print(f"解析: export_cda.xml ({os.path.getsize(CDA_FILE)/1024/1024:.0f} MB)")
print(f"范围: {CUTOFF}~至今")

# ── 逐行读取，提取 observation 段落 ──
with open(CDA_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 提取所有 <observation>...</observation>
obs_pattern = re.compile(r'<observation[^>]*>.*?</observation>', re.DOTALL)
observations = obs_pattern.findall(content)
print(f"找到 {len(observations)} 个 observation 节点")

# ── 解析每个 observation ──
records = []
for obs in observations:
    # 提取 sourceName
    m = re.search(r'<sourceName>(.*?)</sourceName>', obs)
    if not m:
        continue
    source = m.group(1).strip()
    
    # 只保留允许的来源
    allowed = False
    for kw in ALLOWED_SOURCES:
        if kw in source or kw.lower() in source.lower():
            allowed = True
            break
    if not allowed:
        continue
    
    # 提取 type
    m = re.search(r'<type>(.*?)</type>', obs)
    if not m:
        continue
    rtype = m.group(1).strip()
    
    # 提取 value（text 里的 value 字段）
    m = re.search(r'<value>([^<]+)</value>', obs)
    if not m:
        continue
    val = m.group(1).strip()
    
    # 提取 unit
    m = re.search(r'<unit>(.*?)</unit>', obs)
    unit = m.group(1).strip() if m else ""
    
    # 提取有效时间
    m = re.search(r'<low value="(.*?)"', obs)
    if not m:
        m = re.search(r'<high value="(.*?)"', obs)
    time_str = m.group(1) if m else ""
    date = time_str[:10] if time_str else ""
    
    if date < CUTOFF or not date:
        continue
    
    records.append({
        "type": rtype,
        "value": val,
        "unit": unit,
        "source": source,
        "date": date,
    })

print(f"匹配到 {len(records)} 条（{ALLOWED_SOURCES}）")

# ── 统计 ──
by_type = {}
for r in records:
    t = r["type"]
    if t not in by_type:
        by_type[t] = []
    by_type[t].append(r)

print("\n数据类型:")
for t, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
    sources = set(i["source"] for i in items)
    print(f"  {t}: {len(items)} 条 | {', '.join(sources)}")

# ── 写入报告 ──
PATH = os.path.join(OUT, "health_cda_records.md")
with open(PATH, "w", encoding="utf-8") as f:
    f.write("# export_cda.xml 提取数据\n\n")
    f.write(f"提取日期: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 范围: {CUTOFF}~至今\n")
    f.write(f"仅保留: {', '.join(ALLOWED_SOURCES)}\n\n---\n\n")
    
    # 体脂
    if "HKQuantityTypeIdentifierBodyFatPercentage" in by_type:
        f.write("## 体脂率\n\n| 日期 | 体脂(%) | 来源 |\n|------|---------|------|\n")
        for r in sorted(by_type["HKQuantityTypeIdentifierBodyFatPercentage"], key=lambda x: x["date"], reverse=True):
            v = float(r["value"]) * 100 if r["value"] and float(r["value"]) < 1 else r["value"]
            f.write(f"| {r['date']} | {v} | {r['source']} |\n")
        f.write("\n")
    
    # 体重
    if "HKQuantityTypeIdentifierBodyMass" in by_type:
        f.write("## 体重\n\n| 日期 | 体重(kg) | 来源 |\n|------|---------|------|\n")
        for r in sorted(by_type["HKQuantityTypeIdentifierBodyMass"], key=lambda x: x["date"], reverse=True):
            f.write(f"| {r['date']} | {r['value']} | {r['source']} |\n")
        f.write("\n")
    
    # 饮水
    if "HKQuantityTypeIdentifierDietaryWater" in by_type:
        f.write("## 饮水\n\n| 日期 | 水量(ml) | 来源 |\n|------|---------|------|\n")
        for r in sorted(by_type["HKQuantityTypeIdentifierDietaryWater"], key=lambda x: x["date"], reverse=True)[:60]:
            f.write(f"| {r['date']} | {r['value']} | {r['source']} |\n")
        f.write("\n")
    
    # 饮食热量
    if "HKQuantityTypeIdentifierDietaryEnergyConsumed" in by_type:
        f.write("## 饮食热量\n\n| 日期 | 热量(kcal) | 来源 |\n|------|-----------|------|\n")
        for r in sorted(by_type["HKQuantityTypeIdentifierDietaryEnergyConsumed"], key=lambda x: x["date"], reverse=True)[:60]:
            f.write(f"| {r['date']} | {r['value']} | {r['source']} |\n")
        f.write("\n")
    
    # 其他
    for t in ["HKQuantityTypeIdentifierDietaryProtein", "HKQuantityTypeIdentifierDietaryFatTotal",
              "HKQuantityTypeIdentifierDietaryCarbohydrates", "HKQuantityTypeIdentifierDietaryFiber",
              "HKQuantityTypeIdentifierDietarySugar", "HKQuantityTypeIdentifierDietarySodium",
              "HKQuantityTypeIdentifierDietaryCaffeine", "HKQuantityTypeIdentifierDietaryCholesterol"]:
        if t in by_type:
            label = t.replace("HKQuantityTypeIdentifierDietary", "")
            f.write(f"## 饮食{label}\n\n| 日期 | 数值 | 单位 | 来源 |\n|------|------|------|------|\n")
            for r in sorted(by_type[t], key=lambda x: x["date"], reverse=True)[:20]:
                f.write(f"| {r['date']} | {r['value']} | {r['unit']} | {r['source']} |\n")
            f.write("\n")
    
    # 其他未列出的
    handled = {"HKQuantityTypeIdentifierBodyFatPercentage", "HKQuantityTypeIdentifierBodyMass",
               "HKQuantityTypeIdentifierDietaryWater", "HKQuantityTypeIdentifierDietaryEnergyConsumed",
               "HKQuantityTypeIdentifierDietaryProtein", "HKQuantityTypeIdentifierDietaryFatTotal",
               "HKQuantityTypeIdentifierDietaryCarbohydrates", "HKQuantityTypeIdentifierDietaryFiber",
               "HKQuantityTypeIdentifierDietarySugar", "HKQuantityTypeIdentifierDietarySodium",
               "HKQuantityTypeIdentifierDietaryCaffeine", "HKQuantityTypeIdentifierDietaryCholesterol"}
    others = [t for t in by_type if t not in handled]
    if others:
        f.write("## 其他\n\n")
        for t in others:
            f.write(f"### {t}\n\n| 日期 | 数值 | 单位 | 来源 |\n|------|------|------|------|\n")
            for r in sorted(by_type[t], key=lambda x: x["date"], reverse=True)[:15]:
                f.write(f"| {r['date']} | {r['value']} | {r['unit']} | {r['source']} |\n")
            f.write("\n")
    
    f.write("---\n由 export_cda.xml 提取\n")

print(f"\n报告已保存: {PATH}")

# 摘要
print(f"\n摘要:")
for t, items in sorted(by_type.items(), key=lambda x: -len(x[1])):
    print(f"  {t}: {len(items)} 条")
