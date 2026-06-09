import os
import sys
import random
import feedparser
from datetime import datetime

# 添加 subjects_src 到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'subjects_src'))

# 导入五个模块
from real_analysis import plot_function
from complex_analysis import plot_mandelbrot
from linear_algebra import solve_random
from fractal_geometry import generate_fractal
from topology import plot_mobius

# 配置
STUDENT_ID = "3240101229"   # 请替换为你的学号
OUTPUT_DIR = "output_info"
STATIC_DIR = "static"

def ensure_dirs():
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_hot_keywords():
    try:
        feed = feedparser.parse("https://hnrss.org/frontpage?q=math")
        titles = [entry.title for entry in feed.entries[:5]]
        text = ' '.join(titles).lower()
        keywords = []
        for kw in ['integral', 'function', 'mandelbrot', 'fractal', 'koch', 'weierstrass', 'matrix', 'linear', 'mobius', 'topology']:
            if kw in text:
                keywords.append(kw)
        return keywords
    except Exception as e:
        print(f"获取热点失败: {e}，将使用随机选择")
        return []

def choose_module(keywords):
    if any(k in keywords for k in ['integral', 'function', 'gamma', 'sin']):
        return "real_analysis"
    if any(k in keywords for k in ['mandelbrot', 'fractal', 'koch', 'weierstrass']):
        return "fractal_geometry"
    if any(k in keywords for k in ['matrix', 'linear']):
        return "linear_algebra"
    if any(k in keywords for k in ['mobius', 'topology']):
        return "topology"
    return random.choice(["real_analysis", "fractal_geometry", "linear_algebra", "topology"])

def run_module(module_name):
    if module_name == "real_analysis":
        desc = plot_function()
    elif module_name == "fractal_geometry":
        desc = generate_fractal()
    elif module_name == "linear_algebra":
        A, b, x = solve_random()
        # 格式化输出，使其更美观
        lines = []
        lines.append("📐 线性方程组 Ax = b 的解：")
        lines.append("")  # 空行
        for i, row in enumerate(A):
            # 将矩阵行转换为字符串，并补齐宽度
            row_str = "  ".join(f"{val:4d}" if isinstance(val, int) else f"{val:6.2f}" for val in row)
            lines.append(f"  {row_str}   ·   x   =   {b[i]:4d}")
        lines.append("")
        lines.append(f"🔍 解向量 x = [{', '.join(f'{xi:.6f}' for xi in x)}]")
        desc = "<br>".join(lines)  # HTML 换行
    elif module_name == "topology":
        desc = plot_mobius()
    else:
        desc = "未知模块"
    return desc

def generate_html(module_name, description):
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_map = {
        "real_analysis": "function_plot.png",
        "linear_algebra": None,
        "topology": "mobius.png",
    }
    img_tag = ""
    if module_name == "fractal_geometry":
        if os.path.exists(os.path.join(STATIC_DIR, "koch_snowflake.png")):
            img_tag = f'<img src="../{STATIC_DIR}/koch_snowflake.png" alt="Koch Snowflake">'
        elif os.path.exists(os.path.join(STATIC_DIR, "weierstrass.png")):
            img_tag = f'<img src="../{STATIC_DIR}/weierstrass.png" alt="Weierstrass Function">'
    elif module_name in image_map and image_map[module_name]:
        img_tag = f'<img src="../{STATIC_DIR}/{image_map[module_name]}" alt="{module_name}">'
    
    # 读取宣传模板（如果存在）
    pro_html = ""
    template_path = os.path.join(os.path.dirname(__file__), "template.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            pro_html = f.read()
    else:
        pro_html = '<div class="card"><p>宣传模块加载失败，请检查 template.html 文件。</p></div>'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数学数字员工日报</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; background: #f0f2f5; }}
        .card {{ background: white; border-radius: 12px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #1e466e; text-align: center; }}
        h2 {{ color: #2c3e50; border-left: 5px solid #3498db; padding-left: 15px; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 8px; }}
        .footer {{ text-align: center; margin-top: 30px; color: #7f8c8d; font-size: 0.85em; }}
        button {{ background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-size: 1em; }}
        button:hover {{ background: #2980b9; }}
        pre {{ background: #f4f4f4; padding: 15px; overflow-x: auto; border-radius: 6px; }}
        .flex-img {{ display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>数学数字员工每日分析报告</h1>
        <p style="text-align:center;">生成时间：{today} | 学号：{STUDENT_ID}</p>
        <hr>
        <h2>今日智能体推荐：{module_name}</h2>
        {img_tag}
        <p><strong>分析详情：</strong> {description}</p>
    </div>
    {pro_html}
    <div class="footer">
        <p>本报告由数字员工自动生成 | 每日动态更新</p>
    </div>
</body>
</html>
"""
    output_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML 报告已生成: {output_path}")

def main():
    ensure_dirs()
    keywords = get_hot_keywords()
    print(f"今日热点关键词: {keywords}")
    module_name = choose_module(keywords)
    print(f"选中模块: {module_name}")
    description = run_module(module_name)
    generate_html(module_name, description)
    print("每日报告生成完成。")

if __name__ == "__main__":
    main()