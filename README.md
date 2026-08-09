# cartoon-sensitivity-charts

卡通手绘风（马卡龙配色 + xkcd 手绘线条）的数据图表库，内置**敏感性分析三件套**（龙卷风图 / 三情景对比 / 盈亏平衡），以及蛇形演进图、供给热力图、甘特图、金字塔、ROI 区间图等 9 种图型。既是一个独立的 Python 图表库，也是一个开箱即用的 WorkBuddy / Claude Code Skill。

A cartoon hand-drawn chart library (macaron palette + xkcd lines) for matplotlib, featuring a sensitivity-analysis toolkit (tornado / scenarios / breakeven) plus snake roadmap, heatmap, gantt, pyramid and ROI range charts. Works as a standalone Python module or as a WorkBuddy / Claude Code skill.

## 效果预览

运行一行命令生成全部 9 种图型的示例：

```bash
pip install matplotlib numpy
python3 scripts/cartoon_charts.py --demo ./chart-demo
```

## 安装 / Install

**作为 Python 库使用**：直接复制 `scripts/cartoon_charts.py` 到你的项目，import 即可。依赖只有 `matplotlib` 和 `numpy`。

**作为 WorkBuddy / Claude Code Skill 使用**：

```bash
git clone https://github.com/wushen708/cartoon-sensitivity-charts.git ~/.workbuddy/skills/cartoon-sensitivity-charts
```

之后在对话中说「用卡通手绘风画一张敏感性分析龙卷风图」即可自动触发。

## 快速上手 / Quick Start

```python
from cartoon_charts import run_with_xkcd, tornado, scenarios, breakeven, snake_roadmap

# 龙卷风图（敏感性分析）
run_with_xkcd(lambda: tornado(-28.6, [
    ("单价 ±20%", -34.9, -22.3),
    ("销量达成率 50-150%", -44.3, -12.9),
    ("营销费用率 15-35%", -41.7, 10.6),
], "out/tornado.png", xlabel="净利润（万元）", unit=" 万"))

# 三情景对比
run_with_xkcd(lambda: scenarios({"悲观": -57.8, "基准": -28.6, "乐观": 28.2},
                                "out/scenarios.png", ylabel="净利润（万元）", unit=" 万"))

# 盈亏平衡（自动标注保本销量）
run_with_xkcd(lambda: breakeven(price=580, gm=0.50, pf=0.08, fixed=60,
                                mkt_rates=[0.30, 0.20], rr=0.08,
                                planned_vol=4900, path="out/breakeven.png"))

# 蛇形演进图（分阶段路径，任意节点数）
run_with_xkcd(lambda: snake_roadmap([
    ("冷启动", "第 1 阶段", "小步验证\n跑通最小闭环"),
    ("渗透", "第 2 阶段", "内容种草\n积累核心用户"),
    ("破圈", "第 3 阶段", "事件营销\n大众曝光"),
    ("收割", "第 4 阶段", "平台承接\n复购经营"),
], "out/snake.png", title="四阶段演进路径"))
```

## 图型速查 / Chart Types

| 函数 | 场景 |
|---|---|
| `tornado` | 敏感性分析：单变量对目标值的影响排序 |
| `scenarios` | 悲观/基准/乐观三情景联动对比 |
| `breakeven` | 盈亏平衡：边际贡献 vs 成本线，自动标注保本量 |
| `snake_roadmap` | 分阶段路径 / 发展历程 / 营销路径 |
| `heatmap` | 双维度供给/机会密度（0-3 级离散色块） |
| `gantt` | 产品路线图 / 项目排期，支持里程碑 |
| `pyramid` | 品牌梯队 / 用户分层 |
| `range_plot` | 多渠道 ROI/ROAS 区间对比 |
| `pastel_bars` | 通用柱状图 |

## 风格规范

完整配色表与避坑清单（CJK 字体修复、深底白字、对数轴刻度等）见 [references/style-guide.md](references/style-guide.md)。

要点：
- 所有绘图必须包在 `run_with_xkcd(...)` 中（自动修复 xkcd 模式下的中文豆腐块问题）
- 中文字体自动回退：PingFang SC → Hiragino Sans GB → Microsoft YaHei → Noto Sans CJK SC → …

## License

MIT © wushen708
