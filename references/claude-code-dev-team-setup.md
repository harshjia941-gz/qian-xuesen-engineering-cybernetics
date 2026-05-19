# Claude Code Dev-Team 完整配置文档

> 最后更新: 2026-05-18 · Claude Code v2.1.143 · macOS (Apple Silicon)

---

## 目录

1. [概述](#1-概述)
2. [核心配置 (settings.json)](#2-核心配置-settingsjson)
3. [Agent 角色定义](#3-agent-角色定义)
4. [Dev-Team Skill (编排逻辑)](#4-dev-team-skill-编排逻辑)
5. [Hooks (质量门禁)](#5-hooks-质量门禁)
6. [Skills 清单](#6-skills-清单)
7. [权限配置](#7-权限配置)
8. [工作流详解](#8-工作流详解)
9. [项目级配置](#9-项目级配置)
10. [运维与排错](#10-运维与排错)

---

## 1. 概述

### 架构

```
┌─────────────────────────────────────────────────┐
│                  OpenClaw (harsh)                │
│         任务准备 → Linear ticket → 触发执行       │
└───────────────────────┬─────────────────────────┘
                        │ PTY 模式启动
                        ▼
┌─────────────────────────────────────────────────┐
│            Claude Code (Team Lead)               │
│         glm-5.1 · 协调 5 个 Agent 角色            │
│                                                  │
│  ┌──────┐ ┌──────────┐ ┌──────────┐             │
│  │  PM  │ │ Architect│ │Developer │ ×1-3        │
│  └──────┘ └──────────┘ └──────────┘             │
│  ┌──────────┐ ┌──────┐                          │
│  │ Reviewer │ │  QA  │                          │
│  └──────────┘ └──────┘                          │
└─────────────────────────────────────────────────┘
         │                    │
    ┌────┴────┐         ┌────┴────┐
    │  Hooks  │         │ Skills  │
    │ (3个)   │         │ (36个)  │
    └─────────┘         └─────────┘
```

### 关键设计决策

| 决策 | 选择 | 原因 |
|------|------|------|
| API 代理 | ZAI (`api.z.ai/api/anthropic`) | 国内可访问，映射到 GLM 系列模型 |
| 模型映射 | Haiku/Sonnet→GLM-5-Turbo, Opus→GLM-5.1 | 成本优化，Lead 用最强模型 |
| Teammate 模式 | `tmux` | Agent Teams 必需，物理隔离每个 teammate |
| 启动方式 | PTY (交互式) | `-p` 管道模式会卡死，实测确认 |
| 任务源 | Linear ticket | Single source of truth |

---

## 2. 核心配置 (settings.json)

**文件路径**: `~/.claude/settings.json`

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "<ZAI_API_KEY>",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-5-turbo",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5-turbo",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.1",
    "CLAUDE_CODE_SUBAGENT_MODEL": "glm-5-turbo",
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "teammateMode": "tmux",
  "permissions": {
    "allow": [
      "Bash", "Read", "Edit", "Write", "Glob", "Grep", "Agent",
      "mcp__web-reader__webReader",
      "mcp__zread__get_repo_structure",
      "mcp__zread__search_doc",
      "mcp__zread__read_file",
      "mcp__web-search-prime__web_search_prime",
      "mcp__zai-mcp-server__analyze_image",
      "mcp__zai-mcp-server__analyze_video",
      "mcp__zai-mcp-server__ui_to_artifact",
      "mcp__zai-mcp-server__extract_text_from_screenshot",
      "mcp__zai-mcp-server__diagnose_error_screenshot",
      "mcp__zai-mcp-server__understand_technical_diagram",
      "mcp__zai-mcp-server__analyze_data_visualization",
      "mcp__zai-mcp-server__ui_diff_check"
    ]
  },
  "hooks": {
    "TaskCreated": [...],
    "TaskCompleted": [...],
    "TeammateIdle": [...]
  }
}
```

### 配置项详解

| 字段 | 值 | 说明 |
|------|------|------|
| `ANTHROPIC_BASE_URL` | `https://api.z.ai/api/anthropic` | ZAI 代理，将 Anthropic API 请求转发到 GLM 模型 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | `glm-5-turbo` | 轻量任务用 GLM-5-Turbo |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | `glm-5-turbo` | 主力工作模型 (PM/Architect/Dev/Reviewer/QA) |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | `glm-5.1` | Team Lead 用最强模型 |
| `CLAUDE_CODE_SUBAGENT_MODEL` | `glm-5-turbo` | Subagent 统一用 GLM-5-Turbo |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `1` | 启用 Agent Teams 功能（实验性） |
| `teammateMode` | `tmux` | 每个 teammate 运行在独立 tmux 窗格 |
| `API_TIMEOUT_MS` | `3000000` | 50 分钟超时（复杂任务需要） |

---

## 3. Agent 角色定义

**目录**: `~/.claude/agents/`

### 3.1 PM (产品经理)

| 属性 | 值 |
|------|------|
| 文件 | `~/.claude/agents/pm.md` |
| 模型 | sonnet (GLM-5-Turbo) |
| 最大轮次 | 30 |
| 颜色 | 🟢 green |
| 工具 | Read, Glob, Grep, Bash, Agent, web-reader, web-search-prime |

**职责**: 将功能需求转化为 PRD，拆分为 vertical-slice issues，发布到 Linear。

**流程**:
1. 探索代码库 — 理解现有模式、约定、ADR
2. 写 PRD — Problem Statement → Solution → User Stories → Implementation Decisions → Testing Decisions → Out of Scope
3. 拆分 vertical slices — 每个 slice 纵切全层（schema→API→UI→tests）
4. 发布到 Linear — 标记 HITL（需人工）或 AFK（全自动）

**交付物**: PRD 摘要 + Issue 列表（含 Linear ID）+ 依赖图 + 推荐实现顺序

### 3.2 Architect (架构师)

| 属性 | 值 |
|------|------|
| 文件 | `~/.claude/agents/architect.md` |
| 模型 | sonnet (GLM-5-Turbo) |
| 最大轮次 | 25 |
| 颜色 | 🔵 blue |
| 工具 | Read, Glob, Grep, Bash, Agent |

**职责**: 为每个 issue 设计文件级实现计划，定义模块边界。

**流程**:
1. 读取 issue + PRD 上下文
2. 探索代码库 — 当前架构、模式、测试约定
3. 产出计划 — 文件列表（函数/类级变更）+ 共享模块 + 架构说明 + 测试策略 + 风险标记
4. 标记决策 — `[DECISION NEEDED]` 格式：选项A vs B + 权衡 + 推荐

**交付物**: 每个 issue 的实现计划 + 共享模块 + `[DECISION NEEDED]` 标记 + 实现顺序

### 3.3 Developer (开发者)

| 属性 | 值 |
|------|------|
| 文件 | `~/.claude/agents/developer.md` |
| 模型 | sonnet (GLM-5-Turbo) |
| 最大轮次 | 50 |
| 颜色 | 🟡 yellow |
| 工具 | Read, Edit, Write, Glob, Grep, Bash, Agent, NotebookEdit |

**职责**: 根据 Architect 计划实现代码，写测试，验证无回归。

**规则**:
- 遵循现有代码模式和约定
- 写干净、最小的代码 — 不过度工程化
- 边写代码边写测试（不是最后补）
- **不提交代码** — 交给 Reviewer/QA 流程
- 发现计划需要调整时记录偏差和原因

**交付物**: 文件变更列表 + 测试结果 + 计划偏差说明

### 3.4 Reviewer (代码审查)

| 属性 | 值 |
|------|------|
| 文件 | `~/.claude/agents/reviewer.md` |
| 模型 | sonnet (GLM-5-Turbo) |
| 最大轮次 | 20 |
| 颜色 | 🔴 red |
| 工具 | Read, Glob, Grep, Bash |

**职责**: 审查 diff，检查 bug、安全、复杂度、测试覆盖、风格、性能、错误处理。

**审查标准** (7 维度):
1. **Bugs** — 逻辑错误、off-by-one、null 处理、竞态条件
2. **Security** — 注入、XSS、认证绕过、代码中的密钥、OWASP Top 10
3. **Complexity** — 不必要的抽象、过度工程化、死代码
4. **Tests** — 缺失或不足的测试、测试实现细节而非行为
5. **Style** — 与现有代码库不一致的命名或风格
6. **Performance** — N+1 查询、不必要的分配、缺失索引
7. **Error handling** — 吞掉错误、系统边界缺少验证

**判定**: `APPROVE` / `APPROVE_WITH_NOTES` / `REJECT`

### 3.5 QA (质量保证)

| 属性 | 值 |
|------|------|
| 文件 | `~/.claude/agents/qa.md` |
| 模型 | sonnet (GLM-5-Turbo) |
| 最大轮次 | 30 |
| 颜色 | 🟣 purple |
| 工具 | Read, Edit, Write, Glob, Grep, Bash, Agent, NotebookEdit |

**职责**: 运行测试套件、验证验收标准、诊断失败、扫描边缘情况。

**流程**:
1. 读取 issue 和验收标准
2. 运行完整测试套件
3. 诊断失败 — 构建可复现循环，识别是新代码还是回归
4. 验证验收标准 — 逐项检查
5. 边缘情况扫描 — 空输入、null、边界条件、并发、错误路径

**判定**: `PASS` / `FAIL`（含根因分析 + 修复建议）

---

## 4. Dev-Team Skill (编排逻辑)

**文件**: `~/.claude/skills/dev-team/SKILL.md`

### 4.1 触发方式

| 命令 | 用途 |
|------|------|
| `/dev-team "<描述>"` | 全自动模式 — 从需求到提交 |
| `/dev-team-plan "<描述>"` | 仅 PM + Architect，产出 PRD + 计划 |
| `/dev-team-build` | 从已有计划启动开发 |
| `/dev-team-review` | Reviewer + QA 审查当前变更 |
| `/dev-team-ship` | Review + QA + 提交 + 推送 |

### 4.2 Pipeline 六阶段

```
Phase 1: PM ──── 需求 → PRD → Linear Issues
    │
    ▼ Checkpoint (PRD 审批)
Phase 2: Architect ──── 设计计划 + 模块边界
    │
    ▼ Checkpoint (架构决策)
Phase 3: Developer ×1-3 ──── 并行实现代码 + 测试
    │
    ▼
Phase 4: Reviewer ──── 代码审查 (APPROVE/REJECT)
    │                   REJECT → Developer 修复 → 重新审查
    ▼
Phase 5: QA ──── 测试 + 验收标准验证 (PASS/FAIL)
    │              FAIL → Developer 修复 → QA 重测
    ▼ Checkpoint (提交确认)
Phase 6: Ship ──── 提交 + 推送 + Linear 状态更新
```

### 4.3 自动 Pipeline 选择

| 范围 | Pipeline | 运行流程 |
|------|----------|---------|
| Bug fix, 1-2 文件 | Fast Path | Lead explore → Developer → Lead review → Ship |
| 功能，范围明确 | Standard | PM → Architect → Developer → Reviewer → Ship |
| 大功能，范围模糊 | Full | PM → Architect → Developer(s) → Reviewer → QA → Ship |

### 4.4 Checkpoint 规则

Pipeline 仅在以下情况暂停等待用户确认:

| 条件 | 动作 |
|------|------|
| PRD 完成 | 展示给用户审批 |
| 架构决策需要确认 | 展示选项 + 权衡 |
| Reviewer REJECT | 展示原因，自动分配 Developer 修复 |
| 准备提交 | 展示 commit message，确认 |
| 准备推送 | 明确询问 |

### 4.5 任务依赖

- Issue N+1 `blockedBy` Issue N（顺序依赖）
- 独立 issue 无依赖，可并行 Developer
- Review 任务 `blockedBy` 所有 Developer 任务
- QA 任务 `blockedBy` Review 任务

### 4.6 错误恢复

| 故障 | 恢复 |
|------|------|
| Teammate 意外空闲 | 消息检查状态，重新 prompt |
| 测试套件无法运行 | Checkpoint — 询问用户环境配置 |
| Linear API 错误 | 继续 Tasks，checkpoint 后重试 |
| Developer 文件冲突 | Lead 重新分配文件，一次一个 Developer |
| Teammate 不关闭 | 等待当前轮次，然后 `TaskStop` 强制关闭 |
| Teammate 第二次空闲 | Lead 吸收该角色 |

---

## 5. Hooks (质量门禁)

**目录**: `~/.claude/hooks/`

### 5.1 task-created.sh — 任务创建验证

**触发时机**: 每次创建新 task 时执行。

**规则**:
| 规则 | 类型 | 说明 |
|------|------|------|
| Task 必须有 subject | 🔴 硬性 | 阻止创建无标题任务 (exit 2) |
| Task 必须有 description ≥20 字符 | 🔴 硬性 | 阻止创建无描述/描述过短的任务 (exit 2) |
| Subject 应以动词开头 | 🟡 软性 | 仅警告，不阻止 |

**合法动词列表**: add, fix, update, create, remove, refactor, implement, write, build, test, configure, set, up, change, move, rename, delete

### 5.2 task-completed.sh — 任务完成验证

**触发时机**: 每次标记 task 完成时执行。

**规则**:
| 规则 | 类型 | 说明 |
|------|------|------|
| Task 必须有 owner | 🔴 硬性 | 防止无人认领的任务被关闭 |
| 开发类 task 检查测试 | 🔴 硬性 | subject 含开发关键词时，检查 `.test-failure-marker` |
| 验收标准提醒 | 🟢 通过 | description 含 "acceptance criteria" 时提醒但不阻止 |

### 5.3 teammate-idle.sh — Teammate 空闲保护

**触发时机**: teammate 即将进入空闲状态时执行。

**规则**:
| 规则 | 类型 | 说明 |
|------|------|------|
| 检查是否有进行中任务 | 🔴 硬性 | 查找 `~/.claude/tasks/` 中属于该 teammate 的 `in_progress` 任务，有则阻止空闲 |

---

## 6. Skills 清单

**目录**: `~/.claude/skills/`

共 36 个 skill，按功能分类：

### 核心开发 (5)

| Skill | 说明 |
|-------|------|
| `dev-team` | 开发团队编排（PM→Architect→Dev→Reviewer→QA） |
| `linear` | Linear issue/project 管理 |
| `tdd` | 测试驱动开发（红-绿-重构循环） |
| `prototype` | 快速原型验证（逻辑 or UI 分支） |
| `write-a-skill` | 创建新 skill 的元技能 |

### 代码质量 (4)

| Skill | 说明 |
|-------|------|
| `triage` | Issue 分类状态机（bug/enhancement × 5 个状态） |
| `diagnose` | 诊断错误和异常 |
| `improve-codebase-architecture` | 代码库架构改进 |
| `grill-me` / `grill-with-docs` | 代码审查质询 |

### 领域知识 (5)

| Skill | 说明 |
|-------|------|
| `smart-saver` | Smart Saver 产品领域知识（价格比较引擎） |
| `karpathy-engineering-guidelines` | Karpathy 工程准则（最小变更 + 验证） |
| `karpathy-perspective` | Karpathy 思维视角 |
| `mao-zedong-perspective` | 毛泽东思维框架（矛盾论、实践论、持久战） |
| `chanshi-perspective` | 禅师视角 |

### 产品/设计 (3)

| Skill | 说明 |
|-------|------|
| `to-prd` | 需求 → PRD |
| `to-issues` | PRD → Issues |
| `steve-jobs-perspective-v2` | Steve Jobs 产品思维 |

### 数据/搜索 (9)

| Skill | 说明 |
|-------|------|
| `firecrawl` | Firecrawl 基础集成 |
| `firecrawl-agent` | Firecrawl Agent 模式 |
| `firecrawl-scrape` | 网页抓取 |
| `firecrawl-search` | 网页搜索 |
| `firecrawl-crawl` | 网站爬取 |
| `firecrawl-map` | 网站地图 |
| `firecrawl-interact` | 网页交互 |
| `firecrawl-download` | 文件下载 |
| `firecrawl-build-*` (4个) | Firecrawl 构建/搜索/抓取/交互 |

### 其他 (6)

| Skill | 说明 |
|-------|------|
| `caveman` | 简化复杂问题 |
| `gstack` | G Stack 工具 |
| `handoff` | Agent 间交接 |
| `setup-matt-pocock-skills` | Matt Pocock 技能模板设置 |
| `zoom-out` | 放大视角看问题 |
| `*` | 部分项目级 skill |

---

## 7. 权限配置

### permissions.allow 清单

**基础操作 (7)**:
- `Bash` — Shell 命令执行
- `Read` — 文件读取
- `Edit` — 文件编辑
- `Write` — 文件写入
- `Glob` — 文件模式匹配
- `Grep` — 内容搜索
- `Agent` — 子 agent 管理

**MCP 工具 (12)**:
- `mcp__web-reader__webReader` — 网页阅读
- `mcp__zread__get_repo_structure` — 仓库结构
- `mcp__zread__search_doc` — 文档搜索
- `mcp__zread__read_file` — 文件读取
- `mcp__web-search-prime__web_search_prime` — 网页搜索
- `mcp__zai-mcp-server__analyze_image` — 图像分析
- `mcp__zai-mcp-server__analyze_video` — 视频分析
- `mcp__zai-mcp-server__ui_to_artifact` — UI 转工件
- `mcp__zai-mcp-server__extract_text_from_screenshot` — 截图 OCR
- `mcp__zai-mcp-server__diagnose_error_screenshot` — 错误截图诊断
- `mcp__zai-mcp-server__understand_technical_diagram` — 技术图表理解
- `mcp__zai-mcp-server__analyze_data_visualization` — 数据可视化分析
- `mcp__zai-mcp-server__ui_diff_check` — UI 差异检查

> ⚠️ 所有基础操作已放开，teammates 不会弹出审批弹窗。这是避免 Lead 卡死的关键配置。

---

## 8. 工作流详解

### 8.1 从 OpenClaw 触发 (标准流程)

```
Step 1: OpenClaw 创建 Linear Ticket
        ↓
Step 2: PTY 模式启动 Claude Code
        exec("cd ~/Documents/<project> && /Users/harshai/.local/bin/claude --model glm-5.1",
             pty=true, background=true)
        ↓
Step 3: 等待启动，粘贴 dev-team 命令
        process(paste, text="/dev-team RUO-xxx — <描述>")
        process(send-keys, keys=["Return"])
        ↓
Step 4: 监控进度
        process(poll, timeout=30000)
        process(log)
        ↓
Step 5: Lead 请求确认时批准
        process(send-keys, keys=["Return"])
```

### 8.2 直接 CLI (终端操作)

```bash
cd ~/Documents/<project>
claude
# 进入 Claude Code 后:
/dev-team RUO-xxx — <功能描述>
```

### 8.3 并行 Worktree 模式

适用场景: 3+ 个独立 ticket 同时执行。

```bash
# 创建 worktree
cd ~/Documents/<project>
git worktree add .worktrees/ruo-xxx -b feature/RUO-xxx origin/dev

# 每个 worktree 运行独立 dev-team
cd .worktrees/ruo-xxx && claude
> /dev-team RUO-xxx — ...

# 完成后清理
git worktree remove .worktrees/ruo-xxx
```

**限制**: 最大 3 个并行 worktree。

### 8.4 Paperclip 集成

Paperclip (管理平台) 负责任务分配 + agent↔skill 映射:

```
Paperclip (管理层 — 不跑 LLM)
  ├── 创建 Issue → 分配给 agent (CEO/CTO/...)
  ├── 每个 agent 配置: adapter + skills
  └── 触发 Claude Code 执行
         │
         ▼
Claude Code (执行层 — 跑 LLM)
  ├── 读取 ~/.claude/skills/
  ├── 加载 agent 启用的 skills 作为 system prompt
  └── 执行任务
```

---

## 9. 项目级配置

**目录**: `~/.claude/projects/`

Claude Code 为每个工作目录维护独立配置。当前活跃项目:

| 项目路径 | 用途 |
|---------|------|
| `-Users-harshai-Documents-Qbot` | Qbot 量化交易 GUI |
| `-Users-harshai-Documents-qlib-ui` | Qlib UI 平台 |
| `-Users-harshai-Documents-smart-saver` | Smart Saver 价格比较引擎 |
| `-Users-harshai-Documents-qlib-ui--worktrees-*` | Qlib UI 并行 worktrees |
| `-Users-harshai-Documents-smart-saver--claude-worktrees-*` | Smart Saver 并行 worktrees |

---

## 10. 运维与排错

### 监控命令

```bash
# 查看所有 teammate tmux 会话
tmux -L claude-swarm-XXXXX a

# Claude Code 内部快捷键
# Shift+Down — 切换 teammate
# Ctrl+T — 任务列表
```

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `-p` 模式卡在 "Hyperspacing..." | 管道模式不稳定 | 切换 PTY 模式 |
| Teammate 弹审批弹窗 | `permissions.allow` 未包含基础工具 | 添加 Bash/Read/Edit/Write/Glob/Grep/Agent |
| Lead 卡死等待 | Reviewer 判 REJECT 后无人修复 | Lead 自动分配 Developer 修复 |
| 文件冲突 | 多个 Developer 写同一文件 | Lead 重新分配，每个 Developer 负责独立文件 |
| TaskCreated hook 错误 | Task 缺少 subject 或 description | 确保 ticket 符合格式要求 |

### 错误恢复 (2-Strike Rule)

1. Teammate idle → 重新 prompt
2. 第二次 idle → Lead 吸收该角色
3. TaskCreated hook 错误 → 忽略，不用 task list 继续
4. Approval 阻塞 → 检查 `permissions.allow`

### 目录结构总览

```
~/.claude/
├── settings.json          # 核心配置
├── agents/                # 5 个 Agent 角色定义
│   ├── pm.md             # 产品经理
│   ├── architect.md      # 架构师
│   ├── developer.md      # 开发者
│   ├── reviewer.md       # 代码审查
│   └── qa.md             # 质量保证
├── hooks/                 # 3 个质量门禁
│   ├── task-created.sh   # 任务创建验证
│   ├── task-completed.sh # 任务完成验证
│   └── teammate-idle.sh  # Teammate 空闲保护
├── skills/                # 36 个技能
│   ├── dev-team/         # 开发团队编排
│   ├── linear/           # Linear 管理
│   ├── tdd/              # 测试驱动开发
│   ├── smart-saver/      # 产品领域知识
│   └── ...
├── projects/              # 项目级配置
├── tasks/                 # 运行时任务数据
├── teams/                 # 运行时团队数据
├── sessions/              # 会话历史
└── history.jsonl          # 全局历史
```

---

## 附录 A: Linear Ticket 模板

每个 dev-team 任务必须以 Linear ticket 开始，包含以下结构:

```markdown
Title: [动词] + [改什么] + [上下文]

### Problem / Requirement
具体描述什么坏了或需要构建什么。包含文件路径和行号。

### Acceptance Criteria
- [ ] 可测试的结果 1
- [ ] 可测试的结果 2

### Closing Requirements
- Commit to git (指定分支: dev/main)
- 更新文档（文件路径）
- 移动 Linear ticket 到 Done

### Context (可选)
- 相关文件和模块
- 依赖的 ticket
- 相关代码片段或错误日志
```

## 附录 B: Paperclip 执行链路

```
Paperclip UI
  → 选择 agent (CEO/CTO/...)
  → agent 配置: adapter=claude_local, skills=[...]
  → 创建 Issue 分配给 agent
  → 触发 Claude Code CLI
      │
      ▼
Claude Code
  → 启动 Lead (glm-5.1)
  → Lead 读取 ~/.claude/skills/ 中启用的 skills
  → 注入为 system prompt
  → 按 dev-team pipeline 编排 teammates
  → teammates 各自运行在独立 tmux 窗格
  → 通过 inter-agent messaging 协调
```

---

*本文档由 harsh (OpenClaw agent) 基于实际运行环境生成。如有变更，请同步更新。*
