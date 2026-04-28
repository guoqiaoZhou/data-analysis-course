import csv
import random
from datetime import datetime, timedelta

# 设置随机种子保证可复现
random.seed(42)

# 参数设置
N_REGIONS = 10
N_DAYS = 90
HOURS = list(range(24))

# 区域定义
regions = [f'R{str(i).zfill(2)}' for i in range(1, N_REGIONS + 1)]
region_types = random.choices(['cbd', 'residential', 'suburb', 'university'], k=N_REGIONS)
region_type_map = dict(zip(regions, region_types))

# 区域特性
region_density = {r: round(random.uniform(0.1, 1.0), 2) for r in regions}
region_income = {r: round(random.uniform(8, 30), 1) for r in regions}

# 日期范围
dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(N_DAYS)]

# 节假日
holidays = {
    datetime(2024, 1, 1),
    datetime(2024, 2, 10),
    datetime(2024, 2, 11),
    datetime(2024, 2, 12),
}

# 字段列表
fields = [
    'order_id', 'region_id', 'hour', 'date', 'day_of_week', 'is_weekend',
    'weather', 'temperature', 'humidity', 'wind_speed',
    'region_type', 'region_density', 'avg_income',
    'price', 'price_level', 'price_increase', 'price_increase_pct',
    'order_volume', 'ontime_rate', 'rider_supply', 'gmv', 'user_complaint_rate',
    'competitor_price', 'holiday', 'promotion_active',
    'historical_ontime_rate', 'historical_rider_supply', 'historical_order_volume',
    'is_peak', 'true_cate', 'selection_bias', 'price_elasticity'
]

data = []

for date in dates:
    date_str = date.strftime('%Y-%m-%d')
    day_of_week = date.weekday()
    is_weekend = day_of_week >= 5
    is_holiday = date in holidays
    month = date.month
    
    for region in regions:
        for hour in HOURS:
            # 天气
            if month in [12, 1, 2]:
                weather = random.choices(['sunny', 'rainy', 'snowy'], weights=[50, 30, 20])[0]
            elif month in [6, 7, 8]:
                weather = random.choices(['sunny', 'rainy', 'snowy'], weights=[70, 30, 0])[0]
            else:
                weather = random.choices(['sunny', 'rainy', 'snowy'], weights=[60, 35, 5])[0]
            
            # 温度
            base_temp = {1: -2, 2: 3, 3: 10, 4: 18, 5: 24, 6: 28,
                        7: 32, 8: 30, 9: 25, 10: 18, 11: 10, 12: 0}[month]
            if weather == 'rainy':
                base_temp -= 3
            elif weather == 'snowy':
                base_temp -= 8
            temperature = round(base_temp + random.gauss(0, 3), 1)
            
            # 湿度
            humidity = round(random.uniform(70, 95) if weather == 'rainy' else random.uniform(30, 90), 1)
            
            # 风速
            wind_speed = round(random.expovariate(1/8) + (5 if weather in ['rainy', 'snowy'] else 0), 1)
            
            # 区域类型
            rtype = region_type_map[region]
            
            # 是否高峰
            is_peak = hour in [7, 8, 11, 12, 17, 18, 19, 20, 21]
            
            # 基准价格
            base_price = 5.0
            if rtype == 'cbd':
                base_price += 1.0
            elif rtype == 'suburb':
                base_price += 2.0
            if is_peak:
                base_price += 1.5
            
            # 动态加价
            weather_premium = {'sunny': 0, 'rainy': 3.0, 'snowy': 5.0}[weather]
            peak_premium = 2.0 if is_peak else 0
            price = round(max(3.0, min(15.0, base_price + weather_premium + peak_premium + random.gauss(0, 0.5))), 2)
            
            price_increase = round(price - base_price, 2)
            price_increase_pct = round(price_increase / base_price, 3) if base_price > 0 else 0
            
            if price_increase_pct < 0.2:
                price_level = 'low'
            elif price_increase_pct < 0.5:
                price_level = 'medium'
            else:
                price_level = 'high'
            
            # 真实CATE
            if weather == 'rainy' and rtype == 'cbd' and is_peak:
                true_cate = 0.15
            elif weather == 'rainy' and rtype == 'suburb' and not is_peak:
                true_cate = -0.05
            elif weather == 'snowy':
                true_cate = 0.20
            elif weather == 'sunny' and rtype == 'residential' and is_peak:
                true_cate = 0.08
            else:
                true_cate = 0.02
            
            # 订单量
            base_order = 200 * region_density[region]
            weather_effect = {'sunny': 0, 'rainy': -30, 'snowy': -50}[weather]
            peak_effect = 50 if is_peak else -20
            weekend_effect = 20 if is_weekend else 0
            holiday_effect = 40 if is_holiday else 0
            price_effect = true_cate * price_increase * 10
            order_volume = int(max(50, min(500, base_order + weather_effect + peak_effect + 
                             weekend_effect + holiday_effect + price_effect + random.gauss(0, 20))))
            
            # 骑手供给
            base_rider = 100 * region_density[region]
            rider_weather = {'sunny': 0, 'rainy': -15, 'snowy': -25}[weather]
            rider_price_effect = 0.1 * price_increase * 10
            rider_supply = int(max(20, min(200, base_rider + rider_weather + rider_price_effect + random.gauss(0, 10))))
            
            # 准时率
            base_ontime = 0.85
            ontime_weather = {'sunny': 0, 'rainy': -0.05, 'snowy': -0.10}[weather]
            ontime_rider = 0.001 * (rider_supply - base_rider)
            ontime = round(max(0.6, min(0.95, base_ontime + ontime_weather + ontime_rider + random.gauss(0, 0.02))), 3)
            
            # GMV
            gmv = round(order_volume * 35 * (1 + price_increase / 10) / 10000, 3)
            
            # 投诉率
            base_complaint = 0.03
            complaint_price = 0.005 * price_increase
            complaint_ontime = -0.05 * (ontime - 0.85)
            complaint_rate = round(max(0.01, min(0.15, base_complaint + complaint_price + complaint_ontime + random.gauss(0, 0.01))), 3)
            
            # 竞品价格
            competitor_price = round(max(3.0, min(12.0, base_price + random.gauss(0, 1))), 2)
            
            # 营销活动
            promotion_active = random.random() < 0.1
            
            # 历史数据
            historical_ontime = round(ontime + random.gauss(0, 0.03), 3)
            historical_rider = int(rider_supply + random.gauss(0, 5))
            historical_order = int(order_volume + random.gauss(0, 15))
            
            # 价格弹性
            price_elasticity = round(-0.5 + true_cate * 5, 3)
            
            # 选择偏差
            selection_bias = round(abs(weather_effect) / 50, 3)
            
            record = [
                f'ORD_{date_str.replace("-", "")}_{region}_{hour:02d}',
                region, hour, date_str, day_of_week, is_weekend,
                weather, temperature, humidity, wind_speed,
                rtype, region_density[region], region_income[region],
                price, price_level, price_increase, price_increase_pct,
                order_volume, ontime, rider_supply, gmv, complaint_rate,
                competitor_price, is_holiday, promotion_active,
                historical_ontime, historical_rider, historical_order,
                is_peak, true_cate, selection_bias, price_elasticity
            ]
            data.append(record)

# 引入脏数据
n_records = len(data)

# 5% 缺失值
missing_indices = random.sample(range(n_records), int(n_records * 0.05))
for i in missing_indices[:len(missing_indices)//2]:
    data[i][13] = ''  # price
for i in missing_indices[len(missing_indices)//2:]:
    data[i][19] = ''  # rider_supply

# 2% 异常值
outlier_indices = random.sample(range(n_records), int(n_records * 0.02))
for i in outlier_indices:
    data[i][17] = int(data[i][17] * random.choice([3, 0.1]))  # order_volume

# 1% 逻辑错误
logic_indices = random.sample(range(n_records), int(n_records * 0.01))
for i in logic_indices:
    data[i][7] = 35.0  # 雨天但35度

# 保存原始数据
with open('/Users/zhouguoqiao/.openclaw/workspace/projects/data-analysis/curriculum/projects/project-03-rider-pricing/data/raw/rider_pricing_raw.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(data)

# 保存清洗后数据（去除缺失值、异常值、逻辑错误）
clean_data = []
for row in data:
    if row[13] == '' or row[19] == '':  # 跳过缺失值
        continue
    if int(row[17]) > 1000:  # 跳过极端异常值
        continue
    if row[6] == 'rainy' and float(row[7]) > 30:  # 跳过逻辑错误
        continue
    clean_data.append(row)

with open('/Users/zhouguoqiao/.openclaw/workspace/projects/data-analysis/curriculum/projects/project-03-rider-pricing/data/raw/rider_pricing_clean.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(clean_data)

print(f"原始数据: {len(data)} 条")
print(f"清洗后数据: {len(clean_data)} 条")
