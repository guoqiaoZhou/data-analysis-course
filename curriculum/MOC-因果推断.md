# MOC-因果推断

## 核心概念
- [[stage-01-foundation/01-causal-inference-basics/01-potential-outcomes/潜在结果框架|潜在结果框架]] — 现代因果推断的数学基础
- [[stage-01-foundation/01-causal-inference-basics/02-randomized-experiments/随机化实验原理|随机化实验]] — 因果推断的黄金标准
- [[stage-01-foundation/01-causal-inference-basics/03-observational-challenges/观察性数据的挑战|观察性数据挑战]] — 混杂与选择偏误
- [[stage-01-foundation/01-causal-inference-basics/04-causation-vs-correlation/因果与相关的本质区别|因果vs相关]] — 本质区别与判断框架
- [[stage-02-advanced/04-causal-inference/01-psm/01-matching-methods/PSM匹配方法|PSM匹配]] — 倾向得分匹配方法
- [[stage-02-advanced/04-causal-inference/01-psm/02-overlap-assumption/重叠假设|重叠假设]] — 共同支持域
- [[stage-02-advanced/04-causal-inference/01-psm/03-sensitivity-analysis/敏感性分析|敏感性分析]] — 未观测混杂评估
- [[stage-02-advanced/04-causal-inference/02-did/01-parallel-trends/DID平行趋势检验|平行趋势]] — DID核心假设检验
- [[stage-02-advanced/04-causal-inference/02-did/02-event-study/事件研究法|事件研究法]] — 动态效应估计
- [[stage-02-advanced/04-causal-inference/02-did/03-synthetic-control/合成控制法|合成控制]] — 反事实构造
- [[stage-02-advanced/04-causal-inference/03-dml/01-nuisance-estimation/Nuisance函数估计|Nuisance估计]] — DML干扰函数
- [[stage-02-advanced/04-causal-inference/03-dml/02-cross-validation/交叉验证策略|交叉验证]] — DML交叉拟合
- [[stage-02-advanced/04-causal-inference/03-dml/03-high-dimensional/高维场景|高维场景]] — 高维协变量处理
- [[stage-02-advanced/06-causal-ml/01-causal-forest/01-splitting-criteria/因果森林分裂准则|因果森林分裂]] — 异质性发现
- [[stage-02-advanced/06-causal-ml/01-causal-forest/02-confidence-intervals/因果森林置信区间|因果森林置信区间]] — 统计推断
- [[stage-02-advanced/06-causal-ml/02-meta-learners/01-s-learner/S-Learner|S-Learner]] — 单模型CATE估计
- [[stage-02-advanced/06-causal-ml/02-meta-learners/02-t-learner/T-Learner|T-Learner]] — 双模型CATE估计
- [[stage-02-advanced/06-causal-ml/02-meta-learners/03-x-learner/X-Learner|X-Learner]] — 交叉估计CATE
- [[stage-02-advanced/06-causal-ml/02-meta-learners/04-r-learner/R-Learner|R-Learner]] — 残差化CATE估计
- [[stage-02-advanced/06-causal-ml/03-doubly-robust/双重稳健学习|双重稳健]] — AIPW估计

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
1. [[stage-01-foundation/01-causal-inference-basics/01-potential-outcomes/潜在结果框架|潜在结果框架]] → 2. [[stage-01-foundation/01-causal-inference-basics/02-randomized-experiments/随机化实验原理|随机化实验]] → 3. [[stage-01-foundation/01-causal-inference-basics/03-observational-challenges/观察性数据的挑战|观察性数据挑战]]
4. [[stage-02-advanced/04-causal-inference/01-psm/01-matching-methods/PSM匹配方法|PSM匹配]] → 5. [[stage-02-advanced/04-causal-inference/02-did/01-parallel-trends/DID平行趋势检验|平行趋势]] → 6. [[stage-02-advanced/04-causal-inference/02-did/02-event-study/事件研究法|事件研究法]] → 7. [[stage-02-advanced/04-causal-inference/02-did/03-synthetic-control/合成控制法|合成控制]]
8. [[stage-02-advanced/06-causal-ml/02-meta-learners/01-s-learner/S-Learner|S-Learner]] → 9. [[stage-02-advanced/06-causal-ml/02-meta-learners/02-t-learner/T-Learner|T-Learner]] → 10. [[stage-02-advanced/06-causal-ml/02-meta-learners/03-x-learner/X-Learner|X-Learner]] → 11. [[stage-02-advanced/06-causal-ml/02-meta-learners/04-r-learner/R-Learner|R-Learner]]

## 相关主题

- [[MOC-统计基础|统计基础（统计工具）]]
- [[MOC-AB实验|AB实验（实验方法）]]
- [[MOC-机器学习建模|机器学习建模（ML辅助因果）]]
- [[MOC-阶段一-基础夯实|阶段一-基础夯实（阶段索引）]]
- [[MOC-阶段二-方法进阶|阶段二-方法进阶（阶段索引）]]
