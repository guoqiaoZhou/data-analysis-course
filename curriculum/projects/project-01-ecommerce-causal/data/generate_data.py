import pandas as pd
import numpy as np

# 设置随机种子保证可复现
np.random.seed(42)

# 样本量
n = 10000

# 生成协变量
age = np.random.normal(35, 10, n).astype(int)
age = np.clip(age, 18, 65)

gender = np.random.choice([0, 1], n, p=[0.45, 0.55])

city_tier = np.random.choice([1, 2, 3, 4], n, p=[0.15, 0.35, 0.35, 0.15])

membership_level = np.random.choice([0, 1, 2, 3], n, p=[0.3, 0.4, 0.2, 0.1])

# 历史消费（对数正态分布）
historical_gmv = np.random.lognormal(5, 1.2, n)
historical_orders = np.random.poisson(historical_gmv / 500, n)

# 活跃度
activity_score = np.random.beta(2, 5, n) * 100

# 优惠券敏感度（关键变量，影响处理分配和结果）
coupon_sensitivity = np.random.beta(2, 3, n)

# 处理分配：非随机，强选择偏差
# 高历史消费 + 高优惠券敏感度的用户更可能获得优惠券
treatment_prob = 0.1 + 0.4 * coupon_sensitivity + 0.3 * (historical_gmv / 1000) + 0.2 * (activity_score / 100)
treatment_prob = np.clip(treatment_prob, 0.05, 0.95)
treatment = np.random.binomial(1, treatment_prob)

# 生成GMV（结果变量）
# 基础GMV
base_gmv = 50 + 0.1 * historical_gmv + 0.5 * activity_score + 10 * membership_level

# 处理效应：异质性，优惠券敏感度高的用户效应更大
treatment_effect = 30 + 50 * coupon_sensitivity

# 天花板效应：高消费用户效应递减
treatment_effect = treatment_effect * (1 - 0.3 * (historical_gmv > np.percentile(historical_gmv, 80)))

# 最终GMV
gmv = base_gmv + treatment * treatment_effect + np.random.normal(0, 20, n)
gmv = np.maximum(gmv, 0)

# 构造DataFrame
df = pd.DataFrame({
    'user_id': range(10001, 10001 + n),
    'age': age,
    'gender': gender,
    'city_tier': city_tier,
    'membership_level': membership_level,
    'historical_gmv': np.round(historical_gmv, 2),
    'historical_orders': historical_orders,
    'activity_score': np.round(activity_score, 2),
    'coupon_sensitivity': np.round(coupon_sensitivity, 3),
    'treatment': treatment,
    'gmv': np.round(gmv, 2)
})

# 保存
df.to_csv('data/raw/ecommerce_618.csv', index=False)

print(f"数据生成完成：{n}条记录")
print(f"处理组占比：{df['treatment'].mean():.1%}")
print(f"处理组平均GMV：{df[df['treatment']==1]['gmv'].mean():.2f}")
print(f"对照组平均GMV：{df[df['treatment']==0]['gmv'].mean():.2f}")
print(f"简单差异：{df[df['treatment']==1]['gmv'].mean() - df[df['treatment']==0]['gmv'].mean():.2f}")

# 检查选择偏差
covariates = ['historical_gmv', 'activity_score', 'coupon_sensitivity']
for col in covariates:
    treated_mean = df[df['treatment']==1][col].mean()
    control_mean = df[df['treatment']==0][col].mean()
    smd = (treated_mean - control_mean) / np.sqrt((df[df['treatment']==1][col].var() + df[df['treatment']==0][col].var()) / 2)
    print(f"{col}: 处理组={treated_mean:.2f}, 对照组={control_mean:.2f}, SMD={smd:.3f}")
