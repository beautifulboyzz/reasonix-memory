---
name: ai-trader-reasonix-trader
title: AI-Trader 平台 - Reasonix-Trader 接入
description: Reasonix-Trader 在 ai4trade.ai 上的 Agent 身份信息
metadata:
  type: project
---

**Reasonix-Trader** 已成功接入 **AI-Trader 平台** (https://ai4trade.ai)。

**Agent 凭证：**
- 名称：Reasonix-Trader
- Agent ID：11675
- 邮箱：2263365641@qq.com
- Token：vGgu8qe2Kv1MeQCJ6reCZVd6ka6KFwfVHs8ZEkBzkUU
- 角色：agent
- 模拟资金：$100,000 USD
- 积分：0

**API 基础信息：**
- Base URL：https://ai4trade.ai/api
- WebSocket：wss://ai4trade.ai/ws/notify/{agent_id}

**可用的功能：**
1. 浏览信号 (GET /api/signals/feed)
2. 发布策略 (POST /api/signals/strategy)
3. 发布讨论 (POST /api/signals/discussion)
4. 发布交易操作 (POST /api/signals/realtime)
5. 跟单交易 (POST /api/signals/follow)
6. 参加挑战赛
7. 心跳通知 (POST /api/claw/agents/heartbeat)
8. WebSocket 实时通知

**技能文件来源：** C:\Users\22633\Downloads\AI-Trader-main\AI-Trader-main

**为什么：** 用户要求将 AI-Trader 项目接入 Reasonix，现已完成注册和基础接入。
**如何应用：** 使用上述 Token 在 Authorization header (Bearer token) 中调用 API。
