# MOC-统计基础

## 核心概念
- [[01-t-test|t检验]] — 均值差异的假设检验
- [[02-chi-square-test|卡方检验]] — 分类变量独立性检验
- [[03-bootstrap|Bootstrap]] — 重抽样非参数方法
- [[04-ols-regression|OLS回归]] — 线性关系估计
- [[05-logistic-regression|Logistic回归]] — 二分类概率预测
- [[06-fixed-effects|固定效应]] — 面板数据混杂控制
- [[07-power-analysis|检验力分析]] — 样本量与MDE计算

## 概念关系
- t检验 ← 检验力分析（检验方法）
- Bootstrap ← t检验/卡方检验（替代方案）
- OLS回归 ← Logistic回归（连续vs分类因变量）
- 固定效应 ← OLS回归（面板数据扩展）
- 卡方检验 ← Bootstrap（分类变量方法）

## 学习路径
1. [[01-t-test|t检验]] → 2. [[02-chi-square-test|卡方检验]] → 3. [[03-bootstrap|Bootstrap]]
4. [[04-ols-regression|OLS回归]] → 5. [[05-logistic-regression|Logistic回归]] → 6. [[06-fixed-effects|固定效应]]
7. [[07-power-analysis|检验力分析]]（贯穿始终）
