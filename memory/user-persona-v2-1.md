---
name: user-persona-v2-1
title: 用户数字孪生档案V2.1
description: 用户档案V2.1：新增黄河五产品/策略优先级/SimNow tick修复/出租屋设备
metadata:
  type: project
---

## 用户档案已更新至V2.1

**新增内容：**
- 黄河五产品：年化15%/回撤2%/市场中性/规模上限2亿/目前1800万（自营搜不到）
- 三条策略优先级：多空(日频) > 板块轮动(周频) > 情绪因子，彼此不冲突
- SimNow卡单根因已定位+修复：tick_size表不对导致报价被拒，contract_specs.py已添加TICK_SIZE_MAP
- 出租屋电脑配置比公司好，可以完美跑策略

**待补充：** 公司联网公开信息（中基协/天眼查反爬，暂未获取到）

**待做事项：** SimNow修复后需用户验证是否不再撤单

详细档案见 `.reasonix/skills/user-persona.md`
