# MOC-阶段二-方法进阶

## 核心概念

### 因果推断进阶
- [[stage-02-advanced/04-causal-inference/01-psm/01-matching-methods/concept|PSM匹配]] — 倾向得分匹配方法
- [[stage-02-advanced/04-causal-inference/01-psm/02-overlap-assumption/concept|重叠假设]] — 共同支持域
- [[stage-02-advanced/04-causal-inference/01-psm/03-sensitivity-analysis/concept|敏感性分析]] — 未观测混杂评估
- [[stage-02-advanced/04-causal-inference/02-did/01-parallel-trends/concept|平行趋势]] — DID核心假设检验
- [[stage-02-advanced/04-causal-inference/02-did/02-event-study/concept|事件研究法]] — 动态效应估计
- [[stage-02-advanced/04-causal-inference/02-did/03-synthetic-control/concept|合成控制]] — 反事实构造
- [[stage-02-advanced/04-causal-inference/03-dml/01-nuisance-estimation/concept|Nuisance估计]] — DML干扰函数
- [[stage-02-advanced/04-causal-inference/03-dml/02-cross-validation/concept|交叉验证]] — DML交叉拟合
- [[stage-02-advanced/04-causal-inference/03-dml/03-high-dimensional/concept|高维场景]] — 高维协变量处理

### 机器学习建模
- [[stage-02-advanced/05-ml-modeling/01-xgboost/concept|XGBoost]] — 梯度提升决策树
- [[stage-02-advanced/05-ml-modeling/02-shap/01-global-importance/concept|SHAP全局]] — 全局特征重要性
- [[stage-02-advanced/05-ml-modeling/02-shap/02-local-explanation/concept|SHAP局部]] — 单样本解释
- [[stage-02-advanced/05-ml-modeling/02-shap/03-violin-plot/concept|SHAP小提琴图]] — SHAP分布可视化
- [[stage-02-advanced/05-ml-modeling/03-ale-plots/concept|ALE图]] — 累积局部效应
- [[stage-02-advanced/05-ml-modeling/04-shap-interaction/concept|SHAP交互]] — 特征交互效应
- [[stage-02-advanced/05-ml-modeling/05-woe-iv/concept|WOE/IV]] — 分箱与信息值
- [[stage-02-advanced/05-ml-modeling/06-gbdt-lr/concept|GBDT+LR]] — 自动特征交叉

### 因果机器学习
- [[stage-02-advanced/06-causal-ml/01-causal-forest/01-splitting-criteria/concept|因果森林分裂]] — 异质性发现
- [[stage-02-advanced/06-causal-ml/01-causal-forest/02-confidence-intervals/concept|因果森林置信区间]] — 统计推断
- [[stage-02-advanced/06-causal-ml/02-meta-learners/01-s-learner/concept|S-Learner]] — 单模型CATE估计
- [[stage-02-advanced/06-causal-ml/02-meta-learners/02-t-learner/concept|T-Learner]] — 双模型CATE估计
- [[stage-02-advanced/06-causal-ml/02-meta-learners/03-x-learner/concept|X-Learner]] — 交叉估计CATE
- [[stage-02-advanced/06-causal-ml/02-meta-learners/04-r-learner/concept|R-Learner]] — 残差化CATE估计
- [[stage-02-advanced/06-causal-ml/03-doubly-robust/concept|双重稳健]] — AIPW估计

## 概念关系
- PSM匹配 → 重叠假设（匹配前提）
- PSM匹配 → 敏感性分析（稳健性检验）
- 平行趋势 → 事件研究法（假设检验方法）
- 平行趋势 ← 合成控制（替代方案）
- Nuisance估计 → 交叉验证（DML核心机制）
- Nuisance估计 ← 高维场景（应用场景）
- XGBoost → SHAP全局/局部/小提琴图（解释工具链）
- SHAP全局 ← ALE图（互补解释方法）
- SHAP交互 ← SHAP全局/局部（深化分析）
- 因果森林分裂 → 因果森林置信区间（完整流程）
- S-Learner → T-Learner → X-Learner → R-Learner（复杂度递进）
- 双重稳健 ← S/T/X/R-Learner（理论基础）

## 学习路径
1. [[stage-02-advanced/04-causal-inference/01-psm/01-matching-methods/concept|PSM匹配]] → 2. [[stage-02-advanced/04-causal-inference/01-psm/02-overlap-assumption/concept|重叠假设]] → 3. [[stage-02-advanced/04-causal-inference/01-psm/03-sensitivity-analysis/concept|敏感性分析]]
4. [[stage-02-advanced/04-causal-inference/02-did/01-parallel-trends/concept|平行趋势]] → 5. [[stage-02-advanced/04-causal-inference/02-did/02-event-study/concept|事件研究法]] → 6. [[stage-02-advanced/04-causal-inference/02-did/03-synthetic-control/concept|合成控制]]
7. [[stage-02-advanced/05-ml-modeling/01-xgboost/concept|XGBoost]] → 8. [[stage-02-advanced/05-ml-modeling/02-shap/01-global-importance/concept|SHAP全局]] → 9. [[stage-02-advanced/05-ml-modeling/02-shap/02-local-explanation/concept|SHAP局部]] → 10. [[stage-02-advanced/05-ml-modeling/04-shap-interaction/concept|SHAP交互]]
11. [[stage-02-advanced/06-causal-ml/02-meta-learners/01-s-learner/concept|S-Learner]] → 12. [[stage-02-advanced/06-causal-ml/02-meta-learners/02-t-learner/concept|T-Learner]] → 13. [[stage-02-advanced/06-causal-ml/02-meta-learners/03-x-learner/concept|X-Learner]] → 14. [[stage-02-advanced/06-causal-ml/02-meta-learners/04-r-learner/concept|R-Learner]]
