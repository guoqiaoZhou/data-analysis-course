# AGENTS.md — 数据分析进阶课程

> 本文件供 AI 编码助手阅读。项目主要使用中文，所有文档、注释和沟通均以中文为主。

---

## 项目概述

本项目是一套**面向数据分析师的进阶课程体系**，核心覆盖因果推断、机器学习建模、AB实验设计与分析文档写作。课程采用 Obsidian 知识库形态组织，以 Markdown 文件为主，配合 Python 代码示例和 Jupyter Notebook 实战项目。

**课程定位**：从"方法规范"到"体系化能力"，帮助数据分析师建立从问题发现、假设验证到落地建议的完整分析框架。

**当前版本**：v0.4（进行中）
- v0.1 ✅ 知识骨架（56个知识点 + MOC索引）
- v0.2 ✅ 问题引入章节
- v0.3 ✅ 「好问」刻意练习系统（168个练习文件）
- v0.4 🚧 端到端实战项目（3个项目，部分完成）
- v0.5-v1.0 📋 反常识内容、软技能、诊断测试（规划中）

**目标受众**：具备统计基础的数据分析师（定制对象明确标注于 README）。

**维护者**：藤椒先生

---

## 技术栈与工具链

### 文档与知识管理
- **Obsidian**：课程主阅读器，利用 wikilink 双向链接构建知识图谱
- **Markdown**：全部内容载体，使用 YAML frontmatter 标注元数据
- **Git**：版本管理，提交信息遵循 `type: description` 格式

### 代码与数据
- **Python**：数据分析与建模代码
  - 核心库：`pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`, `seaborn`
  - 因果推断库：`econml`（项目中提及，部分 notebook 可能使用）
  - 环境：`jupyter`（notebook 运行）
- **数据格式**：CSV（模拟数据集）、Jupyter Notebook（`.ipynb`）

### 无传统构建系统
本项目**无 `pyproject.toml`、`package.json`、`Cargo.toml` 等传统配置文件**。它是一个纯内容型项目，不依赖编译构建或包管理器构建流程。

---

## 目录结构

```
.
├── README.md                          # 课程总索引：学习路径、快速导航
├── data-analysis-advanced.md          # 数据分析进阶指南：方法速查、规范手册
├── AGENTS.md                          # 本文件
│
├── .obsidian/                         # Obsidian 配置（图谱视图、工作区）
│
└── curriculum/                        # 课程核心内容
    ├── knowledge-points.md            # 知识点总清单（约45个）
    │
    ├── MOC-*.md                       # 9个主题/阶段索引（Map of Content）
    │   ├── MOC-阶段一-基础夯实.md
    │   ├── MOC-阶段二-方法进阶.md
    │   ├── MOC-阶段三-实战整合.md
    │   ├── MOC-因果推断.md
    │   ├── MOC-统计基础.md
    │   ├── MOC-AB实验.md
    │   ├── MOC-机器学习建模.md
    │   ├── MOC-文档写作.md
    │   └── MOC-业务场景.md
    │
    ├── stage-01-foundation/           # 阶段一：基础夯实
    │   ├── 01-causal-inference-basics/    # 因果推断基础（4个知识点）
    │   ├── 02-statistical-basics/         # 统计基础（7个知识点）
    │   └── 03-ab-testing/                 # AB实验全流程（7个知识点）
    │
    ├── stage-02-advanced/             # 阶段二：方法进阶
    │   ├── 04-causal-inference/           # 因果推断进阶（PSM/DID/DML）
    │   ├── 05-ml-modeling/                # 机器学习建模（XGBoost/SHAP/ALE等）
    │   └── 06-causal-ml/                  # 因果×机器学习交叉（因果森林/Meta-Learners）
    │
    ├── stage-03-practice/             # 阶段三：实战整合
    │   ├── 07-document-writing/           # 分析文档写作（6个知识点）
    │   ├── 08-business-scenarios/         # 业务场景实战（4个知识点）
    │   └── 09-tools-engineering/          # 工具与工程（4个知识点）
    │
    ├── projects/                      # 端到端实战项目
    │   ├── project-01-ecommerce-causal/   # 电商大促因果推断（PSM+DID+合成控制）
    │   ├── project-02-app-experiment/     # APP新功能AB实验（STAR框架）
    │   └── project-03-rider-pricing/      # 骑手配送费动态定价（因果森林+Meta-Learners）
    │
    ├── appendix/                      # 附录（预留目录，目前为空）
    │   ├── 01-math-refresher/
    │   ├── 02-code-templates/
    │   ├── 03-datasets/
    │   └── 04-resources/
    │
    ├── review/                        # 审校报告
    │   └── audit-report.md            # 53个文档的审校结果（总分87.0/100）
    │
    └── roadmap/                       # 路线图
        ├── versions.md                # 版本迭代计划
        └── future-features.md         # 未来功能清单
```

---

## 知识点目录组织规范

每个知识点是一个**独立目录**，遵循统一的文件结构：

```
<知识点目录>/
├── <知识点名称>.md          # 主概念文档（必须）
├── 参考资源.md               # 参考文献、扩展阅读
├── code/                     # Python 代码示例（可选）
│   └── simulation.py
└── exercises/                # 「好问」刻意练习（v0.3起）
    ├── GoodQuestions.md      # 5道分层问题（L1概念→L5综合）
    ├── GoodAnswers.md        # Hints引导 + 确定性Answer
    └── DigDeeper.md          # 追问链，触及本质
```

### 概念文档标准结构
每个 `.md` 概念文档包含以下章节（按此顺序）：
1. **YAML frontmatter**：`title`, `course-stage`, `course-order`, `tags`
2. **问题引入**：300-600字，从具体业务场景出发制造认知冲突
3. **核心概念**：理论定义、数学公式（LaTeX）
4. **关键假设**：方法成立的前提条件
5. **常见误区**：初学者易犯的错误
6. **行业使用经验**：3-4条大厂真实案例（美团、滴滴、字节等）
7. **下一步**：wikilink 链接到相关知识点

---

## 内容规范与风格指南

### 文档写作规范
- **语言**：全部使用中文，技术术语保留英文（如 SUTVA、ATE、CATE）
- **链接格式**：使用 Obsidian wikilink `[[路径/文件名|显示文本]]`
- **数学公式**：使用标准 LaTeX，乘号用 `\cdot` 或省略，求和标注上下标
- **数字表达规范**：
  - 百分比变化（AB实验）：`+X.XXpp` 或 `+X.XX%`
  - 相对变化：`+X.XX%（相对）`
  - 倍数关系：`约X.X倍`
  - 相关系数：精确到4位小数

### 代码规范
- Python 代码文件使用 UTF-8 编码
- 注释使用中文
- 代码示例需包含：导入、数据生成、核心逻辑、可视化、总结
- 设置随机种子保证可复现性：`np.random.seed(42)`

### Git 提交规范
```
type: description

类型说明：
- feat: 新功能/新内容
- docs: 文档更新
- fix: 修复错误
- chore: 杂项/清理
```

---

## 审校与质量控制

项目有一份详细的**审校报告**（`curriculum/review/audit-report.md`），覆盖53个文档，从三个维度评分：
- **知识点正确性**（40%）：公式、定义、假设
- **行业经验质量**（40%）：大厂实践、失败案例
- **案例真实性**（20%）：业务逻辑、数字合理性

**当前平均分：87.0/100**

### 已知系统性问题（高优先级）
1. **公式严谨性不足**：8个文档存在公式错误（CUPED、XGBoost正则化、E-value、DML得分函数、因果森林分裂准则、SHAP交互值）
2. **数字一致性**：案例中存在计算逻辑不一致，需统一"绝对提升(pp)"与"相对提升(%)"标注
3. **行业经验缺失**：7个文档完全缺失经验板块
4. **统计结论越界**：卡方检验文档存在方法论误用

**修复优先级**：P0（必须修复）→ P1（建议修复）→ P2（可选优化）

---

## 实战项目结构

每个项目遵循统一的目录结构：

```
project-XX-<name>/
├── README.md                    # 项目背景、STAR框架、阅读路径
├── data/
│   ├── raw/                     # 原始数据（CSV）
│   ├── processed/               # 清洗后数据（运行时生成）
│   ├── data-dictionary.md       # 数据字典
│   └── generate_data.py         # 数据生成脚本（部分项目）
├── notebooks/
│   ├── 01-*.ipynb               # 按序号执行的分析步骤
│   └── ...
├── report-template/
│   └── *-report-template.md     # 标准报告模板
├── solution/
│   └── reference-solution.md    # 参考答案
└── rubric/
    └── scoring-rubric.md        # 评分标准
```

### 项目执行方式
1. 阅读 `README.md` 了解背景
2. 按序号执行 `notebooks/*.ipynb`
3. 每个 notebook 中有 **TODO** 标记引导完成
4. 对照 `solution/reference-solution.md` 验证
5. 根据 `report-template` 撰写最终报告

---

## 使用方式

### Obsidian 用户
1. 用 Obsidian 打开 `curriculum/` 目录
2. 安装 Graph View 插件查看知识图谱
3. 通过 `[[wikilink]]` 在知识点间跳转
4. 使用标签 `#课程/基础夯实` 筛选阶段

### VS Code 用户
1. 用 VS Code 打开项目根目录
2. 安装 Markdown 插件和 Python 插件
3. `curriculum/**/code/` 目录下的 `.py` 文件可直接运行
4. 使用 Jupyter 插件运行交互式代码

---

## 安全与隐私注意事项

- 所有数据均为**模拟生成**，不含真实用户数据
- 数据生成脚本使用随机数，不依赖外部 API
- 项目中不包含密钥、Token 或敏感配置
- `.obsidian/` 目录仅包含编辑器配置，无个人信息

---

## 扩展与修改指南

### 添加新知识点
1. 在对应阶段目录下创建新目录，命名规范：`序号-英文标识/`
2. 按标准结构创建概念文档 + exercises/
3. 更新对应 MOC 索引文件
4. 更新 `knowledge-points.md`

### 添加新项目
1. 在 `curriculum/projects/` 下创建 `project-XX-<name>/`
2. 遵循统一项目结构（README + data + notebooks + report-template + solution + rubric）
3. 在 `README.md` 总索引中添加项目链接

### 修改现有内容时的注意事项
- **公式修改**：对照标准教材核对，参考 `review/audit-report.md` 中的 P0 问题列表
- **案例数字修改**：确保数学一致性，标注基线值
- **新增经验**：需具体到业务线、时间、数字、人物角色，至少包含1条"我们曾犯的错误"
- **链接修改**：确保 wikilink 路径正确，Obsidian 不会自动验证链接有效性

---

## 关键文件速查

| 文件 | 用途 |
|------|------|
| `README.md` | 课程总索引，学习路径入口 |
| `data-analysis-advanced.md` | 方法速查手册、分析规范、写作指南 |
| `curriculum/knowledge-points.md` | 全部知识点清单 |
| `curriculum/review/audit-report.md` | 审校报告，含已知问题清单 |
| `curriculum/roadmap/versions.md` | 版本迭代计划 |
| `curriculum/roadmap/future-features.md` | 未来功能与多形态扩展规划 |

---

*最后更新：2026-04-28*
*文档版本：v1.0*
