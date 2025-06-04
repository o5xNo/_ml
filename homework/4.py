import numpy as np

# 七段顯示器的真值表 (7-bit輸入)
seven_segment_truth_table = {
    0:  (1, 1, 1, 1, 1, 1, 0),
    1:  (0, 1, 1, 0, 0, 0, 0),
    2:  (1, 1, 0, 1, 1, 0, 1),
    3:  (1, 1, 1, 1, 0, 0, 1),
    4:  (0, 1, 1, 0, 0, 1, 1),
    5:  (1, 0, 1, 1, 0, 1, 1),
    6:  (1, 0, 1, 1, 1, 1, 1),
    7:  (1, 1, 1, 0, 0, 0, 0),
    8:  (1, 1, 1, 1, 1, 1, 1),
    9:  (1, 1, 1, 1, 0, 1, 1)
}

# 對應的 4-bit 二進位輸出 (目標)
binary_outputs = {
    0: (0, 0, 0, 0),
    1: (0, 0, 0, 1),
    2: (0, 0, 1, 0),
    3: (0, 0, 1, 1),
    4: (0, 1, 0, 0),
    5: (0, 1, 0, 1),
    6: (0, 1, 1, 0),
    7: (0, 1, 1, 1),
    8: (1, 0, 0, 0),
    9: (1, 0, 0, 1)
}

# 轉成 numpy 陣列，方便矩陣運算
X = np.array([seven_segment_truth_table[i] for i in range(10)])  # (10,7)
Y = np.array([binary_outputs[i] for i in range(10)])             # (10,4)

# 權重初始化 建立神經網路模型（1層）
W = np.random.randn(7, 4) * 0.1
b = np.zeros((1, 4))  # 加上偏差項

def sigmoid(x):
    return 1 / (1 + np.exp(-x)) # 將輸出壓縮在 0~1 之間

def sigmoid_grad(x):
    s = sigmoid(x)
    return s * (1 - s)

def predict(X, W, b):
    return sigmoid(X @ W + b) #X @ W：做矩陣乘法（形狀：(10,7) @ (7,4) → (10,4)）

def mse_loss(y_pred, y_true): #計算模型預測與實際目標之間的誤差（均方誤差 MSE）：
    return np.mean((y_pred - y_true) ** 2)

lr = 0.5
epochs = 5000

for epoch in range(epochs):
    z = X @ W + b
    y_pred = sigmoid(z)
    loss = mse_loss(y_pred, Y)

    grad_y = 2 * (y_pred - Y) / Y.shape[0]  #MSE的導數部分（dL/dy)
    grad_z = grad_y * sigmoid_grad(z) #鏈式法則：[dL/dz=(dL/dy)*(dy/dx)]
    grad_W = X.T @ grad_z
    grad_b = np.sum(grad_z, axis=0, keepdims=True)

    W -= lr * grad_W
    b -= lr * grad_b
    '''
    X (10x7)
    ↓
    線性轉換 (X @ W + b)
    ↓
    sigmoid 非線性轉換 → 預測值 y_pred (10x4)
    ↓
    計算損失 (MSE)
    ↓
    反向傳播：計算導數 → 得到 ∇W, ∇b
    ↓
    梯度下降更新 W 和 b
    ↓
    重複 5000 次
    '''


# 這個函數把 sigmoid 輸出轉成整數（0 或 1），對應數字的 4-bit 二進位。
def binary_predict(X, W, b):
    return np.round(predict(X, W, b)).astype(int)

for i in range(10):
    out = binary_predict(X[i].reshape(1, -1), W, b)[0]
    print(f"Input: {X[i]} -> Predicted: {out}")
