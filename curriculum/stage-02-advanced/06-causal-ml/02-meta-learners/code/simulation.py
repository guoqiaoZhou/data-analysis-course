"""
Meta-Learners 模拟演示
=====================
本脚本演示并对比四种 Meta-Learner：
1. S-Learner：单模型，将处理变量 T 作为特征输入
2. T-Learner：分别为处理组和对照组训练模型
3. X-Learner：基于倾向得分的加权插补 + 第二阶段模型
4. R-Learner：残差化结果回归（基于 Robinson 分解）

在已知异质性效应的数据上对比四种方法，展示偏差-方差权衡。
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_data(n=5000, p=5):
    """
    生成模拟数据，包含异质性处理效应。
    - X ~ Uniform(0, 1)
    - 倾向得分：e(X) = logistic(0.5*(X0 - 0.5) + 0.3*X1)（非随机）
    - 基线结果：mu0(X) = X0 + 2*X1 + X2*X3
    - 真实 CATE：tau(X) = 2 + 3*X0 - 2*X1
    - 观测结果：Y = mu0(X) + T * tau(X) + epsilon
    """
    X = np.random.uniform(0, 1, size=(n, p))
    # 倾向得分（非完全随机）
    logit = 0.5 * (X[:, 0] - 0.5) + 0.3 * X[:, 1]
    e = 1 / (1 + np.exp(-logit))
    T = np.random.binomial(1, e)

    mu0 = X[:, 0] + 2 * X[:, 1] + X[:, 2] * X[:, 3]
    tau_true = 2.0 + 3.0 * X[:, 0] - 2.0 * X[:, 1]
    epsilon = np.random.normal(0, 1, size=n)

    Y = mu0 + T * tau_true + epsilon
    return X, T, Y, tau_true


def fit_s_learner(X, T, Y):
    """S-Learner：单模型，T 作为特征"""
    XT = np.column_stack([X, T])
    model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
    model.fit(XT, Y)

    def predict_cate(X_new):
        XT1 = np.column_stack([X_new, np.ones(X_new.shape[0])])
        XT0 = np.column_stack([X_new, np.zeros(X_new.shape[0])])
        return model.predict(XT1) - model.predict(XT0)

    return predict_cate


def fit_t_learner(X, T, Y):
    """T-Learner：分别为处理组和对照组训练模型"""
    model1 = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
    model0 = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=43)

    model1.fit(X[T == 1], Y[T == 1])
    model0.fit(X[T == 0], Y[T == 0])

    def predict_cate(X_new):
        return model1.predict(X_new) - model0.predict(X_new)

    return predict_cate


def fit_x_learner(X, T, Y):
    """
    X-Learner：
    1. 分别对处理组和对照组训练模型 mu1, mu0
    2. 对处理组样本：D1 = Y1 - mu0(X1)；对照组样本：D0 = mu1(X0) - Y0
    3. 用倾向得分加权，训练 tau(X) 的模型
    """
    model1 = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
    model0 = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=43)

    model1.fit(X[T == 1], Y[T == 1])
    model0.fit(X[T == 0], Y[T == 0])

    # 插补
    D1 = Y[T == 1] - model0.predict(X[T == 1])
    D0 = model1.predict(X[T == 0]) - Y[T == 0]

    # 倾向得分模型
    ps_model = GradientBoostingClassifier(n_estimators=200, max_depth=4, random_state=44)
    ps_model.fit(X, T)
    e_hat = np.clip(ps_model.predict_proba(X)[:, 1], 0.05, 0.95)

    # 构建加权数据集
    X_all = np.vstack([X[T == 1], X[T == 0]])
    D_all = np.concatenate([D1, D0])
    weights = np.concatenate([1 / e_hat[T == 1], 1 / (1 - e_hat[T == 0])])

    tau_model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=45)
    tau_model.fit(X_all, D_all, sample_weight=weights)

    def predict_cate(X_new):
        return tau_model.predict(X_new)

    return predict_cate


def fit_r_learner(X, T, Y):
    """
    R-Learner（基于 Robinson 分解）：
    1. 估计倾向得分 e(X) 和结果回归 m(X) = E[Y|X]
    2. 计算残差：Y_tilde = Y - m(X)，W_tilde = T - e(X)
    3. 用 Ridge 回归拟合 Y_tilde ~ tau(X) * W_tilde
    """
    # 步骤1：估计 m(X) 和 e(X)
    m_model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
    m_model.fit(X, Y)
    m_hat = m_model.predict(X)

    e_model = GradientBoostingClassifier(n_estimators=200, max_depth=4, random_state=43)
    e_model.fit(X, T)
    e_hat = np.clip(e_model.predict_proba(X)[:, 1], 0.05, 0.95)

    # 步骤2：残差化
    Y_tilde = Y - m_hat
    W_tilde = T - e_hat

    # 步骤3：用 Ridge 回归拟合 tau(X) * W_tilde
    # 这里使用简化方法：先计算 pseudo-outcome，再用 GBDT 拟合
    pseudo_outcome = Y_tilde / W_tilde
    weights = W_tilde ** 2

    tau_model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=44)
    tau_model.fit(X, pseudo_outcome, sample_weight=weights)

    def predict_cate(X_new):
        return tau_model.predict(X_new)

    return predict_cate


def evaluate_learner(name, predict_fn, X_test, tau_test):
    """评估单个 learner 的 CATE 估计性能"""
    cate_pred = predict_fn(X_test)
    mse = np.mean((cate_pred - tau_test) ** 2)
    bias = np.mean(cate_pred - tau_test)
    variance = np.var(cate_pred - tau_test)
    return {
        'name': name,
        'mse': mse,
        'bias': bias,
        'variance': variance,
        'cate_pred': cate_pred
    }


def run_comparison(n=5000, n_runs=10):
    """多次运行对比四种 learner"""
    print("\n" + "=" * 60)
    print("Meta-Learners 对比实验")
    print("=" * 60)
    print(f"数据量: {n}, 重复次数: {n_runs}")

    results = {
        'S-Learner': [],
        'T-Learner': [],
        'X-Learner': [],
        'R-Learner': []
    }

    for run in range(n_runs):
        np.random.seed(42 + run)
        X, T, Y, tau_true = generate_data(n=n, p=5)
        X_train, X_test, T_train, T_test, Y_train, Y_test, tau_train, tau_test = train_test_split(
            X, T, Y, tau_true, test_size=0.3, random_state=42 + run
        )

        s_pred = fit_s_learner(X_train, T_train, Y_train)
        t_pred = fit_t_learner(X_train, T_train, Y_train)
        x_pred = fit_x_learner(X_train, T_train, Y_train)
        r_pred = fit_r_learner(X_train, T_train, Y_train)

        results['S-Learner'].append(evaluate_learner('S-Learner', s_pred, X_test, tau_test))
        results['T-Learner'].append(evaluate_learner('T-Learner', t_pred, X_test, tau_test))
        results['X-Learner'].append(evaluate_learner('X-Learner', x_pred, X_test, tau_test))
        results['R-Learner'].append(evaluate_learner('R-Learner', r_pred, X_test, tau_test))

    # 汇总统计
    print(f"\n{'方法':<12} {'平均 MSE':<12} {'平均偏差':<12} {'平均方差':<12}")
    print("-" * 50)
    for name in results:
        mses = [r['mse'] for r in results[name]]
        biases = [r['bias'] for r in results[name]]
        variances = [r['variance'] for r in results[name]]
        print(f"{name:<12} {np.mean(mses):.4f}       {np.mean(biases):.4f}       {np.mean(variances):.4f}")

    return results


def visualize_comparison(results):
    """可视化对比结果"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    methods = list(results.keys())
    mses = [np.mean([r['mse'] for r in results[m]]) for m in methods]
    biases = [np.mean([abs(r['bias']) for r in results[m]]) for m in methods]
    variances = [np.mean([r['variance'] for r in results[m]]) for m in methods]

    # MSE 对比
    ax = axes[0]
    ax.bar(methods, mses, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax.set_ylabel('平均 MSE')
    ax.set_title('CATE 估计 MSE 对比')
    ax.tick_params(axis='x', rotation=15)

    # 偏差对比
    ax = axes[1]
    ax.bar(methods, biases, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax.set_ylabel('平均绝对偏差')
    ax.set_title('CATE 估计偏差对比')
    ax.tick_params(axis='x', rotation=15)

    # 方差对比
    ax = axes[2]
    ax.bar(methods, variances, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax.set_ylabel('平均方差')
    ax.set_title('CATE 估计方差对比')
    ax.tick_params(axis='x', rotation=15)

    plt.tight_layout()
    plt.savefig('meta_learners_comparison.png', dpi=150)
    plt.close()
    print("\n可视化已保存为 meta_learners_comparison.png")


def scenario_bias_variance_tradeoff():
    """展示偏差-方差权衡：改变样本量观察各方法表现"""
    print("\n" + "=" * 60)
    print("偏差-方差权衡：不同样本量下的表现")
    print("=" * 60)

    sample_sizes = [500, 1000, 2000, 5000]
    summary = {m: {'mse': [], 'bias': [], 'var': []} for m in ['S-Learner', 'T-Learner', 'X-Learner', 'R-Learner']}

    for n in sample_sizes:
        np.random.seed(42)
        X, T, Y, tau_true = generate_data(n=n, p=5)
        X_train, X_test, T_train, T_test, Y_train, Y_test, tau_train, tau_test = train_test_split(
            X, T, Y, tau_true, test_size=0.3, random_state=42
        )

        s_pred = fit_s_learner(X_train, T_train, Y_train)
        t_pred = fit_t_learner(X_train, T_train, Y_train)
        x_pred = fit_x_learner(X_train, T_train, Y_train)
        r_pred = fit_r_learner(X_train, T_train, Y_train)

        for name, pred_fn in [('S-Learner', s_pred), ('T-Learner', t_pred),
                               ('X-Learner', x_pred), ('R-Learner', r_pred)]:
            res = evaluate_learner(name, pred_fn, X_test, tau_test)
            summary[name]['mse'].append(res['mse'])
            summary[name]['bias'].append(abs(res['bias']))
            summary[name]['var'].append(res['variance'])

    fig, ax = plt.subplots(figsize=(8, 6))
    for name in summary:
        ax.plot(sample_sizes, summary[name]['mse'], marker='o', label=name)
    ax.set_xlabel('样本量')
    ax.set_ylabel('MSE')
    ax.set_title('不同样本量下的 CATE 估计 MSE')
    ax.set_xscale('log')
    ax.legend()
    plt.tight_layout()
    plt.savefig('meta_learners_sample_size.png', dpi=150)
    plt.close()
    print("可视化已保存为 meta_learners_sample_size.png")

    print(f"\n{'样本量':<10} {'方法':<12} {'MSE':<10} {'|偏差|':<10} {'方差':<10}")
    print("-" * 55)
    for i, n in enumerate(sample_sizes):
        for name in summary:
            print(f"{n:<10} {name:<12} {summary[name]['mse'][i]:.4f}    "
                  f"{summary[name]['bias'][i]:.4f}    {summary[name]['var'][i]:.4f}")


def print_summary():
    """打印总结"""
    print("\n" + "=" * 60)
    print("Meta-Learners 总结")
    print("=" * 60)
    print("""
1. S-Learner：简单，但可能无法捕捉复杂的异质性（正则化偏向零）。
2. T-Learner：直观，但在处理组/对照组样本不平衡时方差较大。
3. X-Learner：通过倾向得分加权改善不平衡问题，适合处理组较小的情况。
4. R-Learner：基于 Robinson 分解，偏差小，但对倾向得分和结果模型的估计质量敏感。

偏差-方差权衡：
- 小样本 / 简单效应：S-Learner 更稳定
- 大样本 / 复杂异质性：X-Learner 或 R-Learner 更优
- T-Learner 是良好基准，但在组间不平衡时需谨慎
""")


if __name__ == "__main__":
    print("Meta-Learners 模拟演示")
    print("=====================")

    # 主要对比实验
    results = run_comparison(n=5000, n_runs=5)
    visualize_comparison(results)

    # 偏差-方差权衡
    scenario_bias_variance_tradeoff()

    # 总结
    print_summary()
