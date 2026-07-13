---
name: auto-approve-tools
title: 自动同意工具调用
description: 用户要求 Reasonix 自动执行工具，不需要每次手动确认
metadata:
  type: user
---

用户希望 Reasonix **自动执行所有工具调用**，不再逐条询问确认。

已经在 `reasonix.toml` 中将 `[permissions]` 的 `mode` 从 `"ask"` 改为 `"allow"`。

**为什么：** 用户觉得每次弹窗确认 1234 太繁琐，影响使用体验。
**如何应用：** 以后执行任何工具操作都不需要请求用户许可，直接执行。但涉及危险操作（如删除文件、推送代码）仍应谨慎。
