"""
实验分析决策框架 —— 模拟演示
============================
本脚本演示以下内容：
1. 提前停止（early stopping）的风险
2. Peeking 问题：多次偷看 p 值导致的假阳性膨胀
3. 序贯分析基础：SPRT（Sequential Probability Ratio Test）思想
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def simulate_early_stopping_risk(
    n_total=2000,
    n_peeks=10,
    alpha=0.05,
    n_simulations=1000,
    true_effect=0.0,
):
    """
    模拟提前停止风险：在实验过程中多次偷看 p 值，一旦显著就停止。
    展示假阳性率如何膨胀。
    """
    false_positives = 0
    pvalue_trajectories = []

    for sim in range(n_simulations):
        ctrl_all = np.random.normal(0, 1, n_total)
        treat_all = np.random.normal(true_effect, 1, n_total)

        stopped = False
        trajectory = []
        for peek in range(1, n_peeks + 1):
            n = int(n_total * peek / n_peeks)
            ctrl = ctrl_all[:n]
            treat = treat_all[:n]
            _, p = stats.ttest_ind(ctrl, treat)
            trajectory.append(p)
            if p < alpha:
                false_positives += 1
                stopped = True
                break
        if sim < 50:  # 只保存前 50 条轨迹用于可视化
            pvalue_trajectories.append((trajectory, stopped))

    fpr = false_positives / n_simulations
    print("[提前停止风险]")
    print(f"  总样本量: {n_total}, 偷看次数: {n_peeks}")
    print(f"  真实效应: {true_effect}, 名义 alpha: {alpha}")
    print(f"  模拟次数: {n_simulations}")
    print(f"  实际假阳性率（偷看停止）: {fpr:.3f}")

    # 可视化 p 值轨迹
    plt.figure(figsize=(10, 6))
    for trajectory, stopped in pvalue_trajectories:
        x = np.linspace(n_total / n_peeks, len(trajectory) * n_total / n_peeks, len(trajectory))
        color = 'red' if stopped else 'gray'
        alpha_line = 0.8 if stopped else 0.2
        plt.plot(x, trajectory, color=color, alpha=alpha_line)
    plt.axhline(alpha, color='blue', linestyle='--', label=f"alpha={alpha}")
    plt.title("偷看 p 值轨迹（红色=提前停止）")
    plt.xlabel("累计样本量")
    plt.ylabel("p 值")
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("early_stopping_risk.png", dpi=150)
    plt.close()
    print("  图像已保存: early_stopping_risk.png")
    return fpr


def simulate_peeking_inflation(
    n_total=2000,
    peek_counts=(1, 5, 10, 20, 50),
    alpha=0.05,
    n_simulations=500,
):
    """
    对比不同偷看次数下的假阳性率膨胀。
    """
    fpr_list = []
    for n_peeks in peek_counts:
        fp = 0
        for _ in range(n_simulations):
            ctrl_all = np.random.normal(0, 1, n_total)
            treat_all = np.random.normal(0, 1, n_total)
            for peek in range(1, n_peeks + 1):
                n = int(n_total * peek / n_peeks)
                _, p = stats.ttest_ind(ctrl_all[:n], treat_all[:n])
                if p < alpha:
                    fp += 1
                    break
        fpr_list.append(fp / n_simulations)

    plt.figure(figsize=(8, 5))
    plt.plot(peek_counts, fpr_list, marker='o')
    plt.axhline(alpha, color='r', linestyle='--', label="名义 alpha")
    plt.title("偷看次数与假阳性率膨胀")
    plt.xlabel("偷看次数")
    plt.ylabel("实际假阳性率")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("peeking_inflation.png", dpi=150)
    plt.close()
    print("\n[Peeking 问题]")
    for n_peeks, fpr in zip(peek_counts, fpr_list):
        print(f"  偷看次数={n_peeks:2d} → 实际假阳性率={fpr:.3f}")
    print("  图像已保存: peeking_inflation.png")


def simulate_sprt_basic(n_total=2000, alpha=0.05, beta=0.2, delta=0.3, n_simulations=500):
    """
    演示 SPRT（序贯概率比检验）基础思想：
    在累积数据过程中计算 likelihood ratio，与上下界比较决定停止或继续。
    此处使用正态均值检验的近似。
    """
    # Wald 边界
    A = (1 - beta) / alpha
    B = beta / (1 - alpha)
    logA = np.log(A)
    logB = np.log(B)

    stopping_times = []
    decisions = []  # 1=拒绝H0, 0=接受H0, -1=到达最大样本量未决

    for _ in range(n_simulations):
        # H1 下生成数据（真实效应 = delta）
        data = np.random.normal(delta, 1, n_total)
        log_lr = 0.0
        stopped = False
        for n in range(1, n_total + 1):
            # 正态均值已知方差=1 的 log likelihood ratio
            log_lr += delta * data[n - 1] - 0.5 * delta ** 2
            if log_lr >= logA:
                stopping_times.append(n)
                decisions.append(1)
                stopped = True
                break
            elif log_lr <= logB:
                stopping_times.append(n)
                decisions.append(0)
                stopped = True
                break
        if not stopped:
            stopping_times.append(n_total)
            decisions.append(-1)

    decisions = np.array(decisions)
    prop_reject = np.mean(decisions == 1)
    prop_accept = np.mean(decisions == 0)
    prop_undecided = np.mean(decisions == -1)
    avg_stop = np.mean(stopping_times)

    print("\n[序贯分析基础 —— SPRT]")
    print(f"  最大样本量: {n_total}, 真实效应: {delta}")
    print(f"  名义 alpha={alpha}, beta={beta}")
    print(f"  拒绝 H0 比例: {prop_reject:.3f}")
    print(f"  接受 H0 比例: {prop_accept:.3f}")
    print(f"  到达最大样本量未决: {prop_undecided:.3f}")
    print(f"  平均停止样本量: {avg_stop:.1f}")

    plt.figure(figsize=(8, 5))
    plt.hist(stopping_times, bins=30, edgecolor='k', alpha=0.7)
    plt.axvline(n_total, color='r', linestyle='--', label="最大样本量")
    plt.title("SPRT 停止时间分布")
    plt.xlabel("停止时的样本量")
    plt.ylabel("频数")
    plt.legend()
    plt.tight_layout()
    plt.savefig("sprt_stopping.png", dpi=150)
    plt.close()
    print("  图像已保存: sprt_stopping.png")


def main():
    print("=" * 50)
    print("实验分析决策框架 —— 模拟演示")
    print("=" * 50)

    simulate_early_stopping_risk(
        n_total=2000,
        n_peeks=10,
        alpha=0.05,
        n_simulations=1000,
        true_effect=0.0,
    )
    simulate_peeking_inflation(
        n_total=2000,
        peek_counts=(1, 5, 10, 20, 50),
        alpha=0.05,
        n_simulations=500,
    )
    simulate_sprt_basic(
        n_total=2000,
        alpha=0.05,
        beta=0.2,
        delta=0.3,
        n_simulations=500,
    )

    print("\n" + "=" * 50)
    print("全部模拟完成。")
    print("=" * 50)


if __name__ == "__main__":
    main()
