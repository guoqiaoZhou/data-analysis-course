"""
多重检验问题 —— 模拟演示
========================
本脚本演示以下内容：
1. Bonferroni 校正
2. Benjamini-Hochberg (BH) 方法控制 FDR
3. 族错误率（FWER）膨胀现象
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def simulate_multiple_tests(
    n_tests=20,
    n_true_effects=5,
    n_per_group=500,
    effect_size=0.5,
    alpha=0.05,
    n_simulations=1000,
):
    """
    模拟多重检验场景：部分检验有真实效应，其余为 null。
    对比无校正、Bonferroni、BH 三种方法的表现。
    """
    results = {
        "uncorrected": {"fwer": 0, "fdr": 0, "power": 0},
        "bonferroni": {"fwer": 0, "fdr": 0, "power": 0},
        "bh": {"fwer": 0, "fdr": 0, "power": 0},
    }

    for _ in range(n_simulations):
        pvalues = []
        true_null = []
        for i in range(n_tests):
            is_true_effect = i < n_true_effects
            true_null.append(not is_true_effect)
            if is_true_effect:
                ctrl = np.random.normal(0, 1, n_per_group)
                treat = np.random.normal(effect_size, 1, n_per_group)
            else:
                ctrl = np.random.normal(0, 1, n_per_group)
                treat = np.random.normal(0, 1, n_per_group)
            _, p = stats.ttest_ind(ctrl, treat)
            pvalues.append(p)

        pvalues = np.array(pvalues)
        true_null = np.array(true_null)

        # 无校正
        reject_unc = pvalues < alpha
        # Bonferroni
        reject_bonf = pvalues < (alpha / n_tests)
        # BH
        sorted_idx = np.argsort(pvalues)
        sorted_p = pvalues[sorted_idx]
        thresholds = np.arange(1, n_tests + 1) / n_tests * alpha
        bh_reject_sorted = sorted_p <= thresholds
        # 找到最大 k
        if bh_reject_sorted.any():
            max_k = np.where(bh_reject_sorted)[0][-1]
            reject_bh = np.zeros(n_tests, dtype=bool)
            reject_bh[sorted_idx[: max_k + 1]] = True
        else:
            reject_bh = np.zeros(n_tests, dtype=bool)

        for method, reject in [
            ("uncorrected", reject_unc),
            ("bonferroni", reject_bonf),
            ("bh", reject_bh),
        ]:
            # FWER: 至少一个假阳性
            if reject[true_null].any():
                results[method]["fwer"] += 1
            # FDR: 假阳性 / 总拒绝
            false_positives = reject[true_null].sum()
            total_reject = reject.sum()
            if total_reject > 0:
                results[method]["fdr"] += false_positives / total_reject
            # Power: 真阳性率
            true_positives = reject[~true_null].sum()
            results[method]["power"] += true_positives / n_true_effects

    for method in results:
        results[method]["fwer"] /= n_simulations
        results[method]["fdr"] /= n_simulations
        results[method]["power"] /= n_simulations

    print("[多重检验模拟]")
    print(f"  总检验数: {n_tests}, 真实效应数: {n_true_effects}")
    print(f"  每组样本量: {n_per_group}, 效应大小: {effect_size}, alpha: {alpha}")
    print(f"  模拟次数: {n_simulations}")
    for method, vals in results.items():
        print(f"  {method:12s}: FWER={vals['fwer']:.3f}, FDR={vals['fdr']:.3f}, Power={vals['power']:.3f}")

    return results


def simulate_fwer_inflation(n_tests_list=None, n_simulations=500, alpha=0.05):
    """
    演示随着检验次数增加，FWER 如何膨胀。
    """
    if n_tests_list is None:
        n_tests_list = [1, 2, 5, 10, 20, 50, 100]

    fwer_observed = []
    fwer_bonferroni = []

    for n_tests in n_tests_list:
        fwer_unc = 0
        fwer_bonf = 0
        for _ in range(n_simulations):
            pvalues = np.random.uniform(0, 1, n_tests)
            if (pvalues < alpha).any():
                fwer_unc += 1
            if (pvalues < alpha / n_tests).any():
                fwer_bonf += 1
        fwer_observed.append(fwer_unc / n_simulations)
        fwer_bonferroni.append(fwer_bonf / n_simulations)

    plt.figure(figsize=(8, 5))
    plt.plot(n_tests_list, fwer_observed, marker='o', label="无校正 FWER")
    plt.plot(n_tests_list, fwer_bonferroni, marker='s', label="Bonferroni FWER")
    plt.axhline(0.05, color='r', linestyle='--', label="目标 alpha=0.05")
    plt.title("FWER 随检验次数膨胀")
    plt.xlabel("检验次数 m")
    plt.ylabel("FWER")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("fwer_inflation.png", dpi=150)
    plt.close()
    print("\n[FWER 膨胀]")
    for m, fwer, fwer_b in zip(n_tests_list, fwer_observed, fwer_bonferroni):
        print(f"  m={m:3d}: 无校正 FWER={fwer:.3f}, Bonferroni FWER={fwer_b:.3f}")
    print("  图像已保存: fwer_inflation.png")


def simulate_bh_procedure():
    """
    可视化一次 BH 过程：排序 p 值与阈值线。
    """
    np.random.seed(42)
    n_tests = 20
    n_true = 5
    pvalues = []
    for i in range(n_tests):
        if i < n_true:
            ctrl = np.random.normal(0, 1, 500)
            treat = np.random.normal(0.6, 1, 500)
        else:
            ctrl = np.random.normal(0, 1, 500)
            treat = np.random.normal(0, 1, 500)
        _, p = stats.ttest_ind(ctrl, treat)
        pvalues.append(p)

    pvalues = np.array(pvalues)
    sorted_idx = np.argsort(pvalues)
    sorted_p = pvalues[sorted_idx]
    thresholds = np.arange(1, n_tests + 1) / n_tests * 0.05

    plt.figure(figsize=(8, 5))
    plt.scatter(range(1, n_tests + 1), sorted_p, label="排序后 p 值")
    plt.plot(range(1, n_tests + 1), thresholds, color='r', label="BH 阈值线")
    plt.axhline(0.05, color='gray', linestyle='--', label="alpha=0.05")
    plt.title("Benjamini-Hochberg 过程示意")
    plt.xlabel("排序序号 k")
    plt.ylabel("p 值")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("bh_procedure.png", dpi=150)
    plt.close()
    print("\n[BH 过程可视化]")
    print("  图像已保存: bh_procedure.png")


def main():
    print("=" * 50)
    print("多重检验问题 —— 模拟演示")
    print("=" * 50)

    simulate_multiple_tests(
        n_tests=20,
        n_true_effects=5,
        n_per_group=500,
        effect_size=0.5,
        alpha=0.05,
        n_simulations=1000,
    )
    simulate_fwer_inflation(n_tests_list=[1, 2, 5, 10, 20, 50, 100], n_simulations=500)
    simulate_bh_procedure()

    print("\n" + "=" * 50)
    print("全部模拟完成。")
    print("=" * 50)


if __name__ == "__main__":
    main()
