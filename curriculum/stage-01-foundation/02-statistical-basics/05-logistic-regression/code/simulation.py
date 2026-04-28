"""
Logistic 回归模拟演示

本脚本演示：
1. Logistic 回归模型拟合
2. 优势比 (Odds Ratio, OR) 解释
3. 预测概率
4. 混淆矩阵 (Confusion Matrix) 与分类效果评估
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_logistic_data(n=200, beta0=-3.0, beta1=0.8):
    """生成二分类数据。"""
    x = np.random.normal(loc=5, scale=2, size=n)
    logit = beta0 + beta1 * x
    prob = 1 / (1 + np.exp(-logit))
    y = (np.random.uniform(size=n) < prob).astype(int)
    return x.reshape(-1, 1), y, beta0, beta1


def demo_logistic_regression():
    """演示 Logistic 回归。"""
    X, y, true_beta0, true_beta1 = generate_logistic_data(n=200, beta0=-3.0, beta1=0.8)

    model = LogisticRegression(solver='lbfgs')
    model.fit(X, y)

    beta0_est = model.intercept_[0]
    beta1_est = model.coef_[0][0]
    odds_ratio = np.exp(beta1_est)

    print("=" * 50)
    print("【Logistic 回归】")
    print(f"真实模型：logit(p) = {true_beta0} + {true_beta1} * x")
    print(f"估计模型：logit(p) = {beta0_est:.3f} + {beta1_est:.3f} * x")
    print(f"优势比 OR = exp(β1) = {odds_ratio:.3f}")
    print(f"解释：x 每增加 1 单位，事件发生 odds 变为原来的 {odds_ratio:.3f} 倍")
    print()

    # 预测概率
    x_range = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)
    prob_pred = model.predict_proba(x_range)[:, 1]

    # 混淆矩阵
    y_pred = model.predict(X)
    cm = confusion_matrix(y, y_pred)
    acc = accuracy_score(y, y_pred)

    print("【分类效果评估】")
    print(f"混淆矩阵：")
    print(f"                 预测=0   预测=1")
    print(f"实际=0    {cm[0, 0]:>8} {cm[0, 1]:>8}")
    print(f"实际=1    {cm[1, 0]:>8} {cm[1, 1]:>8}")
    print(f"准确率 Accuracy = {acc:.3f}")
    print()

    return X, y, x_range, prob_pred, cm, acc, beta0_est, beta1_est


def visualize_logistic(X, y, x_range, prob_pred, cm, acc):
    """绘制 Logistic 回归的散点图、概率曲线与混淆矩阵热图。"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # 散点 + Sigmoid 曲线
    ax = axes[0]
    ax.scatter(X[y == 0], y[y == 0], color='blue', alpha=0.5, label='y=0', edgecolors='black')
    ax.scatter(X[y == 1], y[y == 1], color='red', alpha=0.5, label='y=1', edgecolors='black')
    ax.plot(x_range, prob_pred, color='green', linewidth=2, label='预测概率')
    ax.axhline(0.5, color='gray', linestyle='--', linewidth=1)
    ax.set_title('Logistic 回归：预测概率曲线')
    ax.set_xlabel('x')
    ax.set_ylabel('概率 / 类别')
    ax.legend()

    # 混淆矩阵热图
    ax = axes[1]
    im = ax.imshow(cm, cmap='Blues', aspect='auto')
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['预测=0', '预测=1'])
    ax.set_yticklabels(['实际=0', '实际=1'])
    ax.set_title(f'混淆矩阵 (Accuracy={acc:.3f})')
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha='center', va='center', color='black', fontsize=14)
    fig.colorbar(im, ax=ax)

    plt.tight_layout()
    plt.savefig('logistic_regression_simulation.png', dpi=150)
    plt.close()
    print("可视化已保存为 logistic_regression_simulation.png")


if __name__ == "__main__":
    X, y, x_range, prob_pred, cm, acc, beta0_est, beta1_est = demo_logistic_regression()
    visualize_logistic(X, y, x_range, prob_pred, cm, acc)
