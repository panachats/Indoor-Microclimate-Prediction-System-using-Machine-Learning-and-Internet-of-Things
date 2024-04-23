# ตัวอย่างการใช้ x เพื่อแทนพิกัดละติจูดและลองจิจูด และ y เป็นค่าอุณหภูมิ

import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

df = pd.read_csv("D:\\Model\\[updated_2-67]reformat_datasets.csv", encoding="utf8")

# x = np.linspace(-10, 10, 100).reshape(-1, 1)
# y = np.sin(x).ravel()  # ค่าอุณหภูมิที่เราต้องการทำนาย
df = df.head(100)
grid_x = ['Grid9_Heat_Index']
grid_y = 'Grid2_Heat_Index'
x = df[grid_x].values
y = df[grid_y].values
print(y)
# สร้างโมเดล SVR ด้วย kernel เป็น rbf
# svr_rbf = SVR(kernel='rbf', C=1.0, gamma=10.0)
svr_rbf = SVR(kernel='linear')
# svr_rbf = SVR(kernel='poly')

# ทำการ fit โมเดล
svr_rbf.fit(x, y)

# ทำนายผลลัพธ์
y_pred = svr_rbf.predict(x)

# พล็อตผลลัพธ์
plt.scatter(x, y, color='darkorange', label='data')  # พล็อตข้อมูลจริง
plt.plot(x, y_pred, color='navy', lw=2, label='RBF model')  # พล็อตการทำนาย
plt.xlabel('x')
plt.ylabel('Temperature (y)')
plt.title('Support Vector Regression for Temperature Prediction')
plt.legend()
plt.show()
