"""
PSM (Propensity Score Matching) 模拟演示

本脚本演示：
1. 倾向得分估计（Logistic 回归）
2. 1:1 最近邻匹配
3. 匹配前后的平衡性检验（标准化均值差异 SMD）
4. ATT（处理组平均处理效应）估计
5. 重叠区域 / 共同支撑可视化
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from scipy.spatial.distance import cdist

# 中文显示设置
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_data(n=1000, true_att=3.0):
    """生成观测数据，包含混杂变量。"""
    # 连续型混杂变量
    x1 = np.random.normal(0, 1, n)
    x2 = np.random.normal(0, 1, n)
    # 二分类混杂变量
    x3 = np.random.binomial(1, 0.5, n)

    # 处理分配（受混杂变量影响）
    propensity_logit = -0.5 + 0.8 * x1 + 0.5 * x2 - 0.6 * x3
    propensity = 1 / (1 + np.exp(-propensity_logit))
    treatment = np.random.binomial(1, propensity)

    # 结果变量
    y0 = 1.0 + 1.5 * x1 + 0.8 * x2 + 1.2 * x3 + np.random.normal(0, 1, n)
    y1 = y0 + true_att
    y = treatment * y1 + (1 - treatment) * y0

    df = pd.DataFrame({
        'x1': x1, 'x2': x2, 'x3': x3,
        'treatment': treatment,
        'y': y, 'y0': y0, 'y1': y1,
        'true_att': true_att
    })
    return df


def estimate_propensity(df):
    """使用 Logistic 回归估计倾向得分。"""
    X = df[['x1', 'x2', 'x3']]
    model = LogisticRegression(max_iter=1000, solver='lbfgs')
    model.fit(X, df['treatment'])
    df = df.copy()
    df['propensity'] = model.predict_proba(X)[:, 1]
    return df, model


def nearest_neighbor_matching(df, caliper=None):
    """1:1 最近邻匹配（无放回）。"""
    treated = df[df['treatment'] == 1].copy().reset_index(drop=True)
    control = df[df['treatment'] == 0].copy().reset_index(drop=True)

    treated_ps = treated['propensity'].values.reshape(-1, 1)
    control_ps = control['propensity'].values.reshape(-1, 1)

    distances = cdist(treated_ps, control_ps, metric='euclidean')
    matched_control_indices = []
    used_controls = set()

    for i in range(len(treated)):
        sorted_indices = np.argsort(distances[i])
        for j in sorted_indices:
            if j in used_controls:
                continue
            if caliper is not None and distances[i, j] > caliper:
                break
            matched_control_indices.append(j)
            used_controls.add(j)
            break

    matched_control = control.iloc[matched_control_indices].reset_index(drop=True)
    matched_treated = treated.iloc[:len(matched_control_indices)].reset_index(drop=True)

    matched_df = pd.concat([
        matched_treated.assign(group='treated'),
        matched_control.assign(group='control')
    ], ignore_index=True)

    return matched_df


def compute_smd(df, var, treatment_col='treatment'):
    """计算单个变量的标准化均值差异（SMD）。"""
    treated = df[df[treatment_col] == 1][var]
    control = df[df[treatment_col] == 0][var]
    pooled_std = np.sqrt((treated.var() + control.var()) / 2)
    if pooled_std == 0:
        return 0.0
    return (treated.mean() - control.mean()) / pooled_std


def balance_table(df, vars_list, treatment_col='treatment'):
    """生成平衡性表格。"""
    records = []
    for var in vars_list:
        records.append({
            '变量': var,
            'SMD': compute_smd(df, var, treatment_col)
        })
    return pd.DataFrame(records)


def estimate_att(df, matched_df):
    """估计 ATT：匹配前后对比。"""
    # 匹配前
    pre_treated = df[df['treatment'] == 1]['y'].mean()
    pre_control = df[df['treatment'] == 0]['y'].mean()
    pre_att = pre_treated - pre_control

    # 匹配后
    post_treated = matched_df[matched_df['group'] == 'treated']['y'].mean()
    post_control = matched_df[matched_df['group'] == 'control']['y'].mean()
    post_att = post_treated - post_control

    return pre_att, post_att


def scenario_psm():
    """PSM 完整流程演示。"""
    print("=" * 60)
    print("【场景】PSM 倾向得分匹配完整演示")
    print("=" * 60)

    df = generate_data(n=1000, true_att=3.0)
    print(f"\n1. 数据生成：总样本量 n={len(df)}，处理组 n={df['treatment'].sum()}，对照组 n={len(df)-df['treatment'].sum()}")

    # 倾向得分估计
    df, ps_model = estimate_propensity(df)
    print("\n2. 倾向得分估计完成（Logistic 回归）")
    print(f"   倾向得分范围: [{df['propensity'].min():.4f}, {df['propensity'].max():.4f}]")

    # 匹配
    matched_df = nearest_neighbor_matching(df, caliper=0.2)
    print(f"\n3. 1:1 最近邻匹配完成（caliper=0.2）")
    print(f"   成功匹配对数: {len(matched_df[matched_df['group']=='treated'])}")

    # 平衡性检验
    vars_list = ['x1', 'x2', 'x3']
    print("\n4. 平衡性检验（SMD）")
    print("   匹配前:")
    pre_balance = balance_table(df, vars_list)
    for _, row in pre_balance.iterrows():
        flag = "✓" if abs(row['SMD']) < 0.1 else "✗"
        print(f"      {row['变量']}: SMD={row['SMD']:.4f} {flag}")

    # 为 matched_df 构造 treatment 列以便复用 balance_table
    matched_df_for_balance = matched_df.copy()
    matched_df_for_balance['treatment'] = (matched_df_for_balance['group'] == 'treated').astype(int)
    print("   匹配后:")
    post_balance = balance_table(matched_df_for_balance, vars_list)
    for _, row in post_balance.iterrows():
        flag = "✓" if abs(row['SMD']) < 0.1 else "✗"
        print(f"      {row['变量']}: SMD={row['SMD']:.4f} {flag}")

    # ATT 估计
    pre_att, post_att = estimate_att(df, matched_df)
    true_att = df['true_att'].iloc[0]
    print(f"\n5. ATT 估计")
    print(f"   真实 ATT: {true_att:.4f}")
    print(f"   匹配前 ATT: {pre_att:.4f} (偏差={abs(pre_att-true_att):.4f})")
    print(f"   匹配后 ATT: {post_att:.4f} (偏差={abs(post_att-true_att):.4f})")

    return df, matched_df, pre_balance, post_balance


def visualize_results(df, matched_df, pre_balance, post_balance):
    """生成可视化图表。"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 倾向得分分布（匹配前）
    ax = axes[0, 0]
    ax.hist(df[df['treatment'] == 1]['propensity'], bins=30, alpha=0.6, label='处理组', color='coral')
    ax.hist(df[df['treatment'] == 0]['propensity'], bins=30, alpha=0.6, label='对照组', color='skyblue')
    ax.set_xlabel('倾向得分')
    ax.set_ylabel('频数')
    ax.set_title('匹配前倾向得分分布')
    ax.legend()

    # 2. 倾向得分分布（匹配后）
    ax = axes[0, 1]
    ax.hist(matched_df[matched_df['group'] == 'treated']['propensity'], bins=30, alpha=0.6, label='处理组', color='coral')
    ax.hist(matched_df[matched_df['group'] == 'control']['propensity'], bins=30, alpha=0.6, label='对照组', color='skyblue')
    ax.set_xlabel('倾向得分')
    ax.set_ylabel('频数')
    ax.set_title('匹配后倾向得分分布')
    ax.legend()

    # 3. SMD 对比
    ax = axes[1, 0]
    vars_list = pre_balance['变量'].tolist()
    x = np.arange(len(vars_list))
    width = 0.35
    ax.bar(x - width/2, pre_balance['SMD'].abs(), width, label='匹配前', color='coral')
    ax.bar(x + width/2, post_balance['SMD'].abs(), width, label='匹配后', color='skyblue')
    ax.axhline(0.1, color='red', linestyle='--', linewidth=1, label='SMD=0.1 阈值')
    ax.set_xticks(x)
    ax.set_xticklabels(vars_list)
    ax.set_ylabel('|SMD|')
    ax.set_title('匹配前后标准化均值差异对比')
    ax.legend()

    # 4. 共同支撑区域
    ax = axes[1, 1]
    treated_ps = df[df['treatment'] == 1]['propensity']
    control_ps = df[df['treatment'] == 0]['propensity']
    ax.scatter(treated_ps, np.random.normal(1, 0.02, len(treated_ps)), alpha=0.4, s=20, color='coral', label='处理组')
    ax.scatter(control_ps, np.random.normal(0, 0.02, len(control_ps)), alpha=0.4, s=20, color='skyblue', label='对照组')
    ax.set_xlabel('倾向得分')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['对照组', '处理组'])
    ax.set_title('共同支撑区域可视化')
    ax.legend()

    plt.tight_layout()
    plt.savefig('psm_simulation.png', dpi=150)
    print("\n[可视化已保存] psm_simulation.png")
    plt.close()


def summary():
    """总结说明。"""
    print("\n" + "=" * 60)
    print("【总结】")
    print("=" * 60)
    print("""
本脚本演示了 PSM 的核心流程：
1. 使用 Logistic 回归估计倾向得分
2. 通过 1:1 最近邻匹配构建可比样本
3. 利用 SMD 评估匹配前后的协变量平衡性
4. 估计 ATT 并对比匹配前后的偏差
5. 可视化倾向得分分布与共同支撑区域

关键要点：
- SMD < 0.1 通常认为协变量平衡良好
- Caliper 匹配可避免极差匹配
- 共同支撑区域不足时，需考虑截断或换方法
""")


if __name__ == "__main__":
    df, matched_df, pre_balance, post_balance = scenario_psm()
    visualize_results(df, matched_df, pre_balance, post_balance)
    summary()
