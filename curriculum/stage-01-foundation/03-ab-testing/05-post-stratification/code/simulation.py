"""
后分层分析 —— 模拟演示
======================
本脚本演示以下内容：
1. 后分层加权（post-stratification weighting）
2. 分层带来的方差缩减
3. 对比简单均值差与后分层估计量
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def generate_stratified_data(n_total=10000, n_strata=4):
    """
    生成带有分层结构的数据。
    各层比例不同，层内效应也不同。
    """
    strata_props = np.array([0.1, 0.2, 0.3, 0.4])
    strata_sizes = (strata_props * n_total).astype(int)
    strata_sizes[-1] += n_total - strata_sizes.sum()

    baselines = np.array([50, 60, 70, 80])
    stds = np.array([20, 18, 15, 12])
    true_effects = np.array([1.0, 1.5, 2.0, 2.5])

    x_list, t_list, y_list, s_list = [], [], [], []
    for s, size in enumerate(strata_sizes):
        x = np.random.normal(baselines[s], stds[s], size)
        t = np.random.binomial(1, 0.5, size)
        y = true_effects[s] * t + x + np.random.normal(0, 3, size)
        x_list.append(x)
        t_list.append(t)
        y_list.append(y)
        s_list.append(np.full(size, s))

    return (
        np.concatenate(x_list),
        np.concatenate(t_list),
        np.concatenate(y_list),
        np.concatenate(s_list),
        strata_props,
        true_effects,
    )


def simple_difference(y, t):
    """简单均值差估计量。"""
    ctrl = y[t == 0]
    treat = y[t == 1]
    return treat.mean() - ctrl.mean(), stats.ttest_ind(ctrl, treat).pvalue


def post_stratification_estimate(y, t, s, strata_props):
    """
    后分层估计量：在各层内计算处理效应，再按总体比例加权平均。
    """
    n_strata = len(strata_props)
    effects = []
    variances = []
    for stratum in range(n_strata):
        mask = s == stratum
        y_s = y[mask]
        t_s = t[mask]
        ctrl = y_s[t_s == 0]
        treat = y_s[t_s == 1]
        if len(ctrl) == 0 or len(treat) == 0:
            effects.append(0)
            variances.append(1e6)
            continue
        eff = treat.mean() - ctrl.mean()
        var = treat.var(ddof=1) / len(treat) + ctrl.var(ddof=1) / len(ctrl)
        effects.append(eff)
        variances.append(var)

    # 加权平均
    weighted_effect = np.sum(strata_props * np.array(effects))
    # 方差近似
    weighted_var = np.sum((strata_props ** 2) * np.array(variances))
    return weighted_effect, np.sqrt(weighted_var), effects


def simulate_post_stratification(n_total=10000, n_simulations=500):
    """
    多次模拟，对比简单估计量与后分层估计量的 RMSE。
    """
    simple_effects = []
    post_effects = []

    for _ in range(n_simulations):
        x, t, y, s, props, true_effects = generate_stratified_data(n_total)
        simple_eff, _ = simple_difference(y, t)
        post_eff, _, _ = post_stratification_estimate(y, t, s, props)
        simple_effects.append(simple_eff)
        post_effects.append(post_eff)

    true_overall_effect = np.sum(props * true_effects)
    rmse_simple = np.sqrt(np.mean((np.array(simple_effects) - true_overall_effect) ** 2))
    rmse_post = np.sqrt(np.mean((np.array(post_effects) - true_overall_effect) ** 2))

    print("[后分层分析模拟]")
    print(f"  总样本量: {n_total}")
    print(f"  模拟次数: {n_simulations}")
    print(f"  真实总体效应: {true_overall_effect:.3f}")
    print(f"  简单估计量 RMSE: {rmse_simple:.4f}")
    print(f"  后分层估计量 RMSE: {rmse_post:.4f}")
    print(f"  RMSE 缩减: {(1 - rmse_post / rmse_simple) * 100:.2f}%")

    # 可视化估计量分布
    plt.figure(figsize=(8, 5))
    plt.hist(simple_effects, bins=30, alpha=0.6, label="简单估计量")
    plt.hist(post_effects, bins=30, alpha=0.6, label="后分层估计量")
    plt.axvline(true_overall_effect, color='r', linestyle='--', label="真实效应")
    plt.title("估计量分布对比")
    plt.xlabel("估计效应")
    plt.ylabel("频数")
    plt.legend()
    plt.tight_layout()
    plt.savefig("post_stratification_distribution.png", dpi=150)
    plt.close()
    print("  图像已保存: post_stratification_distribution.png")


def simulate_variance_reduction_visual(n_total=10000):
    """单次模拟，可视化各层效应与加权结果。"""
    x, t, y, s, props, true_effects = generate_stratified_data(n_total)
    post_eff, post_se, layer_effects = post_stratification_estimate(y, t, s, props)
    simple_eff, p_simple = simple_difference(y, t)

    strata_labels = ["层1", "层2", "层3", "层4"]
    x_pos = np.arange(len(strata_labels))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x_pos, layer_effects, color='steelblue', label="各层内估计效应")
    ax.axhline(simple_eff, color='orange', linestyle='--', label=f"简单估计量={simple_eff:.2f}")
    ax.axhline(post_eff, color='green', linestyle='--', label=f"后分层估计量={post_eff:.2f}")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(strata_labels)
    ax.set_ylabel("估计效应")
    ax.set_title("各层效应与总体估计量对比")
    ax.legend()
    plt.tight_layout()
    plt.savefig("post_stratification_layers.png", dpi=150)
    plt.close()
    print("\n[分层可视化]")
    print(f"  简单估计量: {simple_eff:.3f}")
    print(f"  后分层估计量: {post_eff:.3f}")
    print("  图像已保存: post_stratification_layers.png")


def main():
    print("=" * 50)
    print("后分层分析 —— 模拟演示")
    print("=" * 50)

    simulate_post_stratification(n_total=10000, n_simulations=500)
    simulate_variance_reduction_visual(n_total=10000)

    print("\n" + "=" * 50)
    print("全部模拟完成。")
    print("=" * 50)


if __name__ == "__main__":
    main()
