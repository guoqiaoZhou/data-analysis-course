# Python 代码示例：观察性数据的挑战

"""
本代码演示观察性数据中的核心挑战：
1. 混杂变量（Confounding）导致的偏误
2. 碰撞变量（Collider）引入的虚假关联
3. 控制变量选择的后果：该控的没控 vs 不该控的控了
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 设置中文字体（macOS 系统字体）
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
np.random.seed(42)


def scenario_confounding(n=2000):
    """场景1：混杂变量 —— 该控的没控"""
    print("=" * 60)
    print("场景1：混杂变量（Confounding）")
    print("=" * 60)

    # Z 是混杂变量：同时影响 D 和 Y
    Z = np.random.normal(0, 1, n)

    # D 依赖于 Z
    prob_D = 1 / (1 + np.exp(-(0.5 * Z)))
    D = np.random.binomial(1, prob_D)

    # Y 依赖于 D 和 Z（真实效应 = 2.0）
    Y = 2.0 * D + 1.5 * Z + np.random.normal(0, 1, n)

    # Naive 估计（不控制 Z）
    ate_naive = np.mean(Y[D == 1]) - np.mean(Y[D == 0])

    # 回归调整（控制 Z）
    X_reg = np.column_stack([D, Z])
    model = LinearRegression().fit(X_reg, Y)
    ate_adjusted = model.coef_[0]

    print(f"真实处理效应: 2.000")
    print(f"Naive 估计（不控Z）: {ate_naive:.3f} ← 偏误!")
    print(f"回归调整（控制Z）: {ate_adjusted:.3f} ← 无偏")
    print(f"\n偏误分解：")
    print(f"  总偏误 = {ate_naive - 2.0:.3f}")
    print(f"  说明：Z同时影响D和Y，不控制Z时估计混杂了Z→Y的路径")

    return D, Y, Z, ate_naive, ate_adjusted


def scenario_collider(n=2000):
    """场景2：碰撞变量 —— 不该控的控了"""
    print("\n" + "=" * 60)
    print("场景2：碰撞变量（Collider）")
    print("=" * 60)

    # D 和 Y 独立（真实效应 = 0）
    D = np.random.binomial(1, 0.5, n)
    Y = np.random.normal(0, 1, n)  # Y 不依赖 D

    # C 是碰撞变量：被 D 和 Y 共同影响
    # C = 1 当且仅当 D=1 或 Y>0（入选精英项目：需要技能或努力）
    C = ((D == 1) | (Y > 0)).astype(int)

    # 无条件估计（正确）
    ate_unconditional = np.mean(Y[D == 1]) - np.mean(Y[D == 0])

    # 控制碰撞变量 C（错误！）
    mask_c1 = C == 1
    if np.sum(D[mask_c1] == 1) > 0 and np.sum(D[mask_c1] == 0) > 0:
        ate_collider = np.mean(Y[mask_c1 & (D == 1)]) - np.mean(Y[mask_c1 & (D == 0)])
    else:
        ate_collider = np.nan

    print(f"真实处理效应: 0.000（D 和 Y 独立）")
    print(f"无条件估计: {ate_unconditional:.3f} ← 正确")
    print(f"控制碰撞变量C后: {ate_collider:.3f} ← 虚假关联!")
    print(f"\n解释：C = D OR Y>0，控制C=1时，D=0意味着Y必须>0才能入选")
    print(f"      这创造了D和Y之间的负相关——原本不存在的关联")

    return D, Y, C, ate_unconditional, ate_collider


def scenario_mediator(n=2000):
    """场景3：中介变量 —— 过度控制阻断因果路径"""
    print("\n" + "=" * 60)
    print("场景3：中介变量（Mediator）—— 过度控制")
    print("=" * 60)

    # D -> M -> Y，直接效应 = 1.0，通过 M 的间接效应 = 1.5
    D = np.random.binomial(1, 0.5, n)
    M = 1.5 * D + np.random.normal(0, 0.5, n)  # 中介
    Y = 1.0 * D + 1.0 * M + np.random.normal(0, 1, n)  # 总效应 = 2.5

    # 总效应估计（不控制 M）
    ate_total = np.mean(Y[D == 1]) - np.mean(Y[D == 0])

    # 直接效应估计（控制 M）
    X_reg = np.column_stack([D, M])
    model = LinearRegression().fit(X_reg, Y)
    ate_direct = model.coef_[0]

    print(f"真实总效应（D→Y）: 2.500")
    print(f"真实直接效应（D→Y, 不经过M）: 1.000")
    print(f"Naive 估计（不控M）: {ate_total:.3f} ← 总效应")
    print(f"控制中介M后: {ate_direct:.3f} ← 只剩直接效应")
    print(f"\n说明：控制中介变量会阻断因果路径，导致低估总效应")
    print(f"      若目标是总效应，不应控制中介；若目标是直接效应，才控制中介")

    return D, Y, M, ate_total, ate_direct


def visualize_confounding(D, Y, Z, ate_naive, ate_adjusted):
    """可视化：混杂变量的影响"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 左图：Y vs D，按 Z 分层
    ax = axes[0]
    z_bins = np.percentile(Z, [0, 33, 66, 100])
    colors = ['blue', 'green', 'red']
    labels = ['Z 低分位', 'Z 中分位', 'Z 高分位']

    for i in range(3):
        mask = (Z >= z_bins[i]) & (Z < z_bins[i + 1])
        mean_treat = np.mean(Y[mask & (D == 1)])
        mean_control = np.mean(Y[mask & (D == 0)])
        ax.bar([i * 2 - 0.2], [mean_control], width=0.35, color=colors[i], alpha=0.5, label=f'{labels[i]} 对照')
        ax.bar([i * 2 + 0.2], [mean_treat], width=0.35, color=colors[i], alpha=0.8, label=f'{labels[i]} 处理')

    ax.axhline(y=ate_naive + np.mean(Y[D == 0]), color='gray', linestyle='--',
               label=f'Naive 估计差异 = {ate_naive:.2f}')
    ax.set_xticks([0, 2, 4])
    ax.set_xticklabels(labels)
    ax.set_ylabel('Y 的均值')
    ax.set_title('混杂变量：按 Z 分层后，处理效应一致')
    ax.legend(fontsize=8)

    # 右图：D 和 Y 的分布随 Z 变化
    ax = axes[1]
    ax.scatter(Z[D == 0], Y[D == 0], alpha=0.3, label='对照组', s=10)
    ax.scatter(Z[D == 1], Y[D == 1], alpha=0.3, label='处理组', s=10)

    # 拟合线
    z_range = np.linspace(Z.min(), Z.max(), 100)
    for d, color in [(0, 'blue'), (1, 'orange')]:
        mask = D == d
        model = LinearRegression().fit(Z[mask].reshape(-1, 1), Y[mask])
        y_pred = model.predict(z_range.reshape(-1, 1))
        ax.plot(z_range, y_pred, color=color, linewidth=2, label=f'D={d} 回归线')

    ax.set_xlabel('混杂变量 Z')
    ax.set_ylabel('结果 Y')
    ax.set_title('控制 Z 后，两条回归线平行（处理效应恒定）')
    ax.legend()

    plt.tight_layout()
    plt.savefig('observational_challenges_confounding.png', dpi=150)
    print("\n可视化已保存至 observational_challenges_confounding.png")


def visualize_collider(D, Y, C):
    """可视化：碰撞变量的虚假关联"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 左图：无条件时 D 和 Y 独立
    ax = axes[0]
    ax.hist(Y[D == 0], bins=30, alpha=0.5, label='D=0')
    ax.hist(Y[D == 1], bins=30, alpha=0.5, label='D=1')
    ax.set_xlabel('Y')
    ax.set_ylabel('频数')
    ax.set_title('无条件：D 和 Y 独立（分布重叠）')
    ax.legend()

    # 右图：控制 C=1 后，D 和 Y 出现关联
    ax = axes[1]
    mask = C == 1
    if np.sum(D[mask] == 0) > 0 and np.sum(D[mask] == 1) > 0:
        ax.hist(Y[mask & (D == 0)], bins=20, alpha=0.5, label='D=0 | C=1')
        ax.hist(Y[mask & (D == 1)], bins=20, alpha=0.5, label='D=1 | C=1')
        ax.set_xlabel('Y')
        ax.set_ylabel('频数')
        ax.set_title('控制碰撞变量 C=1 后：D 和 Y 出现虚假关联')
        ax.legend()

    plt.tight_layout()
    plt.savefig('observational_challenges_collider.png', dpi=150)
    print("可视化已保存至 observational_challenges_collider.png")


def print_summary():
    """打印关键教训总结"""
    print("\n" + "=" * 60)
    print("观察性数据挑战：核心教训")
    print("=" * 60)
    print("""
1. 混杂变量（Confounder）
   → 同时影响处理和结果，不控制会引入偏误
   → 解决方案：控制、匹配、IPW、双重稳健

2. 碰撞变量（Collider）
   → 被处理和结果共同影响，控制会打开虚假路径
   → 解决方案：识别 DAG 结构，绝不控制碰撞变量及其后代

3. 中介变量（Mediator）
   → 位于因果路径上，控制会阻断间接效应
   → 解决方案：明确估计目标是总效应还是直接效应

4. 控制变量选择原则
   → 该控的：混杂变量（原因）
   → 不该控的：碰撞变量、中介变量（后果）、对结果无影响的变量
   → 画 DAG 是避免错误的最可靠方法
""")


if __name__ == "__main__":
    D_conf, Y_conf, Z, ate_naive, ate_adjusted = scenario_confounding()
    D_col, Y_col, C, ate_unc, ate_col = scenario_collider()
    D_med, Y_med, M, ate_total, ate_direct = scenario_mediator()

    visualize_confounding(D_conf, Y_conf, Z, ate_naive, ate_adjusted)
    visualize_collider(D_col, Y_col, C)
    print_summary()
