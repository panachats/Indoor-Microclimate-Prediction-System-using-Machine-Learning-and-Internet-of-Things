# To find best hyperparam
import warnings

warnings.filterwarnings('ignore')
import statistics
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import pandas as pd
from sklearn.metrics import r2_score

df = pd.read_csv("D:\\Model\\[updated_2-67]reformat_datasets.csv", encoding="utf8")

grid_x = [f'Grid8_Heat_Index', 'Out4_Heat_Index', 'Window_State', 'Curtain_State', 'AC_State',
          'Door_State']
# grid_x = [f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index']
grid_y = f'Grid1_Heat_Index'
x = df[grid_x].values
y = df[grid_y].values
print(f'------------------> X= {grid_x}, y= {grid_y} <-------------------')

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=10)

mlp_regressor = MLPRegressor(
    activation="logistic",
    solver="adam",
    hidden_layer_sizes=(420, 420),
    alpha=0.01,
    random_state=20,
    early_stopping=False,
    verbose=False,
)
nn = mlp_regressor.fit(x_train, y_train)
pred = nn.predict(x_test)
differences = []
max_count = 0
min_count = 0
for x in range(len(pred)):
    s = round(pred[x] - y_test[x], 2)
    differences.append(s)
    if s >= 1:
        max_count += 1
    elif s <= -1:
        min_count += 1

print(f'Total test : {len(pred)}')

print(f'Max differential : {max(differences)}')
print(f'Avg differential : {statistics.mean(differences)}')
print(f'Min differential : {min(differences)}')
print(f'Differential greater than 1 : {max_count}')
print(f'Differential less than -1 : {min_count}')
sumthan1 = max_count + min_count
print(f'Sum differential greater than and less than 1 : {sumthan1}')
mse = mean_squared_error(y_test, pred)
rmse = mean_squared_error(y_test, pred, squared=False)
print('MSE:', round(mse, 2))
print('RMSE:', round(rmse, 2))
print('R2', r2_score(y_test, pred))
