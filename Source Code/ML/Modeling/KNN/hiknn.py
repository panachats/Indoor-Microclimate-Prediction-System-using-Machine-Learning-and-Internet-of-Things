import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, root_mean_squared_error
from sklearn.model_selection import train_test_split
import seaborn as sns
import pickle
import statistics
import os
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import r2_score


def plot(y_knn_pred,y_test,ref_point,num,mse,rmse):
    import time
    plt.rcParams['font.family'] = 'TH SarabunPSK'
    plt.rcParams['font.size'] = 14
    y_knn_pred = y_knn_pred[:150]
    y_test = y_test[:150]
    plt.figure(figsize=(16, 9), facecolor='1.0')
    plt.grid(which='major', axis='both', c='0.95', ls='-', linewidth=0.5, zorder=0)
    plt.plot(y_knn_pred, color='lightseagreen', linewidth=3.0, label='Prediced Outcome', )
    plt.plot(y_test, color='maroon', linewidth=3.0, label='Actual Outcome')
    plt.xlabel('Record', fontsize=30)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.ylabel('Heat index', fontsize=30)
    title_text = f"Comparison between Predicted and Actual Outcomes\n"
    title_text += f"X=Grid{ref_point}, Outdoor4, Window, Curtain, Door, AC, y=Grid{num}\n"
    # title_text += f"kernel= rbf, gamma= auto, C= 10\n"
    title_text += f"MSE= {mse:.2f} RMSE= {rmse:.2f}"
    plt.title(title_text, weight='bold', fontsize=25)
    plt.legend(fontsize=25)
    plt.ylim(22, 40)
    plt.show()
    time.sleep(3)


def saveFile(save_dir, ref_point, num, knn_regressor):
    # Create the directory if it doesn't exist
    save_folder = os.path.join(save_dir, f"Grid{ref_point}-{num}")
    os.makedirs(save_folder, exist_ok=True)

    # Save the model inside the created folder
    save_path = os.path.join(save_folder, f'[Grid{ref_point}-{num}]knn_model.sav')
    pickle.dump(knn_regressor, open(save_path, 'wb'))
    print(f'######################## Save Model Success Grid{ref_point}-Grid{num} ########################')
    print('\n\n')

def plot_regression(y_test, y_knn_pred, ref_point, num):
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_knn_pred, alpha=0.5)
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--', linewidth=2)  # เส้นตรงเพื่อเปรียบเทียบ
    plt.xlabel('Actual Values', fontsize=14)
    plt.ylabel('Predicted Values', fontsize=14)
    plt.title(f'Regression Plot (Grid{ref_point} vs Grid{num})', fontsize=16)
    plt.show()


def multiTrainKnn(df):
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
        # totalLisdiffer = []
        print('______________________ Select Point', ref_point, '______________________')

        for num in ref_point_grid_lists[ref_point]:
            # save_dir = f"D:\\Model\\SVM\\Model_svm\\grid{ref_point}_as_ref\\Out_Window_Curtain_AC_Door\\"
            save_dir = f"D:\\Model\\SVM\\Model_Knn\\grid{ref_point}_as_ref\\ValidationDataKnn"
            # grid_x = [f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index']
            grid_x = [f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index', 'Window_State', 'Curtain_State', 'AC_State',
                      'Door_State']
            grid_y = f'Grid{num}_Heat_Index'
            x = df[grid_x].values
            y = df[grid_y].values
            print(f'------------------> X= {grid_x}, y= {grid_y} <-------------------')

            # Split Data set
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)
            # x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.25, random_state=10)

            knn = KNeighborsRegressor()
            k_list = np.arange(1, 50, 1)
            params = {'n_neighbors': k_list, 'weights': ['uniform', 'distance'],
                      'algorithm': ['ball_tree', 'kd_tree', 'brute']}
            model = RandomizedSearchCV(knn, params, cv=10, verbose=0)
            model.fit(x_train, y_train)
            print(f'Hyper parameter is {model.best_params_}')


            knn_regressor = KNeighborsRegressor(n_neighbors=model.best_params_['n_neighbors'], weights=model.best_params_['weights'], algorithm=model.best_params_['algorithm'])
            model_knn = knn_regressor.fit(x_train, y_train)


            # differences = []
            # max_count = 0
            # min_count = 0
            # for x in range(len(y_knn_pred)):
            #     s = round(y_knn_pred[x] - y_test[x], 2)
            #     differences.append(s)
            #     if s >= 1:
            #         max_count += 1
            #     elif s <= -1:
            #         min_count += 1
            #
            # print(f'Total Validation : {len(y_knn_pred)}')
            # print(f'Max differential : {max(differences)}')
            # print(f'Avg differential : {statistics.mean(differences)}')
            # print(f'Min differential : {min(differences)}')
            # print(f'Differential greater than 1 : {max_count}')
            # print(f'Differential less than -1 : {min_count}')
            # mse = mean_squared_error(y_val, y_knn_pred)
            # y_knn_pred = model_knn.predict(x_val)
            # rmse = root_mean_squared_error(y_val, y_knn_pred)
            # print('Val_RMSE:',rmse)
            # print('Val_R2', r2_score(y_val, y_knn_pred))

            y_knn_pred = model_knn.predict(x_test)
            rmse = root_mean_squared_error(y_test, y_knn_pred)
            print('Test_RMSE:', rmse)
            print('Test_R2', r2_score(y_test, y_knn_pred))


            # saveFile(save_dir, ref_point, num, knn_regressor)

            # plt.scatter(y_test, y_knn_pred)
            # plt.plot(y_test, y_knn_pred)
            #
            # plt.xlabel("X")
            # plt.ylabel("Predicted Grid")
            # plt.title("Actual Rent vs Predicted Rent")
            #
            # plt.show()

            # Plot regression for linear/non-linear inspection
            # plot_regression(y_test, y_knn_pred, ref_point, num)
            plot_regression(y_test, y_knn_pred, ref_point, num)



        if ref_point <= 9:
            print('Next ----------------------> Point', ref_point + 1)


sns.set_style({'font.family': 'Times New Roman'})
print('---')
df = pd.read_csv("D:\\Model\\[updated_2-67]reformat_datasets.csv", encoding="utf8")
multiTrainKnn(df)



