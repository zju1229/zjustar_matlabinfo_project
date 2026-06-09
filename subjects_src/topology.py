# demos/topology.py
import matplotlib.pyplot as plt
import numpy as np
import random
from mpl_toolkits.mplot3d import Axes3D
from utils.image_saver import save_figure

def plot_mobius():
    """绘制莫比乌斯带，随机颜色映射和视角，返回描述字符串"""
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # 参数网格
    u = np.linspace(0, 2 * np.pi, 100)   # 环绕角度
    v = np.linspace(-0.5, 0.5, 50)       # 宽度方向
    u, v = np.meshgrid(u, v)
    
    # 莫比乌斯带参数方程
    r = 1 + v * np.cos(u / 2)
    x = r * np.cos(u)
    y = r * np.sin(u)
    z = v * np.sin(u / 2)
    
    # 随机选择颜色映射
    cmap_choices = ['viridis', 'plasma', 'inferno', 'magma', 'coolwarm', 'cividis', 'twilight']
    cmap = random.choice(cmap_choices)
    
    # 绘制曲面
    surf = ax.plot_surface(x, y, z, cmap=cmap, edgecolor='none', alpha=0.9)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Height')
    
    # 随机视角 (仰角, 方位角)
    elev = random.randint(20, 50)
    azim = random.randint(30, 150)
    ax.view_init(elev=elev, azim=azim)
    
    ax.set_title(f"Möbius Strip (colormap={cmap})")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    save_figure("mobius.png")
    return f"莫比乌斯带，颜色映射={cmap}，视角(elev={elev}, azim={azim})"

# 单独测试
if __name__ == "__main__":
    desc = plot_mobius()
    print(desc)