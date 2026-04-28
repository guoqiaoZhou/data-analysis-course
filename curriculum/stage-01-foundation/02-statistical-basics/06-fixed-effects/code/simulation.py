"""
固定效应模型 (Fixed Effects Model) 模拟演示

本脚本演示：
1. 面板数据 (Panel Data) 的生成
2. Within-estimator（组内估计量）：去除个体不随时间变化的异质性
3. Between variation vs Within variation 的区分
"""

import numpy as np
import matplotlib.pyplot as plt

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_panel_data(n_individuals=50, n_periods=5, beta=2.0):
    """
    生成面板数据，包含：
    - alpha_i：个体固定效应（不随时间变化）
    - x_it：随时间变化的解释变量
    - epsilon_it：随机误差
    """
    alpha = np.random.normal(0, 3, size=n_individuals)  # 个体效应
    data = []
    for i in range(n_individuals):
        for t in range(n_periods):
            x_it = np.random.normal(5, 2) + 0.3 * t  # x 有轻微时间趋势
            epsilon = np.random.normal(0, 1)
            y_it = alpha[i] + beta * x_it + epsilon
            data.append({
                'individual': i,
                'period': t,
                'x': x_it,
                'y': y_it,
                'alpha': alpha[i]
            })
    return data, beta


def _groupby_mean(arr, keys):
    """手动按 keys 分组求均值，返回唯一键和均值数组。"""
    unique_keys = np.unique(keys)
    means = {}
    for k in unique_keys:
        means[k] = arr[keys == k].mean()
    return unique_keys, means


def within_estimator(data):
    """
    手动实现 Within-estimator：对每组去均值后做 OLS。
    """
    individuals = np.array([d['individual'] for d in data])
    x = np.array([d['x'] for d in data])
    y = np.array([d['y'] for d in data])

    _, x_means = _groupby_mean(x, individuals)
    _, y_means = _groupby_mean(y, individuals)

    x_demean = x - np.array([x_means[ind] for ind in individuals])
    y_demean = y - np.array([y_means[ind] for ind in individuals])

    beta_within = np.sum(x_demean * y_demean) / np.sum(x_demean ** 2)
    return beta_within, x_demean, y_demean, individuals, x, y


def between_estimator(data):
    """
    Between-estimator：使用个体均值进行回归。
    """
    individuals = np.array([d['individual'] for d in data])
    x = np.array([d['x'] for d in data])
    y = np.array([d['y'] for d in data])

    unique_ind, x_means = _groupby_mean(x, individuals)
    _, y_means = _groupby_mean(y, individuals)

    x_mean_arr = np.array([x_means[ind] for ind in unique_ind])
    y_mean_arr = np.array([y_means[ind] for ind in unique_ind])

    x_mean, y_mean = x_mean_arr.mean(), y_mean_arr.mean()
    beta_between = np.sum((x_mean_arr - x_mean) * (y_mean_arr - y_mean)) / np.sum((x_mean_arr - x_mean) ** 2)
    return beta_between, x_mean_arr, y_mean_arr


def demo_fixed_effects():
    """演示固定效应模型的估计。"""
    data, true_beta = generate_panel_data(n_individuals=50, n_periods=5, beta=2.0)

    beta_within, x_demean, y_demean, individuals, x_all, y_all = within_estimator(data)
    beta_between, x_mean_arr, y_mean_arr = between_estimator(data)

    # 混合 OLS（忽略个体效应）
    x_mean, y_mean = x_all.mean(), y_all.mean()
    beta_pooled = np.sum((x_all - x_mean) * (y_all - y_mean)) / np.sum((x_all - x_mean) ** 2)

    print("=" * 50)
    print("【固定效应模型估计结果】")
    print(f"真实斜率 β = {true_beta}")
    print(f"混合 OLS 估计 β = {beta_pooled:.3f}  （忽略个体效应，存在遗漏变量偏差）")
    print(f"Between 估计 β = {beta_between:.3f}  （使用个体间变异）")
    print(f"Within 估计 β = {beta_within:.3f}  （使用个体内变异，去除个体固定效应）")
    print()

    # 变异分解
    total_var_y = y_all.var()
    unique_ind = np.unique(individuals)
    within_vars = []
    for ind in unique_ind:
        mask = individuals == ind
        within_vars.append(y_all[mask].var(ddof=1))
    within_var_y = np.mean(within_vars)
    between_var_y = np.array([y_all[individuals == ind].mean() for ind in unique_ind]).var()

    print("【变异分解 (y 的总方差)】")
    print(f"总方差 = {total_var_y:.3f}")
    print(f"组内方差 (Within) = {within_var_y:.3f}")
    print(f"组间方差 (Between) = {between_var_y:.3f}")
    print()

    return data, x_mean_arr, y_mean_arr, beta_within, beta_between, beta_pooled


def visualize_fixed_effects(data, x_mean_arr, y_mean_arr):
    """绘制个体轨迹图与组间回归图。"""
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

    # 个体轨迹（Within variation）
    ax = axes[0]
    individuals = np.array([d['individual'] for d in data])
    x_all = np.array([d['x'] for d in data])
    y_all = np.array([d['y'] for d in data])
    for ind in np.unique(individuals):
        mask = individuals == ind
        ax.plot(x_all[mask], y_all[mask], color='gray', alpha=0.3, linewidth=0.8)
    ax.set_title('个体轨迹图（组内变异）')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # 个体均值（Between variation）
    ax = axes[1]
    ax.scatter(x_mean_arr, y_mean_arr, color='coral', edgecolors='black', alpha=0.7)
    ax.set_title('个体均值散点图（组间变异）')
    ax.set_xlabel('个体平均 x')
    ax.set_ylabel('个体平均 y')

    plt.tight_layout()
    plt.savefig('fixed_effects_simulation.png', dpi=150)
    plt.close()
    print("可视化已保存为 fixed_effects_simulation.png")


if __name__ == "__main__":
    data, x_mean_arr, y_mean_arr, beta_within, beta_between, beta_pooled = demo_fixed_effects()
    visualize_fixed_effects(data, x_mean_arr, y_mean_arr)
