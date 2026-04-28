"""
AB实验设计要素 —— 模拟演示
================================
本脚本演示以下内容：
1. MDE（最小可检测效应）的计算逻辑
2. 样本量规划（基于 power analysis）
3. 指标选择：Primary Metric vs Guardrail Metric
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 设置随机种子与中文字体
np.random.seed(42)
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def calculate_sample_size_per_group(
    baseline_mean: float,
    mde: float,
    std: float,
    alpha: float = 0.05,
    power: float = 0.8,
) -> int:
    """
    基于两独立样本 t 检验，计算每组所需样本量。
    公式来源：n = 2 * (Z_{1-alpha/2} + Z_{power})^2 * sigma^2 / delta^2
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    n = 2 * (z_alpha + z_beta) ** 2 * (std ** 2) / (mde ** 2)
    return int(np.ceil(n))


def simulate_mde_sweep(
    baseline_mean: float = 100.0,
    std: float = 20.0,
    alpha: float = 0.05,
    power: float = 0.8,
    mde_list: np.ndarray = None,
):
    """扫描不同 MDE，展示所需样本量。"""
    if mde_list is None:
        mde_list = np.arange(1, 11, 1)  # MDE 从 1% 到 10%（绝对值）
    sample_sizes = [
        calculate_sample_size_per_group(baseline_mean, mde, std, alpha, power)
        for mde in mde_list
    ]

    plt.figure(figsize=(8, 5))
    plt.plot(mde_list, sample_sizes, marker='o')
    plt.title("MDE 与每组所需样本量关系")
    plt.xlabel("MDE (绝对值)")
    plt.ylabel("每组样本量 n")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("mde_sample_size.png", dpi=150)
    plt.close()
    print("[MDE 扫描] 图像已保存: mde_sample_size.png")
    for mde, n in zip(mde_list, sample_sizes):
        print(f"  MDE={mde:.1f} → 每组 n={n}")
    return mde_list, sample_sizes


def simulate_power_curve(
    n_per_group: int = 500,
    baseline_mean: float = 100.0,
    std: float = 20.0,
    alpha: float = 0.05,
    effect_list: np.ndarray = None,
    n_simulations: int = 2000,
):
    """
    固定样本量，模拟不同真实效应下的检验功效（power）。
    """
    if effect_list is None:
        effect_list = np.linspace(0, 10, 21)

    powers = []
    for effect in effect_list:
        reject_count = 0
        for _ in range(n_simulations):
            ctrl = np.random.normal(baseline_mean, std, n_per_group)
            treat = np.random.normal(baseline_mean + effect, std, n_per_group)
            _, pvalue = stats.ttest_ind(ctrl, treat)
            if pvalue < alpha:
                reject_count += 1
        powers.append(reject_count / n_simulations)

    plt.figure(figsize=(8, 5))
    plt.plot(effect_list, powers, marker='o')
    plt.axhline(0.8, color='r', linestyle='--', label="目标 Power = 0.8")
    plt.title(f"固定样本量 n={n_per_group} 下的 Power 曲线")
    plt.xlabel("真实效应大小")
    plt.ylabel("检验功效 (Power)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("power_curve.png", dpi=150)
    plt.close()
    print("\n[Power 曲线] 图像已保存: power_curve.png")
    for eff, pw in zip(effect_list, powers):
        print(f"  真实效应={eff:.2f} → Power={pw:.3f}")
    return effect_list, powers


def simulate_guardrail_vs_primary(
    n_per_group: int = 1000,
    n_simulations: int = 2000,
    alpha: float = 0.05,
):
    """
    模拟 Primary Metric（核心指标）与 Guardrail Metric（护栏指标）的检测表现。
    场景：
    - Primary Metric 有正向提升（+2）
    - Guardrail Metric（如页面加载时间）有劣化（+0.5）
    """
    primary_baseline, primary_std = 100.0, 20.0
    guard_baseline, guard_std = 2.0, 0.5

    primary_effect = 2.0
    guard_effect = 0.5  # 劣化

    primary_detected = 0
    guard_detected = 0

    for _ in range(n_simulations):
        ctrl_primary = np.random.normal(primary_baseline, primary_std, n_per_group)
        treat_primary = np.random.normal(primary_baseline + primary_effect, primary_std, n_per_group)
        _, p_primary = stats.ttest_ind(ctrl_primary, treat_primary)
        if p_primary < alpha:
            primary_detected += 1

        ctrl_guard = np.random.normal(guard_baseline, guard_std, n_per_group)
        treat_guard = np.random.normal(guard_baseline + guard_effect, guard_std, n_per_group)
        _, p_guard = stats.ttest_ind(ctrl_guard, treat_guard)
        if p_guard < alpha:
            guard_detected += 1

    primary_power = primary_detected / n_simulations
    guard_power = guard_detected / n_simulations

    print("\n[Primary vs Guardrail 模拟]")
    print(f"  每组样本量: {n_per_group}")
    print(f"  Primary Metric (均值={primary_baseline}, std={primary_std}, 效应={primary_effect})")
    print(f"    → 检测率 (Power) = {primary_power:.3f}")
    print(f"  Guardrail Metric (均值={guard_baseline}, std={guard_std}, 劣化={guard_effect})")
    print(f"    → 检测率 (Power) = {guard_power:.3f}")

    # 可视化一次典型样本
    ctrl_primary = np.random.normal(primary_baseline, primary_std, n_per_group)
    treat_primary = np.random.normal(primary_baseline + primary_effect, primary_std, n_per_group)
    ctrl_guard = np.random.normal(guard_baseline, guard_std, n_per_group)
    treat_guard = np.random.normal(guard_baseline + guard_effect, guard_std, n_per_group)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].hist(ctrl_primary, bins=40, alpha=0.6, label="对照组")
    axes[0].hist(treat_primary, bins=40, alpha=0.6, label="实验组")
    axes[0].set_title("Primary Metric 分布")
    axes[0].legend()

    axes[1].hist(ctrl_guard, bins=40, alpha=0.6, label="对照组")
    axes[1].hist(treat_guard, bins=40, alpha=0.6, label="实验组")
    axes[1].set_title("Guardrail Metric 分布")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig("guardrail_primary.png", dpi=150)
    plt.close()
    print("  图像已保存: guardrail_primary.png")


def main():
    print("=" * 50)
    print("AB实验设计要素 —— 模拟演示")
    print("=" * 50)

    # 1. MDE 与样本量
    simulate_mde_sweep(baseline_mean=100.0, std=20.0)

    # 2. Power 曲线
    simulate_power_curve(n_per_group=500, baseline_mean=100.0, std=20.0)

    # 3. Primary vs Guardrail
    simulate_guardrail_vs_primary(n_per_group=1000)

    print("\n" + "=" * 50)
    print("全部模拟完成。")
    print("=" * 50)


if __name__ == "__main__":
    main()
