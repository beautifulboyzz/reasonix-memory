# -*- coding: utf-8 -*-
"""
Apple Health 导出.xml 流式提取器 V2
提取：睡眠、心率、步数、活动能量、HRV、呼吸频率
"""
import os, sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json

sys.stdout.reconfigure(encoding='utf-8')

# ── 路径 ──
BASE_DIR = r"D:\wechat\xwechat_files\wxid_7msi24mq8wso12_7744\msg\file\2026-07\导出\apple_health_export"
OUTPUT_DIR = r"D:\reasonix-memory\health"

xml_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.xml')]
TARGET = None
for f in xml_files:
    fp = os.path.join(BASE_DIR, f)
    if os.path.getsize(fp) > 500 * 1024 * 1024:
        TARGET = fp
        break
if not TARGET:
    print("❌ 未找到大导出文件")
    sys.exit(1)

CUTOFF = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
# ── 睡眠映射 ──
SLEEP_MAP = {"InBed": "在床", "Unspecified": "未指定", "Core": "核心", "Deep": "深睡", "REM": "REM", "Awake": "清醒"}

print(f"处理: {os.path.basename(TARGET)} | 范围: {CUTOFF}~至今")

# ── 第一遍扫描：只收集日期+数值，不存原始记录 ──
data = {
    "sleep_src": {},    # source -> date -> {label: hours}
    "rhr": {},          # date -> min value
    "hrv": {},          # date -> list of values
    "steps": {},        # date -> total steps
    "active": {},       # date -> total active kcal
    "basal": {},        # date -> total basal kcal
    "resp": {},         # date -> list of resp rates
    "hr_min": {},       # date -> min HR
    "hr_max": {},       # date -> max HR
}

context = ET.iterparse(TARGET, events=("end",))
total = 0
matched = 0
for event, elem in context:
    total += 1
    if total % 800000 == 0:
        print(f" 扫到 {total//10000}万 ...")

    if elem.tag == "Record":
        rtype = elem.get("type", "")
        val = elem.get("value", "")
        sdate = elem.get("startDate", "")
        edate = elem.get("endDate", "")
        d = sdate[:10]
        if d < CUTOFF:
            elem.clear()
            continue

        matched += 1

        # ── 睡眠（按来源分别记录，最后选完整度最高的） ──
        if rtype == "HKCategoryTypeIdentifierSleepAnalysis":
            src = elem.get("sourceName", "未知")
            if "sleep_src" not in data:
                data["sleep_src"] = {}  # source -> date -> {label: hours}
            src_key = src.replace(" ", "_")
            if src_key not in data["sleep_src"]:
                data["sleep_src"][src_key] = {}
            src_data = data["sleep_src"][src_key]
            if d not in src_data:
                src_data[d] = {}
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
            src_data[d][label] = src_data.get(d, {}).get(label, 0) + dur

        # ── 睡眠 ── 上面已经处理了带来源的版本

        # ── 静息心率 ──
        elif rtype == "HKQuantityTypeIdentifierRestingHeartRate":
            try:
                v = float(val)
                if d not in data["rhr"] or v < data["rhr"][d]:
                    data["rhr"][d] = v
            except:
                pass

        # ── HRV ──
        elif rtype == "HKQuantityTypeIdentifierHeartRateVariabilitySDNN":
            try:
                data["hrv"].setdefault(d, []).append(float(val))
            except:
                pass

        # ── 步数 ──
        elif rtype == "HKQuantityTypeIdentifierStepCount":
            try:
                data["steps"][d] = data["steps"].get(d, 0) + float(val)
            except:
                pass

        # ── 活动消耗 ──
        elif rtype == "HKQuantityTypeIdentifierActiveEnergyBurned":
            try:
                data["active"][d] = data["active"].get(d, 0) + float(val)
            except:
                pass

        # ── 基础消耗 ──
        elif rtype == "HKQuantityTypeIdentifierBasalEnergyBurned":
            try:
                data["basal"][d] = data["basal"].get(d, 0) + float(val)
            except:
                pass

        # ── 呼吸频率 ──
        elif rtype == "HKQuantityTypeIdentifierRespiratoryRate":
            try:
                data["resp"].setdefault(d, []).append(float(val))
            except:
                pass

        # ── 实时心率（计算当日 min/max） ──
        elif rtype == "HKQuantityTypeIdentifierHeartRate":
            try:
                v = float(val)
                if d not in data["hr_min"] or v < data["hr_min"][d]:
                    data["hr_min"][d] = v
                if d not in data["hr_max"] or v > data["hr_max"][d]:
                    data["hr_max"][d] = v
            except:
                pass

    elem.clear()

print(f"\n扫描完成: {total} 条, 匹配 {matched} 条")

# ── 写入 Markdown 报告 ──
PATH = os.path.join(OUTPUT_DIR, "health_history.md")
with open(PATH, "w", encoding="utf-8") as f:
    f.write("# Apple Health 历史数据\n\n")
    f.write(f"提取日期: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 数据范围: {CUTOFF}~至今\n\n---\n\n")

    # ── 睡眠（多来源去重：每天选总时长最合理的一组） ──
    if "sleep_src" in data and data["sleep_src"]:
        # 合并每天所有 source 的数据
        all_dates = set()
        for src, days in data["sleep_src"].items():
            all_dates.update(days.keys())
        
        f.write("## 睡眠数据（自动去重）\n\n| 日期 | 总睡眠 | 深睡 | REM | 核心 | 清醒 | 数据来源 |\n")
        f.write("|------|--------|------|-----|------|------|---------|\n")
        for d in sorted(all_dates, reverse=True)[:30]:
            # 评估每个 source 的合理性，选最好的
            candidates = []
            for src, days in data["sleep_src"].items():
                if d not in days:
                    continue
                dd = days[d]
                total = dd.get("深睡", 0) + dd.get("REM", 0) + dd.get("核心", 0)
                inbed = dd.get("在床", 0)
                if total > 0:
                    candidates.append((total, inbed, src, dd))
            
            if not candidates:
                continue
            
            # 选择标准：总时长在 4~10h 之间最接近 7.5h 的
            best = min(candidates, key=lambda x: abs(x[0] - 7.5) if 4 <= x[0] <= 10 else 999)
            total_s, inbed_s, src_name, dd = best
            
            f.write(f"| {d} | {total_s:.1f}h | {dd.get('深睡', 0):.1f}h | {dd.get('REM', 0):.1f}h | {dd.get('核心', 0):.1f}h | {dd.get('清醒', 0):.1f}h | {src_name} |\n")
        f.write("\n")

    # ── 静息心率 ──
    if data["rhr"]:
        f.write("## 静息心率 (RHR)\n\n| 日期 | RHR |\n|------|-----|\n")
        for d in sorted(data["rhr"].keys(), reverse=True)[:30]:
            f.write(f"| {d} | {data['rhr'][d]:.0f} BPM |\n")
        vals = list(data["rhr"].values())
        avg = sum(vals)/len(vals); mn = min(vals); mx = max(vals)
        f.write(f"\n范围: {mn:.0f}~{mx:.0f} | 平均: {avg:.0f} BPM\n\n")

    # ── HRV ──
    if data["hrv"]:
        f.write("## HRV (SDNN)\n\n| 日期 | HRV (ms) |\n|------|----------|\n")
        for d in sorted(data["hrv"].keys(), reverse=True)[:30]:
            avg_v = sum(data["hrv"][d])/len(data["hrv"][d])
            f.write(f"| {d} | {avg_v:.0f} |\n")
        f.write("\n")

    # ── 步数 ──
    if data["steps"]:
        f.write("## 步数\n\n| 日期 | 步数 |\n|------|------|\n")
        for d in sorted(data["steps"].keys(), reverse=True)[:30]:
            f.write(f"| {d} | {data['steps'][d]:.0f} |\n")
        f.write("\n")

    # ── 活动消耗 ──
    if data["active"]:
        f.write("## 活动消耗\n\n| 日期 | 活动(kcal) | 基础(kcal) |\n|------|-----------|-----------|\n")
        for d in sorted(data["active"].keys(), reverse=True)[:30]:
            act = data["active"].get(d, 0)
            bas = data["basal"].get(d, 0)
            f.write(f"| {d} | {act:.0f} | {bas:.0f} |\n")
        f.write("\n")

    # ── 呼吸频率 ──
    if data["resp"]:
        f.write("## 呼吸频率\n\n| 日期 | 呼吸(次/分) |\n|------|------------|\n")
        for d in sorted(data["resp"].keys(), reverse=True)[:30]:
            avg_v = sum(data["resp"][d])/len(data["resp"][d])
            f.write(f"| {d} | {avg_v:.1f} |\n")
        f.write("\n")

    # ── 实时心率范围 ──
    if data["hr_min"]:
        f.write("## 实时心率范围\n\n| 日期 | 最低 | 最高 |\n|------|------|------|\n")
        for d in sorted(data["hr_min"].keys(), reverse=True)[:30]:
            f.write(f"| {d} | {data['hr_min'][d]:.0f} | {data['hr_max'].get(d, 0):.0f} |\n")
        f.write("\n")

    f.write("---\n由 Apple Health 导出.xml 自动提取\n")

print(f"报告已保存: {PATH}")

# ── 摘要 ──
rhr_vals = list(data.get('rhr', {}).values())
if rhr_vals:
    rhr_avg = sum(rhr_vals)/len(rhr_vals)
    rhr_min = min(rhr_vals)
    rhr_max = max(rhr_vals)
else:
    rhr_avg = rhr_min = rhr_max = None

summary = {
    "提取日期": datetime.now().strftime("%Y-%m-%d"),
    "RHR": {"平均": f"{rhr_avg:.0f}" if rhr_avg else None, "最低": f"{rhr_min:.0f}" if rhr_min else None, "最高": f"{rhr_max:.0f}" if rhr_max else None},
    "记录天数": {"睡眠(来源数)": len(data.get('sleep_src', {})), "步数": len(data.get('steps', {})), "HRV": len(data.get('hrv', {})), "RHR": len(data.get('rhr', {}))},
}
with open(os.path.join(OUTPUT_DIR, "health_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(f"摘要: {summary}")
