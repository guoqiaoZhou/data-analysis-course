"""
DID (Difference-in-Differences) 模拟演示

本脚本演示：
1. 经典 2x2 DID 估计
2. 平行趋势假设检验（可视化）
3. 事件研究法 / 动态效应估计
4. 合成控制法基础（简化版）
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 中文显示设置
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)


def generate_did_data(n_units=200, n_periods=10, treatment_period=5, true_effect=3.0):
    """
    生成面板数据。
    n_units: 个体数
    n_periods: 期数
    treatment_period: 处理发生的时期（从0开始）
    true_effect: 真实处理效应
    """
    units = []
    for i in range(n_units):
        # 随机分配处理组（50%）
        treated = 1 if i < n_units // 2 else 0
        unit_fe = np.random.normal(0, 1)  # 个体固定效应
        trend = np.random.normal(0.5, 0.2)  # 个体趋势
        for t in range(n_periods):
            post = 1 if t >= treatment_period else 0
            treat_post = treated * post
            # 结果：时间趋势 + 个体效应 + 处理效应 + 噪声
            y = 1.0 + 0.3 * t + unit_fe + trend * t + true_effect * treat_post + np.random.normal(0, 0.5)
            units.append({
                'unit': i,
                'period': t,
                'treated': treated,
                'post': post,
                'treat_post': treat_post,
                'y': y,
                'true_effect': true_effect
            })
    return pd.DataFrame(units)


def generate_did_violation_data(n_units=200, n_periods=10, treatment_period=5, true_effect=3.0):
    """生成违反平行趋势假设的数据（处理组趋势不同）。"""
    units = []
    for i in range(n_units):
        treated = 1 if i < n_units // 2 else 0
        unit_fe = np.random.normal(0, 1)
        # 处理组有额外上升趋势
        extra_trend = 0.4 if treated == 1 else 0.0
        trend = np.random.normal(0.5, 0.2) + extra_trend
        for t in range(n_periods):
            post = 1 if t >= treatment_period else 0
            treat_post = treated * post
            y = 1.0 + 0.3 * t + unit_fe + trend * t + true_effect * treat_post + np.random.normal(0, 0.5)
            units.append({
                'unit': i,
                'period': t,
                'treated': treated,
                'post': post,
                'treat_post': treat_post,
                'y': y,
                'true_effect': true_effect
            })
    return pd.DataFrame(units)


def classic_did(df):
    """经典 2x2 DID 回归估计。"""
    X = df[['treated', 'post', 'treat_post']]
    X = sm.add_constant(X)
    model = sm.OLS(df['y'], X).fit()
    return model


def event_study(df, treatment_period=5):
    """事件研究法：估计每一期的动态效应。"""
    df = df.copy()
    df['rel_time'] = df['period'] - treatment_period
    # 以处理前一期为参照组
    ref_period = -1
    periods = sorted(df['rel_time'].unique())
    periods = [p for p in periods if p != ref_period]

    for p in periods:
        df[f'lead_lag_{p}'] = ((df['rel_time'] == p) & (df['treated'] == 1)).astype(int)

    formula = 'y ~ C(unit) + C(period) + ' + ' + '.join([f'lead_lag_{p}' for p in periods])
    # 使用 dummy 变量避免内存爆炸，这里简化用固定效应均值
    # 为简化，用去均值法
    df['unit_mean'] = df.groupby('unit')['y'].transform('mean')
    df['period_mean'] = df.groupby('period')['y'].transform('mean')
    df['y_demean'] = df['y'] - df['unit_mean'] - df['period_mean'] + df['y'].mean()

    X_cols = [f'lead_lag_{p}' for p in periods]
    X = df[X_cols]
    X = sm.add_constant(X)
    model = sm.OLS(df['y_demean'], X).fit()

    coefs = {}
    for p in periods:
        coefs[p] = model.params.get(f'lead_lag_{p}', np.nan)
    return coefs, model


def simple_synthetic_control(df, treatment_period=5):
    """
    简化版合成控制法：
    选取1个处理单元，用多个对照单元的加权平均构造合成控制。
    这里用等权重平均作为简化示例。
    """
    # 选取第一个处理单元
    treated_unit = df[df['treated'] == 1]['unit'].iloc[0]
    treated_df = df[df['unit'] == treated_unit].sort_values('period')
    control_units = df[df['treated'] == 0]['unit'].unique()

    # 对照组等权重平均
    control_df = df[df['unit'].isin(control_units)].groupby('period')['y'].mean().reset_index()
    control_df = control_df.sort_values('period')

    return treated_df, control_df


def scenario_classic_did():
    """经典 DID 场景。"""
    print("=" * 60)
    print("【场景 1】经典 2x2 DID 估计")
    print("=" * 60)

    df = generate_did_data(n_units=200, n_periods=10, treatment_period=5, true_effect=3.0)
    model = classic_did(df)
    estimated = model.params['treat_post']
    true_effect = df['true_effect'].iloc[0]

    print(f"\n真实处理效应: {true_effect:.4f}")
    print(f"DID 估计系数: {estimated:.4f}")
    print(f"标准误: {model.bse['treat_post']:.4f}")
    print(f"95% 置信区间: [{model.conf_int().loc['treat_post', 0]:.4f}, {model.conf_int().loc['treat_post', 1]:.4f}]")
    return df, model


def scenario_parallel_trends():
    """平行趋势假设检验。"""
    print("\n" + "=" * 60)
    print("【场景 2】平行趋势假设检验")
    print("=" * 60)

    df_valid = generate_did_data(n_units=200, n_periods=10, treatment_period=5, true_effect=3.0)
    df_invalid = generate_did_violation_data(n_units=200, n_periods=10, treatment_period=5, true_effect=3.0)

    # 计算每期均值
    def period_means(df):
        return df.groupby(['period', 'treated'])['y'].mean().unstack()

    means_valid = period_means(df_valid)
    means_invalid = period_means(df_invalid)

    print("\n满足平行趋势假设的数据：处理前各期均值差")
    for t in range(5):
        diff = means_valid.loc[t, 1] - means_valid.loc[t, 0]
        print(f"   期 {t}: 差值={diff:.4f}")

    print("\n违反平行趋势假设的数据：处理前各期均值差")
    for t in range(5):
        diff = means_invalid.loc[t, 1] - means_invalid.loc[t, 0]
        print(f"   期 {t}: 差值={diff:.4f}")

    return df_valid, df_invalid, means_valid, means_invalid


def scenario_event_study():
    """事件研究法。"""
    print("\n" + "=" * 60)
    print("【场景 3】事件研究法 / 动态效应")
    print("=" * 60)

    df = generate_did_data(n_units=200, n_periods=10, treatment_period=5, true_effect=3.0)
    coefs, model = event_study(df, treatment_period=5)

    print("\n各期动态效应估计（相对于处理前一期）：")
    for p, coef in sorted(coefs.items()):
        print(f"   相对期 {p:2d}: {coef:.4f}")
    return df, coefs


def scenario_synthetic_control():
    """合成控制法简化版。"""
    print("\n" + "=" * 60)
    print("【场景 4】合成控制法（简化版）")
    print("=" * 60)

    df = generate_did_data(n_units=50, n_periods=10, treatment_period=5, true_effect=3.0)
    treated_df, control_df = simple_synthetic_control(df, treatment_period=5)

    # 计算处理前拟合度
    pre_treated = treated_df[treated_df['period'] < 5]['y'].values
    pre_control = control_df[control_df['period'] < 5]['y'].values
    pre_mse = np.mean((pre_treated - pre_control) ** 2)

    print(f"\n处理前合成控制拟合 MSE: {pre_mse:.4f}")
    print("处理前处理单元与合成控制走势越接近，合成控制效果越好。")
    return treated_df, control_df


def visualize_results(df_valid, df_invalid, means_valid, means_invalid, coefs, treated_df, control_df):
    """生成可视化图表。"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 平行趋势：满足假设
    ax = axes[0, 0]
    ax.plot(means_valid.index, means_valid[0], marker='o', label='对照组', color='skyblue')
    ax.plot(means_valid.index, means_valid[1], marker='o', label='处理组', color='coral')
    ax.axvline(4.5, color='gray', linestyle='--', label='处理时点')
    ax.set_xlabel('时期')
    ax.set_ylabel('结果变量均值')
    ax.set_title('满足平行趋势假设')
    ax.legend()

    # 2. 平行趋势：违反假设
    ax = axes[0, 1]
    ax.plot(means_invalid.index, means_invalid[0], marker='o', label='对照组', color='skyblue')
    ax.plot(means_invalid.index, means_invalid[1], marker='o', label='处理组', color='coral')
    ax.axvline(4.5, color='gray', linestyle='--', label='处理时点')
    ax.set_xlabel('时期')
    ax.set_ylabel('结果变量均值')
    ax.set_title('违反平行趋势假设')
    ax.legend()

    # 3. 事件研究动态效应
    ax = axes[1, 0]
    periods = sorted(coefs.keys())
    values = [coefs[p] for p in periods]
    ax.plot(periods, values, marker='o', color='green')
    ax.axhline(0, color='black', linestyle='-', linewidth=0.5)
    ax.axvline(-0.5, color='gray', linestyle='--')
    ax.set_xlabel('相对处理时期')
    ax.set_ylabel('动态效应')
    ax.set_title('事件研究法：动态效应')

    # 4. 合成控制
    ax = axes[1, 1]
    ax.plot(treated_df['period'], treated_df['y'], marker='o', label='处理单元', color='coral')
    ax.plot(control_df['period'], control_df['y'], marker='s', label='合成控制', color='skyblue')
    ax.axvline(4.5, color='gray', linestyle='--', label='处理时点')
    ax.set_xlabel('时期')
    ax.set_ylabel('结果变量')
    ax.set_title('合成控制法（简化版）')
    ax.legend()

    plt.tight_layout()
    plt.savefig('did_simulation.png', dpi=150)
    print("\n[可视化已保存] did_simulation.png")
    plt.close()


def summary():
    """总结说明。"""
    print("\n" + "=" * 60)
    print("【总结】")
    print("=" * 60)
    print("""
本脚本演示了 DID 的核心内容：
1. 经典 2x2 DID：通过处理组×时间交互项估计平均处理效应
2. 平行趋势检验：处理前两组趋势应平行，否则估计有偏
3. 事件研究法：估计处理前后各期的动态效应，检验预期效应
4. 合成控制法：为处理单元构造加权对照组合成控制

关键要点：
- 平行趋势是 DID 的核心识别假设，需通过图形和统计检验验证
- 事件研究法可揭示处理效应的动态变化
- 合成控制法适用于只有一个或少数处理单元的情形
""")


if __name__ == "__main__":
    df_valid, model = scenario_classic_did()
    df_valid2, df_invalid, means_valid, means_invalid = scenario_parallel_trends()
    df_event, coefs = scenario_event_study()
    treated_df, control_df = scenario_synthetic_control()
    visualize_results(df_valid, df_invalid, means_valid, means_invalid, coefs, treated_df, control_df)
    summary()
