---
name: ec-tick-fix-0-5
title: ec(欧线) tick=0.5 修复
description: ec(欧线) tick=0.5 不是 0.1，contract_specs.py 已修
metadata:
  type: project
---

## ec(欧线) tick 修复（2026-06-11 15:30）

### 问题
ec2607 所有报单被 INE 拒绝「价格非最小单位的倍数」
- 6/9 前次 session：3938.0 能成交、3938.2/3938.4 被拒
- 6/11今天：所有价格被拒

### 根因
`contract_specs.py` 的 `TICK_SIZE_MAP` 里 ec 配置为 **0.1**，但实际 ec（欧线集运期货）的 tick size 是 **0.5**。

报价 3938.4(=7876.8个tick) 不是 0.5 的倍数，3938.0(=7876个tick) 是。

### 修复
`contract_specs.py` 第29行：`"ec": 0.1` → `"ec": 0.5`

### 同时已完成的改进
`aggressive_executor.py` 新增 `_round_to_tick()` 函数，用 Decimal 精确修约到 tick 整数倍，避免浮点精度问题（对其他品种也有预防作用）。

### 下次重启bot后生效
