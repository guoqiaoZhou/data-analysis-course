"""
WOE / IV (Weight of Evidence / Information Value) 模拟

演示内容：
- 等频分箱与决策树分箱
- WOE 计算
- IV 计算与特征筛选
- 单调性约束展示
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_credit_data(n_samples=5000):
    """
    生成模拟信贷数据：
    - age: 年龄，与违约概率负相关
    - income: 收入，与违约概率负相关
    - debt_ratio: 负债率，与违约概率正相关
    - random_noise: 纯噪声特征
    """
    age = np.random.randint(18, 70, size=n_samples)
    income = np.random.lognormal(10, 0.5, size=n_samples)
    debt_ratio = np.random.beta(2, 5, size=n_samples)
    random_noise = np.random.randn(n_samples)

    # 违约概率逻辑
    logit = (
        -0.08 * (age - 40)
        - 0.0003 * income
        + 5 * debt_ratio
        + 0.0 * random_noise
    )
    prob = 1 / (1 + np.exp(-logit))
    default = (np.random.rand(n_samples) < prob).astype(int)

    df = pd.DataFrame({
        'age': age,
        'income': income,
        'debt_ratio': debt_ratio,
        'random_noise': random_noise,
        'default': default,
    })
    return df


def equal_frequency_bins(x, n_bins=10):
    """等频分箱，返回分箱边界。"""
    # 使用 pandas qcut 获取边界
    _, bins = pd.qcut(x, q=n_bins, retbins=True, duplicates='drop')
    # 确保包含最小最大值
    bins[0] = x.min() - 1e-9
    bins[-1] = x.max() + 1e-9
    return bins


def tree_based_bins(x, y, n_bins=10):
    """决策树分箱：用决策树学习最优切分点。"""
    x = x.reshape(-1, 1)
    tree = DecisionTreeClassifier(max_leaf_nodes=n_bins, random_state=42)
    tree.fit(x, y)
    thresholds = tree.tree_.threshold[tree.tree_.threshold != -2]
    thresholds = np.sort(thresholds)
    # 构建完整边界
    bins = [x.min() - 1e-9]
    bins.extend(thresholds)
    bins.append(x.max() + 1e-9)
    bins = np.array(bins)
    return bins


def calculate_woe_iv(df, feature, target, bins):
    """
    计算 WOE 和 IV。
    返回 DataFrame，包含每箱的统计信息。
    """
    df = df.copy()
    df['bin'] = pd.cut(df[feature], bins=bins, include_lowest=True)

    grouped = df.groupby('bin', observed=False)[target].agg(['count', 'sum'])
    grouped.columns = ['total', 'bad']
    grouped['good'] = grouped['total'] - grouped['bad']

    # 避免除零，加平滑
    grouped['bad_dist'] = (grouped['bad'] + 0.5) / (grouped['bad'].sum() + 0.5)
    grouped['good_dist'] = (grouped['good'] + 0.5) / (grouped['good'].sum() + 0.5)

    grouped['woe'] = np.log(grouped['good_dist'] / grouped['bad_dist'])
    grouped['iv'] = (grouped['good_dist'] - grouped['bad_dist']) * grouped['woe']

    return grouped


def demo_binning_methods(df, feature, target):
    """对比等频分箱与决策树分箱。"""
    x = df[feature].values
    y = df[target].values

    ef_bins = equal_frequency_bins(x, n_bins=10)
    tree_bins = tree_based_bins(x, y, n_bins=6)

    ef_result = calculate_woe_iv(df, feature, target, ef_bins)
    tree_result = calculate_woe_iv(df, feature, target, tree_bins)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 等频分箱 WOE
    ax = axes[0]
    centers = [interval.mid for interval in ef_result.index]
    ax.bar(range(len(centers)), ef_result['woe'], color='steelblue')
    ax.set_xticks(range(len(centers)))
    ax.set_xticklabels([f'{c:.1f}' for c in centers], rotation=45, ha='right')
    ax.set_xlabel('分箱中心值')
    ax.set_ylabel('WOE')
    ax.set_title(f'{feature}: 等频分箱 WOE')
    ax.axhline(y=0, color='red', linestyle='--', linewidth=0.8)
    ax.grid(True, linestyle='--', alpha=0.5, axis='y')

    # 决策树分箱 WOE
    ax = axes[1]
    centers = [interval.mid for interval in tree_result.index]
    ax.bar(range(len(centers)), tree_result['woe'], color='seagreen')
    ax.set_xticks(range(len(centers)))
    ax.set_xticklabels([f'{c:.1f}' for c in centers], rotation=45, ha='right')
    ax.set_xlabel('分箱中心值')
    ax.set_ylabel('WOE')
    ax.set_title(f'{feature}: 决策树分箱 WOE')
    ax.axhline(y=0, color='red', linestyle='--', linewidth=0.8)
    ax.grid(True, linestyle='--', alpha=0.5, axis='y')

    plt.tight_layout()
    plt.savefig('binning_comparison.png', dpi=150)
    plt.close()
    print(f"[分箱对比] 已保存 binning_comparison.png ({feature})")
    print(f"  等频分箱 IV: {ef_result['iv'].sum():.4f}")
    print(f"  决策树分箱 IV: {tree_result['iv'].sum():.4f}")


def demo_iv_feature_selection(df, target):
    """计算所有特征的 IV，并展示特征筛选。"""
    features = ['age', 'income', 'debt_ratio', 'random_noise']
    iv_results = []

    for feat in features:
        x = df[feat].values
        y = df[target].values
        bins = equal_frequency_bins(x, n_bins=10)
        result = calculate_woe_iv(df, feat, target, bins)
        iv_total = result['iv'].sum()
        iv_results.append((feat, iv_total))
        print(f"[IV 计算] {feat}: IV = {iv_total:.4f}")

    iv_df = pd.DataFrame(iv_results, columns=['feature', 'iv'])
    iv_df = iv_df.sort_values('iv', ascending=True)

    plt.figure(figsize=(8, 5))
    colors = ['green' if iv >= 0.1 else 'orange' if iv >= 0.02 else 'red'
              for iv in iv_df['iv']]
    bars = plt.barh(iv_df['feature'], iv_df['iv'], color=colors)
    plt.xlabel('Information Value (IV)')
    plt.title('特征 IV 值与筛选阈值')
    plt.axvline(x=0.02, color='gray', linestyle='--', linewidth=0.8, label='弱预测 (0.02)')
    plt.axvline(x=0.1, color='blue', linestyle='--', linewidth=0.8, label='中等预测 (0.1)')
    plt.axvline(x=0.3, color='purple', linestyle='--', linewidth=0.8, label='强预测 (0.3)')
    plt.legend()
    for bar, val in zip(bars, iv_df['iv']):
        plt.text(val + 0.005, bar.get_y() + bar.get_height() / 2,
                 f'{val:.3f}', va='center', fontsize=10)
    plt.tight_layout()
    plt.savefig('iv_feature_selection.png', dpi=150)
    plt.close()
    print("[IV 特征筛选] 已保存 iv_feature_selection.png")
    print("  IV 解释: <0.02 弱预测, 0.02-0.1 中等, 0.1-0.3 强, >0.3 极强（可能过拟合）")


def demo_monotonicity(df, target):
    """
    展示单调性约束：age 与违约概率应为单调递减关系。
    对比无约束 WOE 与单调调整后的 WOE。
    """
    feature = 'age'
    x = df[feature].values
    bins = equal_frequency_bins(x, n_bins=10)
    result = calculate_woe_iv(df, feature, target, bins)

    woe_raw = result['woe'].values.copy()
    # Pool Adjacent Violators Algorithm (PAVA) 简化版：强制单调递减
    woe_mono = woe_raw.copy()
    for _ in range(len(woe_mono)):
        changed = False
        for i in range(len(woe_mono) - 1):
            if woe_mono[i] < woe_mono[i + 1]:
                # 合并（取平均）
                avg = (woe_mono[i] + woe_mono[i + 1]) / 2
                woe_mono[i] = avg
                woe_mono[i + 1] = avg
                changed = True
        if not changed:
            break

    x_pos = range(len(woe_raw))
    plt.figure(figsize=(10, 5))
    plt.plot(x_pos, woe_raw, marker='o', label='原始 WOE', color='coral', linewidth=2)
    plt.plot(x_pos, woe_mono, marker='s', label='单调约束 WOE (递减)', color='steelblue', linewidth=2)
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    plt.xlabel('分箱序号')
    plt.ylabel('WOE')
    plt.title(f'{feature}: WOE 单调性约束示例')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('monotonicity_constraint.png', dpi=150)
    plt.close()
    print(f"[单调性约束] 已保存 monotonicity_constraint.png ({feature})")
    print("  业务解释：年龄越大，违约概率应越低，WOE 应单调递减。")


def main():
    print("=" * 60)
    print("WOE / IV 模拟")
    print("=" * 60)
    df = generate_credit_data(n_samples=5000)
    print(f"数据规模: {df.shape[0]} 行, {df.shape[1]} 列")
    print(f"违约率: {df['default'].mean():.2%}\n")

    demo_binning_methods(df, feature='age', target='default')
    print()
    demo_iv_feature_selection(df, target='default')
    print()
    demo_monotonicity(df, target='default')
    print()
    print("=" * 60)
    print("所有可视化已保存为 PNG 文件。")
    print("=" * 60)


if __name__ == "__main__":
    main()
