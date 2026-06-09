# demos/fractal_geometry.py
import matplotlib.pyplot as plt
import numpy as np
import random
from utils.image_saver import save_figure

# ------------------- 科赫雪花 -------------------
def koch_curve(p1, p2, depth):
    """返回科赫曲线的点列表 (p1, p2 为复数)"""
    if depth == 0:
        return [p1, p2]
    else:
        p3 = p1 + (p2 - p1) / 3
        p4 = p1 + 2 * (p2 - p1) / 3
        angle = np.pi / 3
        rotation = np.exp(1j * angle)
        p5 = p3 + (p4 - p3) * rotation
        # 递归，去掉中间重复点
        return (koch_curve(p1, p3, depth - 1)[:-1] +
                koch_curve(p3, p5, depth - 1)[:-1] +
                koch_curve(p5, p4, depth - 1)[:-1] +
                koch_curve(p4, p2, depth - 1))

def draw_koch_snowflake(depth):
    """绘制科赫雪花"""
    vertices = [0 + 0j, 1 + 0j, 0.5 + np.sqrt(3) / 2 * 1j]
    points = []
    for i in range(3):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % 3]
        points.extend(koch_curve(p1, p2, depth))
    xs = [p.real for p in points]
    ys = [p.imag for p in points]
    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, 'b-', linewidth=1)
    plt.axis('equal')
    plt.title(f"Koch Snowflake (depth={depth})")
    save_figure("koch_snowflake.png")
    return f"Koch雪花，迭代深度={depth}"

# ------------------- Weierstrass 函数 -------------------
def weierstrass(x, a, b, N):
    """计算 Weierstrass 函数在点 x 处的值"""
    val = 0.0
    for n in range(N + 1):
        val += (a ** n) * np.cos(b ** n * np.pi * x)
    return val

def draw_weierstrass(a, b, N, x_min, x_max):
    """绘制 Weierstrass 函数图像"""
    x = np.linspace(x_min, x_max, 1000)
    y = [weierstrass(xi, a, b, N) for xi in x]
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, 'r-', linewidth=0.8)
    plt.title(f"Weierstrass Function: a={a}, b={b}, N={N}\nContinuous but nowhere differentiable")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    save_figure("weierstrass.png")
    return f"Weierstrass函数，a={a}, b={b}, N={N}, x∈[{x_min},{x_max}]"

def random_weierstrass():
    """随机生成 Weierstrass 函数参数并绘制"""
    # 参数范围：a 在 (0,1) 内，b 为奇数且大于 1，N 足够大
    a = round(random.uniform(0.3, 0.7), 2)
    b = random.choice([3, 5, 7, 9])
    N = random.randint(20, 50)
    # 定义域随机选择
    intervals = [(-2, 2), (-1.5, 1.5), (-1, 1), (0, 2), (-2, 0)]
    x_min, x_max = random.choice(intervals)
    return draw_weierstrass(a, b, N, x_min, x_max)

# ------------------- 统一接口 -------------------
def generate_fractal():
    """
    随机选择科赫雪花或Weierstrass函数，生成图片并返回描述
    """
    choice = random.choice(["koch", "weierstrass"])
    if choice == "koch":
        depth = random.randint(2, 5)
        return draw_koch_snowflake(depth)
    else:
        return random_weierstrass()

# 单独测试
if __name__ == "__main__":
    print(generate_fractal())