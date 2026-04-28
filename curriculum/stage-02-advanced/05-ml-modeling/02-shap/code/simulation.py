"""
SHAP 值模拟：全局重要性、局部解释、SHAP 小提琴图

由于 shap 库未安装，本脚本使用基于特征排列的近似 SHAP 方法：
对每个特征，将其值随机打乱后测量预测变化，作为该特征对预测的影响估计。
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_data(n_samples=1000):
    """生成模拟数据，y 与 X0, X1, X2 相关，X3, X4 为噪声。"""
    X = np.random.randn(n_samples, 5)
    y = (
        3 * X[:, 0] ** 2
        + 2 * np.sin(2 * np.pi * X[:, 1])
        + 1.5 * X[:, 2]
        + np.random.randn(n_samples) * 0.5
    )
    feature_names = ['X0 (非线性)', 'X1 (正弦)', 'X2 (线性)', 'X3 (噪声)', 'X4 (噪声)']
    return X, y, feature_names


def approximate_shap_values(model, X, n_permutations=3):
    """
    使用特征排列法近似 SHAP 值。
    对每个样本、每个特征，随机打乱该特征的值，观察预测变化。
    返回 shape 为 (n_samples, n_features) 的近似 SHAP 矩阵。
    """
    base_pred = model.predict(X)
    n_samples, n_features = X.shape
    shap_matrix = np.zeros((n_samples, n_features))

    for feat in range(n_features):
        diffs = []
        for _ in range(n_permutations):
            X_perm = X.copy()
            # 随机打乱该列
            perm_idx = np.random.permutation(n_samples)
            X_perm[:, feat] = X_perm[perm_idx, feat]
            perm_pred = model.predict(X_perm)
            diffs.append(base_pred - perm_pred)
        # 平均多次排列的结果
        shap_matrix[:, feat] = np.mean(diffs, axis=0)
    return shap_matrix


def demo_global_importance(shap_matrix, feature_names):
    """全局重要性：各特征平均绝对 SHAP 值。"""
    mean_abs_shap = np.mean(np.abs(shap_matrix), axis=0)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(feature_names, mean_abs_shap, color='steelblue')
    plt.ylabel('平均绝对 SHAP 值')
    plt.title('SHAP 全局特征重要性 (近似)')
    plt.xticks(rotation=15)
    for bar, val in zip(bars, mean_abs_shap):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.savefig('shap_global_importance.png', dpi=150)
    plt.close()
    print("[全局重要性] 已保存 shap_global_importance.png")
    for name, val in zip(feature_names, mean_abs_shap):
        print(f"  {name}: {val:.4f}")


def demo_local_explanation(shap_matrix, feature_names, y_pred, sample_idx=0):
    """局部解释：单个样本的 SHAP 值瀑布图概念（用水平条形图展示）。"""
    shap_vals = shap_matrix[sample_idx]
    # 按绝对值排序，便于阅读
    order = np.argsort(np.abs(shap_vals))[::-1]

    plt.figure(figsize=(8, 5))
    colors = ['green' if v > 0 else 'red' for v in shap_vals[order]]
    bars = plt.barh(np.array(feature_names)[order], shap_vals[order], color=colors)
    plt.axvline(x=0, color='black', linewidth=0.8)
    plt.xlabel('SHAP 值 (近似)')
    plt.title(f'样本 {sample_idx} 的局部解释 (预测值={y_pred[sample_idx]:.2f})')
    plt.gca().invert_yaxis()
    for bar, val in zip(bars, shap_vals[order]):
        plt.text(val, bar.get_y() + bar.get_height() / 2,
                 f'{val:.2f}', ha='left' if val > 0 else 'right', va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig('shap_local_explanation.png', dpi=150)
    plt.close()
    print(f"[局部解释] 已保存 shap_local_explanation.png (样本 {sample_idx})")
    print(f"  样本 {sample_idx} 预测值: {y_pred[sample_idx]:.4f}")
    for f, v in zip(np.array(feature_names)[order], shap_vals[order]):
        direction = "增加" if v > 0 else "降低"
        print(f"    {f}: {v:+.4f} ({direction}预测)")


def demo_shap_violin(shap_matrix, feature_names):
    """SHAP 小提琴图概念：展示各特征 SHAP 值的分布。"""
    fig, axes = plt.subplots(1, len(feature_names), figsize=(14, 5), sharey=True)

    for idx, (ax, name) in enumerate(zip(axes, feature_names)):
        data = shap_matrix[:, idx]
        # 绘制小提琴风格的分布：用 hist + KDE 近似
        ax.hist(data, bins=30, orientation='horizontal', color='steelblue', alpha=0.6, density=True)
        # 叠加箱线图元素
        parts = ax.violinplot(data, positions=[0], vert=False, widths=0.7,
                              showmeans=False, showmedians=True, showextrema=False)
        for pc in parts['bodies']:
            pc.set_facecolor('lightblue')
            pc.set_alpha(0.7)
        ax.set_xlabel('密度')
        ax.set_title(name, fontsize=10)
        ax.axvline(x=0, color='black', linewidth=0.8)
        # 隐藏 y 轴刻度
        ax.set_yticks([])

    plt.suptitle('SHAP 值分布 (近似小提琴图)', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('shap_violin_plot.png', dpi=150)
    plt.close()
    print("[SHAP 小提琴图] 已保存 shap_violin_plot.png")


def main():
    print("=" * 60)
    print("SHAP 值模拟 (近似实现)")
    print("=" * 60)
    X, y, feature_names = generate_data(n_samples=1000)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(
        n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42
    )
    model.fit(X_train, y_train)
    print(f"模型测试集 MSE: {mean_squared_error(y_test, model.predict(X_test)):.4f}\n")

    print("正在计算近似 SHAP 值 (特征排列法，请稍候)...")
    shap_matrix = approximate_shap_values(model, X_test, n_permutations=5)
    y_pred = model.predict(X_test)
    print(f"SHAP 矩阵形状: {shap_matrix.shape}\n")

    demo_global_importance(shap_matrix, feature_names)
    print()
    demo_local_explanation(shap_matrix, feature_names, y_pred, sample_idx=0)
    print()
    demo_shap_violin(shap_matrix, feature_names)
    print()
    print("=" * 60)
    print("所有可视化已保存为 PNG 文件。")
    print("=" * 60)


if __name__ == "__main__":
    main()
