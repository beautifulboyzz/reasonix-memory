# -*- coding: utf-8 -*-
"""查看 Apple Health Export 结构"""
import os, xml.etree.ElementTree as ET

d = r"D:\wechat\xwechat_files\wxid_7msi24mq8wso12_7744\msg\file\2026-07\导出\apple_health_export"

# 先看所有 xml 文件名
for f in os.listdir(d):
    fp = os.path.join(d, f)
    if os.path.isfile(fp):
        size_mb = os.path.getsize(fp) / 1024 / 1024
        print(f"  {f}  ({size_mb:.1f} MB)")

# 看 export_cda.xml 的结构
xml_file = os.path.join(d, "export_cda.xml")
print(f"\n读取 {xml_file} 的前30个标签...")
with open(xml_file, 'r', encoding='utf-8') as fh:
    tags = set()
    for i, line in enumerate(fh):
        if i > 5000:
            break
        if '<' in line and '>' in line:
            for c in line:
                if c == '<':
                    start = line.find('<', i) if 'start' in dir() else line.find('<')
                elif c == '>':
                    pass
    # simple approach
    lines = []
    
with open(xml_file, 'r', encoding='utf-8') as fh:
    for i, line in enumerate(fh):
        if i > 5000:
            break
        line = line.strip()
        if line.startswith('<') and not line.startswith('<?xml'):
            # extract tag name
            tag = line.split()[0] if ' ' in line else line.rstrip('>')
            if tag not in ('<HealthData', '</HealthData'):
                if tag not in tags:
                    tags.add(tag)
                    print(f"  {tag}")
