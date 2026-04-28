"""
卡方检验 (Chi-square test) 模拟演示

本脚本演示卡方独立性检验：
- 检验两个分类变量是否独立
- 计算期望频数 (expected frequencies)
- 比较观测频数与期望频数的差异
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 中文支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def demo_chi2_independence():
    """构造列联表并进行卡方独立性检验。"""
    # 构造一个 2x3 列联表（例如：性别 vs 产品偏好）
    observed = np.array([
        [30, 45, 25],   # 男性
        [20, 35, 45],   # 女性
    ])
    row_labels = ['男性', '女性']
    col_labels = ['产品A', '产品B', '产品C']

    chi2, p, dof, expected = stats.chi2_contingency(observed)

    print("=" * 50)
    print("【卡方独立性检验】")
    print("列联表（观测频数）：")
    print(f"{'':>6}", end='')
    for c in col_labels:
        print(f"{c:>8}", end='')
    print()
    for i, r in enumerate(row_labels):
        print(f"{r:>6}", end='')
        for j in range(len(col_labels)):
            print(f"{observed[i, j]:>8}", end='')
        print()

    print("\n期望频数：")
    print(f"{'':>6}", end='')
    for c in col_labels:
        print(f"{c:>8}", end='')
    print()
    for i, r in enumerate(row_labels):
        print(f"{r:>6}", end='')
        for j in range(len(col_labels)):
            print(f"{expected[i, j]:>8.2f}", end='')
        print()

    print(f"\n卡方统计量 = {chi2:.3f}")
    print(f"自由度 df = {dof}")
    print(f"p 值 = {p:.4f}")
    if p < 0.05:
        print("结论：在 α=0.05 水平下拒绝原假设，两个变量不独立，存在关联。")
    else:
        print("结论：在 α=0.05 水平下不拒绝原假设，两个变量独立。")
    print()
    return observed, expected, chi2, p, row_labels, col_labels


def visualize_chi2(observed, expected, row_labels, col_labels):
    """绘制观测频数与期望频数的对比热图。"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    for ax, data, title in zip(axes, [observed, expected], ['观测频数', '期望频数']):
        im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
        ax.set_xticks(np.arange(len(col_labels)))
        ax.set_yticks(np.arange(len(row_labels)))
        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels)
        ax.set_title(title)
        for i in range(len(row_labels)):
            for j in range(len(col_labels)):
                text = f"{data[i, j]:.1f}" if isinstance(data[i, j], float) else f"{data[i, j]}"
                ax.text(j, i, text, ha='center', va='center', color='black', fontsize=12)
        fig.colorbar(im, ax=ax)

    plt.tight_layout()
    plt.savefig('chi_square_simulation.png', dpi=150)
    plt.close()
    print("可视化已保存为 chi_square_simulation.png")


if __name__ == "__main__":
    observed, expected, chi2, p, row_labels, col_labels = demo_chi2_independence()
    visualize_chi2(observed, expected, row_labels, col_labels)
