from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import pandas as pd

# df = pd.read_csv("D:\\Model\\forma_datasets.csv", encoding="utf8")
# df = pd.read_csv("D:\\Model\\forma_datasetsver2.csv", encoding="utf8")
df = pd.read_csv("D:\\Model\\[updated_2-67]reformat_datasets.csv", encoding="utf8")
ref_point_grid_lists = {
    1: [2, 3, 4, 5, 6, 7, 8, 9],
    2: [1, 3, 4, 5, 6, 7, 8, 9],
    3: [1, 2, 4, 5, 6, 7, 8, 9],
    4: [1, 2, 3, 5, 6, 7, 8, 9],
    5: [1, 2, 3, 4, 6, 7, 8, 9],
    6: [1, 2, 3, 4, 5, 7, 8, 9],
    7: [1, 2, 3, 4, 5, 6, 8, 9],
    8: [1, 2, 3, 4, 5, 6, 7, 9],
    9: [1, 2, 3, 4, 5, 6, 7, 8]
}

for ref_point in range(1, 10):
    print('______________________ Select Point', ref_point, '______________________')
    for num in ref_point_grid_lists[ref_point]:
        # grid_x = [f'Grid{ref_point}_Heat_Index','Out4_Heat_Index','Window_State','Curtain_State','AC_State','Door_State']
        grid_x = [f'Grid{ref_point}_Heat_Index']
        grid_y = f'Grid{num}_Heat_Index'
        x = df[grid_x].values
        y = df[grid_y].values
        print(f'------------------> X= {grid_x}, y= {grid_y} <-------------------')

        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=10)

        svpl = SVR()
        # svpl = SVR('rbf')
        # params = {'kernel':['rbf','poly']}
        # params = {'C': [1, 5, 10, 15], 'gamma': [1, 10, 50, 100]}
        # params = {'kernel':['rbf','poly'], 'C': [0.2, 0.8, 1.0, 10.0], 'gamma':[0.5,1.0,3.0,7.0,10.0]}
        params = {'kernel':['linear','rbf']}
        model = GridSearchCV(svpl, params, cv=10, verbose=3)
        model.fit(x_train,y_train)
        print(f'Hyper parameter is {model.best_params_}')