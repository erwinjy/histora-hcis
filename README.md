# HCIS RC0 Code-Locked Bootstrap v2.0

这不是“设计文档包”，而是 **代码级约束的可运行工程骨架**。

## 目标

其他 Agent 的任务不再是重新设计 HCIS，而是：

> 在既有目录、数据库 Schema、Domain Contract、Adapter Contract、Route Contract、Acceptance Tests 内补齐实现。

## 代码锁原则

以下内容属于 **LOCKED CONTRACT**，Agent 不得自行删除、重命名、改语义：

- `backend/hcis/domain/contracts.py`
- `backend/hcis/domain/models.py`
- `backend/hcis/adapters/contracts.py`
- `backend/hcis/model_control/contracts.py`
- `backend/hcis/acquisition/contracts.py`
- `backend/hcis/storage/contracts.py`
- `backend/hcis/core/enums.py`
- `backend/hcis/api/contracts.py`
- `schemas/*.json`
- `tests/acceptance/*`
- `CODE_LOCK_MANIFEST.json`

修改任何锁定文件后，必须：
1. 明确提出 `CONTRACT_CHANGE_PROPOSAL.md`
2. 说明原因和迁移方案
3. 重新生成 Code Lock Manifest
4. 重新执行所有 Acceptance/Adversarial Tests
5. 不允许“为了方便实现”静默改动

## 启动目标

后端：
```bash
cd backend
python -m hcis.main
```

前端：
```bash
cd frontend
npm install
npm run dev
```

Code Lock：
```bash
python scripts/verify_code_lock.py
```

## Agent 执行入口

`RUN_AGENT_PROMPT.txt`
