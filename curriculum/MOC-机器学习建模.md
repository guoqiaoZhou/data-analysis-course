# MOC-机器学习建模

## 核心概念
- [[01-xgboost|XGBoost]] — 梯度提升决策树
- [[01-global-importance|SHAP全局]] — 全局特征重要性
- [[02-local-explanation|SHAP局部]] — 单样本解释
- [[03-violin-plot|SHAP小提琴图]] — SHAP分布可视化
- [[03-ale-plots|ALE图]] — 累积局部效应
- [[04-shap-interaction|SHAP交互]] — 特征交互效应
- [[05-woe-iv|WOE/IV]] — 分箱与信息值
- [[06-gbdt-lr|GBDT+LR]] — 自动特征交叉

## 概念关系
- XGBoost → SHAP全局/局部/小提琴图（解释工具链）
- SHAP全局 ← ALE图（互补解释方法）
- SHAP交互 ← SHAP全局/局部（深化分析）
- WOE/IV ← GBDT+LR（特征工程方法）
- GBDT+LR ← XGBoost（模型架构）

## 学习路径
1. [[01-xgboost|XGBoost]] → 2. [[01-global-importance|SHAP全局]] → 3. [[02-local-explanation|SHAP局部]]
4. [[03-violin-plot|SHAP小提琴图]] → 5. [[03-ale-plots|ALE图]] → 6. [[04-shap-interaction|SHAP交互]]
7. [[05-woe-iv|WOE/IV]] → 8. [[06-gbdt-lr|GBDT+LR]]
