
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


df = pd.read_csv("D:\\Model\\[updated_2-67]reformat_datasets.csv", encoding="utf8")

ref_point = 9
grid_list = [1,2,3,4,5,6,7,8]

params_list = [
    {'n_neighbors': 36, 'weights': 'distance', 'algorithm': 'ball_tree'},
    {'n_neighbors': 13, 'weights': 'distance', 'algorithm': 'kd_tree'},
    {'n_neighbors': 9, 'weights': 'distance', 'algorithm': 'ball_tree'},
    {'n_neighbors': 13, 'weights': 'distance', 'algorithm': 'brute'},
    {'n_neighbors': 23, 'weights': 'distance', 'algorithm': 'brute'},
    {'n_neighbors': 9, 'weights': 'distance', 'algorithm': 'ball_tree'},
    {'n_neighbors': 12, 'weights': 'distance', 'algorithm': 'ball_tree'},
    {'n_neighbors': 13, 'weights': 'distance', 'algorithm': 'brute'}
]


for num in grid_list:
    grid_x = [f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index', 'Window_State', 'Curtain_State', 'AC_State',
              'Door_State']
    grid_y = f'Grid{num}_Heat_Index'
    x = df[grid_x].values
    y = df[grid_y].values
    print(f'------------------> X= {grid_x}, y= {grid_y} <-------------------')


    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=10)
    #
    # x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.25, random_state=10)

    print("Training set size:", x_train.shape[0])
    print("Validation set size:", x_val.shape[0])
    print("Test set size:", x_test.shape[0])

    first_params = params_list[num-1]
    print(f'{first_params}')
    knn_regressor1 = KNeighborsRegressor(n_neighbors=first_params['n_neighbors'], weights=first_params['weights'], algorithm= first_params['algorithm'])

    model_knn1 = knn_regressor1.fit(x_train, y_train)

    v_y_knn_pred1 = model_knn1.predict(x_val)
    vrmse = root_mean_squared_error(y_val, v_y_knn_pred1)
    print('Val RMSE:',round(vrmse, 2))

    # y_knn_pred1 = model_knn1.predict(x_test)
    # rmse = root_mean_squared_error(y_test, y_knn_pred1)
    # print('Test RMSE:',round(rmse, 2))


# import pandas as pd
# from sklearn.neighbors import KNeighborsRegressor
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import train_test_split
# import numpy as np
#
# # Load the dataset
# df = pd.read_csv("D:\\Model\\[updated_2-67]reformat_datasets.csv", encoding="utf8")
#
# ref_point = 9
# grid_list = [1, 2, 3, 4, 5, 6, 7, 8]
#
# params_list = [
#     {'n_neighbors': 36, 'weights': 'distance', 'algorithm': 'ball_tree'},
#     {'n_neighbors': 13, 'weights': 'distance', 'algorithm': 'kd_tree'},
#     {'n_neighbors': 9, 'weights': 'distance', 'algorithm': 'ball_tree'},
#     {'n_neighbors': 13, 'weights': 'distance', 'algorithm': 'brute'},
#     {'n_neighbors': 23, 'weights': 'distance', 'algorithm': 'brute'},
#     {'n_neighbors': 9, 'weights': 'distance', 'algorithm': 'ball_tree'},
#     {'n_neighbors': 12, 'weights': 'distance', 'algorithm': 'ball_tree'},
#     {'n_neighbors': 13, 'weights': 'distance', 'algorithm': 'brute'}
# ]
#
# # Initialize lists to store RMSE from each fold
# test_rmse_list = []
#
# for num in grid_list:
#     grid_x = [f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index', 'Window_State', 'Curtain_State', 'AC_State',
#               'Door_State']
#     grid_y = f'Grid{num}_Heat_Index'
#     x = df[grid_x].values
#     y = df[grid_y].values
#     print(f'------------------> X= {grid_x}, y= {grid_y} <-------------------')
#
#     # Split the data into training and test sets
#     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)
#
#     # Define the model with specified parameters
#     first_params = params_list[num - 1]
#     print(f'{first_params}')
#     knn_regressor1 = KNeighborsRegressor(n_neighbors=first_params['n_neighbors'], weights=first_params['weights'],
#                                          algorithm=first_params['algorithm'])
#
#     # Fit the model on the training data
#     model_knn = knn_regressor1.fit(x_train, y_train)
#
#     # Perform cross-validation and calculate RMSE
#     cv_rmse_scores = np.sqrt(-cross_val_score(model_knn, x_train, y_train, cv=10, scoring='neg_mean_squared_error'))
#
#     # Calculate the mean RMSE across all folds
#     mean_rmse = np.mean(cv_rmse_scores)
#     print("Mean RMSE:", round(mean_rmse,2))
#
#     # Append mean RMSE to the list
#     test_rmse_list.append(mean_rmse)
#
#


