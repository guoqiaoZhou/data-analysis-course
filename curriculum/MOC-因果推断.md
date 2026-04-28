# MOC-因果推断

## 核心概念
- [[01-potential-outcomes|潜在结果框架]] — 现代因果推断的数学基础
- [[02-randomized-experiments|随机化实验]] — 因果推断的黄金标准
- [[03-observational-challenges|观察性数据挑战]] — 混杂与选择偏误
- [[04-causation-vs-correlation|因果vs相关]] — 本质区别与判断框架
- [[01-matching-methods|PSM匹配]] — 倾向得分匹配方法
- [[02-overlap-assumption|重叠假设]] — 共同支持域
- [[03-sensitivity-analysis|敏感性分析]] — 未观测混杂评估
- [[01-parallel-trends|平行趋势]] — DID核心假设检验
- [[02-event-study|事件研究法]] — 动态效应估计
- [[03-synthetic-control|合成控制]] — 反事实构造
- [[01-nuisance-estimation|Nuisance估计]] — DML干扰函数
- [[02-cross-validation|交叉验证]] — DML交叉拟合
- [[03-high-dimensional|高维场景]] — 高维协变量处理
- [[01-splitting-criteria|因果森林分裂]] — 异质性发现
- [[02-confidence-intervals|因果森林置信区间]] — 统计推断
- [[01-s-learner|S-Learner]] — 单模型CATE估计
- [[02-t-learner|T-Learner]] — 双模型CATE估计
- [[03-x-learner|X-Learner]] — 交叉估计CATE
- [[04-r-learner|R-Learner]] — 残差化CATE估计
- [[03-doubly-robust|双重稳健]] — AIPW估计

## 概念关系
- 潜在结果框架 → 随机化实验（理论基础）
- 观察性数据挑战 ← PSM匹配（解决工具）
- PSM匹配 → 重叠假设（匹配前提）
- PSM匹配 → 敏感性分析（稳健性检验）
- 平行趋势 → 事件研究法（检验方法）
- 平行趋势 ← 合成控制（替代方案）
- Nuisance估计 → 交叉验证（DML机制）
- 因果森林分裂 → 因果森林置信区间（完整流程）
- S-Learner → T-Learner → X-Learner → R-Learner（复杂度递进）
- 双重稳健 ← Meta-Learners（理论基础）

## 学习路径
1. [[01-potential-outcomes|潜在结果框架]] → 2. [[02-randomized-experiments|随机化实验]] → 3. [[03-observational-challenges|观察性数据挑战]]
4. [[01-matching-methods|PSM匹配]] → 5. [[01-parallel-trends|平行趋势]] → 6. [[02-event-study|事件研究法]] → 7. [[03-synthetic-control|合成控制]]
8. [[01-s-learner|S-Learner]] → 9. [[02-t-learner|T-Learner]] → 10. [[03-x-learner|X-Learner]] → 11. [[04-r-learner|R-Learner]]
