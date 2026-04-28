"""
t检验 (t-test) 模拟演示

本脚本演示三种常见的t检验方法：
1. 单样本t检验 (One-sample t-test)：检验样本均值是否等于某个已知值
2. 独立双样本t检验 (Two-sample t-test)：检验两组独立样本的均值是否相等
3. 配对t检验 (Paired t-test)：检验配对样本的差值均值是否为零

同时演示p值的含义与解释。
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 中文支持与样式设置
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def demo_one_sample_ttest():
    """单样本t检验：检验样本均值是否等于已知总体均值。"""
    mu_true = 100
    sample = np.random.normal(loc=102, scale=5, size=30)
    t_stat, p_value = stats.ttest_1samp(sample, popmean=mu_true)

    print("=" * 50)
    print("【1. 单样本 t 检验】")
    print(f"假设总体均值 μ = {mu_true}")
    print(f"样本量 n = {len(sample)}, 样本均值 = {sample.mean():.3f}, 样本标准差 = {sample.std(ddof=1):.3f}")
    print(f"t 统计量 = {t_stat:.3f}, p 值 = {p_value:.4f}")
    if p_value < 0.05:
        print("结论：在 α=0.05 水平下拒绝原假设，样本均值与总体均值存在显著差异。")
    else:
        print("结论：在 α=0.05 水平下不拒绝原假设，样本均值与总体均值无显著差异。")
    print()
    return sample, mu_true, t_stat, p_value


def demo_two_sample_ttest():
    """独立双样本t检验：检验两组独立样本均值是否相等。"""
    group_a = np.random.normal(loc=100, scale=8, size=40)
    group_b = np.random.normal(loc=105, scale=8, size=40)
    t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)

    print("=" * 50)
    print("【2. 独立双样本 t 检验】")
    print(f"A组均值 = {group_a.mean():.3f}, 标准差 = {group_a.std(ddof=1):.3f}")
    print(f"B组均值 = {group_b.mean():.3f}, 标准差 = {group_b.std(ddof=1):.3f}")
    print(f"t 统计量 = {t_stat:.3f}, p 值 = {p_value:.4f}")
    if p_value < 0.05:
        print("结论：两组均值存在显著差异 (p < 0.05)。")
    else:
        print("结论：两组均值无显著差异 (p >= 0.05)。")
    print()
    return group_a, group_b, t_stat, p_value


def demo_paired_ttest():
    """配对t检验：检验同一对象前后测差值的均值是否为零。"""
    before = np.random.normal(loc=100, scale=5, size=30)
    after = before + np.random.normal(loc=3, scale=2, size=30)  # 治疗后提升约3
    t_stat, p_value = stats.ttest_rel(before, after)

    print("=" * 50)
    print("【3. 配对 t 检验】")
    print(f"前测均值 = {before.mean():.3f}, 后测均值 = {after.mean():.3f}")
    print(f"平均差值 = {(after - before).mean():.3f}")
    print(f"t 统计量 = {t_stat:.3f}, p 值 = {p_value:.4f}")
    if p_value < 0.05:
        print("结论：前后测存在显著差异，干预可能有效。")
    else:
        print("结论：前后测无显著差异。")
    print()
    return before, after, t_stat, p_value


def visualize_results(sample, mu_true, group_a, group_b, before, after):
    """绘制三种t检验的可视化结果。"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    # 单样本
    ax = axes[0]
    ax.hist(sample, bins=12, color='skyblue', edgecolor='black', alpha=0.7)
    ax.axvline(mu_true, color='red', linestyle='--', linewidth=2, label=f'假设均值 μ={mu_true}')
    ax.axvline(sample.mean(), color='green', linestyle='-', linewidth=2, label=f'样本均值={sample.mean():.2f}')
    ax.set_title('单样本 t 检验')
    ax.set_xlabel('观测值')
    ax.set_ylabel('频数')
    ax.legend()

    # 双样本
    ax = axes[1]
    ax.hist(group_a, bins=12, color='coral', edgecolor='black', alpha=0.6, label='A组')
    ax.hist(group_b, bins=12, color='lightgreen', edgecolor='black', alpha=0.6, label='B组')
    ax.axvline(group_a.mean(), color='darkred', linestyle='-', linewidth=2)
    ax.axvline(group_b.mean(), color='darkgreen', linestyle='-', linewidth=2)
    ax.set_title('独立双样本 t 检验')
    ax.set_xlabel('观测值')
    ax.set_ylabel('频数')
    ax.legend()

    # 配对
    ax = axes[2]
    diff = after - before
    ax.hist(diff, bins=12, color='plum', edgecolor='black', alpha=0.7)
    ax.axvline(0, color='red', linestyle='--', linewidth=2, label='差值=0')
    ax.axvline(diff.mean(), color='green', linestyle='-', linewidth=2, label=f'平均差值={diff.mean():.2f}')
    ax.set_title('配对 t 检验（前后测差值）')
    ax.set_xlabel('差值 (后测 - 前测)')
    ax.set_ylabel('频数')
    ax.legend()

    plt.tight_layout()
    plt.savefig('t_test_simulation.png', dpi=150)
    plt.close()
    print("可视化已保存为 t_test_simulation.png")


def print_summary():
    """打印p值解释摘要。"""
    print("=" * 50)
    print("【p 值解释摘要】")
    print("p 值是在原假设为真的前提下，观察到当前或更极端结果的概率。")
    print("- p < 0.05：通常认为结果具有统计显著性，拒绝原假设。")
    print("- p >= 0.05：证据不足，不拒绝原假设。")
    print("注意：p 值不衡量原假设为真的概率，也不直接衡量效应大小。")
    print()


if __name__ == "__main__":
    sample, mu_true, _, _ = demo_one_sample_ttest()
    group_a, group_b, _, _ = demo_two_sample_ttest()
    before, after, _, _ = demo_paired_ttest()
    print_summary()
    visualize_results(sample, mu_true, group_a, group_b, before, after)
