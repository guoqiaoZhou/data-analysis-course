import csv
import random
import math

random.seed(42)

n = 10000

def normal_mean_std(mean, std):
    # Box-Muller transform
    u1 = random.random()
    u2 = random.random()
    z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return mean + std * z

rows = []
for i in range(n):
    user_id = 10001 + i
    age = max(18, min(65, int(normal_mean_std(35, 10))))
    gender = random.choice([0, 1])
    city_tier = random.choices([1, 2, 3, 4], weights=[15, 35, 35, 15])[0]
    membership_level = random.choices([0, 1, 2, 3], weights=[30, 40, 20, 10])[0]
    
    # 历史消费（对数正态）
    log_gmv = normal_mean_std(5, 1.2)
    historical_gmv = round(math.exp(log_gmv), 2)
    historical_orders = max(0, int(historical_gmv / 500 + random.gauss(0, 2)))
    
    # 活跃度
    activity_score = round(random.betavariate(2, 5) * 100, 2)
    
    # 优惠券敏感度
    coupon_sensitivity = round(random.betavariate(2, 3), 3)
    
    # 处理分配（非随机，强选择偏差）
    # 高历史消费 + 高优惠券敏感度的用户更可能获得优惠券
    treatment_prob = 0.1 + 0.4 * coupon_sensitivity + 0.3 * (historical_gmv / 1000) + 0.2 * (activity_score / 100)
    treatment_prob = min(0.95, max(0.05, treatment_prob))
    treatment = 1 if random.random() < treatment_prob else 0
    
    # 基础GMV
    base_gmv = 50 + 0.1 * historical_gmv + 0.5 * activity_score + 10 * membership_level
    
    # 处理效应（异质性）
    treatment_effect = 30 + 50 * coupon_sensitivity
    if historical_gmv > 400:  # 天花板效应
        treatment_effect *= 0.7
    
    # 最终GMV
    gmv = base_gmv + treatment * treatment_effect + random.gauss(0, 20)
    gmv = max(0, round(gmv, 2))
    
    rows.append([
        user_id, age, gender, city_tier, membership_level,
        historical_gmv, historical_orders, activity_score,
        coupon_sensitivity, treatment, gmv
    ])

# 保存
with open('data/raw/ecommerce_618.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['user_id', 'age', 'gender', 'city_tier', 'membership_level',
                     'historical_gmv', 'historical_orders', 'activity_score',
                     'coupon_sensitivity', 'treatment', 'gmv'])
    writer.writerows(rows)

# 简单统计
treated_gmv = [r[10] for r in rows if r[9] == 1]
control_gmv = [r[10] for r in rows if r[9] == 0]

print(f"数据生成完成：{n}条记录")
print(f"处理组占比：{len(treated_gmv)/n:.1%}")
print(f"处理组平均GMV：{sum(treated_gmv)/len(treated_gmv):.2f}")
print(f"对照组平均GMV：{sum(control_gmv)/len(control_gmv):.2f}")
print(f"简单差异：{sum(treated_gmv)/len(treated_gmv) - sum(control_gmv)/len(control_gmv):.2f}")

# 选择偏差检查
for col_idx, col_name in [(5, 'historical_gmv'), (7, 'activity_score'), (8, 'coupon_sensitivity')]:
    treated_vals = [r[col_idx] for r in rows if r[9] == 1]
    control_vals = [r[col_idx] for r in rows if r[9] == 0]
    t_mean = sum(treated_vals) / len(treated_vals)
    c_mean = sum(control_vals) / len(control_vals)
    t_var = sum((x - t_mean)**2 for x in treated_vals) / len(treated_vals)
    c_var = sum((x - c_mean)**2 for x in control_vals) / len(control_vals)
    smd = (t_mean - c_mean) / math.sqrt((t_var + c_var) / 2)
    print(f"{col_name}: 处理组={t_mean:.2f}, 对照组={c_mean:.2f}, SMD={smd:.3f}")
