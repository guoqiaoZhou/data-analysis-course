---
title: 数据分析进阶课程
course-version: 1.0
course-author: 为国乔妻子定制
tags: [课程索引, 数据分析, 因果推断]
---

# 数据分析进阶课程

> 从方法规范到体系化能力，覆盖因果推断、机器学习建模、实验设计与分析文档写作。
> 
> 每个知识点 = 独立目录，含 concept.md + code/ + exercises/ + references.md
> 知识点间通过 [[wikilink]] 双向链接，Obsidian 自动生成知识图谱。

---

## 学习路径

### 第一阶段：基础夯实

建立因果推断的数学直觉和统计基础。

1. [[01-potential-outcomes|潜在结果框架]] — 因果推断的数学基础
2. [[02-randomized-experiments|随机化实验原理]] — 黄金标准
3. [[03-observational-challenges|观察性数据的挑战]] — 混杂与选择偏误
4. [[04-causation-vs-correlation|因果 vs 相关]] — 本质区别
5. 统计基础
   - [[01-t-test|t检验]]
   - [[02-chi-square-test|卡方检验]]
   - [[03-bootstrap|Bootstrap]]
   - [[04-ols-regression|OLS回归]]
   - [[05-logistic-regression|Logistic回归]]
   - [[06-fixed-effects|固定效应模型]]
   - [[07-power-analysis|检验力与样本量]]
6. AB实验全流程
   - [[01-experiment-design|实验设计要素]]
   - [[02-randomization|随机化与分流]]
   - [[03-pre-aa-check|Pre-AA检验]]
   - [[04-cuped|CUPED方差缩减]]
   - [[05-post-stratification|后分层分析]]
   - [[06-multiple-testing|多重检验问题]]
   - [[07-analysis-decision|实验分析决策]]

### 第二阶段：方法进阶

掌握高级因果推断方法和机器学习建模。

7. 因果推断进阶
   - PSM倾向得分匹配
     - [[01-matching-methods|匹配方法]]
     - [[02-overlap-assumption|重叠假设]]
     - [[03-sensitivity-analysis|敏感性分析]]
   - DID双重差分
     - [[01-parallel-trends|平行趋势检验]]
     - [[02-event-study|事件研究法]]
     - [[03-synthetic-control|合成控制法]]
   - DML双重机器学习
     - [[01-nuisance-estimation|Nuisance函数估计]]
     - [[02-cross-validation|交叉验证策略]]
     - [[03-high-dimensional|高维场景]]
8. 机器学习建模
   - [[01-xgboost|XGBoost]]
   - SHAP解释
     - [[01-global-importance|全局重要性]]
     - [[02-local-explanation|局部解释]]
     - [[03-violin-plot|小提琴图]]
   - [[03-ale-plots|ALE图]]
   - [[04-shap-interaction|SHAP交互效应]]
   - [[05-woe-iv|WOE/IV分箱]]
   - [[06-gbdt-lr|GBDT+LR]]
9. 因果推断×机器学习交叉
   - 因果森林
     - [[01-splitting-criteria|分裂准则]]
     - [[02-confidence-intervals|置信区间]]
   - Meta-Learners
     - [[01-s-learner|S-Learner]]
     - [[02-t-learner|T-Learner]]
     - [[03-x-learner|X-Learner]]
     - [[04-r-learner|R-Learner]]
   - [[03-doubly-robust|双重稳健学习]]

### 第三阶段：实战整合

将方法转化为业务价值和规范文档。

10. 分析文档写作
    - [[01-pyramid-principle|金字塔原理]]
    - [[02-conclusion-writing|核心结论写作]]
    - [[03-methods-section|方法说明写作]]
    - [[04-actionable-recommendations|落地建议颗粒度]]
    - [[05-numeric-expression|数字表达规范]]
    - [[06-limitations|局限性声明]]
11. 业务场景实战
    - [[01-search-analysis|搜索场景]]
    - [[02-recommendation-analysis|推荐场景]]
    - [[03-marketing-analysis|营销场景]]
    - [[04-growth-analysis|用户增长]]
12. 工具与工程
    - [[01-python-ecosystem|Python生态]]
    - [[02-r-ecosystem|R生态]]
    - [[03-experiment-platform|实验平台]]
    - [[04-reproducibility|可复现性]]

---

## 附录

- [[01-math-refresher|数学基础速查]]
- [[02-code-templates|代码模板库]]
- [[03-datasets|案例数据集]]
- [[04-resources|推荐资源清单]]

---

## 使用指南

### Obsidian 用户

1. 用 Obsidian 打开 `curriculum/` 目录
2. 安装 Graph View 插件查看知识图谱
3. 通过 [[wikilink]] 在知识点间跳转
4. 使用标签 `#课程/基础夯实` 筛选阶段

### VS Code 用户

1. 用 VS Code 打开 `projects/data-analysis/`
2. 安装 Markdown 插件和 Python 插件
3. `code/` 目录下的 `.py` 文件可直接运行
4. 使用 Jupyter 插件运行交互式代码

### 学习节奏建议

| 阶段 | 时间 | 目标 |
|---|---|---|
| 基础夯实 | 3-4 周 | 建立因果直觉；能独立分析简单AB实验 |
| 方法进阶 | 4-6 周 | 掌握2-3种高级方法；能处理观察性数据 |
| 实战整合 | 持续 | 输出规范文档；形成个人分析框架 |

---

*课程版本：v1.0*
*更新日期：2026-04-28*
*定制对象：国乔妻子（数据分析师）*
