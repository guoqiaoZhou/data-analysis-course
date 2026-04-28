# Project 02: APP新功能AB实验

> **STAR框架** | **5W2H分析** | **AB实验完整流程**

---

## 📋 项目概述

**业务场景**：某内容APP（类似抖音/快手）想上线新推荐算法，声称能提升用户停留时长。产品团队已经开发完成，准备全量上线。

**你的角色**：作为数据分析师，你需要设计并执行一个实验，验证新算法是否真的有效果，并给出是否上线的建议。

---

## 🎯 STAR框架

### Situation（情境）

- 公司：某头部内容APP，DAU 5000万+
- 背景：推荐算法团队开发了一套新推荐算法，声称能提升用户停留时长15%
- 压力：产品团队已经开发完成，准备全量上线，CEO催得紧
- 问题：直接全量上线风险极大，需要数据验证

### Task（任务）

作为数据分析师，你需要：
1. 设计一个科学的AB实验
2. 执行实验并收集数据
3. 分析数据并给出可靠结论
4. 给出是否上线的明确建议

### Action（行动）

详见各notebook：
- `01-situation-task.ipynb` — 业务背景、问题定义
- `02-action-design.ipynb` — 实验设计、方案确定
- `03-action-execution.ipynb` — 执行实验、数据收集
- `04-action-analysis.ipynb` — 分析数据、逐步完善
- `05-action-iteration.ipynb` — 迭代调整、延伸分析

### Result（结果）

详见 `06-result.ipynb` — 结论、洞察、业务价值

---

## 📖 阅读路径

根据你的时间和目标，选择不同的阅读路径：

### 🚀 快速了解（5分钟）
只想了解这个项目是做什么的、结论是什么：
1. **README.md**（本文档）— 项目背景、STAR框架、核心结论
2. **report-template/experiment-report-template.md** — 标准实验报告结构，了解最终交付物

### 🧠 理解思路（30分钟）
想理解"为什么这么做"，但不需要动手：
1. **notebooks/01-situation-task.ipynb** — 业务背景、问题定义、指标选择
2. **notebooks/02-action-design.ipynb** — 实验设计、样本量计算、随机化方案
3. **notebooks/06-result.ipynb** — 结论、洞察、业务建议

### 🔧 动手实践（2-4小时）
想跟着做一遍，建立实操能力：
按顺序执行：
1. **notebooks/01-situation-task.ipynb** — 理解业务问题
2. **notebooks/02-action-design.ipynb** — 设计实验方案
3. **notebooks/03-action-execution.ipynb** — 生成数据、执行AA检验
4. **notebooks/04-action-analysis.ipynb** — 假设检验、多重检验校正
5. **notebooks/05-action-iteration.ipynb** — CUPED优化、后分层分析
6. **notebooks/06-result.ipynb** — 撰写结论

### 🔍 深入验证（可选）
做完后想对照答案、评估质量：
1. **solution/reference-solution.md** — 参考答案，对照自己的分析
2. **rubric/scoring-rubric.md** — 评分标准，自评或互评

---

## ⚠️ 失败路径警示

本项目特别展示了以下错误做法的后果：

| 错误做法 | 后果 | 在哪看到 |
|---------|------|---------|
| 跳过AA检验 | 分组本来就不平衡，结论不可信 | notebook 03 |
| 忽略多重检验 | 3个指标都显著的概率是14%，不是5% | notebook 04 |
| 实验中途peeking | 假阳性率从5%飙升到30%+ | notebook 05 |
| 不看后分层 | 掩盖了"新用户有效、老用户无效"的重要信息 | notebook 05 |

---

---

## 🔍 5W2H分析

| 维度 | 内容 |
|------|------|
| **Why** | 为什么要做这个实验？直接全量上线新算法风险极大，可能损害用户体验、降低留存，需要数据验证 |
| **What** | 验证新推荐算法是否能显著提升用户停留时长，同时监控CTR、次日留存等guardrail指标 |
| **Who** | 数据分析师（你）、推荐算法团队、产品团队、CEO |
| **When** | 实验周期2周（基于样本量计算），避开节假日和重大运营活动 |
| **Where** | 线上真实环境，随机抽取部分用户参与实验 |
| **How** | AB实验：对照组用老算法，实验组用新算法，随机分配用户 |
| **How much** | 每组约5000用户，共10000用户参与实验；预期停留时长提升15% |

---

## 📁 项目结构

```
project-02-app-experiment/
├── README.md                          # 项目说明（本文件）
├── data/
│   ├── raw/                           # 原始数据
│   ├── processed/                     # 清洗后数据
│   └── data-dictionary.md             # 数据字典
├── notebooks/
│   ├── 01-situation-task.ipynb        # Situation+Task：业务背景、问题定义
│   ├── 02-action-design.ipynb         # Action：实验设计、方案确定
│   ├── 03-action-execution.ipynb      # Action：执行实验、数据收集
│   ├── 04-action-analysis.ipynb       # Action：分析数据、逐步完善
│   ├── 05-action-iteration.ipynb      # Action：迭代调整、延伸分析
│   └── 06-result.ipynb               # Result：结论、洞察、业务价值
├── report-template/
│   └── experiment-report-template.md  # 实验报告模板
├── solution/
│   └── reference-solution.md          # 参考答案
└── rubric/
    └── scoring-rubric.md              # 评分标准
```

---

## 🎓 学习目标

完成本项目后，你将掌握：

1. **AB实验设计**：样本量计算、实验周期确定、指标选择
2. **随机化与AA检验**：确保分组平衡，避免系统性偏差
3. **统计检验**：t检验、z检验的选择与应用
4. **多重检验校正**：Bonferroni、FDR等方法
5. **CUPED**：利用历史数据降低方差，提高检验力
6. **后分层分析**：识别不同用户群体的差异化效果
7. **实验决策**：如何基于数据给出明确的业务建议
8. **失败路径识别**：了解常见错误及其后果

---

## ⚠️ 关键挑战

### 业务干扰（真实职场场景）

1. **Peeking问题**：实验进行到一半，老板问"能不能提前看结果？"
2. **指标异常**：实验组某个指标显著为负，业务方要求"再跑一周看看"
3. **时间压力**：样本量计算显示需要2周，但产品团队希望1周出结论

### 失败路径（必须避免）

1. **跳过AA检验**：分组可能本来就不平衡，导致结论失真
2. **忽略多重检验**：3个指标都"显著"的概率是14%，不是5%
3. **Peeking**：中途偷看结果，假阳性率会飙升

---

## 🛠️ 技术栈

- **Python**：pandas, numpy, scipy, statsmodels, matplotlib
- **统计方法**：假设检验、置信区间、方差分析、CUPED
- **数据**：模拟真实APP用户行为数据

---

## 📝 开始之前

1. 阅读 `data/data-dictionary.md` 了解数据字段
2. 按顺序完成各notebook（01 → 02 → 03 → 04 → 05 → 06）
3. 每个notebook中有明确的 **TODO** 标记，按提示完成
4. 遇到困难时，参考 `solution/reference-solution.md`

---

> **核心原则**：知其然，知其所以然。展示你的思考过程，而不是只给答案。

---

*本项目为数据分析课程实战项目，模拟真实职场场景。*
