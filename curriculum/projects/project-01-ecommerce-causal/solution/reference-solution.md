# 参考答案：电商618优惠券效果评估

## 项目概述

本项目评估618大促期间优惠券对用户GMV的因果效应。由于优惠券发放非随机，简单均值比较存在选择偏差，需使用因果推断方法。

---

## 1. 探索性分析

### 关键发现

- 样本量：10,000条记录
- 处理组占比：约40%
- 简单均值差异：处理组GMV显著高于对照组（约XXX元）
- 选择偏差证据：处理组在historical_gmv、activity_score、coupon_sensitivity上显著高于对照组

### 代码参考

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/raw/ecommerce_618.csv')

# 基本统计
print(df.describe())

# 处理组vs对照组
covariates = ['historical_gmv', 'activity_score', 'coupon_sensitivity', 'membership_level']
balance = df.groupby('treatment')[covariates].mean()
print(balance)

# 标准化差异
def calc_smd(df, col):
    treated = df[df['treatment']==1][col]
    control = df[df['treatment']==0][col]
    return (treated.mean() - control.mean()) / np.sqrt((treated.var() + control.var()) / 2)

for col in covariates:
    print(f"{col}: SMD = {calc_smd(df, col):.3f}")
```

---

## 2. 因果设计

### 方法选择

| 方法 | 适用性 | 理由 |
|------|--------|------|
| RCT | ❌ | 数据非随机分配 |
| PSM | ✅ | 协变量丰富，Common Support良好 |
| DID | ✅ | 有面板数据（pre/post） |
| 合成控制 | ⚠️ | 处理单元过多，非典型场景 |

**决策**：使用PSM和DID两种方法，互相验证。

---

## 3. PSM分析

### 完整代码

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
import statsmodels.api as sm

# 估计倾向得分
covariates = ['age', 'gender', 'city_tier', 'membership_level',
              'historical_gmv', 'historical_orders', 'activity_score', 'coupon_sensitivity']
X = df[covariates]
T = df['treatment']

ps_model = LogisticRegression(max_iter=1000)
ps_model.fit(X, T)
df['propensity_score'] = ps_model.predict_proba(X)[:, 1]

# 1:1最近邻匹配
treated = df[df['treatment'] == 1].copy()
control = df[df['treatment'] == 0].copy()

nbrs = NearestNeighbors(n_neighbors=1).fit(control[['propensity_score']])
distances, indices = nbrs.kneighbors(treated[['propensity_score']])

# 应用caliper
caliper = 0.05
valid = distances.flatten() <= caliper
treated_matched = treated[valid]
matched_control = control.iloc[indices[valid].flatten()]
matched_df = pd.concat([treated_matched, matched_control], ignore_index=True)

# 检查匹配质量
def calc_smd(df, col):
    treated = df[df['treatment']==1][col]
    control = df[df['treatment']==0][col]
    return (treated.mean() - control.mean()) / np.sqrt((treated.var() + control.var()) / 2)

print("匹配前后SMD对比:")
for col in covariates:
    before = calc_smd(df, col)
    after = calc_smd(matched_df, col)
    print(f"{col}: {before:.3f} -> {after:.3f}")

# 估计ATT
att_psm = (matched_df[matched_df['treatment']==1]['gmv'].mean() -
           matched_df[matched_df['treatment']==0]['gmv'].mean())
print(f"PSM ATT: {att_psm:.2f}")
```

### 关键结果

- 匹配后样本量：约3,000-4,000（取决于caliper）
- 匹配后SMD：大部分协变量 < 0.1
- PSM估计ATT：约50-100元（具体值取决于数据生成）

---

## 4. DID分析

### 完整代码

```python
# 构造面板数据
df_long = pd.melt(
    df,
    id_vars=['user_id', 'treatment', 'age', 'gender', 'city_tier',
             'membership_level', 'historical_gmv', 'historical_orders',
             'activity_score', 'coupon_sensitivity'],
    value_vars=['pre_gmv', 'post_gmv'],
    var_name='period',
    value_name='gmv'
)
df_long['post'] = (df_long['period'] == 'post_gmv').astype(int)
df_long['did'] = df_long['treatment'] * df_long['post']

# 经典DID
X = sm.add_constant(df_long[['treatment', 'post', 'did']])
model = sm.OLS(df_long['gmv'], X).fit()
print(model.summary())

att_did = model.params['did']
print(f"DID ATT: {att_did:.2f}")

# 协变量调整DID
covariates_long = ['age', 'gender', 'city_tier', 'membership_level',
                   'historical_gmv', 'historical_orders', 'activity_score', 'coupon_sensitivity']
X_cov = sm.add_constant(df_long[['treatment', 'post', 'did'] + covariates_long])
model_cov = sm.OLS(df_long['gmv'], X_cov).fit()
print(f"协变量DID ATT: {model_cov.params['did']:.2f}")

# PSM-DID
# 在matched_df上构造面板数据并运行DID
matched_long = pd.melt(
    matched_df,
    id_vars=['user_id', 'treatment'],
    value_vars=['pre_gmv', 'post_gmv'],
    var_name='period',
    value_name='gmv'
)
matched_long['post'] = (matched_long['period'] == 'post_gmv').astype(int)
matched_long['did'] = matched_long['treatment'] * matched_long['post']

X_psmdid = sm.add_constant(matched_long[['treatment', 'post', 'did']])
model_psmdid = sm.OLS(matched_long['gmv'], X_psmdid).fit()
print(f"PSM-DID ATT: {model_psmdid.params['did']:.2f}")
```

### 关键结果

- 经典DID ATT：约30-80元
- 协变量DID ATT：相近，标准误更小
- PSM-DID ATT：约40-90元

---

## 5. 结果汇总

| 方法 | ATT估计 | 特点 |
|------|---------|------|
| 简单差异 | 120-150元 | 高估，因选择偏差 |
| PSM | 50-100元 | 纠正选择偏差 |
| DID | 30-80元 | 利用面板结构 |
| PSM-DID | 40-90元 | 双重纠正 |

### 结论

1. **优惠券有正向因果效应**，但效应小于简单比较
2. **选择偏差方向**：处理组本身是高价值用户，简单比较高估了效应
3. **效应大小**：ATT约为50-80元（取决于方法和参数）
4. **异质性**：高优惠券敏感度用户效应更大；高历史消费用户效应较小（天花板效应）

---

## 6. 业务建议

1. **继续发放优惠券**，但优化目标人群
2. **避免过度投放高历史消费用户**（天花板效应）
3. **重点投放高敏感度、中等消费用户**
4. **设计随机化实验**以获得更精确的估计

---

## 7. 局限性

1. 可忽略性假设可能不成立（存在未观测混杂变量）
2. 只有一期前测，无法严格检验平行趋势
3. 数据为模拟数据，结论仅供参考
4. 未考虑溢出效应（处理组可能影响对照组）

---

## 完整分析思路

```
1. 理解业务问题 → 优惠券是否提升GMV？
2. 识别选择偏差 → 高价值用户更可能领券
3. 选择方法 → PSM + DID
4. 执行PSM → 匹配、检验平衡性、估计ATT
5. 执行DID → 构造面板、估计、检验
6. 对比验证 → 方法一致性增强可信度
7. 撰写报告 → 技术结论转化为业务语言
```
