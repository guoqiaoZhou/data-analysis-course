# MOC-统计基础

## 核心概念
- [[stage-01-foundation/02-statistical-basics/01-t-test/concept|t检验]] — 均值差异的假设检验
- [[stage-01-foundation/02-statistical-basics/02-chi-square-test/concept|卡方检验]] — 分类变量独立性检验
- [[stage-01-foundation/02-statistical-basics/03-bootstrap/concept|Bootstrap]] — 重抽样非参数方法
- [[stage-01-foundation/02-statistical-basics/04-ols-regression/concept|OLS回归]] — 线性关系估计
- [[stage-01-foundation/02-statistical-basics/05-logistic-regression/concept|Logistic回归]] — 二分类概率预测
- [[stage-01-foundation/02-statistical-basics/06-fixed-effects/concept|固定效应]] — 面板数据混杂控制
- [[stage-01-foundation/02-statistical-basics/07-power-analysis/concept|检验力分析]] — 样本量与MDE计算

## 概念关系
- t检验 ← 检验力分析（检验方法）
- Bootstrap ← t检验/卡方检验（替代方案）
- OLS回归 ← Logistic回归（连续vs分类因变量）
- 固定效应 ← OLS回归（面板数据扩展）
- 卡方检验 ← Bootstrap（分类变量方法）

## 学习路径
1. [[stage-01-foundation/02-statistical-basics/01-t-test/concept|t检验]] → 2. [[stage-01-foundation/02-statistical-basics/02-chi-square-test/concept|卡方检验]] → 3. [[stage-01-foundation/02-statistical-basics/03-bootstrap/concept|Bootstrap]]
4. [[stage-01-foundation/02-statistical-basics/04-ols-regression/concept|OLS回归]] → 5. [[stage-01-foundation/02-statistical-basics/05-logistic-regression/concept|Logistic回归]] → 6. [[stage-01-foundation/02-statistical-basics/06-fixed-effects/concept|固定效应]]
7. [[stage-01-foundation/02-statistical-basics/07-power-analysis/concept|检验力分析]]（贯穿始终）
