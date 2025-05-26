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

# 權重初始化
W = np.random.randn(7, 4) * 0.1
b = np.zeros((1, 4))  # 加上偏差項

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_grad(x):
    s = sigmoid(x)
    return s * (1 - s)

def predict(X, W, b):
    return sigmoid(X @ W + b)

def mse_loss(y_pred, y_true):
    return np.mean((y_pred - y_true) ** 2)

lr = 0.5
epochs = 5000

for epoch in range(epochs):
    z = X @ W + b
    y_pred = sigmoid(z)
    loss = mse_loss(y_pred, Y)

    grad_y = 2 * (y_pred - Y) / Y.shape[0]
    grad_z = grad_y * sigmoid_grad(z)
    grad_W = X.T @ grad_z
    grad_b = np.sum(grad_z, axis=0, keepdims=True)

    W -= lr * grad_W
    b -= lr * grad_b

# 預測並四捨五入
def binary_predict(X, W, b):
    return np.round(predict(X, W, b)).astype(int)

for i in range(10):
    out = binary_predict(X[i].reshape(1, -1), W, b)[0]
    print(f"Input: {X[i]} -> Predicted: {out}")
