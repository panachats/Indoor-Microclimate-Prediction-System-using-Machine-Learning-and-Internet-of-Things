# Import the necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

import pickle

sns.set_style({'font.family': 'Times New Roman'})

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
        grid_x = [f'Grid{ref_point}_Heat_Index','Out4_Heat_Index','Window_State','Curtain_State','AC_State','Door_State']
        # grid_x = [f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index']
        grid_y = f'Grid{num}_Heat_Index'
        x = df[grid_x].values
        y = df[grid_y].values
        print(f'------------------> X= {grid_x}, y= {grid_y} <-------------------')

        # Split Data set
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7)
        # print(x_test)

        k_list = np.arange(1, 50, 1)
        params = {'n_neighbors': k_list, 'weights': ['uniform', 'distance'],
                  'algorithm': ['ball_tree', 'kd_tree', 'brute']}
        # params = {'n_neighbors': k_list, 'weights': ['uniform', 'distance'],}
        knn = KNeighborsRegressor()
        model = RandomizedSearchCV(knn, params, cv=10)
        model.fit(x_train, y_train)
        print(model)
        print(f'Hyper parameter is {model.best_params_}')