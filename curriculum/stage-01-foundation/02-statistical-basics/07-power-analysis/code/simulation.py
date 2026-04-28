"""
检验力分析与样本量计算 (Power Analysis) 模拟演示

本脚本演示：
1. 统计检验力 (Power) 的概念与计算
2. 样本量确定：在给定效应大小、显著性水平下达到目标检验力所需样本量
3. 第一类错误 (Type I error) 与第二类错误 (Type II error) 的直观理解
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def simulate_power(n_per_group, effect_size, alpha=0.05, n_simulations=2000):
    """
    通过模拟估计两独立样本 t 检验的检验力。

    Parameters
    ----------
    n_per_group : int
        每组样本量
    effect_size : float
        两组均值差异（以标准差为单位）
    alpha : float
        显著性水平
    n_simulations : int
        模拟次数

    Returns
    -------
    power : float
        拒绝原假设的比例
    """
    reject_count = 0
    for _ in range(n_simulations):
        group_a = np.random.normal(loc=0, scale=1, size=n_per_group)
        group_b = np.random.normal(loc=effect_size, scale=1, size=n_per_group)
        _, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)
        if p_value < alpha:
            reject_count += 1
    return reject_count / n_simulations


def demo_power_curve():
    """绘制不同样本量与效应大小下的检验力曲线。"""
    sample_sizes = np.arange(10, 201, 10)
    effect_sizes = [0.2, 0.5, 0.8]  # 小、中、大效应
    alpha = 0.05

    print("=" * 50)
    print("【检验力模拟】")
    print("通过重复模拟两样本 t 检验，估计不同条件下的检验力。\n")

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['skyblue', 'coral', 'lightgreen']
    for es, color in zip(effect_sizes, colors):
        powers = [simulate_power(n, es, alpha=alpha, n_simulations=2000) for n in sample_sizes]
        ax.plot(sample_sizes, powers, color=color, linewidth=2, label=f'效应大小 d={es}')
        # 打印部分结果
        for n, pwr in zip(sample_sizes[::4], powers[::4]):
            print(f"效应大小 d={es}, n={n:>3}, 检验力 ≈ {pwr:.3f}")
        print()

    ax.axhline(0.8, color='red', linestyle='--', linewidth=1.5, label='目标检验力 0.8')
    ax.set_title('检验力曲线：样本量 vs 检验力')
    ax.set_xlabel('每组样本量 n')
    ax.set_ylabel('检验力 (Power)')
    ax.set_ylim(0, 1.05)
    ax.legend()
    plt.tight_layout()
    plt.savefig('power_analysis_simulation.png', dpi=150)
    plt.close()
    print("可视化已保存为 power_analysis_simulation.png")


def demo_type_i_type_ii():
    """直观展示第一类与第二类错误。"""
    n = 50
    mu0 = 0
    mu1 = 0.5  # 真实效应

    # 在原假设下抽样
    type_i_errors = 0
    for _ in range(2000):
        sample = np.random.normal(mu0, 1, size=n)
        _, p = stats.ttest_1samp(sample, popmean=mu0)
        if p < 0.05:
            type_i_errors += 1

    # 在备择假设下抽样
    type_ii_errors = 0
    for _ in range(2000):
        sample = np.random.normal(mu1, 1, size=n)
        _, p = stats.ttest_1samp(sample, popmean=mu0)
        if p >= 0.05:
            type_ii_errors += 1

    print("=" * 50)
    print("【第一类错误与第二类错误】")
    print(f"模拟条件：n={n}, α=0.05, 真实效应 μ={mu1}")
    print(f"第一类错误率 (Type I error) ≈ {type_i_errors / 2000:.3f}  （应接近 α=0.05）")
    print(f"第二类错误率 (Type II error) ≈ {type_ii_errors / 2000:.3f}  （1 - Power）")
    print()


def demo_sample_size_determination():
    """演示如何确定达到目标检验力所需的样本量。"""
    target_power = 0.8
    effect_size = 0.5
    alpha = 0.05

    print("=" * 50)
    print("【样本量确定】")
    print(f"目标：效应大小 d={effect_size}, α={alpha}, 检验力 ≥ {target_power}")

    for n in range(10, 201, 5):
        pwr = simulate_power(n, effect_size, alpha=alpha, n_simulations=2000)
        if pwr >= target_power:
            print(f"所需每组样本量 n ≈ {n} 时，检验力达到 {pwr:.3f}")
            break
    else:
        print("在测试范围内未找到满足条件的样本量。")
    print()


if __name__ == "__main__":
    demo_power_curve()
    demo_type_i_type_ii()
    demo_sample_size_determination()
