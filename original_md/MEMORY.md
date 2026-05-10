# MEMORY.md - Long-term Memory

## Smart Saver 项目状态 (2026-04-25)

### 当前进度
- **RUO-51 (搜索精度)**: PR #13 已 merge ✅ — REGEXP + tiered scoring 即时 fix 完成
- **RUO-62 (ground truth v1)**: Invalid — label 不清晰，query 粒度不够
- **RUO-63 (session mode)**: ✅ Done — 所有角色已改 session mode
- **RUO-64 (ground truth v2)**: ✅ Done — commit 62ff8e3 pushed to dev, 24 products, 175 listings
- **RUO-65 (PM+Agent 工作流)**: In Progress — clone repo 到 workspace 解决 sandbox 限制

### RUO-64 执行结果 (2026-04-25)
- **输出**: `tests/scenarios/search_ground_truth.json` (v2)
- **24 products**: 15 model-specific + 9 category
- **175 listings**: 自动标注 + 去重 + 采样
- **核心改进**: query-relative labeling（query 越具体匹配越严格）
- **数据缺口**: iPhone 15 (0), MacBook Pro 14 M4 (0), MX Master 3S (0) — DB 无数据
- **构建脚本**: `scripts/build_ground_truth_v2.py`（regex 规则自动标注）

### 流程改进 (今天)
- **PM+Agent 工作流验证**: PM 给任务 → Agent 出 plan → PM review → Agent 执行
- **Sandbox 解决方案**: git clone repo 到 workspace 内，agent 可自由读写
- **Plan-Approval 严格化**: 所有角色必须先出 plan 等 PM 审批
- **两阶段 spawn 废弃**: 单 session 内完成 plan→review→execute，上下文连续

### 技术债务
- 4 个产品无 DB 数据，需 Flipp API 补充或等真实数据
- Workspace clone 的 DB 需要手动同步（cp from ~/Documents/smart-saver/）

### Repo
- GitHub: harshjia941-gz/smart-saver
- DB: ~/Documents/smart-saver/scripts/smart_saver.db (原始) / workspace clone (副本)
- Workspace clone: ~/.openclaw/workspace/smart-saver/
- 主要分支: dev, main

---

## 交易系统 v2.0 架构 (2026-02-10)

### 命令结构

```bash
python live_sync.py position-sync  # 仅同步持仓
python live_sync.py oco-setup      # 设置 OCO 止盈止损
python live_sync.py full-sync      # 完整同步
python live_sync.py status         # 查看状态
python live_sync.py history        # 查看历史
```

### 数据库表

| 表名 | 用途 |
|------|------|
| `oco_groups` | OCO 订单组管理 |
| `sync_log` | 同步操作日志 |
| `order_tracking` | 订单全生命周期追踪 (含 oco_group, oco_parent_id, oco_sibling_id) |

### 订单分类

- `POSITION`: 仓位同步订单 (MAINT)
- `OCO_TP`: OCO 止盈单 (PLAN)
- `OCO_SL`: OCO 止损单 (PLAN)
- `SIGNAL`: 信号执行订单 (PLAN)

### IB 连接

- Paper Trading: 端口 4002, clientId 888
- Real Trading: 端口 7497

## 已知问题 (2026-02-11 更新)

- ~~OCO 保护缺失~~: ✅ 已创建20个活跃OCO组，后于20:25全部取消待重新配置
- ~~PENDING 订单~~: ✅ 已取消2个PENDING订单
- ~~同步失败~~: ✅ full-sync连接成功，21个仓位已同步
- ~~TSLA仓位不匹配~~: ✅ DB已更新为100股@$400.44，Paper待明日开盘同步

### 今日新增工具
- `trade_helper.py` - 手动交易后更新DB持仓和成本价
- `sync_check.py` - 检测未同步变更并支持自动同步

### 待处理
- [x] 运行 live_sync.py full-sync
- [x] 处理 2513 PENDING 订单  
- [x] 为所有持仓设置 OCO 保护 → 后取消，待重新配置策略
- [ ] TSLA Paper仓位同步（明日开盘）
- [ ] 添加 `trade.py health-check` 命令

---

## 🧠 Agent CPU需求深度调研 (2026-04-29)

George（Yuan Zhou）提出"Agent推理端CPU需求爆发"的投资主题，进行了多轮深度技术+投资讨论。

**核心文件**: `memory/agent-cpu-deep-dive.md`
**核心洞察**:
- CPU占Agent总延迟50-90.6%（Georgia Tech/Intel论文 arXiv:2511.00739）
- CPU:GPU比例从1:8反转到1:1（Agent时代）
- Agent 24/7运行 → 计算利用率从10%到60-75%（13x乘数）
- RL Post-Training需要CPU模拟Agent环境（CPU:GPU比2:1到10:1）
- 1亿Agent → CPU增量$1,200-1,800亿 + 存储$50-150亿 + 电力6GW
- 最被低估的机会：Agent Memory Layer（$60-200亿新市场，完全未定价）

**George的组合**: NVDA 17% | 智谱02513 17% | GOOGL 10% | AMD 8% | INTC 7%(成本$15) | TSM 3% | OKLO 3%
**INTC $94.75, AMD $337** — 均已严重透支分析师预期
**待续**: George会给自己的增长假设，精确算目标价

---

## 🤖 Anthropic Claude Mythos 追踪 (2026-04-16)

George 长期关注 AI 行业竞争格局。
- **追踪文件**: `memory/anthropic-mythos-tracker.md`
- **分析框架**: 毛泽东思维框架
- **核心判断**: Mythos不公开是五因素叠加（算力不足~30%、护城河~25%、IPO估值~20%、监管捕获~20%、真实安全~15%），安全叙事是包装
- **内部消息**: Anthropic内部团队不是都有大量使用权限
- **关键信源**: Fortune(算力危机)、Guardian(PR策略)、WIRED(监管捕获)、UK AISI(独立验证)
- **待追踪**: 算力缓解进度、OpenAI竞品、IPO进展、开源追赶速度

---

## 🇮🇷 美伊战争持续关注 (2026-04-16)

George 长期关注伊朗局势，建立了追踪文件。
- **追踪文件**: `memory/iran-war-tracker.md`
- **分析框架**: 教员（毛泽东）思维框架
- **核心判断**: 伊朗主要矛盾是内部合法性危机+经济崩溃，外部军事是次要矛盾
- **中国立场分析**: 不选边做和事佬，海湾利益远大于伊朗
- **关键**: 注意信源bias校正，交叉验证

---

## 多因子策略 Ground Truth 方法论 (2026-02-13)

### 现有方法
- **ZigZag v4**: 连续覆盖 ZigZag, 8% deviation, 100% 交易日覆盖
- **已测试股票**: AMD (45趋势段), BABA (47趋势段)

### 公开方法调研
| 方法 | 核心思想 |
|------|----------|
| NPMM | 只在价格触及N周期新低/新高时标记，论文证明效果最好 |
| Triple-Barrier | 止盈/止损/时间三层 barrier (Lopez de Prado) |
| Trend Scanning | 多窗口扫描，自适应视野 |

### 改进方向
1. NPMM 过滤 + ATR 自适应阈值
2. 多尺度 Trend Scanning 混合
3. 融入 Triple-Barrier 风控

---

## Ground Truth 最终算法 (2026-02-13)

### 流程 (最优顺序: 1→2→4)
```
1. NPMM N=5        → 找5日新低/高反转点
2. Merge (min=7)   → 合并短于7天的段
4. Smart Merge     → 只合并同向趋势
```

### 参数
- N=5, min_days=7, up_thresh=5%, down_thresh=5%

### BABA 结果
- 32段 (U=11, D=11, C=10)

### 执行顺序影响
| 顺序 | 结果 |
|------|------|
| 1→2→4 | 32段 (最优) |
| 1→4→2 | 45段 |

### 文件
- 代码: `strategies/multi_factor/ground_truth_generator.py`
- 文档: `strategies/multi_factor/README_GROUND_TRUTH.md`

---

## 多因子策略模型进展 (2026-02-14)

### 最佳模型
- **方法**: Feature Selection + Random Forest
- **准确率**: 69.05%
- **F1 Score**: 0.7033

### GT衍生特征
- 13个新特征，基于GT算法生成的趋势标签
- 重要特征: gt_trend_category, gt_trend_change_pct

### 数据
- 8只股票: BABA, NVDA, TSLA, AMD, PDD, DQ, MQ, LAC
- 总样本: ~5,500

### INTC预测
- GT: CONSOLIDATION (当前)
- ML: UPTREND (69.6%), 置信度51.1%

---

## Target 2: 下一趋势预测实验 (2026-02-15)

### 三分类结果 (困难)
| Iter | 方法 | Accuracy | ROC-AUC |
|------|------|----------|---------|
| 1 | Baseline RF | 32.4% | 0.439 |
| 2 | Tuned RF | 31.7% | 0.439 |
| 3 | RF + Platt | 34.1% | 0.532 |

### 二分类结果 (较好)
| 方法 | Accuracy | ROC-AUC | F1 |
|------|----------|---------|-----|
| RF + Platt | 63.6% | 0.718 | 0.684 |

### 关键发现
- 三分类接近随机 (33%)，非常困难
- 二分类显著更好，AUC=0.72
- GT特征 (gt_trend_change_pct) 最重要

### 下一步
- 使用二分类版本
- 结合 Target 1 的 WEAK 概率
- 扩展到更多股票

---

## 重要教训 (2026-02-17)

### 问题: 特征计算严重缺失导致错误预测

**事件**:
- 运行完整模型预测时，只计算了5个特征，缺失117个
- 当特征为0时，模型默认预测UPTREND (70%概率)
- 导致所有8只股票都显示"买入"信号

**原因**:
- 特征计算脚本不完整，没有包含所有121-122个特征
- 没有验证特征数量是否匹配
- 直接信任了输出，没有质疑

**教训**:
- **遇到问题必须立即告知**，不能假装没发生
- 预测结果看起来异常时必须质疑
- 任何预测前必须验证输入数据的完整性
- 特征数量、分布都应检查

## Promoted From Short-Term Memory (2026-04-27)

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

<!-- openclaw-memory-promotion:memory:memory/2026-04-28.md:486:488 -->
- - - - `docs/WORKFLOW.md` — 全 Agent 模式 - `docs/STRATEGY.md` — gstack Office Hour 策略 ### 工作模式确认 **全 Agent 模式**: - harsh = PM + Technical Manager (创建 ticket、分配 Builder/Tester、review MR、报告 George) - Builder Agent = sub-agent 写代码 - Tester Agent = sub-agent 跑测试 - George = 大方向和节奏 ### 下一步 (新 session 继续) 优先级排序: - 🔴 RUO-5: E2E 测试场景扩展 (High) - 🔴 RUO-6: gstack 价格验证 (High) - 🔴 RUO-12: CI/CD 自动化 (High) ### 关键路径 ``` repo: ~/Documents/smart-saver/ skill: ~/.openclaw/workspace/skills/smart-saver/ github: https://github.com/harshjia941-gz/smart-saver linear: https://linear.app/ruoshuiai ``` ## Smart Saver — PM Session: 三方向全面推进 (12:05-19:03 PDT) ### George 确认的三个方向 1. **数据引擎正确性 + 历史积累** — 数据结构完整，积累 [confidence [confidence=0.71 evidence=memory/2026-04-26.md:405-406] <!-- openclaw:dreaming:rem:end --> [score=0.881 recalls=3 avg=1.000 source=memory/2026-04-28.md:486-488]
<!-- openclaw-memory-promotion:memory:memory/2026-04-24.md:52:75 -->
- - 跑了 init 后，Flipp API 正常工作 - 测试结果：Dyson V15 $499.99, milk 2% $1.78, AirPods Pro 27 results - **Skill 能跑通了！** 但有 outlier 问题（iPhone $7.18 是配件不是手机） ### DB 路径混乱问题 - 昨天的 17,088 条 price_events 数据找不到了 - DB 路径分散在 3 个位置（repo root / scripts/ / skill scripts/） - 当前总共只有 ~386 条 events - **待决策**: DB 统一到 `~/Documents/smart-saver/scripts/price_history_v2.db`，skill 层 symlink ### RUO-38 已创建，调查过程记录在 ticket comments ## Cron 暂停 (12:17 PDT) - `smart-saver-pm` — 已 disable - `flipp-daily-scrape` — 已 disable - George 要求暂停 PM cron ## 待处理 - [ ] DB 路径统一（等 George 决策） - [ ] 清理 7 个过期分支 - [ ] RUO-32 开放问题（等 George 输入） - [ ] E2E 测试发现的 3 个 follow-up（outlier 过滤 / 中文查询 / first-run 脚本） - [ ] 用新角色流程实战测试一个 Backlog ticket [score=0.848 recalls=3 avg=1.000 source=memory/2026-04-24.md:52-75]

## Promoted From Short-Term Memory (2026-05-08)

<!-- openclaw-memory-promotion:memory:memory/2026-05-01.md:466:479 -->
- - - - - `docs/WORKFLOW.md` — 全 Agent 模式 - `docs/STRATEGY.md` — gstack Office Hour 策略 ### 工作模式确认 **全 Agent 模式**: - harsh = PM + Technical Manager (创建 ticket、分配 Builder/Tester、review MR、报告 George) - Builder Agent = sub-agent 写代码 - Tester Agent = sub-agent 跑测试 - George = 大方向和节奏 ### 下一步 (新 session 继续) 优先级排序: - 🔴 RUO-5: E2E 测试场景扩展 (High) - 🔴 RUO-6: gstack 价格验证 (High) - 🔴 RUO-12: CI/CD 自动化 (High) ### 关键路径 ``` repo: ~/Documents/smart-saver/ skill: ~/.openclaw/workspace/skills/smart-saver/ github: https://github.com/harshjia941-gz/smart-saver linear: https://linear.app/ruoshuiai ``` ## Smart Saver — PM Session: 三方向全面推进 (12:05-19:03 PDT) ### George 确认的三个方向 1. **数据引擎正确性 + 历史积累** — 数据结构完整，积累 [confiden [confidence=0.71 evidence=memory/2026-04-28.md:486-488] <!-- openclaw:dreaming:rem:end --> ## OpenCode + opencode-ensemble Team Mode 测试 (08:01-14:31 PDT) ### 背景 George 想测试 multi-agent team mode 协作编程。用 stock analysis 仓位数据做一个 Dashboard Web App 作为测试项目。 ### 工具链安装 - **Crush v0.64.0** — `brew install crush`（Charm, Go） - **OpenCode v1.14.31** — `npm install -g opencode`（anomalyco/opencode, 已从 opencode-ai 迁移） - **opencode-ensemble v0.13.1** — `opencode plugin add @hueyexe/opencode-ensemble` [score=0.829 recalls=3 avg=1.000 source=memory/2026-05-01.md:466-479]
