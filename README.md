---
title: 数据分析进阶课程
course-version: 1.0

tags: [课程索引, 数据分析, 因果推断]
---

# 数据分析进阶课程

> 从方法规范到体系化能力，覆盖因果推断、机器学习建模、实验设计与分析文档写作。
> 
> 每个知识点 = 独立目录，含 concept.md + code/ + exercises/ + references.md
> 知识点间通过 [[wikilink]] 双向链接，Obsidian 自动生成知识图谱。

---

## 快速导航

### 按阶段
- [[MOC-阶段一-基础夯实|MOC-阶段一]]
- [[MOC-阶段二-方法进阶|MOC-阶段二]]
- [[MOC-阶段三-实战整合|MOC-阶段三]]

### 按主题
- [[MOC-因果推断|MOC-因果推断]]
- [[MOC-统计基础|MOC-统计基础]]
- [[MOC-AB实验|MOC-AB实验]]
- [[MOC-机器学习建模|MOC-机器学习建模]]
- [[MOC-文档写作|MOC-文档写作]]
- [[MOC-业务场景|MOC-业务场景]]

---

## 学习路径

### 第一阶段：基础夯实

建立因果推断的数学直觉和统计基础。

1. [[stage-01-foundation/01-causal-inference-basics/01-potential-outcomes/concept|潜在结果框架]] — 因果推断的数学基础
2. [[stage-01-foundation/01-causal-inference-basics/02-randomized-experiments/concept|随机化实验原理]] — 黄金标准
3. [[stage-01-foundation/01-causal-inference-basics/03-observational-challenges/concept|观察性数据的挑战]] — 混杂与选择偏误
4. [[stage-01-foundation/01-causal-inference-basics/04-causation-vs-correlation/concept|因果 vs 相关]] — 本质区别
5. 统计基础
   - [[stage-01-foundation/02-statistical-basics/01-t-test/concept|t检验]]
   - [[stage-01-foundation/02-statistical-basics/02-chi-square-test/concept|卡方检验]]
   - [[stage-01-foundation/02-statistical-basics/03-bootstrap/concept|Bootstrap]]
   - [[stage-01-foundation/02-statistical-basics/04-ols-regression/concept|OLS回归]]
   - [[stage-01-foundation/02-statistical-basics/05-logistic-regression/concept|Logistic回归]]
   - [[stage-01-foundation/02-statistical-basics/06-fixed-effects/concept|固定效应模型]]
   - [[stage-01-foundation/02-statistical-basics/07-power-analysis/concept|检验力与样本量]]
6. AB实验全流程
   - [[stage-01-foundation/03-ab-testing/01-experiment-design/concept|实验设计要素]]
   - [[stage-01-foundation/03-ab-testing/02-randomization/concept|随机化与分流]]
   - [[stage-01-foundation/03-ab-testing/03-pre-aa-check/concept|Pre-AA检验]]
   - [[stage-01-foundation/03-ab-testing/04-cuped/concept|CUPED方差缩减]]
   - [[stage-01-foundation/03-ab-testing/05-post-stratification/concept|后分层分析]]
   - [[stage-01-foundation/03-ab-testing/06-multiple-testing/concept|多重检验问题]]
   - [[stage-01-foundation/03-ab-testing/07-analysis-decision/concept|实验分析决策]]

### 第二阶段：方法进阶

掌握高级因果推断方法和机器学习建模。

7. 因果推断进阶
   - PSM倾向得分匹配
     - [[stage-02-advanced/04-causal-inference/01-psm/01-matching-methods/concept|匹配方法]]
     - [[stage-02-advanced/04-causal-inference/01-psm/02-overlap-assumption/concept|重叠假设]]
     - [[stage-02-advanced/04-causal-inference/01-psm/03-sensitivity-analysis/concept|敏感性分析]]
   - DID双重差分
     - [[stage-02-advanced/04-causal-inference/02-did/01-parallel-trends/concept|平行趋势检验]]
     - [[stage-02-advanced/04-causal-inference/02-did/02-event-study/concept|事件研究法]]
     - [[stage-02-advanced/04-causal-inference/02-did/03-synthetic-control/concept|合成控制法]]
   - DML双重机器学习
     - [[stage-02-advanced/04-causal-inference/03-dml/01-nuisance-estimation/concept|Nuisance函数估计]]
     - [[stage-02-advanced/04-causal-inference/03-dml/02-cross-validation/concept|交叉验证策略]]
     - [[stage-02-advanced/04-causal-inference/03-dml/03-high-dimensional/concept|高维场景]]
8. 机器学习建模
   - [[stage-02-advanced/05-ml-modeling/01-xgboost/concept|XGBoost]]
   - SHAP解释
     - [[stage-02-advanced/05-ml-modeling/02-shap/01-global-importance/concept|全局重要性]]
     - [[stage-02-advanced/05-ml-modeling/02-shap/02-local-explanation/concept|局部解释]]
     - [[stage-02-advanced/05-ml-modeling/02-shap/03-violin-plot/concept|小提琴图]]
   - [[stage-02-advanced/05-ml-modeling/03-ale-plots/concept|ALE图]]
   - [[stage-02-advanced/05-ml-modeling/04-shap-interaction/concept|SHAP交互效应]]
   - [[stage-02-advanced/05-ml-modeling/05-woe-iv/concept|WOE/IV分箱]]
   - [[stage-02-advanced/05-ml-modeling/06-gbdt-lr/concept|GBDT+LR]]
9. 因果推断×机器学习交叉
   - 因果森林
     - [[stage-02-advanced/06-causal-ml/01-causal-forest/01-splitting-criteria/concept|分裂准则]]
     - [[stage-02-advanced/06-causal-ml/01-causal-forest/02-confidence-intervals/concept|置信区间]]
   - Meta-Learners
     - [[stage-02-advanced/06-causal-ml/02-meta-learners/01-s-learner/concept|S-Learner]]
     - [[stage-02-advanced/06-causal-ml/02-meta-learners/02-t-learner/concept|T-Learner]]
     - [[stage-02-advanced/06-causal-ml/02-meta-learners/03-x-learner/concept|X-Learner]]
     - [[stage-02-advanced/06-causal-ml/02-meta-learners/04-r-learner/concept|R-Learner]]
   - [[stage-02-advanced/06-causal-ml/03-doubly-robust/concept|双重稳健学习]]

### 第三阶段：实战整合

将方法转化为业务价值和规范文档。

10. 分析文档写作
    - [[stage-03-practice/07-document-writing/01-pyramid-principle/concept|金字塔原理]]
    - [[stage-03-practice/07-document-writing/02-conclusion-writing/concept|核心结论写作]]
    - [[stage-03-practice/07-document-writing/03-methods-section/concept|方法说明写作]]
    - [[stage-03-practice/07-document-writing/04-actionable-recommendations/concept|落地建议颗粒度]]
    - [[stage-03-practice/07-document-writing/05-numeric-expression/concept|数字表达规范]]
    - [[stage-03-practice/07-document-writing/06-limitations/concept|局限性声明]]
11. 业务场景实战
    - [[stage-03-practice/08-business-scenarios/01-search-analysis/concept|搜索场景]]
    - [[stage-03-practice/08-business-scenarios/02-recommendation-analysis/concept|推荐场景]]
    - [[stage-03-practice/08-business-scenarios/03-marketing-analysis/concept|营销场景]]
    - [[stage-03-practice/08-business-scenarios/04-growth-analysis/concept|用户增长]]
12. 工具与工程
    - [[stage-03-practice/09-tools-engineering/01-python-ecosystem/concept|Python生态]]
    - [[stage-03-practice/09-tools-engineering/02-r-ecosystem/concept|R生态]]
    - [[stage-03-practice/09-tools-engineering/03-experiment-platform/concept|实验平台]]
    - [[stage-03-practice/09-tools-engineering/04-reproducibility/concept|可复现性]]

---

## 附录

- [[appendix/01-math-refresher/concept|数学基础速查]]
- [[appendix/02-code-templates/concept|代码模板库]]
- [[appendix/03-datasets/concept|案例数据集]]
- [[appendix/04-resources/concept|推荐资源清单]]

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
3. `curriculum/**/code/` 目录下的 `.py` 文件可直接运行
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
