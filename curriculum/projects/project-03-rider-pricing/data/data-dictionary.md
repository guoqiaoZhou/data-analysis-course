# 数据字典

## 数据集概述

- **数据集名称**: 骑手配送费动态定价模拟数据
- **记录数**: 10,000+
- **时间跨度**: 3个月（90天）
- **数据结构**: 面板数据（区域 × 时段 × 日期）
- **生成方式**: 基于真实外卖平台业务逻辑模拟

---

## 核心字段

### 标识字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `order_id` | string | 订单唯一标识 | `ORD_20240115_001` |
| `region_id` | categorical | 区域编码（10个区域） | `R01`, `R02`, ..., `R10` |
| `hour` | int | 时段（0-23） | `8`, `12`, `18` |
| `date` | date | 日期 | `2024-01-15` |
| `day_of_week` | int | 星期几（0=周一, 6=周日） | `0`, `5` |
| `is_weekend` | bool | 是否周末 | `True`, `False` |

### 处理变量（Treatment）

| 字段名 | 类型 | 说明 | 取值范围 |
|--------|------|------|----------|
| `price` | float | 配送费（元） | 3.0 - 15.0 |
| `price_level` | categorical | 价格档位 | `low`, `medium`, `high` |
| `price_increase` | float | 相比基准价的涨幅（元） | 0.0 - 8.0 |
| `price_increase_pct` | float | 相比基准价的涨幅比例 | 0.0 - 1.5 |

**价格生成机制**:
- 基准价：根据区域×时段的"历史均价"确定
- 动态加价：雨天/高峰/偏远区域自动加价
- 价格不是随机的——存在选择偏差

### 结果变量（Outcomes）

| 字段名 | 类型 | 说明 | 取值范围 |
|--------|------|------|----------|
| `order_volume` | int | 时段订单量 | 50 - 500 |
| `ontime_rate` | float | 准时率 | 0.6 - 0.95 |
| `rider_supply` | int | 在线骑手数 | 20 - 200 |
| `gmv` | float | 时段GMV（万元） | 1.0 - 50.0 |
| `user_complaint_rate` | float | 用户投诉率 | 0.01 - 0.15 |

### 协变量（Covariates）

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `weather` | categorical | 天气 | `sunny`, `rainy`, `snowy` |
| `temperature` | float | 温度（摄氏度） | `-5.0`, `25.0`, `35.0` |
| `humidity` | float | 湿度（%） | `30.0`, `80.0` |
| `wind_speed` | float | 风速（km/h） | `5.0`, `20.0` |
| `region_type` | categorical | 区域类型 | `cbd`, `residential`, `suburb`, `university` |
| `region_density` | float | 区域订单密度 | 0.1 - 1.0 |
| `avg_income` | float | 区域平均收入（万元/年） | 8.0 - 30.0 |
| `competitor_price` | float | 竞品配送费（元） | 3.0 - 12.0 |
| `holiday` | bool | 是否节假日 | `True`, `False` |
| `promotion_active` | bool | 是否有营销活动 | `True`, `False` |
| `historical_ontime_rate` | float | 历史准时率（7天平均） | 0.7 - 0.95 |
| `historical_rider_supply` | int | 历史骑手供给（7天平均） | 30 - 180 |
| `historical_order_volume` | int | 历史订单量（7天平均） | 60 - 450 |

### 构造字段（用于教学演示）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `true_cate` | float | 真实条件平均处理效应（CATE，用于评估估计精度） |
| `selection_bias` | float | 选择偏差强度（教学用） |
| `price_elasticity` | float | 真实价格弹性（区域×时段特异） |

---

## 数据生成机制（教学用）

### 异质性效应设计

```
真实CATE = f(weather, region_type, hour)

雨天CBD高峰: CATE = +0.15  (加价有效，骑手供给弹性高)
雨天郊区平峰: CATE = -0.05  (加价无效，用户流失效应 > 骑手效应)
晴天住宅高峰: CATE = +0.08  (加价中等有效)
雪天任何区域: CATE = +0.20  (加价高度有效)
```

### 选择偏差设计

```
价格不是随机的：
  price = baseline + weather_premium + peak_premium + region_premium + noise

雨天本来订单就少（不是因为价格）：
  order_volume = baseline - weather_penalty + price_effect + ...

简单回归会混淆：
  "雨天价格高，订单少" → 错误归因于价格
```

### 脏数据设计

| 问题类型 | 出现比例 | 处理方式 |
|----------|----------|----------|
| 缺失值 | 5% | `price` 和 `rider_supply` 字段 |
| 异常值 | 2% | `order_volume` 出现极端值 |
| 重复记录 | 1% | 同一订单ID出现多次 |
| 逻辑错误 | 1% | 雨天但温度35°C（数据录入错误） |

---

## 数据关系图

```
┌─────────────────────────────────────────────────────────────┐
│                        数据关系                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────┐         ┌──────────────┐                    │
│   │  天气    │────────→│    价格      │                    │
│   │ weather  │         │   price      │                    │
│   └──────────┘         └──────┬───────┘                    │
│          ↓                    ↓                             │
│   ┌──────────┐         ┌──────────────┐                    │
│   │  订单量  │←────────│   结果变量   │                    │
│   │order_vol │         │  outcomes    │                    │
│   └──────────┘         └──────────────┘                    │
│          ↑                                                  │
│   ┌──────────┐                                            │
│   │  骑手供给│                                            │
│   │rider_sup │                                            │
│   └──────────┘                                            │
│                                                             │
│   混淆路径：天气 → 价格 → 订单量                             │
│   但天气也直接影响订单量（选择偏差）                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 文件说明

| 文件名 | 说明 | 用途 |
|--------|------|------|
| `raw/rider_pricing_raw.csv` | 原始数据（含脏数据） | 数据清洗练习 |
| `raw/rider_pricing_clean.csv` | 清洗后数据 | 直接分析用 |
| `processed/rider_pricing_processed.csv` | 特征工程后数据 | 建模用 |
| `processed/rider_pricing_train.csv` | 训练集 | 模型训练 |
| `processed/rider_pricing_test.csv` | 测试集 | 模型验证 |

---

## 使用建议

1. **初学者**：从 `raw/rider_pricing_clean.csv` 开始，专注因果推断方法
2. **进阶者**：从 `raw/rider_pricing_raw.csv` 开始，包含数据清洗全流程
3. **教学用**：对比 `raw` 和 `clean` 的差异，理解数据质量对结论的影响
