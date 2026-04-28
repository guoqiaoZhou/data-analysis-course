"""
GBDT + LR (Facebook 方法) 模拟

演示内容：
- GBDT 特征转换：将样本映射到每棵树的叶子节点索引
- 使用叶子索引作为 one-hot 特征训练逻辑回归
- 对比 GBDT 单独、LR 单独、GBDT+LR 的 AUC
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_classification_data(n_samples=5000):
    """
    生成分类数据，包含非线性交互：
    y = 1 if (X0 * X1 + 0.5 * X2) > 0 else 0, 加噪声
    """
    X = np.random.randn(n_samples, 5)
    score = X[:, 0] * X[:, 1] + 0.5 * X[:, 2]
    prob = 1 / (1 + np.exp(-score))
    y = (np.random.rand(n_samples) < prob).astype(int)
    return X, y


def gbdt_leaf_features(gbdt, X, fitted_encoders=None):
    """
    将 GBDT 的叶子节点索引转换为 one-hot 特征矩阵。
    返回 shape: (n_samples, total_n_leaves)
    如果 fitted_encoders 为 None，则基于 X 训练编码器并返回；
    否则使用已拟合的编码器进行转换。
    """
    leaf_indices = gbdt.apply(X)  # shape: (n_samples, n_estimators)
    encoded_parts = []
    return_encoders = fitted_encoders is None
    if return_encoders:
        fitted_encoders = []

    for i in range(leaf_indices.shape[1]):
        col = leaf_indices[:, i].reshape(-1, 1)
        if return_encoders:
            enc = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            enc.fit(col)
            fitted_encoders.append(enc)
        else:
            enc = fitted_encoders[i]
        encoded_parts.append(enc.transform(col))

    result = np.hstack(encoded_parts)
    if return_encoders:
        return result, fitted_encoders
    return result


def demo_gbdt_lr_pipeline(X_train, X_test, y_train, y_test):
    """训练并对比三种模型：GBDT 单独、LR 单独、GBDT+LR。"""
    # 1. GBDT 单独
    gbdt = GradientBoostingClassifier(
        n_estimators=50, max_depth=3, learning_rate=0.1, random_state=42
    )
    gbdt.fit(X_train, y_train)
    gbdt_proba = gbdt.predict_proba(X_test)[:, 1]
    gbdt_auc = roc_auc_score(y_test, gbdt_proba)
    print(f"[GBDT 单独] AUC: {gbdt_auc:.4f}")

    # 2. LR 单独（原始特征）
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    lr_proba = lr.predict_proba(X_test)[:, 1]
    lr_auc = roc_auc_score(y_test, lr_proba)
    print(f"[LR 单独]   AUC: {lr_auc:.4f}")

    # 3. GBDT + LR
    # 使用 GBDT 的叶子索引作为新特征
    X_train_leaf, leaf_encoders = gbdt_leaf_features(gbdt, X_train)
    X_test_leaf = gbdt_leaf_features(gbdt, X_test, fitted_encoders=leaf_encoders)
    print(f"[GBDT+LR]   叶子特征维度: {X_train_leaf.shape[1]}")

    lr_on_leaf = LogisticRegression(max_iter=1000, random_state=42)
    lr_on_leaf.fit(X_train_leaf, y_train)
    gbdt_lr_proba = lr_on_leaf.predict_proba(X_test_leaf)[:, 1]
    gbdt_lr_auc = roc_auc_score(y_test, gbdt_lr_proba)
    print(f"[GBDT+LR]   AUC: {gbdt_lr_auc:.4f}")

    return gbdt_proba, lr_proba, gbdt_lr_proba, gbdt_auc, lr_auc, gbdt_lr_auc


def plot_auc_comparison(auc_values):
    """绘制 AUC 柱状图对比。"""
    labels = ['GBDT 单独', 'LR 单独', 'GBDT + LR']
    colors = ['coral', 'seagreen', 'steelblue']

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, auc_values, color=colors)
    plt.ylabel('AUC')
    plt.title('模型 AUC 对比')
    plt.ylim(0.5, 1.0)
    for bar, val in zip(bars, auc_values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                 f'{val:.4f}', ha='center', va='bottom', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5, axis='y')
    plt.tight_layout()
    plt.savefig('auc_comparison.png', dpi=150)
    plt.close()
    print("[AUC 对比] 已保存 auc_comparison.png")


def plot_roc_curves(y_test, gbdt_proba, lr_proba, gbdt_lr_proba, auc_values):
    """绘制 ROC 曲线对比。"""
    plt.figure(figsize=(8, 6))
    for proba, label, auc_val in zip(
        [gbdt_proba, lr_proba, gbdt_lr_proba],
        ['GBDT 单独', 'LR 单独', 'GBDT + LR'],
        auc_values
    ):
        fpr, tpr, _ = roc_curve(y_test, proba)
        plt.plot(fpr, tpr, label=f'{label} (AUC={auc_val:.4f})', linewidth=2)

    plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='随机猜测')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC 曲线对比')
    plt.legend(loc='lower right')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('roc_curves.png', dpi=150)
    plt.close()
    print("[ROC 曲线] 已保存 roc_curves.png")


def main():
    print("=" * 60)
    print("GBDT + LR (Facebook 方法) 模拟")
    print("=" * 60)
    X, y = generate_classification_data(n_samples=5000)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"数据规模: 训练集 {X_train.shape}, 测试集 {X_test.shape}")
    print(f"正样本比例: {y.mean():.2%}\n")

    gbdt_proba, lr_proba, gbdt_lr_proba, gbdt_auc, lr_auc, gbdt_lr_auc = \
        demo_gbdt_lr_pipeline(X_train, X_test, y_train, y_test)
    print()

    auc_values = [gbdt_auc, lr_auc, gbdt_lr_auc]
    plot_auc_comparison(auc_values)
    plot_roc_curves(y_test, gbdt_proba, lr_proba, gbdt_lr_proba, auc_values)
    print()
    print("=" * 60)
    print("所有可视化已保存为 PNG 文件。")
    print("=" * 60)


if __name__ == "__main__":
    main()
