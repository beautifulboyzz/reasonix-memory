import os, xml.etree.ElementTree as ET

d = r"D:\wechat\xwechat_files\wxid_7msi24mq8wso12_7744\msg\file\2026-07\导出\apple_health_export"
for f in os.listdir(d):
    fp = os.path.join(d, f)
    if os.path.getsize(fp) > 500*1024*1024:
        target = fp
        break

sources = set()
counts = {}
context = ET.iterparse(target, events=("end",))
n = 0
for event, elem in context:
    if elem.tag == "Record" and elem.get("type") == "HKCategoryTypeIdentifierSleepAnalysis":
        src = elem.get("sourceName", "unknown")
        sources.add(src)
        counts[src] = counts.get(src, 0) + 1
        n += 1
        if n >= 5000:
            break
    elem.clear()

print("睡眠数据来源:")
for s, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {s}: {c} 条")
print(f"\n总来源数: {len(sources)}")
