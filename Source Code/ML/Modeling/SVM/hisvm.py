import statistics
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
import os
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import numpy as np

# def plot_regression(x_test,y_test, y_svm_pred, ref_point, num):
#     plt.figure(figsize=(8, 6))
#     plt.scatter(x_test, y_test, alpha=0.5)
#     # plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--', linewidth=2)  # เส้นตรงเพื่อเปรียบเทียบ
#     plt.plot(x_test, y_svm_pred)  # เส้นตรงเพื่อเปรียบเทียบ
#     plt.xlabel('Actual Values', fontsize=14)
#     plt.ylabel('Predicted Values', fontsize=14)
#     plt.title(f'Regression Plot (Grid{ref_point} vs Grid{num})', fontsize=16)
#     plt.show()


df = pd.read_csv("D:\\Model\\[updated_2-67]reformat_datasets.csv", encoding="utf8")
time = df["Timestamp"].values

selected_columns = [
    "Grid1_Heat_Index", "Grid2_Heat_Index", "Grid3_Heat_Index", "Grid4_Heat_Index",
    "Grid5_Heat_Index", "Grid6_Heat_Index", "Grid7_Heat_Index", "Grid8_Heat_Index",
    "Grid9_Heat_Index", "Out1_Heat_Index", "Out2_Heat_Index", "Out3_Heat_Index",
    "Out4_Heat_Index"
]

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
        # save_dir = f"D:\\Model\\SVM\\Model_svm\\grid{ref_point}_as_ref\\Out_Window_Curtain_AC_Door\\"
        save_dir = f"D:\\Model\\SVM\\Model_svm\\grid{ref_point}_as_ref\\SVMFValTestModel"
        # grid_x = [f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index']
        grid_x = [f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index', 'Window_State', 'Curtain_State', 'AC_State',
                  'Door_State']
        grid_y = f'Grid{num}_Heat_Index'
        x = df[grid_x].values
        y = df[grid_y].values
        print(f'------------------> X= {grid_x}, y= {grid_y} <-------------------')

        svpl = SVR(kernel='rbf')
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=10)
        # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=10)
        # x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.25, random_state=10)

        params = {'C': [0.2, 0.8, 1.0, 10.0], 'gamma':[0.5,1.0,3.0,7.0,10.0]}
        # params = {'kernel': ['rbf', 'poly'], 'C': [0.2, 0.8, 1.0, 10.0], 'gamma': [0.5, 1.0, 3.0, 7.0, 10.0]}
        # params = {'kernel': ['rbf', 'poly'], 'C': [0.2, 0.8, 1.0, 10.0, 15.0, 20.0], 'gamma': [0.5, 1.0, 7.0, 10.0, 50.0, 100]}
        # params = {'kernel': ['rbf', 'poly'], 'C': [1, 5, 10, 15], 'gamma': [1, 10, 50, 100]}
        # params = {'C': [1, 5, 10, 15], 'gamma': [1, 10, 50, 100]}
        model = RandomizedSearchCV(svpl, params, cv=5, verbose=0)
        model.fit(x_train,y_train)
        print(f'Hyper parameter is {model.best_params_}')

        # svpl = SVR(kernel=model.best_params_['kernel'], gamma=model.best_params_['gamma'], C=model.best_params_['C'])
        svpl = SVR(kernel='rbf', gamma=model.best_params_['gamma'], C=model.best_params_['C'])
        svpl.fit(x_train, y_train)
        # validation = svpl.predict(x_val)

        # differences = []
        # max_count = 0
        # min_count = 0
        # for x in range(len(y_svr_pred)):
        #     s = round(y_svr_pred[x] - y_test[x], 2)
        #     differences.append(s)
        #     if s >= 1:
        #         max_count += 1
        #     elif s <= -1:
        #         min_count += 1
        #
        # print(f'Total test : {len(y_svr_pred)}')

        # print(f'Sum differential : {sum(differences)}')
        # print(f'Max differential : {max(differences)}')
        # print(f'Avg differential : {statistics.mean(differences)}')
        # print(f'Min differential : {min(differences)}')
        # print(f'Differential greater than 1 : {max_count}')
        # print(f'Differential less than -1 : {min_count}')
        # rmse = root_mean_squared_error(y_val, validation)
        # print('Val_RMSE:', rmse)
        # print('Val_R2', r2_score(y_val, validation))

        y_svm_pred = svpl.predict(x_test)
        rmse = root_mean_squared_error(y_test, y_svm_pred)
        print('Test_RMSE:', rmse)
        print('Test_R2', r2_score( y_test, y_svm_pred))

        # Create the directory if it doesn't exist
        # save_folder = os.path.join(save_dir, f"Grid{ref_point}-{num}")
        # os.makedirs(save_folder, exist_ok=True)
        #
        # # Save the model inside the created folder
        # save_path = os.path.join(save_folder, f'[Grid{ref_point}-{num}]svm_model.sav')
        # pickle.dump(svpl, open(save_path, 'wb'))
        # print(f'######################## Save Model Success Grid{ref_point}-Grid{num} ########################')
        # print('\n\n')


        # plot_regression(x_test,y_test, y_svm_pred, ref_point, num)

        plt.scatter(x, y)
        # plt.plot(train['time_study'], train['linear_svr_pred'], color='orange', label='linear SVR')
        plt.plot(x_test, y_svm_pred, color='green', label='rbf SVR')
        # plt.plot(train['time_study'], train['poly_svr_pred'], color='blue', label='poly SVR')
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('y')


        # print("------------------------> End Point <------------------------", ref_point)

        # import time
        # plt.rcParams['font.family'] = 'TH SarabunPSK'
        # plt.rcParams['font.size'] = 14
        # y_svr_pred = y_svr_pred[:150]
        # y_test = y_test[:150]
        # plt.figure(figsize=(16, 9), facecolor='1.0')
        # plt.grid(which='major', axis='both', c='0.95', ls='-', linewidth=0.5, zorder=0)
        # plt.plot(y_svr_pred, color='lightseagreen', linewidth=3.0, label='Prediced Outcome', )
        # plt.plot(y_test, color='maroon', linewidth=3.0, label='Actual Outcome')
        # plt.xlabel('Record', fontsize=30)
        # plt.xticks(fontsize=25)
        # plt.yticks(fontsize=25)
        # plt.ylabel('Heat index', fontsize=30)
        # title_text = f"Comparison between Predicted and Actual Outcomes\n"
        # title_text += f"X=Grid{ref_point}, Outdoor4, Window, Curtain, Door, AC, y=Grid{num}\n"
        # title_text += f"kernel= rbf, gamma= auto, C= 10\n"
        # title_text += f"MSE= {mse:.2f} RMSE= {rmse:.2f}"
        # plt.title(title_text, weight='bold', fontsize=25)
        # plt.legend(fontsize=25)
        # plt.ylim(22, 40)
        # plt.show()
        # time.sleep(3)

    if ref_point <= 9:
        print('Next ----------------------> Point', ref_point + 1)



