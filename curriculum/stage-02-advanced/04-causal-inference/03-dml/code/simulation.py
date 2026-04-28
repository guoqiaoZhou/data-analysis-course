"""
DML (Double Machine Learning) 模拟演示

本脚本演示：
1. 部分线性模型中的 DML 估计
2. Nuisance 函数估计与交叉拟合 (Cross-fitting)
3. 朴素 ML 方法 vs DML 的偏差对比
4. 高维协变量场景
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold

# 中文显示设置
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_data(n=1000, p=10, true_theta=2.5, high_dim=False):
    """
    生成部分线性模型数据：
    Y = theta * D + g(X) + epsilon
    D = m(X) + eta
    """
    if high_dim:
        p = 200

    X = np.random.normal(0, 1, (n, p))

    # 复杂 nuisance 函数
    g_X = (X[:, 0] * X[:, 1] + np.sin(X[:, 2]) + X[:, 3]**2
           + 0.5 * X[:, 4] * X[:, 5] + np.log(np.abs(X[:, 6]) + 1))

    m_X = (0.5 * X[:, 0] + 0.3 * X[:, 1] - 0.4 * X[:, 2]
           + 0.2 * X[:, 3] * X[:, 4] + 0.1 * np.cos(X[:, 5]))

    eta = np.random.normal(0, 1, n)
    D = m_X + eta

    epsilon = np.random.normal(0, 1, n)
    Y = true_theta * D + g_X + epsilon

    df = pd.DataFrame(X, columns=[f'X{i}' for i in range(p)])
    df['D'] = D
    df['Y'] = Y
    df['true_theta'] = true_theta
    return df


def estimate_nuisance_lasso(X, y, n_splits=5):
    """使用 LassoCV 估计 nuisance 函数。"""
    model = LassoCV(cv=n_splits, max_iter=5000, random_state=42)
    model.fit(X, y)
    return model


def estimate_nuisance_gbm(X, y):
    """使用梯度提升估计 nuisance 函数。"""
    model = GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)
    model.fit(X, y)
    return model


def dml_estimator(df, model_type='lasso', n_splits=5, true_theta=2.5):
    """
    DML 估计器（交叉拟合）。
    返回 theta 估计值及其标准误。
    """
    X_cols = [c for c in df.columns if c.startswith('X')]
    X = df[X_cols].values
    D = df['D'].values
    Y = df['Y'].values
    n = len(df)

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    theta_estimates = []
    residuals_Y = []
    residuals_D = []

    for train_idx, test_idx in kf.split(X):
        X_train, X_test = X[train_idx], X[test_idx]
        D_train, D_test = D[train_idx], D[test_idx]
        Y_train, Y_test = Y[train_idx], Y[test_idx]

        if model_type == 'lasso':
            model_g = estimate_nuisance_lasso(X_train, Y_train)
            model_m = estimate_nuisance_lasso(X_train, D_train)
        else:
            model_g = estimate_nuisance_gbm(X_train, Y_train)
            model_m = estimate_nuisance_gbm(X_train, D_train)

        g_hat = model_g.predict(X_test)
        m_hat = model_m.predict(X_test)

        V = Y_test - g_hat
        W = D_test - m_hat

        # 局部估计
        theta_fold = np.mean(W * V) / np.mean(W ** 2)
        theta_estimates.append(theta_fold)

        residuals_Y.extend(V)
        residuals_D.extend(W)

    # 汇总估计
    V_all = np.array(residuals_Y)
    W_all = np.array(residuals_D)
    theta = np.mean(W_all * V_all) / np.mean(W_all ** 2)

    # 影响函数方差
    psi = W_all * (V_all - theta * W_all)
    var_theta = np.var(psi) / (np.mean(W_all ** 2) ** 2 * n)
    se = np.sqrt(var_theta)

    return theta, se, theta_estimates


def naive_ml_estimator(df, model_type='lasso'):
    """
    朴素 ML 估计：直接用 ML 预测 Y，忽略 D 的 endogeneity。
    即：先预测 Y ~ X，然后用残差对 D 做回归（但不用交叉拟合，导致过拟合偏差）。
    这里用同样本拟合+预测来演示过拟合偏差。
    """
    X_cols = [c for c in df.columns if c.startswith('X')]
    X = df[X_cols].values
    D = df['D'].values
    Y = df['Y'].values

    if model_type == 'lasso':
        model_g = estimate_nuisance_lasso(X, Y)
        model_m = estimate_nuisance_lasso(X, D)
    else:
        model_g = estimate_nuisance_gbm(X, Y)
        model_m = estimate_nuisance_gbm(X, D)

    g_hat = model_g.predict(X)
    m_hat = model_m.predict(X)

    V = Y - g_hat
    W = D - m_hat

    theta = np.mean(W * V) / np.mean(W ** 2)
    return theta


def scenario_dml_lowdim():
    """低维场景下的 DML 估计。"""
    print("=" * 60)
    print("【场景 1】低维协变量下的 DML 估计")
    print("=" * 60)

    df = generate_data(n=1000, p=10, true_theta=2.5, high_dim=False)
    true_theta = df['true_theta'].iloc[0]

    theta_lasso, se_lasso, folds_lasso = dml_estimator(df, model_type='lasso')
    theta_gbm, se_gbm, folds_gbm = dml_estimator(df, model_type='gbm')

    print(f"\n真实 theta: {true_theta:.4f}")
    print(f"DML (Lasso) 估计: {theta_lasso:.4f}, SE={se_lasso:.4f}, 偏差={abs(theta_lasso-true_theta):.4f}")
    print(f"DML (GBM)   估计: {theta_gbm:.4f}, SE={se_gbm:.4f}, 偏差={abs(theta_gbm-true_theta):.4f}")
    print(f"  Lasso 各折估计: {[f'{x:.4f}' for x in folds_lasso]}")
    print(f"  GBM   各折估计: {[f'{x:.4f}' for x in folds_gbm]}")

    return df, true_theta, theta_lasso, theta_gbm


def scenario_naive_vs_dml():
    """朴素 ML vs DML 偏差对比。"""
    print("\n" + "=" * 60)
    print("【场景 2】朴素 ML vs DML 偏差对比")
    print("=" * 60)

    df = generate_data(n=1000, p=10, true_theta=2.5, high_dim=False)
    true_theta = df['true_theta'].iloc[0]

    naive_lasso = naive_ml_estimator(df, model_type='lasso')
    naive_gbm = naive_ml_estimator(df, model_type='gbm')
    dml_lasso, _, _ = dml_estimator(df, model_type='lasso')
    dml_gbm, _, _ = dml_estimator(df, model_type='gbm')

    print(f"\n真实 theta: {true_theta:.4f}")
    print(f"朴素 ML (Lasso): {naive_lasso:.4f}, 偏差={abs(naive_lasso-true_theta):.4f}")
    print(f"朴素 ML (GBM)  : {naive_gbm:.4f}, 偏差={abs(naive_gbm-true_theta):.4f}")
    print(f"DML (Lasso)    : {dml_lasso:.4f}, 偏差={abs(dml_lasso-true_theta):.4f}")
    print(f"DML (GBM)      : {dml_gbm:.4f}, 偏差={abs(dml_gbm-true_theta):.4f}")
    print("\n说明：朴素 ML 由于在同一样本上拟合 nuisance 再估计 theta，")
    print("      产生过拟合偏差；DML 通过交叉拟合消除了该偏差。")

    return true_theta, naive_lasso, naive_gbm, dml_lasso, dml_gbm


def scenario_highdim():
    """高维场景下的 DML 估计。"""
    print("\n" + "=" * 60)
    print("【场景 3】高维协变量下的 DML 估计 (p=200)")
    print("=" * 60)

    df = generate_data(n=1000, p=200, true_theta=2.5, high_dim=True)
    true_theta = df['true_theta'].iloc[0]

    theta_lasso, se_lasso, folds_lasso = dml_estimator(df, model_type='lasso')
    theta_gbm, se_gbm, folds_gbm = dml_estimator(df, model_type='gbm')

    print(f"\n真实 theta: {true_theta:.4f}")
    print(f"DML (Lasso) 估计: {theta_lasso:.4f}, SE={se_lasso:.4f}, 偏差={abs(theta_lasso-true_theta):.4f}")
    print(f"DML (GBM)   估计: {theta_gbm:.4f}, SE={se_gbm:.4f}, 偏差={abs(theta_gbm-true_theta):.4f}")
    print(f"  Lasso 各折估计: {[f'{x:.4f}' for x in folds_lasso]}")
    print(f"  GBM   各折估计: {[f'{x:.4f}' for x in folds_gbm]}")
    print("\n说明：高维场景下，正则化 ML（如 Lasso）能有效筛选重要协变量，")
    print("      交叉拟合保证 nuisance 估计误差不影响 theta 的渐进正态性。")

    return true_theta, theta_lasso, theta_gbm


def visualize_results(true_theta, naive_lasso, naive_gbm, dml_lasso, dml_gbm):
    """生成可视化图表。"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 1. 朴素 ML vs DML 偏差对比
    ax = axes[0]
    methods = ['朴素 Lasso', '朴素 GBM', 'DML Lasso', 'DML GBM']
    estimates = [naive_lasso, naive_gbm, dml_lasso, dml_gbm]
    biases = [abs(e - true_theta) for e in estimates]
    colors = ['coral', 'coral', 'skyblue', 'skyblue']
    bars = ax.bar(methods, biases, color=colors)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_ylabel('绝对偏差')
    ax.set_title('朴素 ML vs DML 估计偏差对比')
    for bar, est in zip(bars, estimates):
        height = bar.get_height()
        ax.annotate(f'{est:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    # 2. 估计值与真实值对比
    ax = axes[1]
    ax.axhline(true_theta, color='green', linestyle='--', linewidth=2, label=f'真实值 θ={true_theta}')
    ax.scatter(methods, estimates, color=colors, s=100, zorder=5)
    ax.plot(methods, estimates, color='gray', linestyle='-', linewidth=1, alpha=0.5)
    ax.set_ylabel('估计值')
    ax.set_title('各方法估计值与真实值对比')
    ax.legend()

    plt.tight_layout()
    plt.savefig('dml_simulation.png', dpi=150)
    print("\n[可视化已保存] dml_simulation.png")
    plt.close()


def summary():
    """总结说明。"""
    print("\n" + "=" * 60)
    print("【总结】")
    print("=" * 60)
    print("""
本脚本演示了 DML 的核心内容：
1. 部分线性模型：Y = θ·D + g(X) + ε，目标是估计 θ
2. Nuisance 函数 g(X) 和 m(X) 可用 ML 灵活估计
3. 交叉拟合（Cross-fitting）：将样本分为 K 折，
   在一折上训练 nuisance，在另一折上估计 θ，消除过拟合偏差
4. 高维场景：正则化 ML + DML 仍能获得一致且渐进正态的估计

关键要点：
- 朴素 ML（同样本拟合+估计）会产生正则化偏差
- DML 通过样本分割消除该偏差，且对 nuisance 估计速率要求较低
- 影响函数法可构造有效的标准误和置信区间
""")


if __name__ == "__main__":
    df, true_theta, theta_lasso, theta_gbm = scenario_dml_lowdim()
    true_theta2, naive_lasso, naive_gbm, dml_lasso, dml_gbm = scenario_naive_vs_dml()
    true_theta3, hd_lasso, hd_gbm = scenario_highdim()
    visualize_results(true_theta2, naive_lasso, naive_gbm, dml_lasso, dml_gbm)
    summary()
