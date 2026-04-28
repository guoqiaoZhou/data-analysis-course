"""
CUPED方差缩减 —— 模拟演示
==========================
本脚本演示以下内容：
1. CUPED（Controlled-experiment Using Pre-Experiment Data）方差缩减原理
2. 协变量选择对缩减效果的影响
3. 计算方差缩减百分比
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def generate_data(n, rho=0.8, treatment_effect=2.0, sigma=10.0):
    """
    生成带有前测协变量的实验数据。
    Y = treatment_effect * T + rho * X + epsilon
    """
    x = np.random.normal(100, sigma, n)
    t = np.random.binomial(1, 0.5, n)
    epsilon = np.random.normal(0, sigma * np.sqrt(1 - rho ** 2), n)
    y = treatment_effect * t + x + epsilon
    return x, t, y


def cuped_adjust(y, x, theta=None):
    """
    CUPED 调整：Y_cuped = Y - theta * (X - mean(X))
    最优 theta = Cov(Y, X) / Var(X)
    """
    if theta is None:
        theta = np.cov(y, x)[0, 1] / np.var(x)
    y_cuped = y - theta * (x - x.mean())
    return y_cuped, theta


def simulate_cuped_variance_reduction(n=5000):
    """
    对比普通估计量与 CUPED 调整后的估计量方差。
    """
    x, t, y = generate_data(n, rho=0.8, treatment_effect=2.0, sigma=10.0)
    y_cuped, theta = cuped_adjust(y, x)

    var_y = np.var(y, ddof=1)
    var_cuped = np.var(y_cuped, ddof=1)
    reduction = (var_y - var_cuped) / var_y * 100

    # 估计效应
    ctrl_y = y[t == 0]
    treat_y = y[t == 1]
    diff_y = treat_y.mean() - ctrl_y.mean()
    se_y = np.sqrt(ctrl_y.var(ddof=1) / len(ctrl_y) + treat_y.var(ddof=1) / len(treat_y))

    ctrl_c = y_cuped[t == 0]
    treat_c = y_cuped[t == 1]
    diff_c = treat_c.mean() - ctrl_c.mean()
    se_c = np.sqrt(ctrl_c.var(ddof=1) / len(ctrl_c) + treat_c.var(ddof=1) / len(treat_c))

    print("[CUPED 方差缩减演示]")
    print(f"  样本量: {n}")
    print(f"  原始指标方差: {var_y:.3f}")
    print(f"  CUPED 后方差: {var_cuped:.3f}")
    print(f"  方差缩减比例: {reduction:.2f}%")
    print(f"  原始估计效应: {diff_y:.3f} (SE={se_y:.3f})")
    print(f"  CUPED 估计效应: {diff_c:.3f} (SE={se_c:.3f})")

    # 可视化方差对比
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].hist(y, bins=50, alpha=0.6, label="原始 Y")
    axes[0].set_title(f"原始 Y 分布 (方差={var_y:.2f})")
    axes[1].hist(y_cuped, bins=50, alpha=0.6, label="CUPED Y", color='orange')
    axes[1].set_title(f"CUPED 调整后分布 (方差={var_cuped:.2f})")
    plt.tight_layout()
    plt.savefig("cuped_variance.png", dpi=150)
    plt.close()
    print("  图像已保存: cuped_variance.png")
    return reduction


def simulate_covariate_selection(n=5000):
    """
    比较不同协变量与 Y 的相关性对 CUPED 缩减效果的影响。
    """
    rhos = np.round(np.arange(0.1, 1.0, 0.1), 2)
    reductions = []

    for rho in rhos:
        x, t, y = generate_data(n, rho=rho, treatment_effect=2.0, sigma=10.0)
        y_cuped, _ = cuped_adjust(y, x)
        var_y = np.var(y, ddof=1)
        var_c = np.var(y_cuped, ddof=1)
        reductions.append((var_y - var_c) / var_y * 100)

    plt.figure(figsize=(8, 5))
    plt.plot(rhos, reductions, marker='o')
    plt.title("协变量与 Y 的相关性对 CUPED 方差缩减的影响")
    plt.xlabel("相关系数 ρ")
    plt.ylabel("方差缩减百分比 (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cuped_covariate_selection.png", dpi=150)
    plt.close()
    print("\n[协变量选择]")
    for rho, red in zip(rhos, reductions):
        print(f"  ρ={rho:.1f} → 方差缩减 {red:.2f}%")
    print("  图像已保存: cuped_covariate_selection.png")


def simulate_multiple_covariates(n=5000):
    """
    演示使用多个协变量时的 CUPED 扩展（多元线性回归残差法）。
    """
    x1 = np.random.normal(100, 10, n)
    x2 = np.random.normal(50, 5, n)
    t = np.random.binomial(1, 0.5, n)
    y = 2.0 * t + 0.8 * x1 + 0.3 * x2 + np.random.normal(0, 5, n)

    # 多元回归残差作为 CUPED 调整
    X = np.column_stack((np.ones(n), x1, x2))
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    y_pred = X.dot(beta)
    residual = y - y_pred
    y_cuped_multi = residual + y.mean()  # 保持均值不变

    var_y = np.var(y, ddof=1)
    var_multi = np.var(y_cuped_multi, ddof=1)
    reduction_multi = (var_y - var_multi) / var_y * 100

    print("\n[多协变量 CUPED]")
    print(f"  原始方差: {var_y:.3f}")
    print(f"  多元 CUPED 后方差: {var_multi:.3f}")
    print(f"  方差缩减: {reduction_multi:.2f}%")


def main():
    print("=" * 50)
    print("CUPED方差缩减 —— 模拟演示")
    print("=" * 50)

    simulate_cuped_variance_reduction(n=5000)
    simulate_covariate_selection(n=5000)
    simulate_multiple_covariates(n=5000)

    print("\n" + "=" * 50)
    print("全部模拟完成。")
    print("=" * 50)


if __name__ == "__main__":
    main()
