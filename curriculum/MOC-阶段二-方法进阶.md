# MOC-阶段二-方法进阶

## 核心概念

### 因果推断进阶
- [[01-matching-methods|PSM匹配]] — 倾向得分匹配方法
- [[02-overlap-assumption|重叠假设]] — 共同支持域
- [[03-sensitivity-analysis|敏感性分析]] — 未观测混杂评估
- [[01-parallel-trends|平行趋势]] — DID核心假设检验
- [[02-event-study|事件研究法]] — 动态效应估计
- [[03-synthetic-control|合成控制]] — 反事实构造
- [[01-nuisance-estimation|Nuisance估计]] — DML干扰函数
- [[02-cross-validation|交叉验证]] — DML交叉拟合
- [[03-high-dimensional|高维场景]] — 高维协变量处理

### 机器学习建模
- [[01-xgboost|XGBoost]] — 梯度提升决策树
- [[01-global-importance|SHAP全局]] — 全局特征重要性
- [[02-local-explanation|SHAP局部]] — 单样本解释
- [[03-violin-plot|SHAP小提琴图]] — SHAP分布可视化
- [[03-ale-plots|ALE图]] — 累积局部效应
- [[04-shap-interaction|SHAP交互]] — 特征交互效应
- [[05-woe-iv|WOE/IV]] — 分箱与信息值
- [[06-gbdt-lr|GBDT+LR]] — 自动特征交叉

### 因果机器学习
- [[01-splitting-criteria|因果森林分裂]] — 异质性发现
- [[02-confidence-intervals|因果森林置信区间]] — 统计推断
- [[01-s-learner|S-Learner]] — 单模型CATE估计
- [[02-t-learner|T-Learner]] — 双模型CATE估计
- [[03-x-learner|X-Learner]] — 交叉估计CATE
- [[04-r-learner|R-Learner]] — 残差化CATE估计
- [[03-doubly-robust|双重稳健]] — AIPW估计

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
1. [[01-matching-methods|PSM匹配]] → 2. [[02-overlap-assumption|重叠假设]] → 3. [[03-sensitivity-analysis|敏感性分析]]
4. [[01-parallel-trends|平行趋势]] → 5. [[02-event-study|事件研究法]] → 6. [[03-synthetic-control|合成控制]]
7. [[01-xgboost|XGBoost]] → 8. [[01-global-importance|SHAP全局]] → 9. [[02-local-explanation|SHAP局部]] → 10. [[04-shap-interaction|SHAP交互]]
11. [[01-s-learner|S-Learner]] → 12. [[02-t-learner|T-Learner]] → 13. [[03-x-learner|X-Learner]] → 14. [[04-r-learner|R-Learner]]
