
import pandas as pd
from sklearn.metrics import mean_squared_error, root_mean_squared_error
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import r2_score

df = pd.read_csv("D:\\Model\\[updated_2-67]reformat_datasets.csv", encoding="utf8")


ref_point = 9

grid_list = [1,2,3,4,5,6,7,8]
for num in grid_list:
    filename = f'C:\\Users\\NITRO V15\\Downloads\\TestMicroClimateProject\\Model\\Grid{ref_point}-{num}\\[Grid{ref_point}-{num}]knn_model.sav'
    knn = pickle.load(open(filename, 'rb'))

    grid_x = f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index', 'Window_State', 'Curtain_State', 'AC_State','Door_State'
    grid_y = f'Grid{num}_Heat_Index'
    x = df[[f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index', 'Window_State', 'Curtain_State', 'AC_State','Door_State']].values
    y = df[grid_y].values
    print(f'------------------> X= {grid_x}, y= {grid_y} <-------------------')
    # x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=10)
    # x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=0.5, random_state=10)

    # แบ่งข้อมูลเป็น train set และ test set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)
    # แบ่ง train set เป็น train set และ validation set
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.5, random_state=10)

    pred = knn.predict(x_val)

    # import statistics
    # a = []
    # max_count = 0
    # min_count = 0
    # max_diff = 1
    # for z in range(len(pred)):
    #     sum = round((pred[z] - y_val[z]), 2)
    #     a.append(sum)
    #     if sum >= max_diff:
    #         max_count += 1
    #     elif sum <= -max_diff:
    #         min_count += 1
    #
    #
    # print(f'Total test/train : {len(pred)}')
    # print(f'Max differential : {max(a)}')
    # print(f'Avg differential : {round(statistics.mean(a),2)}')
    # print(f'Min differential : {min(a)}')
    # print(f'Differential greater than {max_diff} : {max_count}')
    # print(f'Differential less than -{max_diff} : {min_count}')
    mse = mean_squared_error(y_val, pred)
    rmse = root_mean_squared_error(y_val, pred)
    print('RMSE:',rmse)
    print('R2', r2_score(y_val, pred))



import pandas as pd
from sklearn.metrics import mean_squared_error, root_mean_squared_error
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import r2_score

df = pd.read_csv("D:\\Model\\[updated_2-67]reformat_dataset - For_Test", encoding="utf8")


ref_point = 9

grid_list = [1,2,3,4,5,6,7,8]
for num in grid_list:
    filename = f'C:\\Users\\NITRO V15\\Downloads\\TestMicroClimateProject\\Model\\Grid{ref_point}-{num}\\[Grid{ref_point}-{num}]knn_model.sav'
    knn = pickle.load(open(filename, 'rb'))

    grid_x = f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index', 'Window_State', 'Curtain_State', 'AC_State','Door_State'
    grid_y = f'Grid{num}_Heat_Index'
    x = df[[f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index', 'Window_State', 'Curtain_State', 'AC_State','Door_State']].values
    y = df[grid_y].values
    print(f'------------------> X= {grid_x}, y= {grid_y} <-------------------')
    # x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=10)
    # x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=0.5, random_state=10)

    # # แบ่งข้อมูลเป็น train set และ test set
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)
    # # แบ่ง train set เป็น train set และ validation set
    # x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.5, random_state=10)

    # pred = knn.predict(x_val)
    pred = knn.predict(x)

    # mse = mean_squared_error(y, pred)
    rmse = root_mean_squared_error(y, pred)
    print('RMSE:',rmse)
    print('R2', r2_score(y, pred))














