"""
Pre-AA检验 —— 模拟演示
======================
本脚本演示以下内容：
1. AA 测试模拟（两组均不接受处理）
2. 平衡性检验（balance checks）：均值、方差、分布
3. 前置趋势对比（pre-trend comparison）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def simulate_aa_test(n_per_group=5000, n_simulations=1000, alpha=0.05):
    """
    模拟 AA 测试：两组均来自同一分布，统计显著比例应接近 alpha。
    """
    false_positive_rate = 0
    pvalues = []

    for _ in range(n_simulations):
        group_a = np.random.normal(100, 20, n_per_group)
        group_b = np.random.normal(100, 20, n_per_group)
        _, pvalue = stats.ttest_ind(group_a, group_b)
        pvalues.append(pvalue)
        if pvalue < alpha:
            false_positive_rate += 1

    fpr = false_positive_rate / n_simulations

    print("[AA 测试模拟]")
    print(f"  每组样本量: {n_per_group}")
    print(f"  模拟次数: {n_simulations}")
    print(f"  名义显著性水平 alpha: {alpha}")
    print(f"  实际假阳性率 (Type I Error): {fpr:.4f}")

    # p 值分布应接近 Uniform(0,1)
    plt.figure(figsize=(8, 5))
    plt.hist(pvalues, bins=30, edgecolor='k', alpha=0.7)
    plt.axhline(n_simulations / 30, color='r', linestyle='--', label="均匀分布期望")
    plt.title("AA 测试中 p 值的分布")
    plt.xlabel("p 值")
    plt.ylabel("频数")
    plt.legend()
    plt.tight_layout()
    plt.savefig("aa_test_pvalues.png", dpi=150)
    plt.close()
    print("  图像已保存: aa_test_pvalues.png")
    return fpr, pvalues


def simulate_balance_check(n_per_group=5000):
    """
    模拟多维协变量平衡性检验。
    检验两组在年龄、收入、活跃度上的均值差异。
    """
    # 构造协变量
    age = np.random.normal(35, 10, n_per_group * 2)
    income = np.random.lognormal(10, 0.5, n_per_group * 2)
    activity = np.random.poisson(5, n_per_group * 2)

    # 随机分组
    idx = np.random.permutation(n_per_group * 2)
    group_a_idx = idx[:n_per_group]
    group_b_idx = idx[n_per_group:]

    covariates = {
        "年龄": age,
        "收入": income,
        "活跃度": activity,
    }

    print("\n[平衡性检验]")
    print(f"  每组样本量: {n_per_group}")
    results = []
    for name, vec in covariates.items():
        a = vec[group_a_idx]
        b = vec[group_b_idx]
        tstat, pvalue = stats.ttest_ind(a, b)
        std_diff = (b.mean() - a.mean()) / np.sqrt((a.var() + b.var()) / 2)
        results.append((name, a.mean(), b.mean(), std_diff, pvalue))
        print(f"  {name}: A组均值={a.mean():.2f}, B组均值={b.mean():.2f}, 标准化差异={std_diff:.4f}, p={pvalue:.4f}")

    # 可视化标准化差异
    names = [r[0] for r in results]
    std_diffs = [r[3] for r in results]

    plt.figure(figsize=(8, 5))
    plt.barh(names, std_diffs, color='steelblue')
    plt.axvline(0, color='k')
    plt.axvline(0.1, color='r', linestyle='--', label="|标准化差异| = 0.1 阈值")
    plt.axvline(-0.1, color='r', linestyle='--')
    plt.title("协变量标准化差异 (Standardized Difference)")
    plt.xlabel("标准化差异")
    plt.legend()
    plt.tight_layout()
    plt.savefig("balance_check.png", dpi=150)
    plt.close()
    print("  图像已保存: balance_check.png")


def simulate_pre_trend_comparison(n_days=30, n_users_per_day=200):
    """
    模拟实验前趋势对比：两组在实验前 30 天的日均指标应平行。
    """
    days = np.arange(n_days)
    # 共同趋势 + 随机噪声
    base_trend = 100 + 0.5 * days
    noise_a = np.random.normal(0, 5, n_days)
    noise_b = np.random.normal(0, 5, n_days)

    metric_a = base_trend + noise_a
    metric_b = base_trend + noise_b

    # 每天做 t 检验
    pvalues = []
    for d in range(n_days):
        a_daily = np.random.normal(metric_a[d], 10, n_users_per_day)
        b_daily = np.random.normal(metric_b[d], 10, n_users_per_day)
        _, p = stats.ttest_ind(a_daily, b_daily)
        pvalues.append(p)

    print("\n[前置趋势对比]")
    print(f"  实验前天数: {n_days}")
    print(f"  每天显著 (p<0.05) 的天数: {sum(np.array(pvalues) < 0.05)} / {n_days}")

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(days, metric_a, marker='o', label="A组趋势")
    axes[0].plot(days, metric_b, marker='s', label="B组趋势")
    axes[0].set_title("实验前两组指标趋势")
    axes[0].set_ylabel("指标均值")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].scatter(days, pvalues, color='gray')
    axes[1].axhline(0.05, color='r', linestyle='--', label="p = 0.05")
    axes[1].set_title("每日两组差异的 p 值")
    axes[1].set_xlabel("实验前天数")
    axes[1].set_ylabel("p 值")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig("pre_trend_comparison.png", dpi=150)
    plt.close()
    print("  图像已保存: pre_trend_comparison.png")


def main():
    print("=" * 50)
    print("Pre-AA检验 —— 模拟演示")
    print("=" * 50)

    simulate_aa_test(n_per_group=5000, n_simulations=1000)
    simulate_balance_check(n_per_group=5000)
    simulate_pre_trend_comparison(n_days=30, n_users_per_day=200)

    print("\n" + "=" * 50)
    print("全部模拟完成。")
    print("=" * 50)


if __name__ == "__main__":
    main()
