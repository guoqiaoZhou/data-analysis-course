"""
XGBoost 核心概念模拟：梯度提升、特征重要性、正则化与过拟合、与单棵决策树对比

本脚本使用 sklearn 的 GradientBoostingRegressor 演示 XGBoost 核心思想：
- 梯度提升（加法模型 + 前向分步）
- 特征重要性
- 过拟合 vs 正则化（max_depth, learning_rate）
- 与单棵决策树的对比
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_data(n_samples=1000):
    """生成带有非线性关系和噪声的模拟数据。"""
    X = np.random.randn(n_samples, 5)
    # y 与 X0, X1 非线性相关，与 X2 线性相关，X3, X4 为噪声特征
    y = (
        3 * X[:, 0] ** 2
        + 2 * np.sin(2 * np.pi * X[:, 1])
        + 1.5 * X[:, 2]
        + np.random.randn(n_samples) * 0.5
    )
    return X, y


def demo_gradient_boosting(X_train, X_test, y_train, y_test):
    """演示梯度提升：逐步增加树的数量，观察训练/测试误差变化。"""
    n_estimators_range = range(1, 301, 5)
    train_errors = []
    test_errors = []

    for n_est in n_estimators_range:
        model = GradientBoostingRegressor(
            n_estimators=n_est,
            max_depth=3,
            learning_rate=0.1,
            random_state=42,
        )
        model.fit(X_train, y_train)
        train_errors.append(mean_squared_error(y_train, model.predict(X_train)))
        test_errors.append(mean_squared_error(y_test, model.predict(X_test)))

    plt.figure(figsize=(10, 6))
    plt.plot(n_estimators_range, train_errors, label='训练集 MSE', color='blue')
    plt.plot(n_estimators_range, test_errors, label='测试集 MSE', color='orange')
    plt.xlabel('树的数量 (n_estimators)')
    plt.ylabel('均方误差 (MSE)')
    plt.title('梯度提升：逐步增加树的数量对误差的影响')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('gradient_boosting_convergence.png', dpi=150)
    plt.close()
    print("[梯度提升] 已保存 gradient_boosting_convergence.png")
    best_n = list(n_estimators_range)[np.argmin(test_errors)]
    print(f"[梯度提升] 测试集 MSE 最小时对应的树数量: {best_n}, 最小 MSE: {min(test_errors):.4f}")


def demo_feature_importance(X_train, y_train):
    """演示特征重要性。"""
    model = GradientBoostingRegressor(
        n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42
    )
    model.fit(X_train, y_train)

    importances = model.feature_importances_
    feature_names = ['X0 (非线性)', 'X1 (正弦)', 'X2 (线性)', 'X3 (噪声)', 'X4 (噪声)']

    plt.figure(figsize=(8, 5))
    bars = plt.bar(feature_names, importances, color='steelblue')
    plt.ylabel('重要性')
    plt.title('梯度提升特征重要性')
    plt.xticks(rotation=15)
    for bar, imp in zip(bars, importances):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                 f'{imp:.3f}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=150)
    plt.close()
    print("[特征重要性] 已保存 feature_importance.png")
    for name, imp in zip(feature_names, importances):
        print(f"  {name}: {imp:.4f}")


def demo_overfitting_vs_regularization(X_train, X_test, y_train, y_test):
    """演示过拟合与正则化：不同 max_depth 和 learning_rate 的效果。"""
    depths = [1, 3, 5, 7, 10]
    lrs = [0.01, 0.1, 0.5]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左图：不同 max_depth
    for depth in depths:
        model = GradientBoostingRegressor(
            n_estimators=200, max_depth=depth, learning_rate=0.1, random_state=42
        )
        model.fit(X_train, y_train)
        train_err = mean_squared_error(y_train, model.predict(X_train))
        test_err = mean_squared_error(y_test, model.predict(X_test))
        axes[0].bar(str(depth), test_err, label=f'depth={depth}')
        print(f"[正则化] max_depth={depth}: 训练 MSE={train_err:.4f}, 测试 MSE={test_err:.4f}")
    axes[0].set_xlabel('max_depth')
    axes[0].set_ylabel('测试集 MSE')
    axes[0].set_title('不同 max_depth 的测试误差')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # 右图：不同 learning_rate
    for lr in lrs:
        model = GradientBoostingRegressor(
            n_estimators=200, max_depth=3, learning_rate=lr, random_state=42
        )
        model.fit(X_train, y_train)
        train_err = mean_squared_error(y_train, model.predict(X_train))
        test_err = mean_squared_error(y_test, model.predict(X_test))
        axes[1].bar(str(lr), test_err, label=f'lr={lr}')
        print(f"[正则化] learning_rate={lr}: 训练 MSE={train_err:.4f}, 测试 MSE={test_err:.4f}")
    axes[1].set_xlabel('learning_rate')
    axes[1].set_ylabel('测试集 MSE')
    axes[1].set_title('不同 learning_rate 的测试误差')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('overfitting_regularization.png', dpi=150)
    plt.close()
    print("[正则化] 已保存 overfitting_regularization.png")


def demo_vs_single_tree(X_train, X_test, y_train, y_test):
    """对比单棵决策树与梯度提升。"""
    single_tree = DecisionTreeRegressor(max_depth=5, random_state=42)
    single_tree.fit(X_train, y_train)

    gbdt = GradientBoostingRegressor(
        n_estimators=200, max_depth=3, learning_rate=0.1, random_state=42
    )
    gbdt.fit(X_train, y_train)

    tree_train_mse = mean_squared_error(y_train, single_tree.predict(X_train))
    tree_test_mse = mean_squared_error(y_test, single_tree.predict(X_test))
    gbdt_train_mse = mean_squared_error(y_train, gbdt.predict(X_train))
    gbdt_test_mse = mean_squared_error(y_test, gbdt.predict(X_test))

    print("[单树 vs GBDT]")
    print(f"  单棵决策树: 训练 MSE={tree_train_mse:.4f}, 测试 MSE={tree_test_mse:.4f}")
    print(f"  梯度提升  : 训练 MSE={gbdt_train_mse:.4f}, 测试 MSE={gbdt_test_mse:.4f}")

    labels = ['单棵决策树', '梯度提升 (GBDT)']
    train_vals = [tree_train_mse, gbdt_train_mse]
    test_vals = [tree_test_mse, gbdt_test_mse]

    x = np.arange(len(labels))
    width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar(x - width / 2, train_vals, width, label='训练集 MSE', color='coral')
    plt.bar(x + width / 2, test_vals, width, label='测试集 MSE', color='seagreen')
    plt.ylabel('MSE')
    plt.title('单棵决策树 vs 梯度提升')
    plt.xticks(x, labels)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5, axis='y')
    plt.tight_layout()
    plt.savefig('tree_vs_gbdt.png', dpi=150)
    plt.close()
    print("[单树 vs GBDT] 已保存 tree_vs_gbdt.png")


def main():
    print("=" * 60)
    print("XGBoost 核心概念模拟")
    print("=" * 60)
    X, y = generate_data(n_samples=1000)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"数据规模: 训练集 {X_train.shape}, 测试集 {X_test.shape}\n")

    demo_gradient_boosting(X_train, X_test, y_train, y_test)
    print()
    demo_feature_importance(X_train, y_train)
    print()
    demo_overfitting_vs_regularization(X_train, X_test, y_train, y_test)
    print()
    demo_vs_single_tree(X_train, X_test, y_train, y_test)
    print()
    print("=" * 60)
    print("所有可视化已保存为 PNG 文件。")
    print("=" * 60)


if __name__ == "__main__":
    main()
