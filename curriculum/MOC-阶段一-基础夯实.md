# MOC-阶段一-基础夯实

## 核心概念

### 因果推断基础
- [[stage-01-foundation/01-causal-inference-basics/01-potential-outcomes/潜在结果框架|潜在结果框架]] — 现代因果推断的数学基础
- [[stage-01-foundation/01-causal-inference-basics/02-randomized-experiments/随机化实验原理|随机化实验]] — 因果推断的黄金标准
- [[stage-01-foundation/01-causal-inference-basics/03-observational-challenges/观察性数据的挑战|观察性数据挑战]] — 混杂与选择偏误
- [[stage-01-foundation/01-causal-inference-basics/04-causation-vs-correlation/因果与相关的本质区别|因果vs相关]] — 本质区别与判断框架

### 统计基础
- [[stage-01-foundation/02-statistical-basics/01-t-test/t检验|t检验]] — 均值差异的假设检验
- [[stage-01-foundation/02-statistical-basics/02-chi-square-test/卡方检验|卡方检验]] — 分类变量独立性检验
- [[stage-01-foundation/02-statistical-basics/03-bootstrap/Bootstrap重抽样方法|Bootstrap]] — 重抽样非参数方法
- [[stage-01-foundation/02-statistical-basics/04-ols-regression/OLS回归|OLS回归]] — 线性关系估计
- [[stage-01-foundation/02-statistical-basics/05-logistic-regression/Logistic回归|Logistic回归]] — 二分类概率预测
- [[stage-01-foundation/02-statistical-basics/06-fixed-effects/固定效应模型|固定效应]] — 面板数据混杂控制
- [[stage-01-foundation/02-statistical-basics/07-power-analysis/检验力分析与样本量计算|检验力分析]] — 样本量与MDE计算

### AB实验
- [[stage-01-foundation/03-ab-testing/01-experiment-design/AB实验设计要素|实验设计]] — 设计要素详解
- [[stage-01-foundation/03-ab-testing/02-randomization/随机化与分流|随机化]] — 分流与正交分层
- [[stage-01-foundation/03-ab-testing/03-pre-aa-check/Pre-AA检验|Pre-AA检验]] — 实验前平衡检查
- [[stage-01-foundation/03-ab-testing/04-cuped/CUPED方差缩减|CUPED]] — 方差缩减方法
- [[stage-01-foundation/03-ab-testing/05-post-stratification/后分层分析|后分层]] — 协变量分层加权
- [[stage-01-foundation/03-ab-testing/06-multiple-testing/多重检验问题|多重检验]] — FWER与FDR控制
- [[stage-01-foundation/03-ab-testing/07-analysis-decision/实验分析决策框架|分析决策]] — 实验结果决策框架

## 概念关系
- 潜在结果框架 → 随机化实验（理论基础）
- 观察性数据挑战 ← 因果vs相关（应用场景）
- t检验 ← 检验力分析（检验方法）
- Bootstrap ← t检验/卡方检验（替代方案）
- OLS回归 ← Logistic回归（连续vs分类）
- 固定效应 ← OLS回归（面板数据扩展）
- 实验设计 → 随机化 → Pre-AA检验（流程链）
- CUPED ← 检验力分析（方差缩减降低样本量）
- 后分层 ← CUPED（互补方法）
- 多重检验 ← 分析决策（统计基础）

## 学习路径
1. [[stage-01-foundation/01-causal-inference-basics/01-potential-outcomes/潜在结果框架|潜在结果框架]] → 2. [[stage-01-foundation/01-causal-inference-basics/02-randomized-experiments/随机化实验原理|随机化实验]] → 3. [[stage-01-foundation/01-causal-inference-basics/03-observational-challenges/观察性数据的挑战|观察性数据挑战]] → 4. [[stage-01-foundation/01-causal-inference-basics/04-causation-vs-correlation/因果与相关的本质区别|因果vs相关]]
5. [[stage-01-foundation/02-statistical-basics/01-t-test/t检验|t检验]] → 6. [[stage-01-foundation/02-statistical-basics/02-chi-square-test/卡方检验|卡方检验]] → 7. [[stage-01-foundation/02-statistical-basics/03-bootstrap/Bootstrap重抽样方法|Bootstrap]] → 8. [[stage-01-foundation/02-statistical-basics/04-ols-regression/OLS回归|OLS回归]]
9. [[stage-01-foundation/03-ab-testing/01-experiment-design/AB实验设计要素|实验设计]] → 10. [[stage-01-foundation/03-ab-testing/02-randomization/随机化与分流|随机化]] → 11. [[stage-01-foundation/03-ab-testing/03-pre-aa-check/Pre-AA检验|Pre-AA检验]] → 12. [[stage-01-foundation/03-ab-testing/04-cuped/CUPED方差缩减|CUPED]]
