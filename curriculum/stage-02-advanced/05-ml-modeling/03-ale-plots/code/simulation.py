"""
ALE (Accumulated Local Effects) 图模拟

演示内容：
- ALE 计算原理
- ALE 与 PDP (Partial Dependence Plot) 对比
- ALE 如何避免相关特征偏差

使用 RandomForest / GradientBoosting 作为黑盒模型。
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_correlated_data(n_samples=2000):
    """
    生成强相关特征数据，用于展示 ALE 的优势。
    X0 与 X1 高度相关，y = X0 + X1 + noise。
    此时 PDP 会因为联合分布变化而产生偏差，而 ALE 更稳健。
    """
    X0 = np.random.randn(n_samples)
    X1 = X0 + np.random.randn(n_samples) * 0.2  # 强相关
    X2 = np.random.randn(n_samples)  # 独立噪声特征
    X = np.column_stack([X0, X1, X2])
    y = X0 + X1 + np.random.randn(n_samples) * 0.3
    feature_names = ['X0 (与X1强相关)', 'X1 (与X0强相关)', 'X2 (独立噪声)']
    return X, y, feature_names


def compute_pdp(model, X, feature_idx, n_grid=50):
    """计算 PDP：在网格点上，将该特征固定为某值，其他特征保持原值，取平均预测。"""
    feat_vals = X[:, feature_idx]
    grid = np.linspace(feat_vals.min(), feat_vals.max(), n_grid)
    pdp = []
    for val in grid:
        X_copy = X.copy()
        X_copy[:, feature_idx] = val
        pdp.append(np.mean(model.predict(X_copy)))
    return grid, np.array(pdp)


def compute_ale(model, X, feature_idx, n_bins=30):
    """
    计算 ALE (一阶)。
    步骤：
    1. 将特征分箱。
    2. 对每个箱，将该特征替换为箱的上下界，计算预测差值。
    3. 对每个箱内的样本差值取平均。
    4. 累加（从最小箱开始），并以箱中心为横坐标。
    5. 中心化 ALE（使均值为 0）。
    """
    feat_vals = X[:, feature_idx]
    bins = np.linspace(feat_vals.min(), feat_vals.max(), n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    ale_deltas = []
    counts = []

    for i in range(n_bins):
        lower = bins[i]
        upper = bins[i + 1]
        mask = (feat_vals >= lower) & (feat_vals < upper)
        if i == n_bins - 1:
            mask = (feat_vals >= lower) & (feat_vals <= upper)
        if mask.sum() == 0:
            ale_deltas.append(0)
            counts.append(0)
            continue

        X_mask = X[mask].copy()
        # 替换为下界和上界
        X_lower = X_mask.copy()
        X_lower[:, feature_idx] = lower
        X_upper = X_mask.copy()
        X_upper[:, feature_idx] = upper

        delta = np.mean(model.predict(X_upper) - model.predict(X_lower))
        ale_deltas.append(delta)
        counts.append(mask.sum())

    ale_deltas = np.array(ale_deltas)
    # 累加
    ale = np.cumsum(ale_deltas)
    # 中心化：减去加权平均
    counts = np.array(counts, dtype=float)
    if counts.sum() > 0:
        ale = ale - np.sum(ale * counts) / np.sum(counts)
    return bin_centers, ale


def demo_ale_vs_pdp(X_train, X_test, y_train, y_test, feature_names):
    """对比 ALE 与 PDP，重点展示相关特征 X0, X1。"""
    model = GradientBoostingRegressor(
        n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42
    )
    model.fit(X_train, y_train)
    print(f"模型测试集 MSE: {np.mean((model.predict(X_test) - y_test) ** 2):.4f}\n")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for idx, ax in enumerate(axes):
        grid_pdp, pdp = compute_pdp(model, X_test, feature_idx=idx, n_grid=50)
        grid_ale, ale = compute_ale(model, X_test, feature_idx=idx, n_bins=30)

        ax.plot(grid_pdp, pdp, label='PDP', color='coral', linewidth=2)
        ax.plot(grid_ale, ale, label='ALE', color='steelblue', linewidth=2)
        ax.set_xlabel(f'{feature_names[idx]} 取值')
        ax.set_ylabel('效应值')
        ax.set_title(f'{feature_names[idx]}: PDP vs ALE')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('ale_vs_pdp.png', dpi=150)
    plt.close()
    print("[ALE vs PDP] 已保存 ale_vs_pdp.png")


def demo_correlated_bias(X, y, feature_names):
    """
    更直观地展示 ALE 如何避免相关特征偏差：
    对 X0 使用 PDP 时，由于 X1 与 X0 相关，PDP 会"拖拽" X1 的分布，
    导致效应估计偏离真实关系 y = X0 + X1。
    ALE 只在局部箱内扰动，保留了联合分布，因此更稳健。
    """
    model = GradientBoostingRegressor(
        n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42
    )
    model.fit(X, y)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for idx, ax in enumerate(axes):
        grid_pdp, pdp = compute_pdp(model, X, feature_idx=idx, n_grid=50)
        grid_ale, ale = compute_ale(model, X, feature_idx=idx, n_bins=30)

        ax.plot(grid_pdp, pdp, label='PDP', color='coral', linewidth=2)
        ax.plot(grid_ale, ale, label='ALE', color='steelblue', linewidth=2)
        # 真实关系：y = X0 + X1，所以对 X0 和 X1 的偏效应都近似为 1 * x
        ax.plot(grid_pdp, grid_pdp, label='真实关系 (y≈x)', color='green',
                linestyle='--', linewidth=1.5)
        ax.set_xlabel(f'{feature_names[idx]} 取值')
        ax.set_ylabel('效应值')
        ax.set_title(f'{feature_names[idx]}: PDP vs ALE (相关特征场景)')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('ale_avoids_correlation_bias.png', dpi=150)
    plt.close()
    print("[相关特征偏差] 已保存 ale_avoids_correlation_bias.png")
    print("  说明：PDP 在特征相关时可能偏离真实关系（绿色虚线），ALE 更接近真实。")


def main():
    print("=" * 60)
    print("ALE 图模拟")
    print("=" * 60)
    X, y, feature_names = generate_correlated_data(n_samples=2000)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    print(f"数据规模: 训练集 {X_train.shape}, 测试集 {X_test.shape}")
    print("特征关系: X1 = X0 + 噪声 (强相关), y = X0 + X1 + 噪声\n")

    demo_ale_vs_pdp(X_train, X_test, y_train, y_test, feature_names)
    print()
    demo_correlated_bias(X, y, feature_names)
    print()
    print("=" * 60)
    print("所有可视化已保存为 PNG 文件。")
    print("=" * 60)


if __name__ == "__main__":
    main()
