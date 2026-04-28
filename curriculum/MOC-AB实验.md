# MOC-AB实验

## 核心概念
- [[stage-01-foundation/03-ab-testing/01-experiment-design/concept|实验设计]] — 设计要素详解
- [[stage-01-foundation/03-ab-testing/02-randomization/concept|随机化]] — 分流与正交分层
- [[stage-01-foundation/03-ab-testing/03-pre-aa-check/concept|Pre-AA检验]] — 实验前平衡检查
- [[stage-01-foundation/03-ab-testing/04-cuped/concept|CUPED]] — 方差缩减方法
- [[stage-01-foundation/03-ab-testing/05-post-stratification/concept|后分层]] — 协变量分层加权
- [[stage-01-foundation/03-ab-testing/06-multiple-testing/concept|多重检验]] — FWER与FDR控制
- [[stage-01-foundation/03-ab-testing/07-analysis-decision/concept|分析决策]] — 实验结果决策框架

## 概念关系
- 实验设计 → 随机化 → Pre-AA检验（流程链）
- CUPED ← 检验力分析（方差缩减降低样本量）
- 后分层 ← CUPED（互补方法）
- 多重检验 ← 分析决策（统计基础）
- Pre-AA检验 ← 随机化（验证工具）

## 学习路径
1. [[stage-01-foundation/03-ab-testing/01-experiment-design/concept|实验设计]] → 2. [[stage-01-foundation/03-ab-testing/02-randomization/concept|随机化]] → 3. [[stage-01-foundation/03-ab-testing/03-pre-aa-check/concept|Pre-AA检验]]
4. [[stage-01-foundation/03-ab-testing/04-cuped/concept|CUPED]] → 5. [[stage-01-foundation/03-ab-testing/05-post-stratification/concept|后分层]] → 6. [[stage-01-foundation/03-ab-testing/06-multiple-testing/concept|多重检验]] → 7. [[stage-01-foundation/03-ab-testing/07-analysis-decision/concept|分析决策]]
