"""
随机化与分流 —— 模拟演示
========================
本脚本演示以下内容：
1. 基于哈希的随机化（hash-based randomization）
2. SRM（Sample Ratio Mismatch）检测
3. 分层随机化（stratified randomization）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def hash_randomization(user_ids, treatment_prob=0.5, salt="ab_test_v1"):
    """
    基于哈希的随机化：对用户ID进行哈希，根据哈希值模 10000 决定分组。
    保证同一用户始终进入同一组（idempotent）。
    """
    import hashlib
    assignments = []
    for uid in user_ids:
        h = hashlib.md5(f"{uid}_{salt}".encode()).hexdigest()
        val = int(h, 16) % 10000
        assignments.append(1 if val < treatment_prob * 10000 else 0)
    return np.array(assignments)


def simulate_hash_randomization(n_users=10000):
    """演示哈希随机化的稳定性与均匀性。"""
    user_ids = [f"user_{i:05d}" for i in range(n_users)]
    assignments = hash_randomization(user_ids, treatment_prob=0.5)

    # 稳定性测试：再次运行应得到相同结果
    assignments2 = hash_randomization(user_ids, treatment_prob=0.5)
    assert np.array_equal(assignments, assignments2), "哈希随机化结果不一致！"

    treat_ratio = assignments.mean()
    print("[哈希随机化]")
    print(f"  总用户数: {n_users}")
    print(f"  实验组比例: {treat_ratio:.4f}")
    print(f"  对照组比例: {1 - treat_ratio:.4f}")
    print(f"  结果稳定性: 通过（两次哈希结果完全一致）")
    return assignments


def simulate_srm_detection(n_users=10000, true_prob=0.5, biased_prob=None):
    """
    模拟 SRM（样本比例不匹配）检测。
    使用卡方检验判断实际分组比例是否偏离预期。
    """
    if biased_prob is None:
        # 构造一个有偏场景：实验组被多分配了 5%
        biased_prob = 0.55

    # 正常随机化
    normal_assignments = np.random.binomial(1, true_prob, n_users)
    # 有偏随机化
    biased_assignments = np.random.binomial(1, biased_prob, n_users)

    def chi2_test(assignments, expected_prob=0.5):
        n = len(assignments)
        observed = [np.sum(assignments == 0), np.sum(assignments == 1)]
        expected = [n * (1 - expected_prob), n * expected_prob]
        chi2, pvalue = stats.chisquare(observed, expected)
        return chi2, pvalue, observed

    chi2_normal, p_normal, obs_normal = chi2_test(normal_assignments)
    chi2_biased, p_biased, obs_biased = chi2_test(biased_assignments)

    print("\n[SRM 检测]")
    print(f"  正常分流: 对照组={obs_normal[0]}, 实验组={obs_normal[1]}, p={p_normal:.4f}")
    print(f"  有偏分流: 对照组={obs_biased[0]}, 实验组={obs_biased[1]}, p={p_biased:.4e}")
    print(f"  结论: 有偏分流 p < 0.05，SRM 告警触发" if p_biased < 0.05 else "  结论: 未触发 SRM 告警")

    # 可视化
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    labels = ["对照组", "实验组"]
    x = np.arange(len(labels))
    width = 0.35

    axes[0].bar(x, obs_normal, width, label="实际")
    axes[0].axhline(n_users * 0.5, color='r', linestyle='--', label="预期")
    axes[0].set_title(f"正常分流 (p={p_normal:.3f})")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels)
    axes[0].legend()

    axes[1].bar(x, obs_biased, width, label="实际")
    axes[1].axhline(n_users * 0.5, color='r', linestyle='--', label="预期")
    axes[1].set_title(f"有偏分流 (p={p_biased:.3e})")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels)
    axes[1].legend()

    plt.tight_layout()
    plt.savefig("srm_detection.png", dpi=150)
    plt.close()
    print("  图像已保存: srm_detection.png")


def simulate_stratified_randomization(n_total=10000, n_strata=4):
    """
    分层随机化：按用户活跃等级分层，每层内部 1:1 随机化。
    对比简单完全随机化在层间不平衡时的表现。
    """
    # 构造 4 个层级，比例不同
    strata_sizes = np.array([0.1, 0.2, 0.3, 0.4]) * n_total
    strata_sizes = strata_sizes.astype(int)
    # 补齐余数
    strata_sizes[-1] += n_total - strata_sizes.sum()

    strata_labels = ["低活跃", "中低活跃", "中高活跃", "高活跃"]
    true_effects_by_strata = np.array([1.0, 1.5, 2.0, 2.5])
    baseline_by_strata = np.array([50, 60, 70, 80])
    std_by_strata = np.array([20, 18, 15, 12])

    # 简单完全随机化
    simple_assignments = np.random.binomial(1, 0.5, n_total)
    simple_outcomes = []
    idx = 0
    for size, base, std, eff in zip(strata_sizes, baseline_by_strata, std_by_strata, true_effects_by_strata):
        for _ in range(size):
            group = simple_assignments[idx]
            val = np.random.normal(base + eff * group, std)
            simple_outcomes.append(val)
            idx += 1
    simple_outcomes = np.array(simple_outcomes)

    # 分层随机化
    stratified_assignments = []
    stratified_outcomes = []
    for size, base, std, eff in zip(strata_sizes, baseline_by_strata, std_by_strata, true_effects_by_strata):
        layer_assign = np.random.binomial(1, 0.5, size)
        stratified_assignments.extend(layer_assign)
        for group in layer_assign:
            val = np.random.normal(base + eff * group, std)
            stratified_outcomes.append(val)
    stratified_assignments = np.array(stratified_assignments)
    stratified_outcomes = np.array(stratified_outcomes)

    # 检验层间平衡性
    def check_balance(assignments, strata_sizes):
        balances = []
        idx = 0
        for size in strata_sizes:
            layer = assignments[idx: idx + size]
            balances.append(layer.mean())
            idx += size
        return balances

    simple_balance = check_balance(simple_assignments, strata_sizes)
    stratified_balance = check_balance(stratified_assignments, strata_sizes)

    print("\n[分层随机化]")
    print(f"  各层实验组比例（简单随机化）: {[f'{b:.3f}' for b in simple_balance]}")
    print(f"  各层实验组比例（分层随机化）: {[f'{b:.3f}' for b in stratified_balance]}")

    # 估计效应
    def estimate_effect(assignments, outcomes):
        ctrl = outcomes[assignments == 0]
        treat = outcomes[assignments == 1]
        return treat.mean() - ctrl.mean(), stats.ttest_ind(ctrl, treat).pvalue

    eff_simple, p_simple = estimate_effect(simple_assignments, simple_outcomes)
    eff_strat, p_strat = estimate_effect(stratified_assignments, stratified_outcomes)

    print(f"  简单随机化估计效应: {eff_simple:.3f}, p={p_simple:.4f}")
    print(f"  分层随机化估计效应: {eff_strat:.3f}, p={p_strat:.4f}")

    # 可视化各层实验组比例
    x = np.arange(len(strata_labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width / 2, simple_balance, width, label="简单随机化")
    ax.bar(x + width / 2, stratified_balance, width, label="分层随机化")
    ax.axhline(0.5, color='r', linestyle='--', label="目标比例 0.5")
    ax.set_xticks(x)
    ax.set_xticklabels(strata_labels)
    ax.set_ylabel("实验组比例")
    ax.set_title("各层实验组比例对比")
    ax.legend()
    plt.tight_layout()
    plt.savefig("stratified_randomization.png", dpi=150)
    plt.close()
    print("  图像已保存: stratified_randomization.png")


def main():
    print("=" * 50)
    print("随机化与分流 —— 模拟演示")
    print("=" * 50)

    simulate_hash_randomization(n_users=10000)
    simulate_srm_detection(n_users=10000)
    simulate_stratified_randomization(n_total=10000, n_strata=4)

    print("\n" + "=" * 50)
    print("全部模拟完成。")
    print("=" * 50)


if __name__ == "__main__":
    main()
