"""
SHAP 交互效应模拟

演示内容：
- 交互值概念
- 主效应 vs 交互效应分解
- 使用已知交互模型 Y = X1 * X2 + noise
- 可视化交互强度

由于 shap 库未安装，使用基于排列的近似方法估计主效应和交互效应。
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_interaction_data(n_samples=1500):
    """
    生成带有已知交互效应的数据：
    y = X0 * X1 + 0.5 * X2 + noise
    其中 X0*X1 是强交互项。
    """
    X = np.random.randn(n_samples, 4)
    y = X[:, 0] * X[:, 1] + 0.5 * X[:, 2] + np.random.randn(n_samples) * 0.3
    feature_names = ['X0', 'X1', 'X2', 'X3 (噪声)']
    return X, y, feature_names


def approximate_main_effect(model, X, feature_idx, n_permutations=5):
    """
    近似主效应：固定该特征为某值，其他特征随机打乱，预测变化。
    这里简化为：该特征单独排列时的平均预测变化绝对值。
    """
    base_pred = model.predict(X)
    diffs = []
    for _ in range(n_permutations):
        X_perm = X.copy()
        perm_idx = np.random.permutation(X.shape[0])
        X_perm[:, feature_idx] = X_perm[perm_idx, feature_idx]
        diffs.append(np.abs(base_pred - model.predict(X_perm)))
    return np.mean(diffs, axis=0)


def approximate_interaction_effect(model, X, i, j, n_samples=500):
    """
    近似交互效应：
    思路来自 Friedman 的 H-statistic 简化版：
    同时固定特征 i 和 j 为某值，与单独固定相比，预测差异。
    这里使用更简化的方式：同时打乱 i 和 j，与单独打乱 i、单独打乱 j 的预测变化比较。
    interaction_strength = mean(|Δ_{ij} - Δ_i - Δ_j|)
    """
    base_pred = model.predict(X)
    idx = np.random.choice(X.shape[0], size=min(n_samples, X.shape[0]), replace=False)
    X_sub = X[idx]
    base_sub = base_pred[idx]

    def permute(feat):
        Xp = X_sub.copy()
        perm = np.random.permutation(Xp.shape[0])
        Xp[:, feat] = Xp[perm, feat]
        return np.abs(base_sub - model.predict(Xp))

    # 多次采样取平均
    delta_i_list, delta_j_list, delta_ij_list = [], [], []
    for _ in range(5):
        delta_i_list.append(permute(i))
        delta_j_list.append(permute(j))
        Xp = X_sub.copy()
        perm = np.random.permutation(Xp.shape[0])
        Xp[:, i] = Xp[perm, i]
        perm = np.random.permutation(Xp.shape[0])
        Xp[:, j] = Xp[perm, j]
        delta_ij_list.append(np.abs(base_sub - model.predict(Xp)))

    delta_i = np.mean(delta_i_list, axis=0)
    delta_j = np.mean(delta_j_list, axis=0)
    delta_ij = np.mean(delta_ij_list, axis=0)

    interaction = np.mean(np.abs(delta_ij - delta_i - delta_j))
    return interaction


def demo_interaction_heatmap(model, X, feature_names):
    """绘制特征交互强度热力图。"""
    n_features = len(feature_names)
    interaction_matrix = np.zeros((n_features, n_features))

    print("正在计算交互效应矩阵 (采样加速)...")
    for i in range(n_features):
        for j in range(i + 1, n_features):
            strength = approximate_interaction_effect(model, X, i, j, n_samples=400)
            interaction_matrix[i, j] = strength
            interaction_matrix[j, i] = strength
            print(f"  {feature_names[i]} x {feature_names[j]}: {strength:.4f}")

    plt.figure(figsize=(7, 6))
    im = plt.imshow(interaction_matrix, cmap='YlOrRd', aspect='auto')
    plt.colorbar(im, label='交互强度')
    plt.xticks(range(n_features), feature_names, rotation=45, ha='right')
    plt.yticks(range(n_features), feature_names)
    plt.title('特征交互强度热力图 (近似)')
    # 标注数值
    for i in range(n_features):
        for j in range(n_features):
            if i != j:
                plt.text(j, i, f'{interaction_matrix[i, j]:.2f}',
                         ha='center', va='center', color='black', fontsize=10)
    plt.tight_layout()
    plt.savefig('interaction_heatmap.png', dpi=150)
    plt.close()
    print("[交互热力图] 已保存 interaction_heatmap.png")


def demo_main_vs_interaction(model, X, y, feature_names):
    """
    展示主效应 vs 交互效应分解：
    对 X0 和 X1 绘制联合 PDP 风格的网格，观察交互形状。
    """
    n_grid = 30
    x0_vals = np.linspace(X[:, 0].min(), X[:, 0].max(), n_grid)
    x1_vals = np.linspace(X[:, 1].min(), X[:, 1].max(), n_grid)
    grid_pred = np.zeros((n_grid, n_grid))

    # 使用训练集分布的中位数作为其他特征的固定值
    median_x = np.median(X, axis=0)

    for i, x0 in enumerate(x0_vals):
        for j, x1 in enumerate(x1_vals):
            sample = median_x.copy()
            sample[0] = x0
            sample[1] = x1
            grid_pred[j, i] = model.predict(sample.reshape(1, -1))[0]

    plt.figure(figsize=(8, 6))
    contour = plt.contourf(x0_vals, x1_vals, grid_pred, levels=20, cmap='viridis')
    plt.colorbar(contour, label='预测值')
    plt.xlabel('X0')
    plt.ylabel('X1')
    plt.title('X0 与 X1 的联合效应 (预测面)')
    plt.tight_layout()
    plt.savefig('main_vs_interaction_surface.png', dpi=150)
    plt.close()
    print("[主效应 vs 交互效应] 已保存 main_vs_interaction_surface.png")
    print("  观察：若交互强，预测面会呈现明显的非平行等高线（如对角线趋势）。")


def main():
    print("=" * 60)
    print("SHAP 交互效应模拟")
    print("=" * 60)
    X, y, feature_names = generate_interaction_data(n_samples=1500)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(
        n_estimators=150, max_depth=4, learning_rate=0.1, random_state=42
    )
    model.fit(X_train, y_train)
    print(f"模型测试集 MSE: {mean_squared_error(y_test, model.predict(X_test)):.4f}")
    print(f"真实关系: y = X0 * X1 + 0.5*X2 + noise\n")

    demo_interaction_heatmap(model, X_test, feature_names)
    print()
    demo_main_vs_interaction(model, X_test, y_test, feature_names)
    print()
    print("=" * 60)
    print("所有可视化已保存为 PNG 文件。")
    print("=" * 60)


if __name__ == "__main__":
    main()
