# -*- coding: utf-8 -*-
"""
cartoon_charts.py — 卡通手绘风图表库（马卡龙配色 + xkcd 手绘线条）

用法（作为模块导入）：
    from cartoon_charts import run_with_xkcd, newfig, stylize, save
    from cartoon_charts import tornado, scenarios, snake_roadmap, ...

或直接运行 demo（生成所有图表示例到指定目录）：
    python3 cartoon_charts.py --demo /path/to/outdir

依赖：matplotlib、numpy
中文字体：macOS 用 PingFang SC；其他平台见 set_cjk_font()
"""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------- 风格常量
# 马卡龙/二次元配色（可按需替换，保持低饱和高明度即可）
PASTEL = ["#FFB3C7", "#9BD1FF", "#FFE08A", "#A8E6B0", "#D5B3FF",
          "#FFCF9E", "#8FE3E0", "#F6A6B2", "#B7E4A8", "#FFC6E8"]
INK = "#3D3D5C"      # 线条/文字主色（深蓝灰，比纯黑柔和）
BG = "#FFFDF5"       # 米白背景（奶油纸感）
SUBTLE = "#6B6B85"   # 次级文字
ACCENT = "#FF5C8A"   # 强调色（星标/高亮框）


def set_cjk_font():
    """按平台选择可用的中文字体。xkcd 模式会覆盖字体，必须在 context 内调用。"""
    from matplotlib import font_manager
    available = {f.name for f in font_manager.fontManager.ttflist}
    for cand in ["PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
                 "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Micro Hei",
                 "Arial Unicode MS"]:
        if cand in available:
            return cand
    return "sans-serif"


def run_with_xkcd(fn):
    """在手绘风 context 中执行绘图函数，并修复 CJK 字体（关键！）。

    plt.xkcd() 会把 font.family 改成 xkcd/Comic Sans 等西文字体，
    导致中文全部缺字形（豆腐块）。必须在 context 内重置 font.family。
    """
    with plt.xkcd():
        font = set_cjk_font()
        plt.rcParams["font.family"] = [font]
        plt.rcParams["font.sans-serif"] = [font]
        plt.rcParams["axes.unicode_minus"] = False
        fn()


def newfig(w=9, h=5.5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG)
    return fig, ax


def stylize(ax, title, xlabel="", ylabel=""):
    ax.set_title(title, fontsize=17, color=INK, pad=14, fontweight="bold")
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12, color=INK)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12, color=INK)
    ax.tick_params(colors=INK, labelsize=10)
    for s in ax.spines.values():
        s.set_color(INK)
    ax.set_facecolor(BG)


def save(fig, path):
    """保存到指定路径（自动建目录），统一米白底 150dpi。"""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)
    print("saved", path)


# ---------------------------------------------------------------- 1. 龙卷风图（敏感性分析）
def tornado(base_value, factors, path, title="敏感性分析（龙卷风图）",
            xlabel="目标值", unit=""):
    """单变量敏感性龙卷风图。

    base_value: 基准情景下的目标值（如基准净利）
    factors: list of (label, low_value, high_value)，按影响幅度自动排序（最大在顶部）
    """
    items = sorted(factors, key=lambda kv: abs(kv[2] - kv[1]))  # 小→大，barh 自下而上
    names = [k for k, _, _ in items]
    lows = [v[1] for v in items]
    highs = [v[2] for v in items]
    fig, ax = newfig(9, 0.9 * len(names) + 2)
    for i, (lo, hi) in enumerate(zip(lows, highs)):
        ax.barh(i, hi - base_value, left=base_value, color=PASTEL[3], edgecolor=INK, linewidth=1.5)
        ax.barh(i, lo - base_value, left=base_value, color=PASTEL[0], edgecolor=INK, linewidth=1.5)
        ax.text(min(lo, base_value) - (max(highs) - min(lows)) * 0.015, i, f"{lo:g}{unit}",
                va="center", ha="right", fontsize=10, color=INK)
        ax.text(max(hi, base_value) + (max(highs) - min(lows)) * 0.015, i, f"{hi:g}{unit}",
                va="center", ha="left", fontsize=10, color=INK)
    ax.axvline(base_value, color=INK, lw=2, linestyle="--")
    ax.text(base_value, len(names) + 0.15, f"基准 {base_value:g}{unit}",
            ha="center", fontsize=11, color=INK, fontweight="bold")
    ax.set_ylim(-0.6, len(names) + 0.7)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=11, color=INK)
    stylize(ax, title, xlabel=xlabel)
    ax.set_xlim(min(lows + [base_value]) * 1.25, max(highs + [base_value]) * 1.25)
    save(fig, path)


# ---------------------------------------------------------------- 2. 三情景对比
def scenarios(values, path, title="情景测算对比", ylabel="目标值", unit=""):
    """悲观/基准/乐观柱状图，负值自动用粉色、正值用绿色。"""
    names = list(values.keys())
    vals = list(values.values())
    span = max(vals) - min(vals) or 1
    colors = [PASTEL[0] if v < 0 else PASTEL[3] for v in vals]
    fig, ax = newfig(8, 5)
    bars = ax.bar(names, vals, color=colors, edgecolor=INK, linewidth=2)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2,
                v + span * 0.04 if v >= 0 else v - span * 0.09,
                f"{v:g}{unit}", ha="center", fontsize=13, color=INK, fontweight="bold")
    ax.axhline(0, color=INK, lw=1.5)
    stylize(ax, title, ylabel=ylabel)
    ax.set_ylim(min(vals) - span * 0.35, max(vals) + span * 0.35)
    save(fig, path)


# ---------------------------------------------------------------- 3. 盈亏平衡
def breakeven(price, gm, pf, fixed, mkt_rates, path, planned_vol=None,
              rr=0.0, title="盈亏平衡分析", xmax=10000):
    """边际贡献曲线 vs 固定成本+不同营销费率的总成本曲线。

    price: 平均单价; gm: 毛利率; pf: 平台费率; fixed: 固定成本
    mkt_rates: list of 营销费率（每条成本线一个）
    planned_vol: 计划销量（画参考竖线）; rr: 退货率
    """
    fig, ax = newfig(9, 5.5)
    vol = np.linspace(0, xmax, 100)
    unit_contrib = price * (1 - rr) * (gm - pf)          # 每单位边际贡献（未扣营销）
    ax.plot(vol, unit_contrib * vol / 1e4, color="#3D7BC2", lw=3,
            label="边际贡献（毛利-平台费）")
    colors = ["#FF5C8A", "#8a5a00", "#7B4FB3"]
    for k, m in enumerate(mkt_rates):
        cost = fixed + price * (1 - rr) * m * vol / 1e4
        ax.plot(vol, cost, color=colors[k % 3], lw=3, ls="--",
                label=f"固定成本+营销({m:.0%})")
        cm = gm - pf - m
        if cm > 0:
            be = fixed * 1e4 / (price * cm)
            ax.axvline(be, color=colors[k % 3], lw=1.5, ls=":")
            ax.text(be + xmax * 0.01, max(fixed, unit_contrib * xmax / 1e4) * 0.15 + k * fixed * 0.35,
                    f"{be:,.0f} 件", color=colors[k % 3], fontsize=11, fontweight="bold")
    if planned_vol:
        ax.axvline(planned_vol, color=PASTEL[4], lw=2, ls="-.")
        ax.text(planned_vol * 1.01, unit_contrib * xmax / 1e4 * 0.85,
                f"计划 {planned_vol:,.0f} 件", color="#7B4FB3", fontsize=10, fontweight="bold")
    ax.legend(fontsize=10, facecolor=BG, edgecolor=INK, loc="upper left")
    stylize(ax, title, xlabel="销量（件）", ylabel="金额（万元）")
    save(fig, path)


# ---------------------------------------------------------------- 4. 蛇形演进图
def snake_roadmap(stages, path, title="演进路径"):
    """S 形蛇形路径图，适合「分阶段路径/发展历程」。

    stages: list of (节点名, 时间/副标题, 描述(支持\n))，数量任意，自动左右交替
    """
    n = len(stages)
    fig, ax = newfig(10.5, max(6, 1.7 * n))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    t = np.linspace(0, 1, 400)
    y = 0.94 - 0.86 * t
    x = 0.5 - 0.28 * np.sin(np.pi * n * t)   # f=n/2 时 n 个节点恰好交替落在波峰/波谷
    ax.plot(x, y, color=INK, lw=4.5, zorder=1)
    ax.plot(x, y, color="#FF9FBE", lw=1.8, zorder=2)
    ax.annotate("", xy=(x[-1], y[-1] - 0.02), xytext=(x[-6], y[-6]),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=4.5, mutation_scale=35))
    nums = "①②③④⑤⑥⑦⑧⑨⑩"
    for k, (name, period, desc) in enumerate(stages):
        tt = (2 * k + 1) / (2 * n)
        ny = 0.94 - 0.86 * tt
        nx = 0.5 - 0.28 * np.sin(np.pi * n * tt)
        left = nx < 0.5
        ax.scatter([nx], [ny], s=2600, color=PASTEL[k % len(PASTEL)],
                   edgecolor=INK, linewidth=2.5, zorder=3)
        ax.text(nx, ny, nums[k], ha="center", va="center", fontsize=17,
                color=INK, fontweight="bold", zorder=4)
        tx = nx + 0.16 if left else nx - 0.16
        ha = "left" if left else "right"
        ax.text(tx, ny + 0.055, f"{name} · {period}", ha=ha, fontsize=13.5,
                color=INK, fontweight="bold", zorder=4)
        ax.text(tx, ny - 0.045, desc, ha=ha, va="top", fontsize=11,
                color=SUBTLE, zorder=4, linespacing=1.6)
    ax.set_title(title, fontsize=17, color=INK, fontweight="bold", pad=16)
    save(fig, path)


# ---------------------------------------------------------------- 5. 供给/机会热力图
def heatmap(matrix, row_labels, col_labels, path, star=None, star_label="★ 主攻区",
            title="密度热力图"):
    """离散等级热力图（0-3 级），手绘方格风。

    matrix: 二维 list，值 0-3（空白/稀少/竞争/红海）
    star: (row, col) 高亮框位置；自动带箭头标注
    """
    colors_map = {0: "#FFFFFF", 1: "#C9E7FF", 2: "#7FB8F0", 3: "#5B93D6"}
    labels_map = {0: "空白", 1: "稀少", 2: "竞争", 3: "红海"}
    m = np.array(matrix)
    nr, nc = m.shape
    fig, ax = newfig(2.2 * nc, 1.6 * nr + 1.5)
    for i in range(nr):
        for j in range(nc):
            v = int(m[i, j])
            ax.add_patch(plt.Rectangle((j, nr - 1 - i), 0.92, 0.92,
                                       facecolor=colors_map[v], edgecolor=INK, linewidth=2))
            ax.text(j + 0.46, nr - 1 - i + 0.46, labels_map[v], ha="center",
                    va="center", fontsize=10, color=INK, fontweight="bold")
    if star:
        si, sj = star
        ax.add_patch(plt.Rectangle((sj, nr - 1 - si), 0.92, 0.92, fill=False,
                                   edgecolor=ACCENT, linewidth=4))
        ax.annotate(star_label, xy=(sj + 0.46, nr - 1 - si + 0.92),
                    xytext=(sj + 1.8, nr - 1 - si + 1.5),
                    fontsize=12, color=ACCENT, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=ACCENT, lw=2))
    ax.set_xticks([j + 0.46 for j in range(nc)])
    ax.set_xticklabels(col_labels, fontsize=11, color=INK)
    ax.set_yticks([nr - 1 - i + 0.46 for i in range(nr)])
    ax.set_yticklabels(row_labels, fontsize=11, color=INK)
    ax.set_xlim(0, nc); ax.set_ylim(0, nr + 0.6)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title(title, fontsize=17, color=INK, fontweight="bold", pad=12)
    save(fig, path)


# ---------------------------------------------------------------- 6. 甘特图
def gantt(tasks, path, milestones=None, title="路线图", xmax=None, xlabel="月份"):
    """tasks: list of (任务名, 开始, 时长)；milestones: list of (x位置, 标签)"""
    fig, ax = newfig(10.5, 0.55 * len(tasks) + 1.5)
    end_max = 0
    for i, (name, start, dur) in enumerate(tasks):
        ax.barh(len(tasks) - 1 - i, dur, left=start, height=0.6,
                color=PASTEL[i % len(PASTEL)], edgecolor=INK, linewidth=1.8)
        ax.text(start + 0.15, len(tasks) - 1 - i, name, va="center", fontsize=9.5, color=INK)
        end_max = max(end_max, start + dur)
    for x, lab in (milestones or []):
        ax.axvline(x, color=ACCENT, lw=2, ls="--")
        ax.text(x, len(tasks) - 0.2, lab, ha="center", fontsize=10,
                color=ACCENT, fontweight="bold")
    stylize(ax, title, xlabel=xlabel)
    ax.set_xlim(0, xmax or end_max + 1)
    ax.set_yticks([])
    save(fig, path)


# ---------------------------------------------------------------- 7. 层级金字塔
def pyramid(layers, path, title="层级金字塔", width=8):
    """layers: 从上到下 list of 文本"""
    fig, ax = newfig(width, 2 * len(layers))
    y = len(layers)
    for k, text in enumerate(layers):
        w = 1.0 + 0.6 * k
        ax.fill_between([-w, w], y - 1, y, color=PASTEL[k % len(PASTEL)],
                        edgecolor=INK, linewidth=2)
        ax.text(0, y - 0.5, text, ha="center", va="center", fontsize=10.5,
                color=INK, fontweight="bold")
        y -= 1
    ax.set_xlim(-1.0 - 0.6 * len(layers) - 0.6, 1.0 + 0.6 * len(layers) + 0.6)
    ax.set_ylim(-0.2, len(layers) + 0.3)
    ax.axis("off")
    ax.set_title(title, fontsize=17, color=INK, fontweight="bold", pad=10)
    save(fig, path)


# ---------------------------------------------------------------- 8. 区间对比（ROI/ROAS）
def range_plot(items, path, title="区间对比", xlabel="数值", unit=""):
    """items: list of (名称, 下限, 上限)，画圆头区间线"""
    fig, ax = newfig(9, 1.1 * len(items) + 1.5)
    for i, (name, lo, hi) in enumerate(items):
        ax.plot([lo, hi], [i, i], lw=10, solid_capstyle="round",
                color=PASTEL[i % len(PASTEL)], zorder=2)
        ax.scatter([lo, hi], [i, i], s=120, color=INK, zorder=3)
        ax.text(hi * 1.03 + 0.1, i, f"{lo:g}-{hi:g}{unit}", va="center",
                fontsize=11, color=INK, fontweight="bold")
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([n for n, _, _ in items], fontsize=11, color=INK)
    stylize(ax, title, xlabel=xlabel)
    ax.set_xlim(0, max(h for _, _, h in items) * 1.25)
    save(fig, path)


# ---------------------------------------------------------------- 9. 基础柱状图
def pastel_bars(labels, values, path, title="", xlabel="", ylabel="",
                fmt="{v:g}", rotate=False):
    fig, ax = newfig(max(8, 1.2 * len(labels)), 5.5)
    bars = ax.bar(labels, values, color=PASTEL[:len(labels)], edgecolor=INK, linewidth=2)
    vmax = max(values)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + vmax * 0.02, fmt.format(v=v),
                ha="center", fontsize=12, color=INK, fontweight="bold")
    stylize(ax, title, xlabel=xlabel, ylabel=ylabel)
    if rotate:
        plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    ax.set_ylim(0, vmax * 1.18)
    save(fig, path)


# ---------------------------------------------------------------- demo
def _demo(outdir):
    p = lambda name: os.path.join(outdir, name)
    run_with_xkcd(lambda: tornado(-28.6, [
        ("单价 ±20%", -34.9, -22.3), ("销量达成率 50-150%", -44.3, -12.9),
        ("毛利率 45-55%", -41.7, -15.6), ("营销费用率 15-35%", -41.7, 10.6),
        ("退货率 5-15%", -31.0, -27.6), ("材料价 ±15%", -34.5, -22.7),
    ], p("demo_tornado.png"), title="首年净利敏感性分析", xlabel="净利润（万元）", unit=" 万"))
    run_with_xkcd(lambda: scenarios({"悲观": -57.8, "基准": -28.6, "乐观": 28.2},
                                    p("demo_scenarios.png"), ylabel="净利润（万元）", unit=" 万"))
    run_with_xkcd(lambda: breakeven(580, 0.50, 0.08, 60, [0.30, 0.20],
                                    p("demo_breakeven.png"), planned_vol=4900, rr=0.08))
    run_with_xkcd(lambda: snake_roadmap([
        ("冷启动", "第 1 阶段", "小步验证\n跑通最小闭环"),
        ("渗透", "第 2 阶段", "内容种草\n积累核心用户"),
        ("破圈", "第 3 阶段", "事件营销\n大众曝光"),
        ("收割", "第 4 阶段", "平台承接\n复购经营"),
    ], p("demo_snake.png"), title="四阶段演进路径"))
    run_with_xkcd(lambda: heatmap(
        [[3, 2, 1, 0], [2, 3, 2, 1], [1, 2, 1, 2], [0, 1, 1, 2]],
        ["材质A", "材质B", "材质C", "材质D"], ["低价", "中低", "中高", "高价"],
        p("demo_heatmap.png"), star=(2, 2), title="供给密度热力图"))
    run_with_xkcd(lambda: gantt([("任务A", 0, 6), ("任务B", 4, 8), ("任务C", 10, 6)],
                                p("demo_gantt.png"), milestones=[(6, "阶段1→2")],
                                title="路线图甘特图", xmax=18))
    run_with_xkcd(lambda: pyramid(["头部：1-2 家", "中腰部：20-30 家", "长尾：200+ 家"],
                                  p("demo_pyramid.png"), title="梯队金字塔"))
    run_with_xkcd(lambda: range_plot([("渠道A", 1.5, 3), ("渠道B", 4, 9), ("渠道C", 5, 10)],
                                     p("demo_range.png"), title="渠道 ROI 区间", xlabel="ROI"))
    run_with_xkcd(lambda: pastel_bars(["A", "B", "C", "D"], [7.5, 4, 21, 73],
                                      p("demo_bars.png"), title="规模对比", ylabel="亿美元"))
    print("DEMO DONE ->", outdir)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", metavar="OUTDIR", help="生成全部图表示例到指定目录")
    args = ap.parse_args()
    if args.demo:
        _demo(args.demo)
    else:
        ap.print_help()
