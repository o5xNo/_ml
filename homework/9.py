import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

matplotlib.rcParams['font.family'] = 'Microsoft JhengHei'  # Windows 微軟正黑體

# 產生假資料
np.random.seed(0)
X = 2 * np.random.rand(100, 1)  # 100 個隨機點，範圍 0~2
y = 4 + 3 * X + np.random.randn(100, 1)  # y = 4 + 3X + 雜訊

# 建立線性回歸模型並訓練
model = LinearRegression()
model.fit(X, y)

# 預測
X_new = np.array([[0], [2]])
y_predict = model.predict(X_new)

# 畫圖
plt.scatter(X, y, color='blue', label='資料點')
plt.plot(X_new, y_predict, color='red', linewidth=2, label='線性回歸擬合線')
plt.xlabel('X')
plt.ylabel('y')
plt.title('簡單線性回歸示意圖')
plt.legend()
plt.show()
