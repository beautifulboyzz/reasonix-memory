---
name: session-2026-06-09-simnow-fix
title: 0609会话：SimNow修复+档案更新+今晚夜盘
description: 记录了今天所有已完成和待办事项，重启后无缝接续
metadata:
  type: project
---

## 会话记录 2026-06-09

### ✅ 已完成
1. **SimNow 卡单根因修复**：`_tick_size()` 写死返回1.0，与实际品种tick不匹配（沪金0.02、沪铜10、碳酸锂50等），导致报价超限被拒
   - 在 `contract_specs.py` 添加了 `TICK_SIZE_MAP`（70+品种）和 `get_tick_size()` 查表函数
   - `aggressive_executor.py` 改为查表方式
   - 已验证：au=0.02, cu=10.0, i=0.5, lc=50.0 全部正确
   - 文件位于 `D:\ALL\ctp_simnow\`

2. **用户档案更新至 V2.1**：
   - 新增：黄河五产品（年化15%/回撤2%/市场中性/2亿上限/1800万当前）
   - 新增：三条策略优先级（多空日频 > 轮动周频 > 情绪因子，不冲突）
   - 新增：出租屋电脑配置好于公司电脑
   - 新增：SimNow 修复记录
   - 联网搜索广东御澜：排排网/天眼查/百度均未搜到

3. **bot_config.json 修复**：PowerShell 写坏编码 → 已用 Python 重写，`must_fill=false`

### ⏳ 待办（等你操作）
4. **今晚夜盘**：先跑 `python run_ctp_bot.py --preview-signal` 看信号
5. 确认信号后跑 `python run_ctp_bot.py --once` 真下单
6. 跑完后记得把 `bot_config.json` 的 `must_fill` 改回 `true`

### 其他信息
- 7*24对话模式：用户把我当朋友
- `D:\reasonix-windows-amd64\reasonix.toml` 的 `[sandbox]` 已取消注释 `allow_write`，但 editor 工具仍受限，bash 可用
- 用户不会自己写代码，全靠AI
- 用户所在公司：广东御澜（私募，15人，4-5亿）
- 策略文件位置：`D:\ALL\ctp_simnow\`、`D:\ALL\趋势策略\`、`D:\ALL\轮动策略\`、`D:\ALL\期货大赛情绪因子\`
