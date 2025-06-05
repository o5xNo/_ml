import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

matplotlib.rcParams['font.family'] = 'Microsoft JhengHei'  # Windows 微軟正黑體

# 載入資料
df = pd.read_csv(r'c:\Users\user\Desktop\人工智慧\_ml\homework\11\heart.csv')
X = df.drop('target', axis=1)
y = df['target']

# 分割資料集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 標準化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 建立模型
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

# 評估結果
print("🔍 模型：K-Nearest Neighbors")
print("準確率：", accuracy_score(y_test, y_pred))
print("分類報告：\n", classification_report(y_test, y_pred))

# 混淆矩陣
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["低機率", "高機率"], yticklabels=["低機率", "高機率"])
plt.title("KNN 的混淆矩陣")
plt.xlabel("預測值")
plt.ylabel("真實值")
plt.show()

# https://medium.com/@jason8410271027/%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-k%E8%BF%91%E9%84%B0%E6%BC%94%E7%AE%97%E6%B3%95-%E7%90%86%E8%AB%96-python%E5%AF%A6%E4%BD%9C-73c9bc9251c8