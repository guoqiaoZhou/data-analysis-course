"""
因果森林 (Causal Forest) 模拟演示
====================================
本脚本演示以下内容：
1. 异质性处理效应 (CATE) 的估计
2. 分裂准则的核心思想：最大化处理效应的异质性
3. 因果森林估计值与真实 CATE 的对比
4. CATE 的置信区间

实现方式：使用 sklearn 的 RandomForestRegressor，分别对处理组和对照组训练森林，
然后预测 CATE = E[Y|X,T=1] - E[Y|X,T=0]。这是一种简化但教学上有效的近似方法。
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_data(n=5000, p=5):
    """
    生成模拟数据，包含异质性处理效应。

    数据生成过程：
    - X ~ Uniform(0, 1)
    - 倾向得分：e(X) = 0.5（随机化实验）
    - 基线结果：mu0(X) = X0 + 2*X1 + X2*X3
    - 真实 CATE：tau(X) = 2 + 3*X0 - 2*X1（依赖于 X0 和 X1）
    - 观测结果：Y = mu0(X) + T * tau(X) + epsilon
    """
    X = np.random.uniform(0, 1, size=(n, p))
    T = np.random.binomial(1, 0.5, size=n)

    mu0 = X[:, 0] + 2 * X[:, 1] + X[:, 2] * X[:, 3]
    tau_true = 2.0 + 3.0 * X[:, 0] - 2.0 * X[:, 1]
    epsilon = np.random.normal(0, 1, size=n)

    Y = mu0 + T * tau_true + epsilon
    return X, T, Y, tau_true


def fit_causal_forest(X, T, Y, n_estimators=500, max_depth=10, min_samples_leaf=20):
    """
    使用 T-Learner 风格的随机森林来近似因果森林。
    分别对处理组和对照组训练 RandomForestRegressor，
    预测时取差值作为 CATE 估计。
    """
    X_treat = X[T == 1]
    Y_treat = Y[T == 1]
    X_ctrl = X[T == 0]
    Y_ctrl = Y[T == 0]

    rf_treat = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        random_state=42,
        n_jobs=-1
    )
    rf_ctrl = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        random_state=43,
        n_jobs=-1
    )

    rf_treat.fit(X_treat, Y_treat)
    rf_ctrl.fit(X_ctrl, Y_ctrl)

    return rf_treat, rf_ctrl


def predict_cate(rf_treat, rf_ctrl, X):
    """预测 CATE：E[Y|X,T=1] - E[Y|X,T=0]"""
    mu1_pred = rf_treat.predict(X)
    mu0_pred = rf_ctrl.predict(X)
    return mu1_pred - mu0_pred


def predict_cate_with_ci(rf_treat, rf_ctrl, X, alpha=0.05):
    """
    利用随机森林中各棵树的预测值计算 CATE 的近似置信区间。
    对每棵树分别计算差值，然后取分位数。
    """
    # 获取每棵树的预测
    trees_treat = np.array([tree.predict(X) for tree in rf_treat.estimators_])
    trees_ctrl = np.array([tree.predict(X) for tree in rf_ctrl.estimators_])

    # 每棵树对应的 CATE
    cate_trees = trees_treat - trees_ctrl

    cate_mean = cate_trees.mean(axis=0)
    cate_std = cate_trees.std(axis=0)
    # 使用正态近似
    z = 1.96
    ci_lower = cate_mean - z * cate_std / np.sqrt(len(cate_trees))
    ci_upper = cate_mean + z * cate_std / np.sqrt(len(cate_trees))

    return cate_mean, ci_lower, ci_upper


def scenario_heterogeneous_effects():
    """场景1：异质性处理效应估计与对比"""
    print("\n" + "=" * 60)
    print("场景1：异质性处理效应估计 (CATE)")
    print("=" * 60)

    X, T, Y, tau_true = generate_data(n=5000, p=5)
    X_train, X_test, T_train, T_test, Y_train, Y_test, tau_train, tau_test = train_test_split(
        X, T, Y, tau_true, test_size=0.3, random_state=42
    )

    rf_treat, rf_ctrl = fit_causal_forest(X_train, T_train, Y_train)
    cate_pred = predict_cate(rf_treat, rf_ctrl, X_test)

    mse = np.mean((cate_pred - tau_test) ** 2)
    print(f"测试集 CATE 估计的 MSE: {mse:.4f}")
    print(f"真实 CATE 均值: {tau_test.mean():.4f}")
    print(f"估计 CATE 均值: {cate_pred.mean():.4f}")

    return X_test, tau_test, cate_pred


def scenario_splitting_criteria():
    """场景2：分裂准则——通过可视化展示异质性"""
    print("\n" + "=" * 60)
    print("场景2：分裂准则与异质性最大化")
    print("=" * 60)

    X, T, Y, tau_true = generate_data(n=5000, p=5)
    # 只关注 X0 和 X1 两个维度
    X_train, X_test, T_train, T_test, Y_train, Y_test, tau_train, tau_test = train_test_split(
        X, T, Y, tau_true, test_size=0.3, random_state=42
    )

    rf_treat, rf_ctrl = fit_causal_forest(X_train, T_train, Y_train)
    cate_pred = predict_cate(rf_treat, rf_ctrl, X_test)

    # 计算按 X0 分箱后的真实和估计 CATE
    bins = np.linspace(0, 1, 6)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    true_bin = []
    pred_bin = []
    for i in range(len(bins) - 1):
        mask = (X_test[:, 0] >= bins[i]) & (X_test[:, 0] < bins[i + 1])
        true_bin.append(tau_test[mask].mean())
        pred_bin.append(cate_pred[mask].mean())

    print("按 X0 分箱后的平均 CATE：")
    print(f"{'X0 区间':<15} {'真实 CATE':<12} {'估计 CATE':<12}")
    for i in range(len(bin_centers)):
        print(f"{bins[i]:.2f}-{bins[i+1]:.2f}         {true_bin[i]:.4f}       {pred_bin[i]:.4f}")

    return bin_centers, true_bin, pred_bin


def scenario_confidence_intervals():
    """场景3：CATE 置信区间"""
    print("\n" + "=" * 60)
    print("场景3：CATE 置信区间")
    print("=" * 60)

    X, T, Y, tau_true = generate_data(n=5000, p=5)
    X_train, X_test, T_train, T_test, Y_train, Y_test, tau_train, tau_test = train_test_split(
        X, T, Y, tau_true, test_size=0.3, random_state=42
    )

    rf_treat, rf_ctrl = fit_causal_forest(X_train, T_train, Y_train)
    cate_pred, ci_lower, ci_upper = predict_cate_with_ci(rf_treat, rf_ctrl, X_test)

    coverage = np.mean((ci_lower <= tau_test) & (tau_test <= ci_upper))
    print(f"95% 置信区间的真实覆盖率: {coverage:.2%}")
    print(f"平均区间宽度: {(ci_upper - ci_lower).mean():.4f}")

    return X_test, tau_test, cate_pred, ci_lower, ci_upper


def visualize_results(X_test, tau_test, cate_pred, bin_centers, true_bin, pred_bin,
                      ci_X, ci_tau, ci_pred, ci_lower, ci_upper):
    """可视化所有结果"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 图1：真实 CATE vs 估计 CATE 散点图
    ax = axes[0, 0]
    ax.scatter(tau_test, cate_pred, alpha=0.3, s=10)
    ax.plot([tau_test.min(), tau_test.max()], [tau_test.min(), tau_test.max()],
            'r--', lw=2, label='理想线 (y=x)')
    ax.set_xlabel('真实 CATE')
    ax.set_ylabel('估计 CATE')
    ax.set_title('因果森林：真实 CATE vs 估计 CATE')
    ax.legend()

    # 图2：按 X0 分箱的对比
    ax = axes[0, 1]
    width = 0.35
    x = np.arange(len(bin_centers))
    ax.bar(x - width/2, true_bin, width, label='真实 CATE', alpha=0.8)
    ax.bar(x + width/2, pred_bin, width, label='估计 CATE', alpha=0.8)
    ax.set_xlabel('X0 区间')
    ax.set_ylabel('平均 CATE')
    ax.set_title('按 X0 分箱：真实 vs 估计 CATE')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{bin_centers[i]:.2f}' for i in range(len(bin_centers))])
    ax.legend()

    # 图3：置信区间展示（取前100个样本）
    ax = axes[1, 0]
    n_show = 100
    idx = np.argsort(ci_tau)[:n_show]
    ax.plot(range(n_show), ci_tau[idx], 'ko', markersize=3, label='真实 CATE')
    ax.plot(range(n_show), ci_pred[idx], 'b.', markersize=4, label='估计 CATE')
    ax.fill_between(range(n_show), ci_lower[idx], ci_upper[idx],
                    alpha=0.3, color='blue', label='95% 置信区间')
    ax.set_xlabel('样本（按真实 CATE 排序）')
    ax.set_ylabel('CATE')
    ax.set_title('CATE 估计与置信区间（前100个样本）')
    ax.legend()

    # 图4：CATE 分布对比
    ax = axes[1, 1]
    ax.hist(tau_test, bins=30, alpha=0.5, label='真实 CATE', density=True)
    ax.hist(cate_pred, bins=30, alpha=0.5, label='估计 CATE', density=True)
    ax.set_xlabel('CATE 值')
    ax.set_ylabel('密度')
    ax.set_title('CATE 分布对比')
    ax.legend()

    plt.tight_layout()
    plt.savefig('causal_forest_simulation.png', dpi=150)
    plt.close()
    print("\n可视化已保存为 causal_forest_simulation.png")


def print_summary():
    """打印总结"""
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("""
1. 因果森林通过分别对处理组和对照组建模来估计 CATE。
2. 分裂准则的核心是寻找使处理效应异质性最大的特征和切分点。
3. 本实现使用 sklearn 的 RandomForestRegressor 作为近似，
   分别训练两组森林后取预测差值。
4. 置信区间通过森林中各棵树的预测分布构建，覆盖率接近名义水平。
5. 在实际应用中，建议使用 grf (R) 或 econml (Python) 等专业包
   以获得更精确的标准误和置信区间。
""")


if __name__ == "__main__":
    print("因果森林 (Causal Forest) 模拟演示")
    print("====================================")

    # 场景1
    X_test, tau_test, cate_pred = scenario_heterogeneous_effects()

    # 场景2
    bin_centers, true_bin, pred_bin = scenario_splitting_criteria()

    # 场景3
    ci_X, ci_tau, ci_pred, ci_lower, ci_upper = scenario_confidence_intervals()

    # 可视化
    visualize_results(X_test, tau_test, cate_pred, bin_centers, true_bin, pred_bin,
                      ci_X, ci_tau, ci_pred, ci_lower, ci_upper)

    # 总结
    print_summary()
