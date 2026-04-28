# 数据字典

## 原始数据 (`data/raw/`)

### `experiment_data.csv`

实验主数据，包含用户实验分组及各项指标。

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `user_id` | string | 用户唯一标识 | `U_10001` |
| `group` | string | 实验分组：`control`（对照组）或 `treatment`（实验组） | `treatment` |
| `dau_date` | date | 实验日期 | `2024-01-15` |
| `dwell_time` | float | 当日停留时长（秒），右偏分布 | 1865.3 |
| `ctr` | float | 点击率（点击次数/曝光次数） | 0.085 |
| `retention_next_day` | int | 次日是否留存：0=否，1=是 | 1 |
| `historical_dwell_time` | float | 历史平均停留时长（CUPED用，实验前30天） | 1723.5 |
| `user_type` | string | 用户类型：`new`（新用户）或 `old`（老用户） | `old` |
| `device_type` | string | 设备类型：`iOS` 或 `Android` | `iOS` |
| `signup_date` | date | 注册日期 | `2023-06-12` |

### `user_attributes.csv`

用户属性数据，用于后分层分析。

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `user_id` | string | 用户唯一标识 | `U_10001` |
| `age_group` | string | 年龄段：`18-24`, `25-34`, `35-44`, `45+` | `25-34` |
| `gender` | string | 性别：`M`, `F`, `unknown` | `M` |
| `city_tier` | string | 城市级别：`tier1`, `tier2`, `tier3`, `tier4+` | `tier1` |
| `content_preference` | string | 内容偏好：`entertainment`, `knowledge`, `lifestyle`, `mixed` | `entertainment` |

---

## 清洗后数据 (`data/processed/`)

### `experiment_data_cleaned.csv`

清洗后的实验数据，已处理缺失值、异常值。

| 字段名 | 类型 | 说明 | 清洗规则 |
|--------|------|------|----------|
| `user_id` | string | 用户唯一标识 | 去重，保留首次出现 |
| `group` | string | 实验分组 | 校验：仅允许 `control` 或 `treatment` |
| `dau_date` | date | 实验日期 | 格式统一为 `YYYY-MM-DD` |
| `dwell_time` | float | 当日停留时长（秒） | 缺失值用历史均值填充；>7200秒（2小时）视为异常值，用99分位数截断 |
| `ctr` | float | 点击率 | 缺失值用0填充；>0.5视为异常值，用0.5截断 |
| `retention_next_day` | int | 次日留存 | 缺失值用历史留存率填充 |
| `historical_dwell_time` | float | 历史平均停留时长 | 缺失值用全局均值填充 |
| `user_type` | string | 用户类型 | 缺失值标记为 `unknown` |
| `device_type` | string | 设备类型 | 缺失值标记为 `unknown` |
| `dwell_time_cuped` | float | CUPED调整后的停留时长 | 详见 notebook 05 |

---

## 数据质量问题说明

### 缺失值

| 字段 | 缺失比例 | 原因 | 处理策略 |
|------|----------|------|----------|
| `dwell_time` | ~2% | 用户当日未产生有效行为 | 用历史均值填充 |
| `ctr` | ~3% | 曝光数为0，无法计算CTR | 用0填充 |
| `retention_next_day` | ~1% | 次日数据未回传 | 用历史留存率填充 |
| `historical_dwell_time` | ~5% | 新用户无历史数据 | 用全局均值填充 |
| `user_type` | ~0.5% | 注册信息缺失 | 标记为 `unknown` |

### 异常值

| 字段 | 异常规则 | 处理策略 |
|------|----------|----------|
| `dwell_time` | >7200秒（2小时） | 用99分位数截断 |
| `ctr` | >0.5（不合理的高点击率） | 用0.5截断 |
| `historical_dwell_time` | >7200秒 | 用99分位数截断 |

### 分布特征

- **停留时长**：右偏分布（对数正态），均值约1800秒，中位数约1200秒，标准差大
- **CTR**：近似Beta分布，均值约0.08，方差小
- **次日留存**：二项分布，均值约0.35

---

## 数据生成说明

本数据为模拟数据，但遵循真实APP用户行为规律：

- 用户停留时长服从对数正态分布
- 新用户停留时长显著低于老用户
- 实验组新算法对老用户效果更明显
- 包含真实的脏数据和异常值

---

## 使用建议

1. **先查看原始数据**：了解数据质量问题
2. **按notebook顺序处理**：清洗逻辑在 `04-action-analysis.ipynb` 中实现
3. **保留原始数据**：清洗后的数据另存，不覆盖原始数据
4. **记录清洗规则**：任何数据清洗都需要记录原因和方法
