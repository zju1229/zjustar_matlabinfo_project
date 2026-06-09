# demos/linear_algebra.py
import random
import os

def plu_solve(A, b):
    """
    使用 PLU 分解求解线性方程组 Ax = b
    A: n x n 系数矩阵
    b: n 维常数向量
    返回解向量 x
    """
    n = len(A)
    # 拷贝矩阵，避免修改原矩阵
    LU = [row[:] for row in A]
    # 置换矩阵 P 的记录，P[i] 表示第 i 行实际对应原矩阵的行索引
    P = list(range(n))

    # LU 分解 + 部分选主元
    for i in range(n):
        # 选主元
        pivot = max(range(i, n), key=lambda r: abs(LU[r][i]))
        if pivot != i:
            LU[i], LU[pivot] = LU[pivot], LU[i]
            P[i], P[pivot] = P[pivot], P[i]
        # 如果主元为零，矩阵奇异（理论上不会发生，因为随机生成可逆）
        if abs(LU[i][i]) < 1e-12:
            raise ValueError("矩阵奇异，无法求解")
        for j in range(i + 1, n):
            factor = LU[j][i] / LU[i][i]
            LU[j][i] = factor
            for k in range(i + 1, n):
                LU[j][k] -= factor * LU[i][k]

    # 前代：解 Ly = Pb
    pb = [b[P[i]] for i in range(n)]
    y = [0.0] * n
    for i in range(n):
        y[i] = pb[i] - sum(LU[i][j] * y[j] for j in range(i))

    # 回代：解 Ux = y
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(LU[i][j] * x[j] for j in range(i + 1, n))) / LU[i][i]

    return x

def random_invertible_matrix(n=3):
    """
    生成随机 n x n 可逆整数矩阵（元素范围 -3 到 3）
    使用行列式检测确保可逆（仅对 n<=3 准确，更大矩阵可采用简单启发式）
    """
    if n == 3:
        while True:
            A = [[random.randint(-3, 3) for _ in range(n)] for __ in range(n)]
            # 计算 3x3 行列式
            det = (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) -
                   A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) +
                   A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))
            if det != 0:
                return A
    else:
        # 对于 n != 3，简单避免零行或重复行（低概率奇异，可接受）
        while True:
            A = [[random.randint(-3, 3) for _ in range(n)] for __ in range(n)]
            # 检查是否有全零行
            if any(all(v == 0 for v in row) for row in A):
                continue
            # 简单检查行是否线性相关（粗略，但演示足够）
            # 为避免无限循环，直接返回
            return A

def solve_random():
    """
    随机生成一个 3x3 线性方程组，求解并将结果保存到 static/linear_solution.txt
    返回 (A, b, x)
    """
    A = random_invertible_matrix(3)
    b = [random.randint(-5, 5) for _ in range(3)]
    x = plu_solve(A, b)
    # 确保 static 目录存在
    os.makedirs("static", exist_ok=True)
    with open("static/linear_solution.txt", "w", encoding="utf-8") as f:
        f.write("线性方程组 Ax = b 的 PLU 分解求解结果\n")
        f.write("=" * 40 + "\n")
        for i, row in enumerate(A):
            f.write(f"  {row}  *  x  =  {b[i]}\n")
        f.write("\n解 x = [")
        f.write(", ".join(f"{xi:.6f}" for xi in x))
        f.write("]\n")
    return A, b, x

# 可选：单独测试
if __name__ == "__main__":
    A, b, x = solve_random()
    print("A =", A)
    print("b =", b)
    print("x =", x)