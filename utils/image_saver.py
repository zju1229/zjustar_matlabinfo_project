import os
import matplotlib.pyplot as plt

def save_figure(filename, dpi=100):
    """保存当前 matplotlib 图形到 static 目录"""
    os.makedirs("static", exist_ok=True)
    plt.savefig(os.path.join("static", filename), dpi=dpi, bbox_inches='tight')
    plt.close()
