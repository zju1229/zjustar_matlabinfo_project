import numpy as np
import matplotlib.pyplot as plt
import random
from utils.image_saver import save_figure

def mandelbrot(c, max_iter):
    """计算单个点c的逃逸时间"""
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    """生成Mandelbrot集的逃逸时间数组（向量化加速）"""
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C, dtype=np.complex128)
    img = np.zeros(C.shape, dtype=int)
    
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        img[mask] = i + 1
    # 未逃逸的点设为 max_iter
    img[img == 0] = max_iter
    return img

def plot_mandelbrot():
    # 预定义几个有趣的区域
    regions = [
        {"xmin": -2.0, "xmax": 1.0, "ymin": -1.2, "ymax": 1.2, "name": "Full Set"},
        {"xmin": -0.75, "xmax": -0.5, "ymin": 0.0, "ymax": 0.25, "name": "Seahorse Valley"},
        {"xmin": -0.2, "xmax": 0.1, "ymin": 0.8, "ymax": 1.0, "name": "Tail"},
        {"xmin": -1.5, "xmax": -1.0, "ymin": -0.1, "ymax": 0.2, "name": "Left Side"},
    ]
    chosen = random.choice(regions)
    width, height = 600, 600
    max_iter = 200
    img = mandelbrot_set(chosen["xmin"], chosen["xmax"], chosen["ymin"], chosen["ymax"],
                         width, height, max_iter)
    
    plt.figure(figsize=(6,6))
    plt.imshow(img, extent=[chosen["xmin"], chosen["xmax"], chosen["ymin"], chosen["ymax"]],
               cmap='hot', origin='lower')
    plt.colorbar(label='Iterations')
    plt.title(f"Mandelbrot Set - {chosen['name']}")
    save_figure("mandelbrot.png")
    return chosen["name"]
if __name__ == "__main__":
    print(plot_mandelbrot())