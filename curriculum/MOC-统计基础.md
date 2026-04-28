# MOC-统计基础

## 核心概念
- [[stage-01-foundation/02-statistical-basics/01-t-test/t检验|t检验]] — 均值差异的假设检验
- [[stage-01-foundation/02-statistical-basics/02-chi-square-test/卡方检验|卡方检验]] — 分类变量独立性检验
- [[stage-01-foundation/02-statistical-basics/03-bootstrap/Bootstrap重抽样方法|Bootstrap]] — 重抽样非参数方法
- [[stage-01-foundation/02-statistical-basics/04-ols-regression/OLS回归|OLS回归]] — 线性关系估计
- [[stage-01-foundation/02-statistical-basics/05-logistic-regression/Logistic回归|Logistic回归]] — 二分类概率预测
- [[stage-01-foundation/02-statistical-basics/06-fixed-effects/固定效应模型|固定效应]] — 面板数据混杂控制
- [[stage-01-foundation/02-statistical-basics/07-power-analysis/检验力分析与样本量计算|检验力分析]] — 样本量与MDE计算

## 概念关系
- t检验 ← 检验力分析（检验方法）
- Bootstrap ← t检验/卡方检验（替代方案）
- OLS回归 ← Logistic回归（连续vs分类因变量）
- 固定效应 ← OLS回归（面板数据扩展）
- 卡方检验 ← Bootstrap（分类变量方法）

## 学习路径
1. [[stage-01-foundation/02-statistical-basics/01-t-test/t检验|t检验]] → 2. [[stage-01-foundation/02-statistical-basics/02-chi-square-test/卡方检验|卡方检验]] → 3. [[stage-01-foundation/02-statistical-basics/03-bootstrap/Bootstrap重抽样方法|Bootstrap]]
4. [[stage-01-foundation/02-statistical-basics/04-ols-regression/OLS回归|OLS回归]] → 5. [[stage-01-foundation/02-statistical-basics/05-logistic-regression/Logistic回归|Logistic回归]] → 6. [[stage-01-foundation/02-statistical-basics/06-fixed-effects/固定效应模型|固定效应]]
7. [[stage-01-foundation/02-statistical-basics/07-power-analysis/检验力分析与样本量计算|检验力分析]]（贯穿始终）

## 相关主题

- [[MOC-因果推断|因果推断（应用场景）]]
- [[MOC-AB实验|AB实验（应用场景）]]
- [[MOC-机器学习建模|机器学习建模（应用场景）]]
- [[MOC-阶段一-基础夯实|阶段一-基础夯实（阶段索引）]]
