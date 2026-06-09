import matplotlib.pyplot as plt
import numpy as np
import random
import math
from utils.image_saver import save_figure

def gamma_vectorized(x):
    """向量化 Gamma 函数，处理 NumPy 数组"""
    return np.array([math.gamma(xi) if xi > 0 else np.nan for xi in x])

def plot_function():
    # 候选函数库
    functions = [
        {"name": r"$f(x)=e^{-x^2}$", "func": lambda x: np.exp(-x**2), "xlim": (-2, 2)},
        {"name": r"$f(x)=\frac{\sin x}{x}$", "func": lambda x: np.sinc(x/np.pi), "xlim": (-10, 10)},
        {"name": r"$f(x)=x^3 - x$", "func": lambda x: x**3 - x, "xlim": (-1.5, 1.5)},
        {"name": r"$f(x)=\frac{1}{1+x^2}$", "func": lambda x: 1/(1+x**2), "xlim": (-5, 5)},
        {"name": r"$\Gamma(x)$ (Gamma function)", "func": gamma_vectorized, "xlim": (0.1, 5)},   # 修复：使用向量化版本
    ]
    chosen = random.choice(functions)
    x = np.linspace(chosen["xlim"][0], chosen["xlim"][1], 500)
    y = chosen["func"](x)
    plt.figure(figsize=(6,4))
    plt.plot(x, y, 'b-', linewidth=2)
    plt.title(chosen["name"])
    plt.grid(True)
    save_figure("function_plot.png")
    return chosen["name"]

if __name__ == "__main__":
    print(plot_function())