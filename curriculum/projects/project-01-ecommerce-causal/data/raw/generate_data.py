import csv
import random
import math

random.seed(42)

n = 10000

rows = []
for user_id in range(1, n + 1):
    age = max(18, min(65, int(random.gauss(35, 10))))
    gender = 1 if random.random() < 0.45 else 0
    city_tier = random.choices([1, 2, 3, 4], weights=[15, 30, 35, 20])[0]
    membership_level = random.choices([1, 2, 3, 4], weights=[40, 35, 20, 5])[0]

    base_consumption = 500 + age * 10 + membership_level * 200 + (5 - city_tier) * 100
    historical_gmv = max(0, round(base_consumption + random.gauss(0, 300), 2))
    historical_orders = max(0, int(historical_gmv / 150 + random.gauss(0, 5)))

    activity_score = round(max(0, min(100, 30 + membership_level * 15 + random.gauss(0, 15))), 2)
    coupon_sensitivity = round(max(0, min(1, 0.2 + activity_score / 200 + random.gauss(0, 0.1))), 3)

    # 非随机发放
    logit = -2.0 + 0.001 * historical_gmv + 0.02 * activity_score + 1.5 * coupon_sensitivity + 0.1 * membership_level
    treatment_prob = 1 / (1 + math.exp(-logit))
    treatment = 1 if random.random() < treatment_prob else 0

    # 真实因果效应
    treatment_effect = max(0, 50 + 200 * coupon_sensitivity - 0.05 * historical_gmv)

    gmv = max(0, round(0.3 * historical_gmv + treatment * treatment_effect + random.gauss(0, 100), 2))
    pre_gmv = max(0, round(0.25 * historical_gmv + random.gauss(0, 80), 2))
    post_gmv = max(0, round(0.25 * historical_gmv + treatment * treatment_effect * 0.5 + random.gauss(0, 80), 2))

    device_type = random.choices(["iOS", "Android", "Web"], weights=[35, 45, 20])[0]
    channel = random.choices(["app", "mini_program", "web"], weights=[50, 35, 15])[0]

    rows.append([
        user_id, treatment, gmv, age, gender, city_tier, membership_level,
        historical_gmv, historical_orders, activity_score, coupon_sensitivity,
        pre_gmv, post_gmv, device_type, channel
    ])

headers = [
    "user_id", "treatment", "gmv", "age", "gender", "city_tier", "membership_level",
    "historical_gmv", "historical_orders", "activity_score", "coupon_sensitivity",
    "pre_gmv", "post_gmv", "device_type", "channel"
]

with open("ecommerce_618.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"数据集已生成：{n}条记录")

treatment_count = sum(1 for r in rows if r[1] == 1)
print(f"处理组占比：{treatment_count / n:.1%}")

treated_gmv = [r[2] for r in rows if r[1] == 1]
control_gmv = [r[2] for r in rows if r[1] == 0]
print(f"平均GMV：处理组={sum(treated_gmv)/len(treated_gmv):.0f}, 对照组={sum(control_gmv)/len(control_gmv):.0f}")

treated_hist = [r[7] for r in rows if r[1] == 1]
control_hist = [r[7] for r in rows if r[1] == 0]
print(f"历史GMV差异：处理组={sum(treated_hist)/len(treated_hist):.0f}, 对照组={sum(control_hist)/len(control_hist):.0f}")
