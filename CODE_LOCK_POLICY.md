# HCIS Code Lock Policy v2.0

## Level A — HARD LOCK
不可由实现 Agent 静默修改：
- Domain table names and separation
- Adapter protocol method names
- API contract object names
- Enums with epistemic meaning
- Acceptance tests
- Architecture-freeze P0 tables
- Privacy routing rule
- Source immutability rule

## Level B — CONTROLLED EXTENSION
允许新增，不允许破坏已有：
- API routes
- Repository implementations
- Workers
- UI components
- Provider connectors

## Level C — IMPLEMENTATION AREA
Agent 主要工作区：
- TODO methods
- concrete adapters
- extraction pipelines
- frontend behavior/styles
- performance optimization
- provider-specific code

## Contract Change
若必须修改 Level A：
创建 `CONTRACT_CHANGE_PROPOSAL.md`，说明：
1. blocker
2. why existing contract cannot support requirement
3. schema migration
4. backward compatibility
5. test changes
6. rollback
未经明确接受，不得实施。
