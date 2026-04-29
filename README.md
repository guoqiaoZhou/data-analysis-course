---
title: 数据分析进阶课程
course-version: 0.5

tags: [课程索引, 数据分析, 因果推断]
---

# 数据分析进阶课程

> 从方法规范到体系化能力，覆盖因果推断、机器学习建模、实验设计与分析文档写作。
> 
> 每个知识点 = 独立目录，含概念文档 + simulation.py + 好问练习 + 参考资源
> 知识点间通过 [[wikilink]] 双向链接，Obsidian 自动生成知识图谱。

---

## 课程背景

这套课程脱胎于**大厂数科团队内部封装的数据分析 SKILL 体系**——一套经过业务实战检验的方法论框架，用于规范团队内数据分析师的工作流程、分析标准和输出质量。

在此基础上，结合作者**大厂 5 年数据分析师**的一线经验，将零散的技能点体系化为可学习的课程内容。课程中的每一个案例、每一条"行业经验"、每一个"我们曾犯的错误"，都来自真实的业务场景：从电商大促的效果评估到 APP 新功能的 AB 实验，从骑手动态定价策略到推荐算法的因果推断。方法论的骨架来自团队 SKILL 的标准化沉淀，血肉则来自个人在字节、美团等大厂的实战总结。

课程设计遵循"**从业务问题出发，到方法落地，再到反常识反思**"的闭环：先让你理解"为什么需要这个方法"，再教你"怎么用"，最后提醒你"哪里会踩坑"。不是教科书式的知识罗列，而是分析师的实战手册。

---

## 课程概览

| 维度 | 数据 |
|------|------|
| **知识点** | 38 个核心概念文档 + 44 个参考资源 |
| **代码示例** | 30 个 simulation.py（覆盖全部知识点） |
| **刻意练习** | 56 个知识点 × 3 文件 = 168 个「好问」练习 |
| **实战项目** | 3 个端到端项目（可运行 Notebook + 数据） |
| **知识图谱** | 10 个 MOC 索引 + 概念关系图谱 |
| **审校质量** | 53 个文档审校完成，平均分 87.0/100 |
| **反常识内容** | 100 个常见陷阱 + 10 个知识点反常识章节 + 10 个审校案例 |

---

## 快速导航

### 按阶段
- [[MOC-阶段一-基础夯实|MOC-阶段一]] — 因果推断 + 统计基础 + AB实验
- [[MOC-阶段二-方法进阶|MOC-阶段二]] — 因果推断进阶 + ML建模 + 因果ML
- [[MOC-阶段三-实战整合|MOC-阶段三]] — 文档写作 + 业务场景 + 工具工程

### 按主题
- [[MOC-因果推断|MOC-因果推断]] — 全阶段因果推断方法
- [[MOC-统计基础|MOC-统计基础]] — 假设检验与回归方法
- [[MOC-AB实验|MOC-AB实验]] — 实验设计与分析
- [[MOC-机器学习建模|MOC-机器学习建模]] — XGBoost、SHAP、ALE等
- [[MOC-文档写作|MOC-文档写作]] — 分析文档写作规范
- [[MOC-业务场景|MOC-业务场景]] — 搜索、推荐、营销、增长

### 全局导航
- [[MOC-概念关系图谱|MOC-概念关系图谱]] — 按概念关系类型组织的全局索引

---

## 学习路径

### 第一阶段：基础夯实（3-4 周）

建立因果推断的数学直觉和统计基础。

1. **因果推断基础**
   - [[curriculum/stage-01-foundation/01-causal-inference-basics/01-potential-outcomes/潜在结果框架|潜在结果框架]] — 因果推断的数学基础
   - [[curriculum/stage-01-foundation/01-causal-inference-basics/02-randomized-experiments/随机化实验原理|随机化实验原理]] — 黄金标准
   - [[curriculum/stage-01-foundation/01-causal-inference-basics/03-observational-challenges/观察性数据的挑战|观察性数据的挑战]] — 混杂与选择偏误
   - [[curriculum/stage-01-foundation/01-causal-inference-basics/04-causation-vs-correlation/因果与相关的本质区别|因果 vs 相关]] — 本质区别
2. **统计基础**
   - [[curriculum/stage-01-foundation/02-statistical-basics/01-t-test/t检验|t检验]]
   - [[curriculum/stage-01-foundation/02-statistical-basics/02-chi-square-test/卡方检验|卡方检验]]
   - [[curriculum/stage-01-foundation/02-statistical-basics/03-bootstrap/Bootstrap重抽样方法|Bootstrap]]
   - [[curriculum/stage-01-foundation/02-statistical-basics/04-ols-regression/OLS回归|OLS回归]]
   - [[curriculum/stage-01-foundation/02-statistical-basics/05-logistic-regression/Logistic回归|Logistic回归]]
   - [[curriculum/stage-01-foundation/02-statistical-basics/06-fixed-effects/固定效应模型|固定效应模型]]
   - [[curriculum/stage-01-foundation/02-statistical-basics/07-power-analysis/检验力分析与样本量计算|检验力与样本量]]
3. **AB实验全流程**
   - [[curriculum/stage-01-foundation/03-ab-testing/01-experiment-design/AB实验设计要素|实验设计要素]]
   - [[curriculum/stage-01-foundation/03-ab-testing/02-randomization/随机化与分流|随机化与分流]]
   - [[curriculum/stage-01-foundation/03-ab-testing/03-pre-aa-check/Pre-AA检验|Pre-AA检验]]
   - [[curriculum/stage-01-foundation/03-ab-testing/04-cuped/CUPED方差缩减|CUPED方差缩减]]
   - [[curriculum/stage-01-foundation/03-ab-testing/05-post-stratification/后分层分析|后分层分析]]
   - [[curriculum/stage-01-foundation/03-ab-testing/06-multiple-testing/多重检验问题|多重检验问题]]
   - [[curriculum/stage-01-foundation/03-ab-testing/07-analysis-decision/实验分析决策框架|实验分析决策]]

### 第二阶段：方法进阶（4-6 周）

掌握高级因果推断方法和机器学习建模。

4. **因果推断进阶**
   - PSM倾向得分匹配：[[curriculum/stage-02-advanced/04-causal-inference/01-psm/01-matching-methods/PSM匹配方法|匹配方法]] → [[curriculum/stage-02-advanced/04-causal-inference/01-psm/02-overlap-assumption/重叠假设|重叠假设]] → [[curriculum/stage-02-advanced/04-causal-inference/01-psm/03-sensitivity-analysis/敏感性分析|敏感性分析]]
   - DID双重差分：[[curriculum/stage-02-advanced/04-causal-inference/02-did/01-parallel-trends/DID平行趋势检验|平行趋势]] → [[curriculum/stage-02-advanced/04-causal-inference/02-did/02-event-study/事件研究法|事件研究法]] → [[curriculum/stage-02-advanced/04-causal-inference/02-did/03-synthetic-control/合成控制法|合成控制法]]
   - DML双重机器学习：[[curriculum/stage-02-advanced/04-causal-inference/03-dml/01-nuisance-estimation/Nuisance函数估计|Nuisance估计]] → [[curriculum/stage-02-advanced/04-causal-inference/03-dml/02-cross-validation/交叉验证策略|交叉验证]] → [[curriculum/stage-02-advanced/04-causal-inference/03-dml/03-high-dimensional/高维场景|高维场景]]
5. **机器学习建模**
   - [[curriculum/stage-02-advanced/05-ml-modeling/01-xgboost/XGBoost|XGBoost]]
   - SHAP解释：[[curriculum/stage-02-advanced/05-ml-modeling/02-shap/01-global-importance/SHAP全局重要性|全局重要性]] → [[curriculum/stage-02-advanced/05-ml-modeling/02-shap/02-local-explanation/SHAP局部解释|局部解释]] → [[curriculum/stage-02-advanced/05-ml-modeling/02-shap/03-violin-plot/SHAP小提琴图|小提琴图]]
   - [[curriculum/stage-02-advanced/05-ml-modeling/03-ale-plots/ALE图|ALE图]]
   - [[curriculum/stage-02-advanced/05-ml-modeling/04-shap-interaction/SHAP交互效应|SHAP交互效应]]
   - [[curriculum/stage-02-advanced/05-ml-modeling/05-woe-iv/WOE-IV分箱|WOE/IV分箱]]
   - [[curriculum/stage-02-advanced/05-ml-modeling/06-gbdt-lr/GBDT-LR|GBDT+LR]]
6. **因果推断×机器学习交叉**
   - 因果森林：[[curriculum/stage-02-advanced/06-causal-ml/01-causal-forest/01-splitting-criteria/因果森林分裂准则|分裂准则]] → [[curriculum/stage-02-advanced/06-causal-ml/01-causal-forest/02-confidence-intervals/因果森林置信区间|置信区间]]
   - Meta-Learners：[[curriculum/stage-02-advanced/06-causal-ml/02-meta-learners/01-s-learner/S-Learner|S-Learner]] → [[curriculum/stage-02-advanced/06-causal-ml/02-meta-learners/02-t-learner/T-Learner|T-Learner]] → [[curriculum/stage-02-advanced/06-causal-ml/02-meta-learners/03-x-learner/X-Learner|X-Learner]] → [[curriculum/stage-02-advanced/06-causal-ml/02-meta-learners/04-r-learner/R-Learner|R-Learner]]
   - [[curriculum/stage-02-advanced/06-causal-ml/03-doubly-robust/双重稳健学习|双重稳健学习]]

### 第三阶段：实战整合（持续）

将方法转化为业务价值和规范文档。

7. **分析文档写作**
   - [[curriculum/stage-03-practice/07-document-writing/01-pyramid-principle/金字塔原理|金字塔原理]]
   - [[curriculum/stage-03-practice/07-document-writing/02-conclusion-writing/核心结论写作|核心结论写作]]
   - [[curriculum/stage-03-practice/07-document-writing/03-methods-section/方法说明写作|方法说明写作]]
   - [[curriculum/stage-03-practice/07-document-writing/04-actionable-recommendations/落地建议颗粒度|落地建议颗粒度]]
   - [[curriculum/stage-03-practice/07-document-writing/05-numeric-expression/数字表达规范|数字表达规范]]
   - [[curriculum/stage-03-practice/07-document-writing/06-limitations/局限性声明|局限性声明]]
8. **业务场景实战**
   - [[curriculum/stage-03-practice/08-business-scenarios/01-search-analysis/搜索场景分析|搜索场景]]
   - [[curriculum/stage-03-practice/08-business-scenarios/02-recommendation-analysis/推荐场景分析|推荐场景]]
   - [[curriculum/stage-03-practice/08-business-scenarios/03-marketing-analysis/营销场景分析|营销场景]]
   - [[curriculum/stage-03-practice/08-business-scenarios/04-growth-analysis/用户增长分析|用户增长]]
9. **工具与工程**
   - [[curriculum/stage-03-practice/09-tools-engineering/01-python-ecosystem/Python因果推断生态|Python生态]]
   - [[curriculum/stage-03-practice/09-tools-engineering/02-r-ecosystem/R因果推断生态|R生态]]
   - [[curriculum/stage-03-practice/09-tools-engineering/03-experiment-platform/实验平台搭建思路|实验平台]]
   - [[curriculum/stage-03-practice/09-tools-engineering/04-reproducibility/分析可复现性|可复现性]]

---

## 实战项目

三个端到端实战项目，覆盖课程核心方法：

| 项目 | 主题 | 覆盖方法 | 数据规模 | 状态 |
|------|------|----------|----------|------|
| [Project 01](curriculum/projects/project-01-ecommerce-causal/) | 电商大促效果评估 | PSM + DID + 合成控制 | 10,000 用户 | ✅ 可运行 |
| [Project 02](curriculum/projects/project-02-app-experiment/) | APP新功能AB实验 | 实验设计 + CUPED + 后分层 | 10,000 用户 | ✅ 可运行 |
| [Project 03](curriculum/projects/project-03-rider-pricing/) | 骑手动态定价 | DML + 因果森林 + Meta-Learners | 20,464 面板 | ✅ 可运行 |

每个项目包含：
- `README.md` — 项目背景、STAR框架、学习路径
- `data/` — 模拟数据集 + 数据字典
- `notebooks/` — 6 个可执行 Jupyter Notebook（TODO引导）
- `report-template/` — 标准报告模板
- `solution/` — 参考答案
- `rubric/` — 评分标准

---

## 使用指南

### Obsidian 用户

1. 用 Obsidian 打开 `curriculum/` 目录
2. 安装 Graph View 插件查看知识图谱
3. 通过 [[wikilink]] 在知识点间跳转
4. 使用标签 `#课程/基础夯实` 筛选阶段

### VS Code 用户

1. 用 VS Code 打开 `data-analysis-course/`
2. 安装 Markdown 插件和 Python 插件
3. `curriculum/**/simulation.py` 可直接运行
4. 使用 Jupyter 插件运行项目 Notebook

### 学习节奏建议

| 阶段 | 时间 | 目标 |
|---|---|---|
| 基础夯实 | 3-4 周 | 建立因果直觉；能独立分析简单AB实验 |
| 方法进阶 | 4-6 周 | 掌握2-3种高级方法；能处理观察性数据 |
| 实战整合 | 2-3 周/项目 | 输出规范文档；形成个人分析框架 |

---

## 附录

- [[curriculum/appendix/01-math-refresher/数学基础速查|数学基础速查]]
- [[curriculum/appendix/02-code-templates/代码模板库|代码模板库]]
- [[curriculum/appendix/03-datasets/案例数据集|案例数据集]]
- [[curriculum/appendix/04-resources/推荐资源清单|推荐资源清单]]
- [[curriculum/review/audit-report|审校报告]] — 53 个文档质量评估

---

## 版本迭代

详见 [[curriculum/roadmap/versions|版本迭代计划]] 和 [[curriculum/roadmap/future-features|未来功能清单]]。

| 版本 | 状态 | 核心内容 |
|------|------|----------|
| v0.1 | ✅ 已完成 | 56 个知识点概念文档 + MOC 索引 |
| v0.2 | ✅ 已完成 | 每个知识点增加「问题引入」章节 |
| v0.3 | ✅ 已完成 | 「好问」刻意练习系统（168 个练习文件） |
| v0.4 | ✅ 已完成 | 3 个端到端实战项目（可运行 Notebook） |
| v0.5 | ✅ 已完成 | 反常识内容：100 个坑 + 10 个知识点反常识章节 + lessons-learned.md |
| v0.6 | 📋 规划中 | 软技能：说服力 + 拒绝艺术 + 数据权威 |
| v1.0 | 📋 规划中 | 诊断测试 + 个性化路径 + 学习进度追踪 |

---

*课程版本：v0.5*
*更新日期：2026-04-28*
