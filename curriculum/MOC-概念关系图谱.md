---
title: 概念关系图谱（全局导航）
course-stage: 全阶段
tags: [导航, 知识图谱, MOC]
---

# 概念关系图谱

> 本文件是课程的全局概念关系索引。不同于按主题组织的 MOC，这里按**概念之间的关系类型**组织，帮助你理解知识点之间的依赖、对比和应用关系。

---

## 一、因果推断核心链路

```
[[stage-01-foundation/01-causal-inference-basics/04-causation-vs-correlation/因果与相关的本质区别|因果vs相关]]
    ↓ （基础概念铺垫）
[[stage-01-foundation/01-causal-inference-basics/01-potential-outcomes/潜在结果框架|潜在结果框架]]
    ↓ （方法论实现）
├─→ [[stage-01-foundation/01-causal-inference-basics/02-randomized-experiments/随机化实验原理|随机化实验]]（黄金标准）
│       ↓ （实验设计细节）
│   [[stage-01-foundation/03-ab-testing/01-experiment-design/AB实验设计要素|AB实验设计]]
│       ↓ （统计检验工具）
│   [[stage-01-foundation/02-statistical-basics/01-t-test/t检验|t检验]] + [[stage-01-foundation/02-statistical-basics/07-power-analysis/检验力分析与样本量计算|检验力分析]]
│
└─→ [[stage-01-foundation/01-causal-inference-basics/03-observational-challenges/观察性数据的挑战|观察性数据挑战]]
        ↓ （应对策略）
    ├─→ [[stage-02-advanced/04-causal-inference/01-psm/01-matching-methods/PSM匹配方法|PSM]]（匹配）
    ├─→ [[stage-02-advanced/04-causal-inference/02-did/01-parallel-trends/DID平行趋势检验|DID]]（面板数据）
    ├─→ [[stage-02-advanced/04-causal-inference/03-dml/01-nuisance-estimation/Nuisance函数估计|DML]]（机器学习辅助）
    └─→ [[stage-02-advanced/06-causal-ml/03-doubly-robust/双重稳健学习|双重稳健]]（组合策略）
```

---

## 二、统计基础工具箱

### 2.1 假设检验家族

| 场景 | 方法 | 关联概念 |
|------|------|----------|
| 连续变量，两组均值 | [[stage-01-foundation/02-statistical-basics/01-t-test/t检验\|t检验]] | [[stage-01-foundation/02-statistical-basics/07-power-analysis/检验力分析与样本量计算\|检验力分析]] |
| 分类变量，独立性 | [[stage-01-foundation/02-statistical-basics/02-chi-square-test/卡方检验\|卡方检验]] | [[stage-01-foundation/03-ab-testing/02-randomization/随机化与分流\|SRM检测]] |
| 不依赖分布假设 | [[stage-01-foundation/02-statistical-basics/03-bootstrap/Bootstrap重抽样方法\|Bootstrap]] | [[stage-01-foundation/02-statistical-basics/01-t-test/t检验\|t检验]]（对比） |
| 控制混杂变量 | [[stage-01-foundation/02-statistical-basics/04-ols-regression/OLS回归\|OLS回归]] | [[stage-01-foundation/02-statistical-basics/06-fixed-effects/固定效应模型\|固定效应]] |
| 二分类结果 | [[stage-01-foundation/02-statistical-basics/05-logistic-regression/Logistic回归\|Logistic回归]] | [[stage-02-advanced/05-ml-modeling/05-woe-iv/WOE-IV分箱\|WOE/IV]] |

### 2.2 方法对比矩阵

- **t检验 vs Bootstrap**：[[stage-01-foundation/02-statistical-basics/01-t-test/t检验|t检验]] 依赖正态假设，[[stage-01-foundation/02-statistical-basics/03-bootstrap/Bootstrap重抽样方法|Bootstrap]] 不依赖分布假设但计算量大
- **OLS vs 固定效应**：[[stage-01-foundation/02-statistical-basics/04-ols-regression/OLS回归|OLS]] 控制可观测混杂，[[stage-01-foundation/02-statistical-basics/06-fixed-effects/固定效应模型|固定效应]] 控制不随时间变化的未观测混杂
- **卡方检验 vs t检验**：[[stage-01-foundation/02-statistical-basics/02-chi-square-test/卡方检验|卡方]] 处理分类变量，[[stage-01-foundation/02-statistical-basics/01-t-test/t检验|t检验]] 处理连续变量

---

## 三、AB实验完整链路

```
实验设计阶段
    ├─→ [[stage-01-foundation/03-ab-testing/01-experiment-design/AB实验设计要素|实验设计]]
    │       ├─ 前置：[[stage-01-foundation/02-statistical-basics/07-power-analysis/检验力分析与样本量计算|样本量计算]]
    │       └─ 前置：[[stage-01-foundation/02-statistical-basics/01-t-test/t检验|t检验]]
    │
    ├─→ [[stage-01-foundation/03-ab-testing/02-randomization/随机化与分流|随机化与分流]]
    │       └─ 平行：[[stage-01-foundation/01-causal-inference-basics/02-randomized-experiments/随机化实验原理|随机化原理]]
    │
    └─→ [[stage-01-foundation/03-ab-testing/03-pre-aa-check/Pre-AA检验|Pre-AA检验]]

实验执行阶段
    ├─→ [[stage-01-foundation/03-ab-testing/04-cuped/CUPED方差缩减|CUPED]]（方差缩减）
    ├─→ [[stage-01-foundation/03-ab-testing/05-post-stratification/后分层分析|后分层]]（纠偏）
    └─→ [[stage-01-foundation/03-ab-testing/06-multiple-testing/多重检验问题|多重检验校正]]

实验决策阶段
    └─→ [[stage-01-foundation/03-ab-testing/07-analysis-decision/实验分析决策框架|分析决策]]
```

---

## 四、机器学习建模 → 可解释性 → 因果推断

### 4.1 模型训练

- [[stage-02-advanced/05-ml-modeling/01-xgboost/XGBoost|XGBoost]]（梯度提升）
- [[stage-02-advanced/05-ml-modeling/06-gbdt-lr/GBDT-LR|GBDT+LR]]（特征变换+线性模型）

### 4.2 模型解释

| 解释层级 | 方法 | 适用场景 |
|----------|------|----------|
| 全局特征重要性 | [[stage-02-advanced/05-ml-modeling/02-shap/01-global-importance/SHAP全局重要性\|SHAP全局]] | 回答"哪些特征最重要" |
| 局部单样本解释 | [[stage-02-advanced/05-ml-modeling/02-shap/02-local-explanation/SHAP局部解释\|SHAP局部]] | 回答"为什么这个用户被预测为高流失" |
| 特征效应可视化 | [[stage-02-advanced/05-ml-modeling/03-ale-plots/ALE图\|ALE图]] | 回答"X增加时Y如何变化"（避免相关特征偏差） |
| 特征交互效应 | [[stage-02-advanced/05-ml-modeling/04-shap-interaction/SHAP交互效应\|SHAP交互]] | 回答"X1和X2是否有协同效应" |

### 4.3 从预测到因果

```
预测模型
    ├─→ [[stage-02-advanced/05-ml-modeling/01-xgboost/XGBoost|XGBoost]]
    │       ↓ （需要解释）
    │   [[stage-02-advanced/05-ml-modeling/02-shap/01-global-importance/SHAP全局重要性|SHAP]] / [[stage-02-advanced/05-ml-modeling/03-ale-plots/ALE图|ALE]]
    │       ↓ （但相关≠因果）
    │   [[stage-01-foundation/01-causal-inference-basics/04-causation-vs-correlation/因果与相关的本质区别|因果vs相关]]
    │       ↓ （因果推断方法）
    └─→ [[stage-02-advanced/06-causal-ml/01-causal-forest/01-splitting-criteria/因果森林分裂准则|因果森林]] / [[stage-02-advanced/06-causal-ml/02-meta-learners/01-s-learner/S-Learner|Meta-Learners]]
```

---

## 五、因果推断方法选择决策树

```
能否做随机化实验？
    ├─ 是 → [[stage-01-foundation/03-ab-testing/01-experiment-design/AB实验设计要素|AB实验]]
    │           ├─ 样本量足够？ → [[stage-01-foundation/02-statistical-basics/01-t-test/t检验|t检验]]
    │           └─ 样本量紧张？ → [[stage-01-foundation/03-ab-testing/04-cuped/CUPED方差缩减|CUPED]] / [[stage-01-foundation/03-ab-testing/05-post-stratification/后分层分析|后分层]]
    │
    └─ 否 → 有什么数据？
            ├─ 面板数据（多期） → [[stage-02-advanced/04-causal-inference/02-did/01-parallel-trends/DID平行趋势检验|DID]]
            │                       └─ 平行趋势不成立？ → [[stage-02-advanced/04-causal-inference/02-did/03-synthetic-control/合成控制法|合成控制]]
            ├─ 截面数据 + 可匹配 → [[stage-02-advanced/04-causal-inference/01-psm/01-matching-methods/PSM匹配方法|PSM]]
            │                       └─ 匹配后仍不放心？ → [[stage-02-advanced/04-causal-inference/01-psm/03-sensitivity-analysis/敏感性分析|敏感性分析]]
            ├─ 高维数据 + ML工具 → [[stage-02-advanced/04-causal-inference/03-dml/01-nuisance-estimation/Nuisance函数估计|DML]]
            └─ 异质性效应 → [[stage-02-advanced/06-causal-ml/01-causal-forest/01-splitting-criteria/因果森林分裂准则|因果森林]] / [[stage-02-advanced/06-causal-ml/02-meta-learners/01-s-learner/S-Learner|Meta-Learners]]
```

---

## 六、跨主题关联

### 6.1 因果推断 ↔ 统计基础

| 因果推断概念 | 统计工具 | 关系 |
|-------------|---------|------|
| 处理效应估计 | [[stage-01-foundation/02-statistical-basics/01-t-test/t检验\|t检验]] | 检验效应是否显著 |
| 观察性数据调整 | [[stage-01-foundation/02-statistical-basics/04-ols-regression/OLS回归\|OLS]] / [[stage-01-foundation/02-statistical-basics/05-logistic-regression/Logistic回归\|Logistic]] | 控制混杂变量 |
| 方差估计 | [[stage-01-foundation/02-statistical-basics/03-bootstrap/Bootstrap重抽样方法\|Bootstrap]] | 不依赖分布假设 |
| 实验设计 | [[stage-01-foundation/02-statistical-basics/07-power-analysis/检验力分析与样本量计算\|检验力分析]] | 确定样本量 |

### 6.2 AB实验 ↔ 因果推断

| AB实验环节 | 因果推断概念 | 关系 |
|-----------|-------------|------|
| 随机化 | [[stage-01-foundation/01-causal-inference-basics/02-randomized-experiments/随机化实验原理\|随机化原理]] | 实现可忽略性 |
| Pre-AA检验 | [[stage-01-foundation/01-causal-inference-basics/03-observational-challenges/观察性数据的挑战\|观察性挑战]] | 检验随机化是否成功 |
| 实验不可行时 | [[stage-02-advanced/04-causal-inference/01-psm/01-matching-methods/PSM匹配方法\|PSM]] / [[stage-02-advanced/04-causal-inference/02-did/01-parallel-trends/DID平行趋势检验\|DID]] | 替代方案 |

### 6.3 ML建模 ↔ 因果推断

| ML概念 | 因果推断应用 | 关系 |
|--------|-------------|------|
| [[stage-02-advanced/05-ml-modeling/01-xgboost/XGBoost\|XGBoost]] | [[stage-02-advanced/04-causal-inference/03-dml/01-nuisance-estimation/Nuisance函数估计\|DML]] | 估计nuisance函数 |
| [[stage-02-advanced/05-ml-modeling/02-shap/01-global-importance/SHAP全局重要性\|SHAP]] | [[stage-02-advanced/06-causal-ml/02-meta-learners/01-s-learner/S-Learner\|S-Learner]] | 特征重要性 vs 处理效应异质性 |
| [[stage-02-advanced/05-ml-modeling/03-ale-plots/ALE图\|ALE]] | [[stage-02-advanced/06-causal-ml/01-causal-forest/01-splitting-criteria/因果森林分裂准则\|因果森林]] | 边际效应 vs 条件平均效应 |

---

## 七、主题 MOC 导航

| 主题 | MOC | 核心内容 |
|------|-----|----------|
| 阶段一 | [[MOC-阶段一-基础夯实\|MOC-阶段一-基础夯实]] | 因果推断 + 统计基础 + AB实验 |
| 阶段二 | [[MOC-阶段二-方法进阶\|MOC-阶段二-方法进阶]] | 因果推断进阶 + ML建模 + 因果ML |
| 阶段三 | [[MOC-阶段三-实战整合\|MOC-阶段三-实战整合]] | 文档写作 + 业务场景 + 工具工程 |
| 因果推断 | [[MOC-因果推断\|MOC-因果推断]] | 全阶段因果推断方法 |
| 统计基础 | [[MOC-统计基础\|MOC-统计基础]] | 假设检验与回归方法 |
| AB实验 | [[MOC-AB实验\|MOC-AB实验]] | 实验设计与分析 |
| 机器学习建模 | [[MOC-机器学习建模\|MOC-机器学习建模]] | XGBoost、SHAP、ALE等 |
| 文档写作 | [[MOC-文档写作\|MOC-文档写作]] | 分析文档写作规范 |
| 业务场景 | [[MOC-业务场景\|MOC-业务场景]] | 搜索、推荐、营销、增长 |

---

> 💡 **使用提示**：在 Obsidian 中打开 Graph View，以本文件为起点，可以看到整个课程的知识图谱全貌。每个知识点文档中的"概念关联"章节会标注该知识点的**前置知识**、**后续应用**和**平行概念**，帮助你定位当前概念在知识体系中的位置。
