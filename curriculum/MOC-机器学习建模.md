# MOC-机器学习建模

## 核心概念
- [[stage-02-advanced/05-ml-modeling/01-xgboost/XGBoost|XGBoost]] — 梯度提升决策树
- [[stage-02-advanced/05-ml-modeling/02-shap/01-global-importance/SHAP全局重要性|SHAP全局]] — 全局特征重要性
- [[stage-02-advanced/05-ml-modeling/02-shap/02-local-explanation/SHAP局部解释|SHAP局部]] — 单样本解释
- [[stage-02-advanced/05-ml-modeling/02-shap/03-violin-plot/SHAP小提琴图|SHAP小提琴图]] — SHAP分布可视化
- [[stage-02-advanced/05-ml-modeling/03-ale-plots/ALE图|ALE图]] — 累积局部效应
- [[stage-02-advanced/05-ml-modeling/04-shap-interaction/SHAP交互效应|SHAP交互]] — 特征交互效应
- [[stage-02-advanced/05-ml-modeling/05-woe-iv/WOE-IV分箱|WOE/IV]] — 分箱与信息值
- [[stage-02-advanced/05-ml-modeling/06-gbdt-lr/GBDT-LR|GBDT+LR]] — 自动特征交叉

## 概念关系
- XGBoost → SHAP全局/局部/小提琴图（解释工具链）
- SHAP全局 ← ALE图（互补解释方法）
- SHAP交互 ← SHAP全局/局部（深化分析）
- WOE/IV ← GBDT+LR（特征工程方法）
- GBDT+LR ← XGBoost（模型架构）

## 学习路径
1. [[stage-02-advanced/05-ml-modeling/01-xgboost/XGBoost|XGBoost]] → 2. [[stage-02-advanced/05-ml-modeling/02-shap/01-global-importance/SHAP全局重要性|SHAP全局]] → 3. [[stage-02-advanced/05-ml-modeling/02-shap/02-local-explanation/SHAP局部解释|SHAP局部]]
4. [[stage-02-advanced/05-ml-modeling/02-shap/03-violin-plot/SHAP小提琴图|SHAP小提琴图]] → 5. [[stage-02-advanced/05-ml-modeling/03-ale-plots/ALE图|ALE图]] → 6. [[stage-02-advanced/05-ml-modeling/04-shap-interaction/SHAP交互效应|SHAP交互]]
7. [[stage-02-advanced/05-ml-modeling/05-woe-iv/WOE-IV分箱|WOE/IV]] → 8. [[stage-02-advanced/05-ml-modeling/06-gbdt-lr/GBDT-LR|GBDT+LR]]

## 相关主题

- [[MOC-因果推断|因果推断（因果ML）]]
- [[MOC-统计基础|统计基础（统计基础）]]
- [[MOC-阶段二-方法进阶|阶段二-方法进阶（阶段索引）]]
