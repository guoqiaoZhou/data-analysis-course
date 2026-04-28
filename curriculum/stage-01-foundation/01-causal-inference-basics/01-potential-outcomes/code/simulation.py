# Python 代码示例：潜在结果框架模拟

"""
本代码演示潜在结果框架的核心概念：
1. 个体处理效应（ITE）
2. 平均处理效应（ATE）
3. 随机化实验如何识别 ATE
4. 观察性数据中的选择偏误
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# 设置随机种子
np.random.seed(42)

# ============================================
# 1. 生成模拟数据
# ============================================

n = 1000  # 样本量

# 生成协变量（混杂变量）
X = np.random.normal(0, 1, n)

# 生成潜在结果
# Y(0) = 2 + 0.5*X + 噪声
Y0 = 2 + 0.5 * X + np.random.normal(0, 0.5, n)

# Y(1) = Y(0) + 处理效应（ATE = 1.0，且处理效应随 X 变化）
treatment_effect = 1.0 + 0.3 * X  # 异质性处理效应
Y1 = Y0 + treatment_effect

# ============================================
# 2. 随机化实验场景
# ============================================

print("=" * 50)
print("场景1：随机化实验")
print("=" * 50)

# 随机分配处理
D_random = np.random.binomial(1, 0.5, n)

# 观测结果
Y_random = D_random * Y1 + (1 - D_random) * Y0

# 计算 ATE 估计（简单均值差）
ate_random = np.mean(Y_random[D_random == 1]) - np.mean(Y_random[D_random == 0])
print(f"真实 ATE: {np.mean(treatment_effect):.3f}")
print(f"随机化实验估计 ATE: {ate_random:.3f}")
print(f"误差: {abs(ate_random - np.mean(treatment_effect)):.3f}")

# ============================================
# 3. 观察性数据场景（有混杂）
# ============================================

print("\n" + "=" * 50)
print("场景2：观察性数据（有混杂）")
print("=" * 50)

# 处理分配依赖于 X（混杂）
prob_treatment = 1 / (1 + np.exp(-(0.5 * X)))  # logistic
D_obs = np.random.binomial(1, prob_treatment)

# 观测结果
Y_obs = D_obs * Y1 + (1 - D_obs) * Y0

#  naive 估计（简单均值差）
ate_naive = np.mean(Y_obs[D_obs == 1]) - np.mean(Y_obs[D_obs == 0])
print(f"真实 ATE: {np.mean(treatment_effect):.3f}")
print(f"Naive 估计（有偏）: {ate_naive:.3f}")
print(f"偏误: {ate_naive - np.mean(treatment_effect):.3f}")

# 回归调整（控制 X）
from sklearn.linear_model import LinearRegression

# 构建回归模型：Y ~ D + X
X_reg = np.column_stack([D_obs, X])
model = LinearRegression().fit(X_reg, Y_obs)
ate_adjusted = model.coef_[0]
print(f"回归调整后估计: {ate_adjusted:.3f}")
print(f"调整后误差: {abs(ate_adjusted - np.mean(treatment_effect)):.3f}")

# ============================================
# 4. 可视化
# ============================================

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 图1：潜在结果分布
ax = axes[0, 0]
ax.hist(Y0, bins=30, alpha=0.5, label='Y(0)')
ax.hist(Y1, bins=30, alpha=0.5, label='Y(1)')
ax.axvline(np.mean(Y0), color='blue', linestyle='--', label=f'E[Y(0)]={np.mean(Y0):.2f}')
ax.axvline(np.mean(Y1), color='orange', linestyle='--', label=f'E[Y(1)]={np.mean(Y1):.2f}')
ax.set_title('潜在结果分布')
ax.legend()

# 图2：处理效应异质性
ax = axes[0, 1]
ax.scatter(X, treatment_effect, alpha=0.5)
ax.axhline(np.mean(treatment_effect), color='red', linestyle='--', label=f'ATE={np.mean(treatment_effect):.2f}')
ax.set_xlabel('协变量 X')
ax.set_ylabel('个体处理效应')
ax.set_title('异质性处理效应（CATE）')
ax.legend()

# 图3：随机化实验 - 处理组vs对照组
ax = axes[1, 0]
ax.hist(Y_random[D_random == 0], bins=30, alpha=0.5, label='对照组')
ax.hist(Y_random[D_random == 1], bins=30, alpha=0.5, label='处理组')
ax.set_title('随机化实验：处理组 vs 对照组')
ax.legend()

# 图4：观察性数据 - 混杂导致不平衡
ax = axes[1, 1]
ax.hist(X[D_obs == 0], bins=30, alpha=0.5, label='对照组')
ax.hist(X[D_obs == 1], bins=30, alpha=0.5, label='处理组')
ax.set_title('观察性数据：混杂导致协变量不平衡')
ax.legend()

plt.tight_layout()
plt.savefig('potential_outcomes_simulation.png', dpi=150)
print("\n可视化已保存至 potential_outcomes_simulation.png")

# ============================================
# 5. 关键概念总结
# ============================================

print("\n" + "=" * 50)
print("关键概念总结")
print("=" * 50)
print(f"样本量: {n}")
print(f"真实 ATE: {np.mean(treatment_effect):.3f}")
print(f"随机化实验估计: {ate_random:.3f} (无偏)")
print(f"观察性数据 Naive: {ate_naive:.3f} (有偏)")
print(f"观察性数据调整后: {ate_adjusted:.3f} (近似无偏)")
print("\n结论：")
print("1. 随机化实验自动平衡混杂变量，Naive 估计无偏")
print("2. 观察性数据中，处理分配依赖于混杂变量，Naive 估计有偏")
print("3. 控制混杂变量（回归调整）可以消除大部分偏误")
