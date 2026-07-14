# -*- coding: utf-8 -*-
"""
Apple Health 全量数据提取 V3
提取导出.xml 中所有 11 种数据 + 睡眠
"""
import os, sys, json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

# ── 路径 ──
BASE = r"D:\wechat\xwechat_files\wxid_7msi24mq8wso12_7744\msg\file\2026-07\导出\apple_health_export"
OUT = r"D:\reasonix-memory\health"

# 找到 2GB 主导出文件
for f in os.listdir(BASE):
    fp = os.path.join(BASE, f)
    if os.path.getsize(fp) > 500 * 1024 * 1024:
        TARGET = fp
        break

CUTOFF = "2000-01-01"  # 不限日期，提取全部

# ── Apple 系统来源识别 ──
APPLE_SOURCES = ["Apple Watch", "Apple", "Watch", "时钟", "健康", "iPhone"]

def is_apple_source(src):
    """判断是否是 Apple 系统原生来源"""
    if not src:
        return False
    for kw in APPLE_SOURCES:
        if kw in src:
            return True
    return False
SLEEP_MAP = {"InBed": "在床", "Unspecified": "未指定", "Core": "核心", "Deep": "深睡", "REM": "REM", "Awake": "清醒"}

print(f"处理: {os.path.basename(TARGET)} | 范围: {CUTOFF}~至今")

# ── 数据容器 ──
d = {}
d["steps"] = {}
d["distance"] = {}
d["rhr"] = {}
d["hr_min"] = {}
d["hr_max"] = {}
d["hrv"] = {}
d["resp"] = {}
d["spo2"] = {}
d["active"] = {}
d["basal"] = {}
d["weight"] = {}
d["bodyfat"] = {}
d["leanmass"] = {}
d["bmi"] = {}
d["water"] = {}
d["sleep_src"] = {}

context = ET.iterparse(TARGET, events=("end",))
total = 0
matched = 0

for event, elem in context:
    total += 1
    if elem.tag != "Record":
        elem.clear()
        continue
    if total % 800000 == 0:
        print(f"  扫到 {total//10000}万 ...")

    rtype = elem.get("type", "")
    val = elem.get("value", "")
    sdate = elem.get("startDate", "")
    edate = elem.get("endDate", "")
    date = sdate[:10]
    src_name = elem.get("sourceName", "")
    if date < CUTOFF:
        elem.clear()
        continue

    # 非 Apple 系统来源跳过（睡眠单独处理）
    if rtype != "HKCategoryTypeIdentifierSleepAnalysis" and not is_apple_source(src_name):
        elem.clear()
        continue

    matched += 1
    try:
        # 睡眠（特殊处理：按来源去重，仅 Apple 系统）
        if rtype == "HKCategoryTypeIdentifierSleepAnalysis":
            src = elem.get("sourceName", "未知").replace(" ", "_")
            if not is_apple_source(src):
                elem.clear()
                continue
            if src not in d["sleep_src"]:
                d["sleep_src"][src] = {}
            if date not in d["sleep_src"][src]:
                d["sleep_src"][src][date] = {}
            try:
                sd = sdate.replace(" +0800", "").replace(" +0000", "").replace("T", " ").strip()[:19]
                ed = edate.replace(" +0800", "").replace(" +0000", "").replace("T", " ").strip()[:19]
                dur = (datetime.strptime(ed, "%Y-%m-%d %H:%M:%S") - datetime.strptime(sd, "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600
            except:
                dur = 0
            label = "其他"
            for k, v in SLEEP_MAP.items():
                if k in val:
                    label = v
                    break
            d["sleep_src"][src][date][label] = d["sleep_src"][src][date].get(label, 0) + dur

        # 步数
        elif rtype == "HKQuantityTypeIdentifierStepCount":
            d["steps"][date] = d["steps"].get(date, 0) + float(val)

        # 步行/跑步距离（米 -> 公里）
        elif rtype == "HKQuantityTypeIdentifierDistanceWalkingRunning":
            d["distance"][date] = d["distance"].get(date, 0) + float(val)

        # 静息心率（取最低）
        elif rtype == "HKQuantityTypeIdentifierRestingHeartRate":
            v = float(val)
            if date not in d["rhr"] or v < d["rhr"][date]:
                d["rhr"][date] = v

        # HRV（取均值）
        elif rtype == "HKQuantityTypeIdentifierHeartRateVariabilitySDNN":
            d["hrv"].setdefault(date, []).append(float(val))

        # 实时心率（范围）
        elif rtype == "HKQuantityTypeIdentifierHeartRate":
            v = float(val)
            if date not in d["hr_min"] or v < d["hr_min"][date]:
                d["hr_min"][date] = v
            if date not in d["hr_max"] or v > d["hr_max"][date]:
                d["hr_max"][date] = v

        # 呼吸频率
        elif rtype == "HKQuantityTypeIdentifierRespiratoryRate":
            d["resp"].setdefault(date, []).append(float(val))

        # 血氧
        elif rtype == "HKQuantityTypeIdentifierOxygenSaturation":
            d["spo2"].setdefault(date, []).append(float(val))

        # 活动消耗
        elif rtype == "HKQuantityTypeIdentifierActiveEnergyBurned":
            d["active"][date] = d["active"].get(date, 0) + float(val)

        # 基础消耗
        elif rtype == "HKQuantityTypeIdentifierBasalEnergyBurned":
            d["basal"][date] = d["basal"].get(date, 0) + float(val)

        # 体重
        elif rtype == "HKQuantityTypeIdentifierBodyMass":
            if date not in d["weight"]:
                d["weight"][date] = float(val)

        # 体脂率
        elif rtype == "HKQuantityTypeIdentifierBodyFatPercentage":
            if date not in d["bodyfat"]:
                d["bodyfat"][date] = float(val)

        # 去脂体重
        elif rtype == "HKQuantityTypeIdentifierLeanBodyMass":
            if date not in d["leanmass"]:
                d["leanmass"][date] = float(val)

        # BMI
        elif rtype == "HKQuantityTypeIdentifierBodyMassIndex":
            if date not in d["bmi"]:
                d["bmi"][date] = float(val)

        # 饮水
        elif rtype == "HKQuantityTypeIdentifierDietaryWater":
            d["water"][date] = d["water"].get(date, 0) + float(val)

    except Exception as e:
        pass

    elem.clear()

print(f"扫描完成: {total} 条, 匹配 {matched} 条")

# ── 生成报告 ──
PATH = os.path.join(OUT, "health_history_complete.md")
with open(PATH, "w", encoding="utf-8") as f:
    f.write("# Apple Health 全量数据报告\n\n")
    f.write(f"提取日期: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 数据范围: {CUTOFF}~至今\n\n---\n\n")

    # 1. 体重/体脂
    if d["weight"] or d["bodyfat"]:
        f.write("## 身体成分\n\n| 日期 | 体重(kg) | 体脂(%) | 去脂体重(kg) | BMI |\n")
        f.write("|------|---------|---------|-------------|-----|\n")
        all_wdates = set(list(d["weight"].keys()) + list(d["bodyfat"].keys()) + list(d["leanmass"].keys()) + list(d["bmi"].keys()))
        for dt in sorted(all_wdates, reverse=True)[:60]:
            w = d["weight"].get(dt, "")
            bf = d["bodyfat"].get(dt, "")
            lm = d["leanmass"].get(dt, "")
            bmi = d["bmi"].get(dt, "")
            ws = f"{w:.1f}" if w != "" else ""
            bfs = f"{bf*100:.1f}" if bf != "" and bf < 1 else (f"{bf:.1f}" if bf != "" else "")
            lms = f"{lm:.1f}" if lm != "" else ""
            bmis = f"{bmi:.1f}" if bmi != "" else ""
            f.write(f"| {dt} | {ws} | {bfs} | {lms} | {bmis} |\n")
        f.write("\n")

    # 2. 睡眠
    if d["sleep_src"]:
        all_dates = set()
        for src, days in d["sleep_src"].items():
            all_dates.update(days.keys())
        f.write("## 睡眠数据\n\n| 日期 | 总睡眠 | 深睡 | REM | 核心 | 清醒 | 来源 |\n")
        f.write("|------|--------|------|-----|------|------|------|\n")
        for dt in sorted(all_dates, reverse=True)[:30]:
            candidates = []
            for src, days in d["sleep_src"].items():
                if dt not in days:
                    continue
                dd = days[dt]
                total = dd.get("深睡", 0) + dd.get("REM", 0) + dd.get("核心", 0)
                if 0 < total < 24:
                    candidates.append((total, src, dd))
            if not candidates:
                continue
            best = min(candidates, key=lambda x: abs(x[0] - 7.5) if 4 <= x[0] <= 10 else 999)
            ts, src_name, dd = best
            f.write(f"| {dt} | {ts:.1f}h | {dd.get('深睡',0):.1f}h | {dd.get('REM',0):.1f}h | {dd.get('核心',0):.1f}h | {dd.get('清醒',0):.1f}h | {src_name} |\n")
        f.write("\n")

    # 3. 心率
    if d["rhr"]:
        f.write("## 静息心率\n\n| 日期 | RHR |\n|------|-----|\n")
        for dt in sorted(d["rhr"].keys(), reverse=True)[:30]:
            f.write(f"| {dt} | {d['rhr'][dt]:.0f} |\n")
        vals = list(d["rhr"].values())
        f.write(f"\n范围: {min(vals):.0f}~{max(vals):.0f} | 平均: {sum(vals)/len(vals):.0f} BPM\n\n")

    if d["hr_min"]:
        f.write("## 实时心率范围\n\n| 日期 | 最低 | 最高 | HRV |\n|------|------|------|-----|\n")
        for dt in sorted(d["hr_min"].keys(), reverse=True)[:30]:
            hrv_avg = ""
            if d["hrv"].get(dt):
                hrv_avg = f"{sum(d['hrv'][dt])/len(d['hrv'][dt]):.0f}"
            f.write(f"| {dt} | {d['hr_min'][dt]:.0f} | {d['hr_max'].get(dt,0):.0f} | {hrv_avg} |\n")
        f.write("\n")

    # 4. 每日活动
    if d["steps"]:
        f.write("## 每日活动\n\n| 日期 | 步数 | 距离(km) | 活动(kcal) | 基础(kcal) |\n")
        f.write("|------|------|---------|-----------|-----------|\n")
        for dt in sorted(d["steps"].keys(), reverse=True)[:30]:
            steps = d["steps"].get(dt, 0)
            dist = d["distance"].get(dt, 0) / 1000
            act = d["active"].get(dt, 0)
            bas = d["basal"].get(dt, 0)
            f.write(f"| {dt} | {steps:.0f} | {dist:.2f} | {act:.0f} | {bas:.0f} |\n")
        f.write("\n")

    # 5. 呼吸/血氧
    if d["resp"] or d["spo2"]:
        f.write("## 呼吸与血氧\n\n| 日期 | 呼吸(次/分) | 血氧(%) |\n")
        f.write("|------|------------|--------|\n")
        all_rd = set(list(d["resp"].keys()) + list(d["spo2"].keys()))
        for dt in sorted(all_rd, reverse=True)[:30]:
            resp_avg = ""
            spo2_avg = ""
            if d["resp"].get(dt):
                resp_avg = f"{sum(d['resp'][dt])/len(d['resp'][dt]):.1f}"
            if d["spo2"].get(dt):
                spo2_avg = f"{sum(d['spo2'][dt])/len(d['spo2'][dt])*100:.1f}"
            f.write(f"| {dt} | {resp_avg} | {spo2_avg} |\n")
        f.write("\n")

    # 6. 饮水
    if d["water"]:
        f.write("## 饮水\n\n| 日期 | 饮水量(ml) |\n")
        f.write("|------|-----------|\n")
        for dt in sorted(d["water"].keys(), reverse=True)[:30]:
            f.write(f"| {dt} | {d['water'][dt]:.0f} |\n")
        f.write("\n")

    f.write("---\n由 Apple Health 导出.xml 全量提取 V3\n")

print(f"全量报告已保存: {PATH}")

# ── 摘要 ──
summary = {
    "提取日期": datetime.now().strftime("%Y-%m-%d"),
    "数据类型": {k: len(v) for k, v in d.items() if isinstance(v, dict) and k != "sleep_src"},
    "睡眠来源": {k: len(v) for k, v in d["sleep_src"].items()},
}
rhr_vals = list(d.get("rhr", {}).values())
if rhr_vals:
    summary["RHR"] = {"平均": f"{sum(rhr_vals)/len(rhr_vals):.0f}", "最低": f"{min(rhr_vals):.0f}", "最高": f"{max(rhr_vals):.0f}"}

with open(os.path.join(OUT, "health_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(f"摘要: {json.dumps(summary, ensure_ascii=False, indent=2)}")
