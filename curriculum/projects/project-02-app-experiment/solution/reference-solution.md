# 参考答案

> ⚠️ **重要提示**：这是参考答案，用于在你遇到困难时参考。建议先独立完成，再对照查看。

---

## Notebook 01: Situation + Task

### 核心思路

1. **理解业务背景**：内容APP的核心指标是用户停留时长，新算法声称提升15%
2. **识别风险**：直接全量上线的风险包括——损害用户体验、降低留存、技术故障
3. **明确任务**：设计AB实验，用数据验证效果，给出上线建议

### 关键问题清单

- [ ] 主要指标（OEC）是什么？为什么是停留时长而不是CTR或留存？
- [ ] Guardrail指标是什么？需要监控哪些"不能坏"的指标？
- [ ] 实验周期多长？样本量多少？
- [ ] 如何分配用户？随机化的最小单元是什么？

### 参考答案要点

**OEC选择理由**：
- 停留时长是内容APP的核心北极星指标，直接反映用户参与度
- CTR可能受标题党影响，不代表真实满意度
- 留存是长期指标，实验周期内难以观测显著变化

**Guardrail指标**：
- 次日留存（不能显著下降）
- CTR（不能显著下降，反映内容匹配质量）

---

## Notebook 02: Action - 实验设计

### 核心思路

1. **确定统计参数**：α=0.05, 1-β=0.8, MDE=15%
2. **计算样本量**：使用t检验样本量公式或Python计算
3. **确定实验周期**：基于样本量和DAU计算
4. **设计随机化方案**：用户级别随机，确保同一用户始终在同一组

### 样本量计算代码

```python
import numpy as np
from scipy import stats

def sample_size_continuous(mean, std, mde_relative, alpha=0.05, power=0.8):
    """
    计算连续型指标的样本量
    
    参数:
        mean: 对照组均值
        std: 对照组标准差
        mde_relative: 相对最小可检测效应（如0.15表示15%）
        alpha: 显著性水平
        power: 统计功效
    """
    mde_absolute = mean * mde_relative
    
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    n = 2 * ((z_alpha + z_beta) * std / mde_absolute) ** 2
    
    return int(np.ceil(n))

# 假设历史数据：停留时长均值1800秒，标准差1200秒
mean_dwell = 1800
std_dwell = 1200
mde = 0.15  # 15%

n_per_group = sample_size_continuous(mean_dwell, std_dwell, mde)
print(f"每组需要样本量: {n_per_group}")
print(f"总样本量: {n_per_group * 2}")
```

### 随机化方案

```python
import pandas as pd
import hashlib

def assign_group(user_id, salt="experiment_2024_01", num_buckets=1000):
    """
    基于用户ID的确定性随机化
    确保同一用户始终分配到同一组
    """
    hash_input = f"{user_id}_{salt}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    bucket = hash_value % num_buckets
    
    if bucket < num_buckets // 2:
        return "control"
    else:
        return "treatment"

# 示例
users = pd.DataFrame({"user_id": [f"U_{i}" for i in range(10000)]})
users["group"] = users["user_id"].apply(assign_group)
print(users["group"].value_counts())
```

---

## Notebook 03: Action - 执行实验

### 核心思路

1. **模拟数据生成**：生成符合真实分布的实验数据
2. **数据验证**：检查分组比例、数据完整性
3. **AA检验**：实验前检验分组是否平衡

### 数据生成代码

```python
import numpy as np
import pandas as pd

np.random.seed(42)

n_users = 10000

# 用户属性
users = pd.DataFrame({
    "user_id": [f"U_{10000+i}" for i in range(n_users)],
    "user_type": np.random.choice(["new", "old"], n_users, p=[0.3, 0.7]),
    "device_type": np.random.choice(["iOS", "Android"], n_users, p=[0.4, 0.6]),
})

# 分组
users["group"] = users["user_id"].apply(assign_group)

# 历史停留时长（对数正态分布）
users["historical_dwell_time"] = np.random.lognormal(
    mean=np.log(1500), sigma=0.8, size=n_users
)

# 实验期间停留时长
# 对照组：与历史持平
# 实验组：提升约15%（对老用户效果更明显）
def generate_dwell_time(row):
    base = row["historical_dwell_time"]
    
    if row["group"] == "control":
        effect = 1.0
    else:
        # 新算法效果：老用户+18%，新用户+8%
        if row["user_type"] == "old":
            effect = 1.18
        else:
            effect = 1.08
    
    # 添加噪声
    noise = np.random.normal(0, base * 0.2)
    dwell = base * effect + noise
    
    return max(60, dwell)  # 至少60秒

users["dwell_time"] = users.apply(generate_dwell_time, axis=1)

# CTR（Beta分布）
users["ctr"] = np.random.beta(2, 23, n_users)
# 实验组CTR略降（推荐更精准但曝光减少）
users.loc[users["group"] == "treatment", "ctr"] *= 0.95

# 次日留存
base_retention = 0.35
users["retention_next_day"] = np.random.binomial(
    1, base_retention + (users["group"] == "treatment").astype(int) * 0.02
)

# 添加缺失值和异常值（脏数据）
# 约2%的dwell_time缺失
missing_idx = np.random.choice(users.index, size=int(n_users*0.02), replace=False)
users.loc[missing_idx, "dwell_time"] = np.nan

# 约0.5%的异常高停留时长
outlier_idx = np.random.choice(users.index, size=int(n_users*0.005), replace=False)
users.loc[outlier_idx, "dwell_time"] = np.random.uniform(7200, 18000, len(outlier_idx))

print(users.head())
print(f"\n分组比例:\n{users['group'].value_counts()}")
print(f"\n缺失值比例:\n{users.isnull().mean()}")
```

### AA检验代码

```python
from scipy import stats

def aa_test(df, metric, group_col="group"):
    """
    AA检验：检验实验前两组在指标上是否平衡
    """
    control = df[df[group_col] == "control"][metric].dropna()
    treatment = df[df[group_col] == "treatment"][metric].dropna()
    
    # t检验
    t_stat, p_value = stats.ttest_ind(control, treatment)
    
    print(f"AA检验 - {metric}")
    print(f"  对照组均值: {control.mean():.2f}")
    print(f"  实验组均值: {treatment.mean():.2f}")
    print(f"  差异: {treatment.mean() - control.mean():.2f}")
    print(f"  t统计量: {t_stat:.4f}")
    print(f"  p值: {p_value:.4f}")
    print(f"  结论: {'通过' if p_value > 0.05 else '未通过'} (p > 0.05)")
    print()
    
    return p_value > 0.05

# 对历史停留时长做AA检验
aa_test(users, "historical_dwell_time")
```

---

## Notebook 04: Action - 分析数据

### 核心思路

1. **数据清洗**：处理缺失值、异常值
2. **描述统计**：了解数据分布
3. **假设检验**：t检验比较两组差异
4. **效应量**：计算Cohen's d
5. **置信区间**：给出效应范围

### 数据清洗代码

```python
# 清洗逻辑
def clean_data(df):
    df_clean = df.copy()
    
    # 处理缺失值
    # dwell_time缺失：用历史均值填充
    dwell_mean = df_clean["historical_dwell_time"].mean()
    df_clean["dwell_time"] = df_clean["dwell_time"].fillna(dwell_mean)
    
    # 处理异常值：dwell_time > 7200秒（2小时）视为异常
    dwell_99 = df_clean["dwell_time"].quantile(0.99)
    df_clean["dwell_time"] = df_clean["dwell_time"].clip(upper=dwell_99)
    
    # CTR异常值
    df_clean["ctr"] = df_clean["ctr"].clip(upper=0.5)
    
    return df_clean

users_clean = clean_data(users)
```

### 假设检验代码

```python
from scipy import stats

def ab_test(df, metric, group_col="group"):
    """
    AB检验：比较两组在指标上的差异
    """
    control = df[df[group_col] == "control"][metric].dropna()
    treatment = df[df[group_col] == "treatment"][metric].dropna()
    
    # t检验（假设方差不等）
    t_stat, p_value = stats.ttest_ind(control, treatment, equal_var=False)
    
    # 效应量（Cohen's d）
    pooled_std = np.sqrt((control.var() + treatment.var()) / 2)
    cohens_d = (treatment.mean() - control.mean()) / pooled_std
    
    # 置信区间（95%）
    diff = treatment.mean() - control.mean()
    se = np.sqrt(control.var()/len(control) + treatment.var()/len(treatment))
    ci_lower = diff - 1.96 * se
    ci_upper = diff + 1.96 * se
    
    print(f"AB检验 - {metric}")
    print(f"  对照组: n={len(control)}, mean={control.mean():.2f}, std={control.std():.2f}")
    print(f"  实验组: n={len(treatment)}, mean={treatment.mean():.2f}, std={treatment.std():.2f}")
    print(f"  绝对差异: {diff:.2f}")
    print(f"  相对差异: {diff/control.mean()*100:.2f}%")
    print(f"  t统计量: {t_stat:.4f}")
    print(f"  p值: {p_value:.4f}")
    print(f"  Cohen's d: {cohens_d:.4f}")
    print(f"  95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]")
    print(f"  结论: {'显著' if p_value < 0.05 else '不显著'} (α=0.05)")
    print()
    
    return {
        "metric": metric,
        "control_mean": control.mean(),
        "treatment_mean": treatment.mean(),
        "diff": diff,
        "relative_diff": diff/control.mean(),
        "p_value": p_value,
        "cohens_d": cohens_d,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "significant": p_value < 0.05
    }

# 检验主要指标和guardrail指标
results = []
for metric in ["dwell_time", "ctr", "retention_next_day"]:
    result = ab_test(users_clean, metric)
    results.append(result)
```

### 多重检验校正

```python
from statsmodels.stats.multitest import multipletests

# 提取p值
p_values = [r["p_value"] for r in results]

# Bonferroni校正
reject_bonf, pvals_bonf, _, _ = multipletests(p_values, alpha=0.05, method='bonferroni')

# FDR校正 (Benjamini-Hochberg)
reject_fdr, pvals_fdr, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

print("多重检验校正结果:")
print(f"{'指标':<15} {'原始p值':<12} {'Bonferroni':<12} {'FDR':<12}")
for i, r in enumerate(results):
    print(f"{r['metric']:<15} {r['p_value']:<12.4f} {pvals_bonf[i]:<12.4f} {pvals_fdr[i]:<12.4f}")

print(f"\nBonferroni校正后显著: {sum(reject_bonf)}个")
print(f"FDR校正后显著: {sum(reject_fdr)}个")
```

---

## Notebook 05: Action - 迭代调整

### 核心思路

1. **CUPED方差缩减**：利用历史数据降低方差，提高检验力
2. **后分层分析**：识别不同用户群体的效果差异
3. **业务干扰处理**：记录并评估干扰对结论的影响

### CUPED代码

```python
def cuped_adjustment(df, metric, covariate, group_col="group"):
    """
    CUPED (Controlled-experiment Using Pre-Experiment Data)
    利用实验前数据作为协变量，降低方差
    """
    # 计算协方差和方差
    cov = df[metric].cov(df[covariate])
    var_cov = df[covariate].var()
    
    # 最优theta
    theta = cov / var_cov
    
    # 调整后的指标
    df["dwell_time_cuped"] = df[metric] - theta * (df[covariate] - df[covariate].mean())
    
    print(f"CUPED调整:")
    print(f"  原始方差: {df[metric].var():.2f}")
    print(f"  CUPED后方差: {df['dwell_time_cuped'].var():.2f}")
    print(f"  方差缩减: {(1 - df['dwell_time_cuped'].var()/df[metric].var())*100:.1f}%")
    print()
    
    return df

# 应用CUPED
users_cuped = cuped_adjustment(users_clean, "dwell_time", "historical_dwell_time")

# 用CUPED后的指标重新检验
ab_test(users_cuped, "dwell_time_cuped")
```

### 后分层分析代码

```python
def stratified_analysis(df, metric, stratify_col, group_col="group"):
    """
    后分层分析：按用户属性分层，看效果是否一致
    """
    print(f"后分层分析 - 按 {stratify_col} 分层")
    print("="*60)
    
    for stratum in df[stratify_col].unique():
        if pd.isna(stratum):
            continue
            
        subset = df[df[stratify_col] == stratum]
        control = subset[subset[group_col] == "control"][metric].dropna()
        treatment = subset[subset[group_col] == "treatment"][metric].dropna()
        
        if len(control) < 30 or len(treatment) < 30:
            continue
        
        t_stat, p_value = stats.ttest_ind(control, treatment, equal_var=False)
        diff = treatment.mean() - control.mean()
        
        print(f"  {stratum}: n={len(subset)}, 差异={diff:.2f}, p={p_value:.4f}, {'显著' if p_value < 0.05 else '不显著'}")
    
    print()

# 按用户类型分层
stratified_analysis(users_clean, "dwell_time", "user_type")

# 按设备类型分层
stratified_analysis(users_clean, "dwell_time", "device_type")
```

### 业务干扰处理

```python
# 干扰1：Peeking问题演示
def peeking_simulation(df, metric, n_peeks=5, alpha=0.05):
    """
    演示peeking问题：多次查看数据会提高假阳性率
    """
    print("Peeking问题演示:")
    print(f"  计划查看次数: {n_peeks}")
    print(f"  每次α={alpha}, 整体α≈{1-(1-alpha)**n_peeks:.3f}")
    print()
    
    # 模拟多次查看
    n_total = len(df)
    for i in range(1, n_peeks + 1):
        n_sample = int(n_total * i / n_peeks)
        subset = df.iloc[:n_sample]
        
        control = subset[subset["group"] == "control"][metric].dropna()
        treatment = subset[subset["group"] == "treatment"][metric].dropna()
        
        if len(control) > 10 and len(treatment) > 10:
            t_stat, p_value = stats.ttest_ind(control, treatment, equal_var=False)
            print(f"  第{i}次查看 (n={n_sample}): p={p_value:.4f} {'***' if p_value < alpha else ''}")

peeking_simulation(users_clean, "dwell_time")
```

---

## Notebook 06: Result

### 核心思路

1. **汇总所有分析结果**
2. **评估业务影响**
3. **给出明确建议**
4. **指出局限性和后续计划**

### 结论模板

```markdown
## 实验结论

### 主要发现
1. 新算法对用户停留时长有显著正向影响（+X%，p<0.05）
2. Guardrail指标安全：次日留存无显著下降，CTR略有下降但未达显著
3. 效果存在异质性：老用户效果更明显（+18%），新用户效果较弱（+8%）

### 业务建议
**建议：逐步上线**

理由：
- 主要指标显著为正，且效应量中等（Cohen's d ≈ 0.3）
- Guardrail指标安全，无重大风险
- 但CTR有下降趋势，需要监控

上线策略：
1. 先对老用户全量上线（效果最明显）
2. 对新用户保持观察，优化后再上线
3. 上线后持续监控CTR和留存

### 局限性
1. 实验周期仅2周，长期效果未知
2. 新用户样本量较小，结论不够稳健
3. 未考虑网络效应（社交推荐场景）

### 后续计划
1. 上线后跑反转实验（roll-back test）
2. 扩大样本量，专门验证新用户效果
3. 探索CTR下降的原因，优化推荐策略
```

---

## 常见错误与正确做法

| 错误做法 | 后果 | 正确做法 |
|----------|------|----------|
| 跳过AA检验 | 分组不平衡，结论失真 | 实验前必须做AA检验 |
| 忽略多重检验 | 假阳性率飙升（3个指标14%） | 使用Bonferroni或FDR校正 |
| Peeking | 假阳性率随查看次数增加 | 设定固定分析点，使用O'Brien-Fleming边界 |
| 只看p值 | 忽略效应量和业务意义 | 同时报告p值、效应量、置信区间 |
| 样本量不足 | 检验力不足，可能漏掉真实效应 | 实验前计算样本量，确保足够的统计功效 |
| 不看Guardrail | 主要指标提升但关键指标恶化 | 同时监控主要指标和guardrail指标 |

---

## 评分标准（供参考）

| 维度 | 权重 | 优秀标准 |
|------|------|----------|
| 实验设计 | 20% | 样本量计算正确，参数选择有依据 |
| 数据清洗 | 15% | 清洗逻辑清晰，记录完整 |
| 统计分析 | 25% | 检验方法正确，多重检验校正 |
| 深入分析 | 20% | CUPED、后分层等高级方法 |
| 业务洞察 | 20% | 结论明确，建议具体可操作 |
