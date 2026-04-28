# Python 代码示例：随机化实验模拟

"""
本代码演示随机化实验的核心概念：
1. 完全随机化 vs 分层随机化
2. 协变量平衡检验（SMD）
3. 样本量与检验力的关系
4. 实验设计检查清单
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 设置中文字体（macOS 系统字体）
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 设置随机种子保证可复现
np.random.seed(42)


def generate_data(n=1000):
    """生成模拟数据：包含协变量和潜在结果"""
    age = np.random.normal(35, 10, n)          # 年龄
    income = np.random.normal(5000, 1500, n)   # 收入
    activity = np.random.choice(['high', 'medium', 'low'], n, p=[0.3, 0.5, 0.2])

    # 潜在结果（依赖于协变量）
    Y0 = 100 + 0.5 * age + 0.01 * income + np.random.normal(0, 10, n)
    ATE = 5  # 真实处理效应
    Y1 = Y0 + ATE

    return age, income, activity, Y0, Y1, ATE


def calc_smd(var, treatment_indicator):
    """计算标准化均值差异（Standardized Mean Difference）"""
    mean_treat = np.mean(var[treatment_indicator == 1])
    mean_control = np.mean(var[treatment_indicator == 0])
    pooled_std = np.sqrt((np.var(var[treatment_indicator == 1]) +
                          np.var(var[treatment_indicator == 0])) / 2)
    return (mean_treat - mean_control) / pooled_std


def scenario_complete_randomization(age, income, Y0, Y1, ATE, n=1000):
    """场景1：完全随机化"""
    print("=" * 50)
    print("完全随机化")
    print("=" * 50)

    D_complete = np.random.binomial(1, 0.5, n)
    Y_complete = D_complete * Y1 + (1 - D_complete) * Y0

    # 协变量平衡检验
    print("\n协变量平衡（标准化均值差异 SMD）：")
    for var, name in [(age, '年龄'), (income, '收入')]:
        smd = calc_smd(var, D_complete)
        print(f"  {name}: SMD = {smd:.4f} (< 0.1 为平衡)")

    # ATE 估计
    ate_complete = np.mean(Y_complete[D_complete == 1]) - np.mean(Y_complete[D_complete == 0])
    print(f"\nATE 估计: {ate_complete:.3f} (真实值: {ATE})")

    return D_complete, Y_complete, ate_complete


def scenario_stratified_randomization(age, activity, Y0, Y1, ATE, n=1000):
    """场景2：分层随机化（按活跃度分层）"""
    print("\n" + "=" * 50)
    print("分层随机化（按活跃度分层）")
    print("=" * 50)

    # 将活跃度转换为数值
    activity_map = {'high': 2, 'medium': 1, 'low': 0}
    activity_num = np.array([activity_map[a] for a in activity])

    D_stratified = np.zeros(n, dtype=int)
    for level in [2, 1, 0]:
        mask = activity_num == level
        n_level = np.sum(mask)
        D_stratified[mask] = np.random.binomial(1, 0.5, n_level)

    Y_stratified = D_stratified * Y1 + (1 - D_stratified) * Y0

    # 分层内平衡检验
    print("\n分层内协变量平衡：")
    for level_name, level in [('high', 2), ('medium', 1), ('low', 0)]:
        mask = activity_num == level
        if np.sum(D_stratified[mask] == 1) > 0 and np.sum(D_stratified[mask] == 0) > 0:
            mean_treat = np.mean(age[mask & (D_stratified == 1)])
            mean_control = np.mean(age[mask & (D_stratified == 0)])
            print(f"  {level_name}: 处理组年龄={mean_treat:.1f}, 对照组年龄={mean_control:.1f}")

    ate_stratified = np.mean(Y_stratified[D_stratified == 1]) - np.mean(Y_stratified[D_stratified == 0])
    print(f"\nATE 估计: {ate_stratified:.3f} (真实值: {ATE})")

    return D_stratified, Y_stratified, ate_stratified


def simulate_experiment(n, ate, sigma, n_sim=1000):
    """模拟多次实验，计算检出率（检验力）"""
    detected = 0
    for _ in range(n_sim):
        Y0 = np.random.normal(100, sigma, n)
        Y1 = Y0 + ate
        D = np.random.binomial(1, 0.5, n)
        Y = D * Y1 + (1 - D) * Y0

        treat = Y[D == 1]
        control = Y[D == 0]

        t_stat, p_value = stats.ttest_ind(treat, control)
        if p_value < 0.05:
            detected += 1

    return detected / n_sim


def power_analysis(ATE):
    """样本量与检验力分析"""
    print("\n" + "=" * 50)
    print("样本量与检验力分析")
    print("=" * 50)

    sample_sizes = [100, 200, 500, 1000, 2000, 5000]
    powers = []

    print(f"\n真实效应 = {ATE}, 标准差 = 10")
    print("样本量 -> 检验力（模拟）")
    for n_test in sample_sizes:
        power = simulate_experiment(n_test, ATE, 10, n_sim=500)
        powers.append(power)
        print(f"  {n_test:5d} -> {power:.3f}")

    # 理论检验力（使用 statsmodels）
    try:
        from statsmodels.stats.power import TTestIndPower
        power_analysis = TTestIndPower()

        print("\n理论检验力（statsmodels）：")
        for n_test in sample_sizes:
            theoretical_power = power_analysis.power(
                effect_size=ATE / 10,  # Cohen's d
                nobs1=n_test,
                alpha=0.05,
                ratio=1.0
            )
            print(f"  {n_test:5d} -> {theoretical_power:.3f}")
    except ImportError:
        print("\n（安装 statsmodels 可查看理论检验力）")

    return sample_sizes, powers


def visualize(age, D_complete, D_stratified, sample_sizes, powers, Y0, Y1, ATE):
    """可视化：协变量分布、样本量-检验力曲线、ATE估计分布"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 图1：完全随机化的协变量分布
    ax = axes[0, 0]
    ax.hist(age[D_complete == 0], bins=30, alpha=0.5, label='对照组')
    ax.hist(age[D_complete == 1], bins=30, alpha=0.5, label='处理组')
    ax.set_title('完全随机化：年龄分布')
    ax.legend()

    # 图2：分层随机化的协变量分布
    ax = axes[0, 1]
    for d, label in [(0, '对照组'), (1, '处理组')]:
        mask = D_stratified == d
        ax.hist(age[mask], bins=30, alpha=0.5, label=label)
    ax.set_title('分层随机化：年龄分布')
    ax.legend()

    # 图3：样本量 vs 检验力
    ax = axes[1, 0]
    ax.plot(sample_sizes, powers, 'o-', label='模拟检验力')
    ax.axhline(0.8, color='red', linestyle='--', label='目标检验力 80%')
    ax.set_xlabel('样本量（每组）')
    ax.set_ylabel('检验力')
    ax.set_title('样本量与检验力')
    ax.legend()
    ax.grid(True)

    # 图4：效应估计的分布（多次模拟）
    ax = axes[1, 1]
    ate_estimates = []
    for _ in range(1000):
        D = np.random.binomial(1, 0.5, 500)
        Y = D * Y1[:500] + (1 - D) * Y0[:500]
        ate_est = np.mean(Y[D == 1]) - np.mean(Y[D == 0])
        ate_estimates.append(ate_est)

    ax.hist(ate_estimates, bins=50, alpha=0.7)
    ax.axvline(ATE, color='red', linestyle='--', linewidth=2, label=f'真实 ATE={ATE}')
    ax.axvline(np.mean(ate_estimates), color='blue', linestyle='--',
               label=f'估计均值={np.mean(ate_estimates):.2f}')
    ax.set_title('ATE 估计的抽样分布（n=500）')
    ax.legend()

    plt.tight_layout()
    plt.savefig('randomized_experiments.png', dpi=150)
    print("\n可视化已保存至 randomized_experiments.png")


def print_checklist(n):
    """打印实验设计检查清单"""
    print("\n" + "=" * 50)
    print("实验设计检查清单")
    print("=" * 50)

    checklist = [
        ("随机化单元", "用户级/会话级/页面级？"),
        ("处理定义", "实验组和对照组的体验差异是否清晰？"),
        ("样本量", f"是否足够检测 MDE？（当前设计 n={n}）"),
        ("实验周期", "是否覆盖完整用户行为周期？"),
        ("核心指标", "1-2个，业务最关注的指标"),
        ("护栏指标", "确保不伤害用户体验/系统稳定性"),
        ("分流比例", "通常为 50/50，或根据风险调整"),
        ("Pre-AA检验", "实验前处理组和对照组是否平衡？"),
    ]

    for item, question in checklist:
        print(f"  [ ] {item}: {question}")

    print("\n提示：使用此清单在实验启动前逐项检查。")


if __name__ == "__main__":
    n = 1000
    age, income, activity, Y0, Y1, ATE = generate_data(n)

    D_complete, Y_complete, ate_complete = scenario_complete_randomization(
        age, income, Y0, Y1, ATE, n)
    D_stratified, Y_stratified, ate_stratified = scenario_stratified_randomization(
        age, activity, Y0, Y1, ATE, n)
    sample_sizes, powers = power_analysis(ATE)
    visualize(age, D_complete, D_stratified, sample_sizes, powers, Y0, Y1, ATE)
    print_checklist(n)
