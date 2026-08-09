# 卡通手绘风图表 · 风格规范与避坑指南

## 风格三要素

1. **手绘线条**：matplotlib `plt.xkcd()` context（所有线条带抖动手绘感）
2. **马卡龙配色**（低饱和、高明度，二次元/奶油感）：

| 色板 | HEX | 用途 |
|---|---|---|
| 粉 | `#FFB3C7` | 主数据 / 负值 / 悲观 |
| 蓝 | `#9BD1FF` | 次数据 / 对照组 |
| 黄 | `#FFE08A` | 高亮区 / 机会带 |
| 绿 | `#A8E6B0` | 正值 / 乐观 / 达标 |
| 紫 | `#D5B3FF` | 第三系列 / 计划参考线 |
| 橙 | `#FFCF9E` | 备用 |
| 青 | `#8FE3E0` | 备用 |
| 墨蓝灰 | `#3D3D5C` (INK) | 全部文字与描边（**不要用纯黑**） |
| 米白 | `#FFFDF5` (BG) | 背景（奶油纸感，**不要用纯白**） |
| 强调粉 | `#FF5C8A` (ACCENT) | 星标、高亮框、里程碑线 |
| 灰紫 | `#6B6B85` (SUBTLE) | 次级说明文字 |

3. **描边规则**：所有色块带 `edgecolor=INK, linewidth=1.5~2.5`，文字加粗（`fontweight="bold"`），dpi=150

## 关键避坑（都是实际踩过的坑）

1. **CJK 豆腐块（最高频）**：`plt.xkcd()` 会把 `font.family` 覆盖成 xkcd/Comic Sans MS，
   中文全部缺字形。必须在 context **内部**重置：
   ```python
   with plt.xkcd():
       plt.rcParams["font.family"] = ["PingFang SC"]   # 见 set_cjk_font()
   ```
   只设 `font.sans-serif` 不够，必须设 `font.family`。
2. **深底白字糊团**：饱和底色（如 `#3D7BC2`）上的白色加粗文字在手绘风下会糊成白团。
   规则：**热力图/色块内统一用 INK 深色字**，需要拉开对比时把填充色调浅（如 `#5B93D6`）。
3. **对数轴冗余刻度**：`set_xscale("log")` 后 `set_xticks` 仍可能冒出 `3×10²` 之类的次要刻度。
   用 `FixedLocator` + `NullFormatter`：
   ```python
   ax.xaxis.set_major_locator(FixedLocator([200, 500, 1000, 2000, 5000]))
   ax.xaxis.set_minor_formatter(NullFormatter())
   ```
4. **标签重叠**：散点/气泡图标注必须逐点指定 `xytext` 偏移和 `ha`（左点向右偏、右点向左偏），
   不要偷懒统一 `(0, 16)`。
5. **龙卷风图基准线标签**：`axvline` 的文字放 `len(names)+0.15` 并 `set_ylim(-0.6, len+0.7)` 留头部空间，避免压在最上方条上。
6. **中文字体回退顺序**：PingFang SC → Hiragino Sans GB → Microsoft YaHei → Noto Sans CJK SC →
   Source Han Sans SC → WenQuanYi Micro Hei → Arial Unicode MS（`set_cjk_font()` 已内置）。

## 各图表适用场景

| 函数 | 场景 |
|---|---|
| `tornado` | 敏感性分析核心图：单变量对目标值的影响排序（最大影响在顶部） |
| `scenarios` | 悲观/基准/乐观三情景联动对比（负值自动粉色、正值绿色） |
| `breakeven` | 盈亏平衡：边际贡献线 vs 多条成本线（不同费用率），自动标注保本量 |
| `snake_roadmap` | 分阶段路径/发展历程/营销路径（任意节点数，自动左右交替） |
| `heatmap` | 价格带×材质等双维度供给/机会密度（0-3 级离散色块） |
| `gantt` | 产品路线图/项目排期，支持里程碑虚线 |
| `pyramid` | 品牌梯队/用户分层 |
| `range_plot` | 多渠道 ROI/ROAS 区间对比（圆头区间线） |
| `pastel_bars` | 通用柱状图（市场规模等） |

## 敏感性分析的标准组合（三件套）

1. **龙卷风图**：先把每个变量单独扰动，展示影响排序 → 找出关键变量
2. **三情景表/图**：把关键变量联动（悲观=单价-10%×达成率50%×费用率上限）→ 展示整体风险敞口
3. **盈亏平衡图**：固定成本 ÷（单价×边际贡献率），画出不同费用率下的保本销量，并标注计划销量参考线

参数区间必须有行业依据（如对标公司费率、品类价格波动范围），在报告正文中标注来源。
