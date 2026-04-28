# Python 代码示例：因果与相关的本质区别

"""
本代码演示因果与相关的核心区别：
1. 相关≠因果：混杂、反向因果、共同原因
2. 随机化实验如何打破相关与因果之间的壁垒
3. do-算子 vs 条件概率的数学差异
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 设置中文字体（macOS 系统字体）
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
np.random.seed(42)


def scenario_common_cause(n=2000):
    """场景1：共同原因 —— 冰淇淋销量与溺水事件"""
    print("=" * 60)
    print("场景1：共同原因（Common Cause）")
    print("=" * 60)

    # Z = 气温（共同原因）
    Z = np.random.uniform(0, 40, n)  # 0-40度

    # X = 冰淇淋销量（依赖于气温）
    X = 10 + 2 * Z + np.random.normal(0, 5, n)

    # Y = 溺水事件（依赖于气温，不依赖冰淇淋销量）
    Y = 5 + 0.5 * Z + np.random.normal(0, 2, n)

    # 观察到的相关
    corr_xy = np.corrcoef(X, Y)[0, 1]

    # Naive 回归：Y ~ X
    model_naive = LinearRegression().fit(X.reshape(-1, 1), Y)
    beta_naive = model_naive.coef_[0]

    # 控制 Z 后：Y ~ X + Z
    XZ = np.column_stack([X, Z])
    model_adjusted = LinearRegression().fit(XZ, Y)
    beta_adjusted = model_adjusted.coef_[0]

    print(f"X(冰淇淋) 和 Y(溺水) 的相关系数: {corr_xy:.3f}")
    print(f"Naive 回归 Y~X: 系数 = {beta_naive:.3f} ← 虚假因果!")
    print(f"控制 Z 后 Y~X+Z: 系数 = {beta_adjusted:.3f} ← 接近0，无因果")
    print(f"\n解释：气温 Z 同时导致 X 和 Y，X 和 Y 的相关是 Z 的副产品")

    return X, Y, Z, corr_xy, beta_naive, beta_adjusted


def scenario_reverse_causality(n=2000):
    """场景2：反向因果 —— 医院与健康状况"""
    print("\n" + "=" * 60)
    print("场景2：反向因果（Reverse Causality）")
    print("=" * 60)

    # Y = 健康状况（基础健康水平）
    health = np.random.normal(50, 10, n)

    # X = 去医院次数（健康状况差的人去得更多）
    hospital_visits = np.maximum(0, 20 - 0.3 * health + np.random.normal(0, 3, n))

    # 观察到的相关
    corr = np.corrcoef(hospital_visits, health)[0, 1]

    # Naive 回归：health ~ hospital
    model = LinearRegression().fit(hospital_visits.reshape(-1, 1), health)
    beta = model.coef_[0]

    print(f"去医院次数 和 健康状况 的相关系数: {corr:.3f}")
    print(f"Naive 回归: 去医院每多1次，健康评分变化 {beta:.3f}")
    print(f"\n错误解读：'去医院损害健康'（β={beta:.3f}）")
    print(f"正确理解：'健康差的人去更多医院'（反向因果）")
    print(f"因果效应：去医院本身对健康的影响无法从观察数据识别")

    return hospital_visits, health, corr, beta


def scenario_randomization_breaks_confounding(n=2000):
    """场景3：随机化如何打破混杂"""
    print("\n" + "=" * 60)
    print("场景3：随机化打破混杂（Randomization）")
    print("=" * 60)

    # Z = 能力（混杂变量）
    Z = np.random.normal(0, 1, n)

    # 观察性数据：处理分配依赖于 Z
    prob_obs = 1 / (1 + np.exp(-(0.5 * Z)))
    D_obs = np.random.binomial(1, prob_obs)
    Y_obs = 2.0 * D_obs + 1.0 * Z + np.random.normal(0, 1, n)

    # 随机化实验：处理分配独立于 Z
    D_rand = np.random.binomial(1, 0.5, n)
    Y_rand = 2.0 * D_rand + 1.0 * Z + np.random.normal(0, 1, n)

    # 估计
    ate_obs = np.mean(Y_obs[D_obs == 1]) - np.mean(Y_obs[D_obs == 0])
    ate_rand = np.mean(Y_rand[D_rand == 1]) - np.mean(Y_rand[D_rand == 0])

    print(f"真实处理效应: 2.000")
    print(f"观察性数据估计: {ate_obs:.3f} ← 有偏（混杂了Z）")
    print(f"随机化实验估计: {ate_rand:.3f} ← 无偏")
    print(f"\n关键差异：")
    print(f"  观察性：P(D=1|Z) 依赖于 Z，处理组和对照组的 Z 分布不同")
    print(f"  随机化：P(D=1|Z) = 0.5，处理组和对照组的 Z 分布相同")

    return D_obs, Y_obs, D_rand, Y_rand, Z, ate_obs, ate_rand


def visualize_common_cause(X, Y, Z):
    """可视化：共同原因"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 左图：X 和 Y 的散点图
    ax = axes[0]
    scatter = ax.scatter(X, Y, c=Z, cmap='coolwarm', alpha=0.5, s=15)
    ax.set_xlabel('冰淇淋销量')
    ax.set_ylabel('溺水事件')
    ax.set_title('X 和 Y 强相关（r≈0.95）')
    plt.colorbar(scatter, ax=ax, label='气温')

    # 右图：控制 Z 后，X 和 Y 无关
    ax = axes[1]
    # 按气温分层，每层内看 X 和 Y 的关系
    z_low = Z < np.percentile(Z, 33)
    z_mid = (Z >= np.percentile(Z, 33)) & (Z < np.percentile(Z, 66))
    z_high = Z >= np.percentile(Z, 66)

    for mask, label, color in [(z_low, '低温', 'blue'),
                                (z_mid, '中温', 'green'),
                                (z_high, '高温', 'red')]:
        ax.scatter(X[mask], Y[mask], alpha=0.4, s=15, label=label, color=color)

    ax.set_xlabel('冰淇淋销量')
    ax.set_ylabel('溺水事件')
    ax.set_title('按气温分层后：X 和 Y 几乎无关')
    ax.legend()

    plt.tight_layout()
    plt.savefig('causation_correlation_common_cause.png', dpi=150)
    print("\n可视化已保存至 causation_correlation_common_cause.png")


def visualize_randomization(Z, D_obs, Y_obs, D_rand, Y_rand):
    """可视化：随机化如何平衡混杂"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 左图：观察性数据中，处理组的 Z 更高
    ax = axes[0]
    ax.hist(Z[D_obs == 0], bins=30, alpha=0.5, label='对照组')
    ax.hist(Z[D_obs == 1], bins=30, alpha=0.5, label='处理组')
    ax.set_xlabel('能力 Z')
    ax.set_ylabel('频数')
    ax.set_title('观察性数据：处理组 Z 更高（混杂）')
    ax.legend()

    # 右图：随机化后，两组 Z 分布相同
    ax = axes[1]
    ax.hist(Z[D_rand == 0], bins=30, alpha=0.5, label='对照组')
    ax.hist(Z[D_rand == 1], bins=30, alpha=0.5, label='处理组')
    ax.set_xlabel('能力 Z')
    ax.set_ylabel('频数')
    ax.set_title('随机化实验：两组 Z 分布相同（平衡）')
    ax.legend()

    plt.tight_layout()
    plt.savefig('causation_correlation_randomization.png', dpi=150)
    print("可视化已保存至 causation_correlation_randomization.png")


def print_summary():
    """打印核心教训"""
    print("\n" + "=" * 60)
    print("因果 vs 相关：核心教训")
    print("=" * 60)
    print("""
相关≠因果的三大原因：

1. 共同原因（Common Cause）
   → Z 同时导致 X 和 Y，X 和 Y 相关但无直接因果
   → 例子：气温 → 冰淇淋销量 & 溺水事件
   → 解决：控制 Z

2. 反向因果（Reverse Causality）
   → Y 导致 X，但数据上 X 和 Y 也相关
   → 例子：健康差 → 去医院多
   → 解决：时间序列、工具变量、实验

3. 混杂（Confounding）
   → Z 同时影响 X 和 Y，创造虚假关联
   → 例子：能力强的员工既参加培训又绩效高
   → 解决：随机化、控制、匹配

随机化的魔力：
   → 使处理分配独立于所有混杂变量
   → P(D=1|Z) = P(D=1) = 0.5，对所有 Z 成立
   → 处理组和对照组在期望上完全相同
   → 任何结果差异只能归因于处理
""")


if __name__ == "__main__":
    X, Y, Z, corr_xy, beta_naive, beta_adjusted = scenario_common_cause()
    hosp, health, corr_rev, beta_rev = scenario_reverse_causality()
    D_obs, Y_obs, D_rand, Y_rand, Z2, ate_obs, ate_rand = scenario_randomization_breaks_confounding()

    visualize_common_cause(X, Y, Z)
    visualize_randomization(Z2, D_obs, Y_obs, D_rand, Y_rand)
    print_summary()
