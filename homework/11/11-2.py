import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
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
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

# 評估結果
print("🔍 模型：Random Forest")
print("準確率：", accuracy_score(y_test, y_pred))
print("分類報告：\n", classification_report(y_test, y_pred))

# 混淆矩陣
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["低機率", "高機率"], yticklabels=["低機率", "高機率"])
plt.title("Random Forest 的混淆矩陣")
plt.xlabel("預測值")
plt.ylabel("真實值")
plt.show()
