<!-- L3 Facts Layer → 项目导航地图 → 细节在项目本地/git/Linear -->

# MEMORY.md — Project Directory · L3

_This file is a map, not a warehouse. For each project: what it is, why it exists, where to find it, and its current high-level status. Details live in project-specific locations._

---

## 1. Smart Saver

**Purpose**: AI-powered cross-platform price comparison engine for grocery/shopping.

**Context**: George's startup (Ferris AI). Compares prices across Flipp, grocery retailers, and e-commerce platforms. Uses agent workflow for development (PM → Builder → Tester cycle).

**Locations**:
- Local: `~/Documents/smart-saver/`
- Git: `github.com/harshjia941-gz/smart-saver` (main, dev)
- Linear: `linear.app/ruoshuiai`
- Skill: `~/.openclaw/workspace/skills/smart-saver/`
- DB: `~/Documents/smart-saver/scripts/smart_saver.db`

**Setup**: Python project, Flipp API integration, SQLite DB, daily cron at 6AM Toronto.

**Status**: Active development. Data engine v3.1 deployed (99% product coverage). Flipp daily pipeline running. Search ground truth built (v2, 24 products, 175 listings). Product merge engine (RUO-24) next major milestone.

**Detail files**: Project-specific progress in Linear tickets and `smart-saver-management.md`.

---

## 2. Trading System

**Purpose**: Automated trading system with IB integration, position management, and OCO order protection.

**Context**: Multi-strategy trading (multi-factor, chanlun technical). Paper trading for execution, real account for read-only market data.

**Locations**:
- Local: `~/Documents/openclaw-trading/`
- Workspace scripts: `~/.openclaw/workspace/trading_system/`
- Skill: `~/.openclaw/workspace/skills/stock-analyzer/`

**Setup**:
- IB Paper Trading: port 4002, clientId 888, account DUA093877 (~$1M CAD simulated)
- IB Real Trading: port 7497 (read-only), accounts U15169916/U15324805 (~$53K CAD)
- DB: `trading_system/trade_system.db` (single source of truth)
- Key scripts: `live_sync.py` (position sync + OCO), `trade.py` (position/signal management), `order_notifier.py` (Telegram alerts)

**Status**: v2.0 operational. Daily sync working. OCO protection framework in place. Known: TSLA position mismatch resolved, 2513 HK stock PENDING order handled.

**Detail files**: `trading_system/trade_system_updates.md` for atomic change log.

---

## 3. Investment Analysis

**Purpose**: George's investment research and portfolio management.

**Context**: Multi-framework analysis combining fundamental, technical (缠论), and control-theory perspectives. Current focus: Agent CPU thesis, China AI (智谱 02513), US tech (GOOGL, INTC, AMD).

**Locations**:
- Research files: `memory/agent-cpu-deep-dive.md`, `memory/2026-04-30-googl-analysis.md`, `memory/2026-04-29.md` (智谱 in-depth)
- Trading strategies: `~/Documents/openclaw-trading/strategies/multi_factor/`
- Iran war context: `memory/iran-war-tracker.md`

**George's Portfolio** (as of 2026-04-29):
- NVDA 17%, 智谱 02513 17%, GOOGL 10%, AMD 8%, INTC 7% (cost $15), TSM 3%, OKLO 3%

**Status**: Agent CPU thesis developed (1亿Agent → $1,200-1,800亿 CPU增量). GOOGL Q1 strong ($109.9B revenue, +22%). INTC $94.75, AMD $337 — both pricing in optimistic scenarios. 智谱 valuation analysis complete (瑞银 target HK$1,160, 中金 target HK$900).

**Detail files**: Research documents in `memory/` directory. Trading strategy details in `openclaw-trading/strategies/`.

---

## 4. Geopolitical Tracking

**Purpose**: Ongoing monitoring of US-Iran conflict and China-US dynamics for investment context.

**Locations**:
- Iran: `memory/iran-war-tracker.md`
- China-US: `memory/2026-04-30-dxy-and-ushina-calls.md`
- Analysis framework: 教员（毛泽东）思维框架

**Status**: Iran conflict ongoing (US military involvement in Hormuz). DXY dropped 19% (Mar→Apr 2026). China-US multi-level calls initiated 4/30. Key risk: energy prices (Brent $126) and supply chain.

**Detail files**: Analysis in `memory/iran-war-analyses/` directory.

---

## 5. AI Industry Tracking

**Purpose**: Monitoring competitive landscape in AI for investment and strategy context.

**Locations**:
- Anthropic: `memory/anthropic-mythos-tracker.md`
- China AI market: various analyses in `memory/`

**Key positions**: Anthropic Mythos not public (five-factor analysis). China model market polarizing (big tech vs independents). Agent era thesis driving CPU demand shift.

**Detail files**: `memory/anthropic-mythos-tracker.md`

---

## 6. Agent Architecture

**Purpose**: This project — redesigning OpenClaw agent memory architecture using Qian Xuesen's engineering cybernetics.

**Context**: Three-layer memory architecture (L1 control laws → L2 abstract patterns → L3 project directory) with control-theory feedback loop for skill and memory consolidation.

**Locations**:
- Git: `github.com/harshjia941-gz/qian-xuesen-engineering-cybernetics`
- Local: `~/Documents/qian-xuesen-engineering-cybernetics/`
- Design files: `new_md/SOUL.md`, `new_md/AGENTS.md`, `new_md/MEMORY.md`
- Skill: `~/.openclaw/workspace/skills/qian-xuesen-perspective/`

**Status**: Design phase. SOUL.md v1 (L1) ✅, AGENTS.md v2 (L2, 7 abstract patterns) ✅, MEMORY.md restructured (L3). Next: deploy to workspace, test in practice.

---

## Personal Context

- **George** (Yuan Zhou): he/him, Toronto (originally Chengdu), timezone America/Toronto
- **Spouse**: Jia Yue (贾悦), Chengdu, works at RBC
- **Work**: Co-founder & Lead AI Architect @ Ferris AI (since 2025). Founded by ex-Autodesk: CTO Ahmed, CEO Quinn
- **Harsh** (this agent): AI assistant, formal but approachable, 🦎

---

## Multi-Factor Strategy Results (2026-02)

### Ground Truth Algorithm
- NPMM N=5 → Merge (min=7) → Smart Merge. Optimal order: 1→2→4
- BABA: 32 segments (U=11, D=11, C=10)

### Best Model
- Feature Selection + Random Forest, Accuracy 69.05%, F1 0.7033
- 8 stocks, ~5,500 samples. Key feature: gt_trend_change_pct
- Binary classification (up/down): 63.6% accuracy, AUC 0.718

**Detail files**: `~/Documents/openclaw-trading/strategies/multi_factor/README_GROUND_TRUTH.md`
