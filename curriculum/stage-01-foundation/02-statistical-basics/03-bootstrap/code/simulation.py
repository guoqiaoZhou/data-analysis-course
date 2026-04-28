"""
Bootstrap 重抽样方法模拟演示

本脚本演示：
1. Bootstrap 置信区间（percentile 方法）
2. Bootstrap 标准误估计
3. 通过重抽样理解统计量的抽样分布
"""

import numpy as np
import matplotlib.pyplot as plt

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def bootstrap_statistics(data, n_bootstrap=5000, statistic_func=np.mean):
    """
    对给定数据进行 Bootstrap 重抽样，计算统计量的分布。

    Parameters
    ----------
    data : array-like
        原始样本数据
    n_bootstrap : int
        Bootstrap 重抽样次数
    statistic_func : callable
        要计算的统计量函数，如 np.mean, np.median

    Returns
    -------
    boot_stats : ndarray
        每次重抽样得到的统计量
    """
    n = len(data)
    boot_stats = np.empty(n_bootstrap)
    for i in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        boot_stats[i] = statistic_func(sample)
    return boot_stats


def demo_bootstrap_ci():
    """演示 Bootstrap 置信区间。"""
    # 生成一个右偏的样本
    data = np.random.exponential(scale=2, size=100) + 5

    boot_means = bootstrap_statistics(data, n_bootstrap=5000, statistic_func=np.mean)
    ci_lower = np.percentile(boot_means, 2.5)
    ci_upper = np.percentile(boot_means, 97.5)
    boot_se = boot_means.std(ddof=1)

    print("=" * 50)
    print("【Bootstrap 置信区间与标准误】")
    print(f"原始样本量 n = {len(data)}")
    print(f"样本均值 = {data.mean():.3f}")
    print(f"Bootstrap 均值的标准误 = {boot_se:.3f}")
    print(f"Bootstrap 95% 置信区间 (percentile) = [{ci_lower:.3f}, {ci_upper:.3f}]")
    print()
    return data, boot_means, ci_lower, ci_upper, boot_se


def demo_bootstrap_median():
    """演示 Bootstrap 估计中位数的标准误。"""
    data = np.random.normal(loc=50, scale=10, size=80)
    boot_medians = bootstrap_statistics(data, n_bootstrap=5000, statistic_func=np.median)
    ci_lower = np.percentile(boot_medians, 2.5)
    ci_upper = np.percentile(boot_medians, 97.5)
    boot_se = boot_medians.std(ddof=1)

    print("=" * 50)
    print("【Bootstrap 估计中位数】")
    print(f"样本中位数 = {np.median(data):.3f}")
    print(f"Bootstrap 中位数的标准误 = {boot_se:.3f}")
    print(f"Bootstrap 95% 置信区间 = [{ci_lower:.3f}, {ci_upper:.3f}]")
    print()
    return data, boot_medians, ci_lower, ci_upper, boot_se


def visualize_bootstrap(data, boot_means, ci_lower, ci_upper, boot_medians, ci_lower_med, ci_upper_med):
    """绘制 Bootstrap 抽样分布与置信区间。"""
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

    # 均值
    ax = axes[0]
    ax.hist(boot_means, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    ax.axvline(data.mean(), color='green', linestyle='-', linewidth=2, label=f'样本均值={data.mean():.2f}')
    ax.axvline(ci_lower, color='red', linestyle='--', linewidth=2, label=f'95% CI')
    ax.axvline(ci_upper, color='red', linestyle='--', linewidth=2)
    ax.set_title('Bootstrap 均值的抽样分布')
    ax.set_xlabel('均值')
    ax.set_ylabel('频数')
    ax.legend()

    # 中位数
    ax = axes[1]
    ax.hist(boot_medians, bins=50, color='plum', edgecolor='black', alpha=0.7)
    ax.axvline(np.median(data), color='green', linestyle='-', linewidth=2, label=f'样本中位数={np.median(data):.2f}')
    ax.axvline(ci_lower_med, color='red', linestyle='--', linewidth=2, label=f'95% CI')
    ax.axvline(ci_upper_med, color='red', linestyle='--', linewidth=2)
    ax.set_title('Bootstrap 中位数的抽样分布')
    ax.set_xlabel('中位数')
    ax.set_ylabel('频数')
    ax.legend()

    plt.tight_layout()
    plt.savefig('bootstrap_simulation.png', dpi=150)
    plt.close()
    print("可视化已保存为 bootstrap_simulation.png")


if __name__ == "__main__":
    data, boot_means, ci_lower, ci_upper, boot_se = demo_bootstrap_ci()
    data2, boot_medians, ci_lower_med, ci_upper_med, boot_se_med = demo_bootstrap_median()
    visualize_bootstrap(data, boot_means, ci_lower, ci_upper, boot_medians, ci_lower_med, ci_upper_med)
