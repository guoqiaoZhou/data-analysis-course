# Project 01: 电商大促活动效果评估

> **因果推断全流程** | **观察性数据** | **PSM + DID + 合成控制**

---

## 📖 阅读路径

### ⏱️ 快速了解（5分钟）
如果你只想了解这个项目的流程和结论：
1. **README.md**（本文件）— 项目背景、核心问题、结论预览
2. **report-template/analysis-report-template.md** — 标准分析报告长什么样

### 🧠 理解思路（30分钟）
如果你想理解"为什么这么做"的分析思路：
1. **notebooks/01-exploratory-analysis.ipynb** — 数据探索、发现选择偏差
2. **notebooks/02-causal-design.ipynb** — 方法选择：为什么用PSM不用回归？
3. **notebooks/05-report.ipynb** — 结论整合、业务建议

### 🛠️ 动手实践（2-4小时）
如果你想跟着做一遍：
按顺序执行 notebooks/01 → 02 → 03 → 04 → 05，每个都有TODO标记引导你完成

### 🔍 深入验证（可选）
做完后对照：
- **solution/reference-solution.md** — 参考答案
- **rubric/scoring-rubric.md** — 自评标准

---

## 📋 项目背景

某电商平台在"618大促"期间，向部分用户发放了满减优惠券。平台希望评估这一营销策略的真实效果：优惠券是否真正提升了用户的GMV（成交总额）？

这是一个经典的因果推断问题。用户是否领券并非随机分配——高价值用户更可能领取并使用优惠券。简单的均值比较会陷入**选择偏差**的陷阱。

---

## 业务问题

> **核心问题**：优惠券对GMV的因果效应（ATT）是多少？

衍生问题：
- 优惠券对不同用户群体的效果是否一致？
- 是否存在"优惠券依赖"现象（历史高消费用户反而效果更小）？
- 如果重新设计实验，如何获得更干净的因果估计？

## 数据说明

本项目提供模拟数据集，模拟真实电商场景中的用户行为。数据包含用户ID、是否领券、GMV、历史消费、用户属性等字段。

详见 [[data-dictionary|数据字典]]。

## 覆盖知识点

- [[潜在结果框架|潜在结果框架（Potential Outcomes Framework）]]
- [[选择偏差|选择偏差与可忽略性假设]]
- [[PSM|倾向得分匹配（PSM）]]
- [[DID|双重差分（DID）]]
- [[合成控制法|合成控制法（Synthetic Control）]]
- [[随机化实验|随机化实验设计]]

## 学习路径

建议按以下顺序执行 notebooks：

1. [[01-exploratory-analysis|探索性分析]] —— 理解数据分布，发现潜在问题
2. [[02-causal-design|因果设计]] —— 选择适当的因果推断方法
3. [[03-psm-analysis|PSM匹配分析]] —— 用倾向得分匹配估计因果效应
4. [[04-did-analysis|DID分析]] —— 用双重差分处理面板数据
5. [[05-report|报告生成]] —— 整合分析结果，撰写业务报告

## 项目结构

```
project-01-ecommerce-causal/
├── README.md
├── data/
│   ├── raw/              # 原始数据
│   ├── processed/        # 清洗后数据
│   └── data-dictionary.md # 数据字典
├── notebooks/
│   ├── 01-exploratory-analysis.ipynb
│   ├── 02-causal-design.ipynb
│   ├── 03-psm-analysis.ipynb
│   ├── 04-did-analysis.ipynb
│   └── 05-report.ipynb
├── report-template/
│   └── analysis-report-template.md
├── solution/
│   └── reference-solution.md
└── rubric/
    └── scoring-rubric.md
```

## 环境要求

```bash
pip install pandas numpy statsmodels scikit-learn matplotlib seaborn jupyter
```

## 提交要求

完成所有 notebooks 后，根据 [[analysis-report-template|分析报告模板]] 撰写最终报告。提交内容包括：
- 完成的 notebooks（含输出）
- 生成的分析报告（Markdown或PDF）

## 评分标准

详见 [[scoring-rubric|评分标准]]。

---

> "相关性不等于因果性。在这个项目中，你将学会如何从纷繁复杂的业务数据中，剥离出真实的因果效应。"
