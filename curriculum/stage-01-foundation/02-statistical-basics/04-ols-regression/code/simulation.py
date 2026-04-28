"""
OLS 回归 (Ordinary Least Squares) 模拟演示

本脚本演示：
1. 简单线性回归：建立 y = β0 + β1 * x + ε 模型
2. 系数解释：截距与斜率的含义
3. R-squared：模型解释力
4. 残差分析：检验模型假设
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_data(n=100, beta0=2.0, beta1=3.5, noise_std=5.0):
    """生成模拟数据：y = β0 + β1*x + ε"""
    x = np.random.uniform(0, 10, size=n)
    epsilon = np.random.normal(0, noise_std, size=n)
    y = beta0 + beta1 * x + epsilon
    return x, y, beta0, beta1


def ols_fit(x, y):
    """手动实现 OLS 估计（也可用 np.polyfit 或 sklearn）。"""
    x_mean, y_mean = x.mean(), y.mean()
    beta1 = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    beta0 = y_mean - beta1 * x_mean
    y_pred = beta0 + beta1 * x
    residuals = y - y_pred
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y - y_mean) ** 2)
    r_squared = 1 - ss_res / ss_tot
    return beta0, beta1, y_pred, residuals, r_squared


def demo_ols_regression():
    """演示 OLS 回归的估计与解释。"""
    x, y, true_beta0, true_beta1 = generate_data(n=100, beta0=2.0, beta1=3.5, noise_std=5.0)
    beta0_est, beta1_est, y_pred, residuals, r_squared = ols_fit(x, y)

    # 使用 scipy 进行显著性检验
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    print("=" * 50)
    print("【OLS 简单线性回归】")
    print(f"真实模型：y = {true_beta0} + {true_beta1} * x + ε")
    print(f"估计模型：y = {beta0_est:.3f} + {beta1_est:.3f} * x")
    print(f"截距 (β0) = {beta0_est:.3f}，表示 x=0 时 y 的期望值")
    print(f"斜率 (β1) = {beta1_est:.3f}，表示 x 每增加 1 单位，y 平均变化 {beta1_est:.3f}")
    print(f"R² = {r_squared:.3f}，说明模型解释了 {r_squared*100:.1f}% 的 y 变异")
    print(f"斜率显著性检验 p 值 = {p_value:.4f}")
    if p_value < 0.05:
        print("结论：斜率显著不为零，x 对 y 有显著线性影响。")
    else:
        print("结论：斜率不显著，x 对 y 的线性影响证据不足。")
    print()
    return x, y, y_pred, residuals, r_squared, beta0_est, beta1_est


def visualize_regression(x, y, y_pred, residuals, r_squared, beta0_est, beta1_est):
    """绘制回归线、残差图。"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # 散点图 + 回归线
    ax = axes[0]
    ax.scatter(x, y, color='steelblue', alpha=0.6, edgecolors='black', label='观测值')
    ax.plot(x, y_pred, color='red', linewidth=2, label='OLS 回归线')
    ax.set_title(f'简单线性回归 (R²={r_squared:.3f})')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()

    # 残差图
    ax = axes[1]
    ax.scatter(y_pred, residuals, color='coral', alpha=0.6, edgecolors='black')
    ax.axhline(0, color='black', linestyle='--', linewidth=1)
    ax.set_title('残差图 (Residuals vs Fitted)')
    ax.set_xlabel('拟合值')
    ax.set_ylabel('残差')

    plt.tight_layout()
    plt.savefig('ols_regression_simulation.png', dpi=150)
    plt.close()
    print("可视化已保存为 ols_regression_simulation.png")


if __name__ == "__main__":
    x, y, y_pred, residuals, r_squared, beta0_est, beta1_est = demo_ols_regression()
    visualize_regression(x, y, y_pred, residuals, r_squared, beta0_est, beta1_est)
