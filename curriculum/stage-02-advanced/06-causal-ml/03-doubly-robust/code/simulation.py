"""
双重稳健学习 (Doubly Robust Learning) 模拟演示
===============================================
本脚本演示以下内容：
1. AIPW (Augmented Inverse Probability Weighting) 估计量
2. 双重稳健性：只要倾向得分模型或结果模型之一正确，估计量就是一致的
3. 对比：IPW 估计量、回归估计量、DR 估计量
4. 当其中一个模型设定错误时的稳健性表现
"""

import warnings
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression

# 抑制 sklearn LinearRegression 在极端数据上的数值警告
warnings.filterwarnings('ignore', category=RuntimeWarning)

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_data(n=5000, p=5, misspecify=False):
    """
    生成模拟数据。

    真实数据生成过程：
    - X ~ Uniform(0, 1)
    - 倾向得分（真实）：e(X) = logistic(0.5*(X0 - 0.5) + 0.3*X1)
    - 基线结果（真实）：mu0(X) = X0 + 2*X1 + X2*X3
    - 处理效应：tau = 2.0（常数 ATE）
    - Y = mu0(X) + T * tau + epsilon

    参数 misspecify：如果为 True，在生成中引入非线性交互，使得线性模型设定错误。
    """
    X = np.random.uniform(0, 1, size=(n, p))

    # 真实倾向得分
    logit = 0.5 * (X[:, 0] - 0.5) + 0.3 * X[:, 1]
    e_true = 1 / (1 + np.exp(-logit))
    T = np.random.binomial(1, e_true)

    # 真实结果模型
    if misspecify:
        # 加入非线性项，使线性模型设定错误
        mu0 = X[:, 0] + 2 * X[:, 1] + 5 * np.sin(2 * np.pi * X[:, 2]) + X[:, 3] ** 2
    else:
        mu0 = X[:, 0] + 2 * X[:, 1] + X[:, 2] * X[:, 3]

    tau_true = 2.0
    epsilon = np.random.normal(0, 1, size=n)
    Y = mu0 + T * tau_true + epsilon

    return X, T, Y, tau_true


def estimate_ipw(X, T, Y, use_correct_ps=True):
    """
    IPW (Inverse Probability Weighting) 估计量。
    ATE = E[ T*Y/e(X) - (1-T)*Y/(1-e(X)) ]
    """
    if use_correct_ps:
        # 使用正确的模型设定（GBDT 可以较好地拟合真实倾向得分）
        ps_model = GradientBoostingClassifier(n_estimators=200, max_depth=4, random_state=42)
        ps_model.fit(X, T)
        e_hat = np.clip(ps_model.predict_proba(X)[:, 1], 0.05, 0.95)
    else:
        # 错误设定：只用 X0 做逻辑回归，遗漏了 X1
        ps_model = LogisticRegression(max_iter=1000, random_state=42)
        ps_model.fit(X[:, :1], T)
        e_hat = np.clip(ps_model.predict_proba(X[:, :1])[:, 1], 0.05, 0.95)

    ipw = np.mean(T * Y / e_hat - (1 - T) * Y / (1 - e_hat))
    return ipw


def estimate_regression(X, T, Y, use_correct_outcome=True):
    """
    回归估计量（G-computation）。
    ATE = E[ mu1(X) - mu0(X) ]
    """
    if use_correct_outcome:
        # 正确设定：GBDT 可以较好地拟合非线性结果
        model1 = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
        model0 = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=43)
    else:
        # 错误设定：线性回归，无法捕捉非线性
        model1 = LinearRegression()
        model0 = LinearRegression()

    model1.fit(X[T == 1], Y[T == 1])
    model0.fit(X[T == 0], Y[T == 0])

    mu1_hat = model1.predict(X)
    mu0_hat = model0.predict(X)

    ate_reg = np.mean(mu1_hat - mu0_hat)
    return ate_reg


def estimate_aipw(X, T, Y, use_correct_ps=True, use_correct_outcome=True):
    """
    AIPW (Augmented Inverse Probability Weighting) / DR 估计量。
    ATE = E[ mu1(X) - mu0(X)
             + T*(Y - mu1(X))/e(X)
             - (1-T)*(Y - mu0(X))/(1-e(X)) ]
    """
    # 倾向得分估计
    if use_correct_ps:
        ps_model = GradientBoostingClassifier(n_estimators=200, max_depth=4, random_state=42)
        ps_model.fit(X, T)
        e_hat = np.clip(ps_model.predict_proba(X)[:, 1], 0.05, 0.95)
    else:
        ps_model = LogisticRegression(max_iter=1000, random_state=42)
        ps_model.fit(X[:, :1], T)
        e_hat = np.clip(ps_model.predict_proba(X[:, :1])[:, 1], 0.05, 0.95)

    # 结果模型估计
    if use_correct_outcome:
        model1 = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
        model0 = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=43)
    else:
        model1 = LinearRegression()
        model0 = LinearRegression()

    model1.fit(X[T == 1], Y[T == 1])
    model0.fit(X[T == 0], Y[T == 0])

    mu1_hat = model1.predict(X)
    mu0_hat = model0.predict(X)

    # AIPW 公式
    dr_term1 = mu1_hat - mu0_hat
    dr_term2 = T * (Y - mu1_hat) / e_hat
    dr_term3 = (1 - T) * (Y - mu0_hat) / (1 - e_hat)

    ate_aipw = np.mean(dr_term1 + dr_term2 - dr_term3)
    return ate_aipw


def scenario_correct_models():
    """场景1：所有模型都正确设定"""
    print("\n" + "=" * 60)
    print("场景1：模型均正确设定")
    print("=" * 60)

    X, T, Y, tau_true = generate_data(n=5000, p=5, misspecify=False)

    ate_ipw = estimate_ipw(X, T, Y, use_correct_ps=True)
    ate_reg = estimate_regression(X, T, Y, use_correct_outcome=True)
    ate_dr = estimate_aipw(X, T, Y, use_correct_ps=True, use_correct_outcome=True)

    print(f"真实 ATE: {tau_true:.4f}")
    print(f"IPW 估计: {ate_ipw:.4f} (误差: {abs(ate_ipw - tau_true):.4f})")
    print(f"回归估计: {ate_reg:.4f} (误差: {abs(ate_reg - tau_true):.4f})")
    print(f"DR  估计: {ate_dr:.4f} (误差: {abs(ate_dr - tau_true):.4f})")

    return ate_ipw, ate_reg, ate_dr


def scenario_misspecified_ps():
    """场景2：倾向得分模型错误设定，结果模型正确"""
    print("\n" + "=" * 60)
    print("场景2：倾向得分模型错误设定，结果模型正确")
    print("=" * 60)

    X, T, Y, tau_true = generate_data(n=5000, p=5, misspecify=False)

    ate_ipw = estimate_ipw(X, T, Y, use_correct_ps=False)
    ate_reg = estimate_regression(X, T, Y, use_correct_outcome=True)
    ate_dr = estimate_aipw(X, T, Y, use_correct_ps=False, use_correct_outcome=True)

    print(f"真实 ATE: {tau_true:.4f}")
    print(f"IPW 估计: {ate_ipw:.4f} (误差: {abs(ate_ipw - tau_true):.4f})")
    print(f"回归估计: {ate_reg:.4f} (误差: {abs(ate_reg - tau_true):.4f})")
    print(f"DR  估计: {ate_dr:.4f} (误差: {abs(ate_dr - tau_true):.4f})")

    return ate_ipw, ate_reg, ate_dr


def scenario_misspecified_outcome():
    """场景3：倾向得分模型正确，结果模型错误设定"""
    print("\n" + "=" * 60)
    print("场景3：倾向得分模型正确，结果模型错误设定")
    print("=" * 60)

    X, T, Y, tau_true = generate_data(n=5000, p=5, misspecify=True)

    ate_ipw = estimate_ipw(X, T, Y, use_correct_ps=True)
    ate_reg = estimate_regression(X, T, Y, use_correct_outcome=False)
    ate_dr = estimate_aipw(X, T, Y, use_correct_ps=True, use_correct_outcome=False)

    print(f"真实 ATE: {tau_true:.4f}")
    print(f"IPW 估计: {ate_ipw:.4f} (误差: {abs(ate_ipw - tau_true):.4f})")
    print(f"回归估计: {ate_reg:.4f} (误差: {abs(ate_reg - tau_true):.4f})")
    print(f"DR  估计: {ate_dr:.4f} (误差: {abs(ate_dr - tau_true):.4f})")

    return ate_ipw, ate_reg, ate_dr


def scenario_both_misspecified():
    """场景4：两个模型都错误设定"""
    print("\n" + "=" * 60)
    print("场景4：两个模型均错误设定")
    print("=" * 60)

    X, T, Y, tau_true = generate_data(n=5000, p=5, misspecify=True)

    ate_ipw = estimate_ipw(X, T, Y, use_correct_ps=False)
    ate_reg = estimate_regression(X, T, Y, use_correct_outcome=False)
    ate_dr = estimate_aipw(X, T, Y, use_correct_ps=False, use_correct_outcome=False)

    print(f"真实 ATE: {tau_true:.4f}")
    print(f"IPW 估计: {ate_ipw:.4f} (误差: {abs(ate_ipw - tau_true):.4f})")
    print(f"回归估计: {ate_reg:.4f} (误差: {abs(ate_reg - tau_true):.4f})")
    print(f"DR  估计: {ate_dr:.4f} (误差: {abs(ate_dr - tau_true):.4f})")

    return ate_ipw, ate_reg, ate_dr


def run_monte_carlo(n_runs=20):
    """蒙特卡洛模拟：多次重复评估稳健性"""
    print("\n" + "=" * 60)
    print("蒙特卡洛模拟：评估各估计量的稳健性")
    print("=" * 60)

    scenarios = {
        '均正确': (False, True, True),
        'PS错误': (False, False, True),
        '结果错误': (True, True, False),
        '均错误': (True, False, False)
    }

    results = {name: {'IPW': [], '回归': [], 'DR': []} for name in scenarios}

    for run in range(n_runs):
        for scen_name, (misspec, correct_ps, correct_out) in scenarios.items():
            np.random.seed(42 + run)
            X, T, Y, tau_true = generate_data(n=3000, p=5, misspecify=misspec)

            ate_ipw = estimate_ipw(X, T, Y, use_correct_ps=correct_ps)
            ate_reg = estimate_regression(X, T, Y, use_correct_outcome=correct_out)
            ate_dr = estimate_aipw(X, T, Y, use_correct_ps=correct_ps, use_correct_outcome=correct_out)

            results[scen_name]['IPW'].append(ate_ipw - tau_true)
            results[scen_name]['回归'].append(ate_reg - tau_true)
            results[scen_name]['DR'].append(ate_dr - tau_true)

    print(f"\n{'场景':<10} {'估计量':<8} {'平均偏差':<12} {'RMSE':<12}")
    print("-" * 45)
    for scen_name in scenarios:
        for est_name in ['IPW', '回归', 'DR']:
            biases = results[scen_name][est_name]
            mean_bias = np.mean(biases)
            rmse = np.sqrt(np.mean(np.array(biases) ** 2))
            print(f"{scen_name:<10} {est_name:<8} {mean_bias:>10.4f}   {rmse:>10.4f}")

    return results


def visualize_results(mc_results):
    """可视化蒙特卡洛结果"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    scenarios = list(mc_results.keys())
    estimators = ['IPW', '回归', 'DR']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for idx, scen_name in enumerate(scenarios):
        ax = axes[idx // 2, idx % 2]
        data = [mc_results[scen_name][est] for est in estimators]
        bp = ax.boxplot(data, labels=estimators, patch_artist=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        ax.axhline(0, color='red', linestyle='--', lw=1)
        ax.set_ylabel('估计误差 (估计值 - 真实值)')
        ax.set_title(f'场景：{scen_name}')

    plt.tight_layout()
    plt.savefig('doubly_robust_simulation.png', dpi=150)
    plt.close()
    print("\n可视化已保存为 doubly_robust_simulation.png")


def print_summary():
    """打印总结"""
    print("\n" + "=" * 60)
    print("双重稳健学习总结")
    print("=" * 60)
    print("""
1. IPW 估计量：仅依赖倾向得分模型。当 PS 模型错误时，估计有偏。
2. 回归估计量：仅依赖结果模型。当结果模型错误时，估计有偏。
3. AIPW / DR 估计量：结合两者，具有双重稳健性：
   - 只要倾向得分模型 OR 结果模型之一正确，估计量就是一致的
   - 当两者都正确时，达到半参数效率界
4. 实际应用建议：
   - 尽量使用机器学习方法（如 GBDT）灵活建模
   - 交叉拟合 (cross-fitting) 可进一步减少过拟合偏差
   - 在观察性研究中，DR 估计量比单一方法更可靠
""")


if __name__ == "__main__":
    print("双重稳健学习 (Doubly Robust Learning) 模拟演示")
    print("===============================================")

    # 四个场景
    scenario_correct_models()
    scenario_misspecified_ps()
    scenario_misspecified_outcome()
    scenario_both_misspecified()

    # 蒙特卡洛模拟
    mc_results = run_monte_carlo(n_runs=20)
    visualize_results(mc_results)

    # 总结
    print_summary()
