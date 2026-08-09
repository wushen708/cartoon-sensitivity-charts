---
name: cartoon-sensitivity-charts
description: 卡通手绘风（马卡龙配色 + xkcd 线条）数据图表生成库，内置敏感性分析三件套（龙卷风图/三情景对比/盈亏平衡）及蛇形演进图、热力图、甘特图、金字塔、ROI 区间图等 9 种图型。This skill should be used when用户需要为报告生成偏卡通/二次元/手绘风的数据可视化图表，尤其是财务敏感性分析（tornado/scenario/breakeven）、分阶段路径图、路线图甘特图等；或用户明确要求"不要商务风"的图表时。
agent_created: true
---

# 卡通手绘风图表 · 敏感性分析可视化

## 用途

用 matplotlib 生成卡通手绘风（马卡龙配色 + xkcd 手绘线条 + 米白奶油底）的数据图表，避免商务风。核心场景是报告的**敏感性分析三件套**：龙卷风图、三情景对比、盈亏平衡图；同时提供蛇形演进图、供给热力图、甘特图、金字塔、区间对比、基础柱状图。

## 工作流程

1. 确认环境：任一装有 `matplotlib` 和 `numpy` 的 Python 3 即可。
2. 将 `scripts/cartoon_charts.py` 复制到工作目录（或直接 import 其路径），按需调用图表函数。
3. 绘图前必读 `references/style-guide.md` 中的**避坑清单**（CJK 豆腐块、深底白字糊团、对数轴冗余刻度等，均为已验证的实际问题）。
4. 所有绘图调用必须包在 `run_with_xkcd(...)` 中——它负责进入 xkcd 手绘 context 并修复中文字体。
5. 生成后务必打开图片检查：中文渲染、标签重叠、基准线/图例遮挡，发现问题按 style-guide.md 调整。

## 快速示例

```python
from cartoon_charts import run_with_xkcd, tornado, scenarios, breakeven, snake_roadmap

# 1. 龙卷风图：factors = (标签, 低值, 高值)，自动按影响幅度排序
run_with_xkcd(lambda: tornado(-28.6, [
    ("单价 ±20%", -34.9, -22.3),
    ("销量达成率 50-150%", -44.3, -12.9),
    ("营销费用率 15-35%", -41.7, 10.6),
], "out/tornado.png", xlabel="净利润（万元）", unit=" 万"))

# 2. 三情景对比
run_with_xkcd(lambda: scenarios({"悲观": -57.8, "基准": -28.6, "乐观": 28.2},
                                "out/scenarios.png", ylabel="净利润（万元）", unit=" 万"))

# 3. 盈亏平衡（自动计算并标注各费用率下的保本销量）
run_with_xkcd(lambda: breakeven(price=580, gm=0.50, pf=0.08, fixed=60,
                                mkt_rates=[0.30, 0.20], rr=0.08,
                                planned_vol=4900, path="out/breakeven.png"))

# 4. 蛇形演进图（任意阶段数，自动左右交替排版）
run_with_xkcd(lambda: snake_roadmap([
    ("冷启动", "2017-2018", "微信群接龙试产\n首月仅售 300 元"),
    ("圈层渗透", "2019-2023", "种草视频引爆\nB站科普 + 抖音探访"),
    ("破圈", "2024", "综艺植入 + 自办展会"),
    ("平台收割", "2025", "类目第一 · 单日 250 万"),
], "out/snake.png", title="品牌四阶段路径"))
```

运行 `python3 scripts/cartoon_charts.py --demo /tmp/chart-demo` 可一次生成全部 9 种图型的示例，用于预览风格。

## 函数速查

| 函数 | 签名要点 |
|---|---|
| `tornado(base_value, factors, path, title, xlabel, unit)` | 敏感性龙卷风图 |
| `scenarios(values: dict, path, title, ylabel, unit)` | 三情景柱状图 |
| `breakeven(price, gm, pf, fixed, mkt_rates, path, planned_vol, rr)` | 盈亏平衡分析 |
| `snake_roadmap(stages, path, title)` | stages=(名称, 副标题, 描述) |
| `heatmap(matrix, row_labels, col_labels, path, star, title)` | 0-3 级密度热力图 |
| `gantt(tasks, path, milestones, title, xmax, xlabel)` | tasks=(名称, 开始, 时长) |
| `pyramid(layers, path, title)` | 梯队金字塔（自上而下） |
| `range_plot(items, path, title, xlabel, unit)` | items=(名称, 下限, 上限) |
| `pastel_bars(labels, values, path, title, ...)` | 通用柱状图 |

## 敏感性分析方法论（配合图表使用）

1. 先建基准模型（收入 = 单价 × 销量；净利 = 毛利 - 平台费 - 营销 - 固定成本）；
2. 龙卷风图单变量扰动，找出影响最大的变量（通常排序：费用率 ≈ 销量 > 毛利率 > 单价 > 材料价 > 退货率）；
3. 三情景做变量联动（悲观 = 多个不利假设叠加），展示整体风险敞口；
4. 盈亏平衡给出保本销量，并对照行业标杆的动销能力验证可行性；
5. 每个变量的扰动区间必须有出处（对标公司财报、行业价格波动、平台常规费率），在正文中标注来源与年份。
