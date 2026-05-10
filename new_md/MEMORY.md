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
- Research files: `memory/agent-cpu-deep-dive.md`, `memory/2026-04-30-googl-analysis.md`
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

---

---

<!-- openclaw-memory-promotion:memory:memory/2026-04-23.md:35:75 -->
- - `docs/WORKFLOW.md` — 全 Agent 模式 - `docs/STRATEGY.md` — gstack Office Hour 策略 ### 工作模式确认 **全 Agent 模式**: - harsh = PM + Technical Manager (创建 ticket、分配 Builder/Tester、review MR、报告 George) - Builder Agent = sub-agent 写代码 - Tester Agent = sub-agent 跑测试 - George = 大方向和节奏 ### 下一步 (新 session 继续) 优先级排序: - 🔴 RUO-5: E2E 测试场景扩展 (High) - 🔴 RUO-6: gstack 价格验证 (High) - 🔴 RUO-12: CI/CD 自动化 (High) ### 关键路径 ``` repo: ~/Documents/smart-saver/ skill: ~/.openclaw/workspace/skills/smart-saver/ github: https://github.com/harshjia941-gz/smart-saver linear: https://linear.app/ruoshuiai ``` ## Smart Saver — PM Session: 三方向全面推进 (12:05-19:03 PDT) ### George 确认的三个方向 1. **数据引擎正确性 + 历史积累** — 数据结构完整，积累 2-3 个月 Flipp 数据 2. **功能逻辑** — 核心功能无漏洞，跨平台比价 + 智能替代推荐 3. **数据源调研** — Keepa/Walmart/PC Express 调研 + 接入路线图 ### 完成项 **方向 1:** - ✅ RUO-17: 产品标准化 — 0.9% → **99%** listings 有 product_id - ✅ RUO-18: Schema 迁移 v3.1 — +name/canonical_name/brand/model/key_specs, CHECK(price>0) - ✅ RUO-19: 每日 Flipp cron 管道 — `scripts/daily_flipp_cron.py`, 每天 6AM Toronto - ✅ RUO-22: flipp_search_v2.py retailers→merchants 修复 [score=0.931 recalls=6 avg=1.000 source=memory/2026-04-23.md:35-75]
<!-- openclaw-memory-promotion:memory:memory/2026-04-23.md:112:148 -->
- - `docs/DATA_SOURCE_RESEARCH.md` — 数据源调研报告 - `smart-saver-management.md` — 管理流程 + 教训（workspace 根目录） - `tests/test_data/product_validation.csv` — 200 labeled products - `tests/test_data/model_extraction_validation.csv` — 52 branded products - `tests/unit/test_product_validation.py` — 39 tests - `scripts/daily_flipp_cron.py` — 每日 Flipp 采集管道 ### Linear 状态 (19:30 PDT 最终) - Done: RUO-1~6, RUO-12~23, RUO-28~30 (共 22 个) - Backlog: RUO-7, RUO-8, RUO-9, RUO-10, RUO-11, RUO-24~27 - 总计 30 issues 创建 ### Linear Projects (source of truth) - **D1: Data Engine** (started) — RUO-11/17/18/19/22/23/28/29/30 - **D2: Feature Logic** — RUO-5/6/12/14/15/16/20/24/25/26 - **D3: Data Sources** — RUO-7/8/9/21/27 [score=0.868 recalls=4 avg=1.000 source=memory/2026-04-23.md:112-130]
<!-- openclaw-memory-promotion:memory:memory/2026-04-23.md:141:179 -->
- - brand 75.2%, category 100%, model 76.9% — 清洗后预期会提升 ### 待跟进 - [ ] 执行 RUO-30 清洗 pipeline（pipeline 建好但没跑） - [ ] 启动 RUO-24 产品合并引擎（W18 核心） - [ ] 品牌 75.2% → 数据清洗后预期 85%+ - [ ] model 提取: 电子产品定向优化 (Samsung, Weber, ASUS) - [ ] 每周和 George review ROADMAP - [ ] 保持并行任务 ≤ 5 ## PM Cron 设计 + 自主决策 (19:40-19:55 PDT) ### PM Cron v2.0 上线 - 每小时自动检查 Linear + GitHub MRs - 新增依赖感知逻辑：spawn 前检查依赖 - Open Questions → RUO-32 (避免阻塞) - ticket 状态规则：sub-agent 完成 → REVIEW（George 改 DONE） - Cron 自主推进无阻塞 ticket ### 依赖分析 + 自主决策 **RUO-24 vs RUO-31**: - 结论: RUO-24 design 可以并行 start - 原因: merge 逻辑不依赖 model field 完整度，RUO-31 只提升精度不 enable 功能 - RUO-25/26 blocked by RUO-24，RUO-9 无依赖可随时 start ### Linear Tickets - RUO-31: Fix model extraction (1.2% → 60%+, High, builder sub-agent 跑着) - RUO-32: Open Questions - 等待 George 决策 - RUO-33: Designer - RUO-24 Product Merge Engine Design (spawned) ### Sub-agents Running - RUO-31 builder: feature/RUO-31-model-extraction-fix - RUO-33 designer: feature/RUO-33-product-merge-design ### Scripts Created - scripts/pm_manager.py — PM cron 检查脚本（open MRs、Linear standup） - tasks/pm_hourly_task.md — PM cron task prompt [score=0.849 recalls=4 avg=1.000 source=memory/2026-04-23.md:141-179]
<!-- openclaw-memory-promotion:memory:memory/2026-04-26.md:8:22 -->
- - Candidate: Possible Lasting Truths: - **3对内在张力**：「不预测」vs实际预判、「没有庄家」vs操盘手身份、狂傲vs慈悲 - **关键争议**：缠论不可证伪（类似占星术）、无学术研究验证、无统计数据证明长期盈利 - **缠师判断失误**：6124后仍看多、中石油说便宜 ### 文件位置 - SKILL.md: `skills/chanshi-perspective/SKILL.md` - 调研素材: `skills/chanshi-perspective/references/research/01-06.md` - 精炼评审: `s - confidence: 0.62 - evidence: memory/2026-04-25.md:454-454 - recalls: 0 - status: staged - Candidate: Assistant: 现在 commit： - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-24.txt:183-183 - recalls: 0 - status: staged - Candidate: Assistant: 搞定了。回答你的问题： **数据 single source of truth 以后不会再有问题。** 原因： 1. **物理上只有一个 DB 文件**：`~/Documents/smart-saver/scripts/smart_saver.db` 2. Skill 目录是 **symlink**，不是副本：`~/.openclaw/workspace/skills/smart-saver/scripts/smart_saver.db` → 指向同一个文件 3. 所有脚本的 `DB_PATH = Path(__file__).pa - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-24.txt:184-184 - recalls: 0 - status: staged [score=0.806 recalls=4 avg=1.000 source=memory/2026-04-26.md:8-22]
<!-- openclaw-memory-promotion:memory:memory/2026-04-26.md:18:32 -->
- - Candidate: Assistant: 搞定了。回答你的问题： **数据 single source of truth 以后不会再有问题。** 原因： 1. **物理上只有一个 DB 文件**：`~/Documents/smart-saver/scripts/smart_saver.db` 2. Skill 目录是 **symlink**，不是副本：`~/.openclaw/workspace/skills/smart-saver/scripts/smart_saver.db` → 指向同一个文件 3. 所有脚本的 `DB_PATH = Path(__file__).pa - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-24.txt:184-184 - recalls: 0 - status: staged - Candidate: Assistant: RUO-54 的 CLI 兼容性问题也一并看下——刚才所有脚本从 skill 目录都能正常执行（用 `/usr/bin/python3`），所以核心问题就是 SKILL.md 里的 `python3` 需要改成能在 OpenClaw exec 里跑的写法。这个我更新到 ticket 里就行。 - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-24.txt:185-185 - recalls: 0 - status: staged - Candidate: Assistant: 总结当前状态： | 问题 | 状态 | |------|------| | DB single source of truth | ✅ 已修（symlink） | | Skill 目录旧垃圾清理 | ✅ 已清理 | | sync_skill.sh 修复 | ✅ 已 commit + push | | 数据 pipeline 能正确写入 | ✅ 已验证 | | canonical_name (RUO-45) | 🔴 待做，HIGH | | 搜索精度 (RUO-51) | 🔴 待做，HIGH | | SKILL.md CLI (RU - confidence: 0.58 - evidence: memory/.dreams/session-corpus/2026-04-24.txt:186-186 - recalls: 0 - status: staged [score=0.806 recalls=4 avg=1.000 source=memory/2026-04-26.md:18-32]

## 🌍 美元暴跌 + 中美多层面通话追踪 (2026-04-30)

**完整文件**: `memory/2026-04-30-dxy-and-uschina-calls.md`

**美元**: DXY 3月121→4/30 98.41，一个月暴跌19%
**油价**: Brent飙至$126（战时新高），24h涨13%

**4/30中美两通通话（中方主动发起）**:
1. 王毅→鲁比奥：台湾是

**完整文件**: `memory/2026-04-30-googl-analysis.md`

**George仓位**: GOOGL 成本$200, 10%仓位

**Q1 2026业绩**: 收入$109.9B(+22%), 净利润$62.6B(+81%), Cloud $20B(+63%)
- Cloud backlog $462B, API 160亿tokens/分钟, CapEx上调至$180-190B
- SpaceX持仓6.11% → IPO可能价值$1000亿+
- 分析师共识Strong Buy, 目标价$357-370, 最高$420

**缠论技术面**:
- 周线：盘整突破中枢W1(ZG=$348.75, ZD=$295.91)，第三买点已确认
- 日线：第三买点确认(ZG=$328.38)，向上笔延伸中
- 关键价位：止损$328, 强支撑$296, 周线ZG=$348.75

**4/30盘中**: 财报beat后盘前$374 → 开盘回落至$368
- 建议$368减仓1/3(10%→7%)锁利
- 跳空缺口$350-374大概率回补
- 基本面长期看多 + SpaceX IPO催化剂

---

## Promoted From Short-Term Memory (2026-04-30)

<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:671:694 -->
- - AutoClaw（澳龙）3月上线：国内首个一键本地部署OpenClaw **竞争格局**: - 两级格局：大厂（阿里/字节/腾讯/百度）vs 独立厂商（智谱/MiniMax/DeepSeek/月之暗面） - 大厂自有算力成本远低，阿里云Coding Plan 7.9元/月（智谱149元） - 字节豆包1.55亿用户C端碾压 - DeepSeek核心作者郭达雅离职加入字节（人才向大厂流动） **宏观**: - 《时代》2026十大AI公司：字节/智谱/阿里入选（国际认可） - 国产替代加速，85%政企客户要求国产化模型 - 2026全球AI基础设施支出预计4500亿美元 **分析师覆盖**: - 中金：目标价900港元，跑赢行业，26/27年收入预测30/71亿 - 瑞银：首次覆盖买入，目标价1,160港元，称"中国版Anthropic" - 瑞银按2026E P/S 145x定价，2025-2027E营收CAGR 231% - 华尔街见闻称"泡沫之王"——7亿营收4000亿市值 - 4/24收935港元，4/29收816.5港元 **教员框架核心结论**: - 主要矛盾：技术领先性 vs 商业化可持续性 - 次要矛盾：独立厂商vs大厂挤压、估值泡沫vs长期价值、短期现金流vs长期投入 - 判断：长期看多（国产替代结构性+独立大模型稀缺性），中期高度不确定（483x P/S定价了完美执行），短期波动极大 [score=0.928 recalls=7 avg=1.000 source=memory/2026-04-29.md:671-694]

## Promoted From Short-Term Memory (2026-05-05)

<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:853:884 -->
- - Fortune, WSJ, Yahoo Finance, Reuters, CNBC, Forbes - Motley Fool, SeekingAlpha, TipRanks, MarketBeat - TechCrunch, ServeTheHome, NextPlatform - More Than Moore(Substack), Counterpoint Research - 搜索时间: 2026-04-29 18:47-19:15 PDT --- ## 智谱 02513 增量分析 + "Agent时代最大受益者"论证 (20:28-21:50 PDT) ### 背景 今日智谱盘中：高开850→回调799→反弹880。George要求在之前分析基础上继续深入。提供了"Scaling Pain: 超大规模Coding Agent推理实践"文章。 ### 核心发现 #### 1. "Scaling Pain"文章关键数据 - "每天数亿次Coding Agent调用" → 验证API ARR真实性 - 3个月3个大版本 → 中国迭代速度第一 - Bug Fix #2贡献SGLang社区(PR #22811) - LayerSplit优化：40K-120K上下文吞吐+10-132% #### 2. 中国模型成本结构完全不同于美国（关键修正） - DS V4-Pro 2.5折缓存命中$0.0036/MTok = Claude Opus 4.7的0.7% - GLM-5.1原价缓存命中$0.475 = Claude的95%（几乎持平） - Agent场景缓存命中率决定成本（George判断正确） #### 3. 智谱 vs Anthropic对比 - Anthropic: $1万亿估值, $300亿ARR(2026.3), Opus 4.7 $5/$25/MTok - 智谱: $450亿HKD, ~17亿RMB ARR(账面), GLM-5.1 $0.52/$4.40 = 1/6~1/10 - 智谱领先国内大厂~2个月，落后Anthropic ~2-3个月 - 价格永远在Anthropic对标模型~1/10（George核心假设） #### 4. Coding Plan Token经济学 [score=1.000 recalls=7 avg=1.000 source=memory/2026-04-29.md:853-884]

## Promoted From Short-Term Memory (2026-05-06)

<!-- openclaw-memory-promotion:memory:memory/2026-04-29.md:590:612 -->
- - 存储：5 EB高性能NVMe（Agent长期记忆+KV Cache持久化） - 网络：708 TB/秒持续东西向流量 - 液冷：从可选变必选，40-100+kW/rack（风冷极限20） - 新市场：Agent Memory Layer ($60-200亿), Agent编排网络 ($100-500亿), KV Cache存储平台 ($100-300亿) - NVIDIA已出手：BlueField-4 + CMX平台专为KV Cache offload设计 **7. GPU时刻 vs CPU时刻对比** - 需求逻辑相似（Scaling Law驱动），但利润逻辑不同（CPU是commodity，NVDA GPU是垄断） - NVDA用3年从$4B→$62B/季度（15x），CPU市场可能$270B→$540-800B（2-3x/5年） - 市场低估程度相似（⭐⭐⭐⭐⭐），但单一公司受益程度远不如NVDA **8. INTC/AMD估值硬核拆解** - INTC $98.50: Forward P/E FY2026 193x, FY2027 96x, 定价了从1.8%→20-25%营业利润率的飞跃 - AMD $337: Forward P/E FY2026 50x, FY2027 30.5x, 已完全定价FY2027一致预期 - 分析师目标价严重滞后（大部分是Q1业绩前定的） - 建立了目标价计算框架 + 4档场景（保守/中性/乐观/极致） **9. 市占率反推营收** - 服务器CPU份额：Intel ~50%(收入), AMD ~35%, ARM ~15% - 假设Agent增量份额：Intel 45%, AMD 30%, ARM 25%（考虑Vera+大厂自研ARM） - 基准场景(1亿Agent/10并发)：Intel +$170亿, AMD +$115亿/年增量 - 保守场景下INTC合理价$51-71（仍高估），基准场景下$143-201（低估） [score=0.941 recalls=3 avg=1.000 source=memory/2026-04-29.md:590-612]

## Promoted From Short-Term Memory (2026-05-07)

<!-- openclaw-memory-promotion:memory:memory/2026-04-28.md:486:488 -->[score=0.881 recalls=3 avg=1.000 source=memory/2026-04-28.md:486-488]
<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:52:75 -->[... 133 more lines truncated]

## Promoted From Short-Term Memory (2026-05-08)

<!-- openclaw-memory-promotion:memory:memory/2026-05-01.md:466:479 -->
- - - - - `docs/WORKFLOW.md` — 全 Agent 模式 - `docs/STRATEGY.md` — gstack Office Hour 策略 ### 工作模式确认 **全 Agent 模式**: - harsh = PM + Technical Manager (创建 ticket、分配 Builder/Tester、review MR、报告 George) - Builder Agent = sub-agent 写代码 - Tester Agent = sub-agent 跑测试 - George = 大方向和节奏 ### 下一步 (新 session 继续) 优先级排序: - 🔴 RUO-5: E2E 测试场景扩展 (High) - 🔴 RUO-6: gstack 价格验证 (High) - 🔴 RUO-12: CI/CD 自动化 (High) ### 关键路径 ``` repo: ~/Documents/smart-saver/ skill: ~/.openclaw/workspace/skills/smart-saver/ github: https://github.com/harshjia941-gz/smart-saver linear: https://linear.app/ruoshuiai ``` ## Smart Saver — PM Session: 三方向全面推进 (12:05-19:03 PDT) ### George 确认的三个方向 1. **数据引擎正确性 + 历史积累** — 数据结构完整，积累 [confiden [confidence=0.71 evidence=memory/2026-04-28.md:486-488] <!-- openclaw:dreaming:rem:end --> ## OpenCode + opencode-ensemble Team Mode 测试 (08:01-14:31 PDT) ### 背景 George 想测试 multi-agent team mode 协作编程。用 stock analysis 仓位数据做一个 Dashboard Web App 作为测试项目。 ### 工具链安装 - **Crush v0.64.0** — `brew install crush`（Charm, Go） - **OpenCode v1.14.31** — `npm install -g opencode`（anomalyco/opencode, 已从 opencode-ai 迁移） - **opencode-ensemble v0.13.1** — `opencode plugin add @hueyexe/opencode-ensemble` [score=0.829 recalls=3 avg=1.000 source=memory/2026-05-01.md:466-479]
