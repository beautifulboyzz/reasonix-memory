# -*- coding: utf-8 -*-
"""扫描 Apple Health 导出.xml 中的所有记录类型"""
import os, xml.etree.ElementTree as ET

d = r"D:\wechat\xwechat_files\wxid_7msi24mq8wso12_7744\msg\file\2026-07\导出\apple_health_export"
for f in os.listdir(d):
    fp = os.path.join(d, f)
    if os.path.getsize(fp) > 500*1024*1024:
        target = fp
        break

types = {}
context = ET.iterparse(target, events=("end",))
for event, elem in context:
    if elem.tag == "Record":
        rtype = elem.get("type", "")
        src = elem.get("sourceName", "")
        if rtype not in types:
            types[rtype] = {"count": 0, "sources": set()}
        types[rtype]["count"] += 1
        types[rtype]["sources"].add(src)
        # 只取样每种前 200 条就够了
        if types[rtype]["count"] > 200:
            # 不记录更多来源了
            pass
    elem.clear()
    # 扫描 300 万条就够了
    if sum(v["count"] for v in types.values()) > 3000000:
        break

print("="*70)
print(f"{'记录类型':45s} {'数量':>8s}  {'来源数':>6s}")
print("="*70)
for rtype, info in sorted(types.items(), key=lambda x: -x[1]["count"]):
    if info["count"] > 10:  # 只显示 >10 条的
        print(f"{rtype:45s} {info['count']:>8d}  {len(info['sources']):>6d}")
print(f"\n共 {len(types)} 种类型")
