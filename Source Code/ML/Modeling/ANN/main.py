# To find best hyperparam
import warnings

warnings.filterwarnings('ignore')
import statistics
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import pandas as pd
from sklearn.metrics import r2_score

try:
    # df = pd.read_csv("C:\\Users\\user\Desktop\Microclimate\Source_Code\\reformat_datasets02.csv", encoding="utf8")
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
        totalLisdiffer = []
        print('______________________ Select Point', ref_point, '______________________')
        for num in ref_point_grid_lists[ref_point]:
            grid_x = [f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index', 'Window_State', 'Curtain_State', 'AC_State',
                      'Door_State']
            # grid_x = [f'Grid{ref_point}_Heat_Index', 'Out4_Heat_Index']
            grid_y = f'Grid{num}_Heat_Index'
            x = df[grid_x].values
            y = df[grid_y].values
            print(f'------------------> X= {grid_x}, y= {grid_y} <-------------------')

            x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=10)

            mlp = MLPRegressor()
            params = [
                {
                    'activation': ['identity', 'logistic', 'tanh', 'relu'],
                    'solver': ['lbfgs', 'sgd', 'adam'],
                    'alpha': [0.0001, 0.001, 0.01],
                    'hidden_layer_sizes': [
                        # ผสม
                        # (10,), (30,), (50,), (70), (90,), (110,), (130,), (150,), (170,), (190,), (210,),
                        # (10,10), (30,30), (50,50), (70,70), (90,90),

                        # สามชั้น รอบแรก
                        # (10, 10, 10), (30, 30, 30), (50, 50, 50), (70, 70, 70), (90, 90, 90),

                        # หนึ่งชั้น รอบสอง
                        (30,), (50,), (70,), (90,), (110,), (130,), (150,), (170,), (190,), (210,), (230,), (250,),
                        (270,), (320,), (350,), (420),

                        # สองชั้น
                        # (30,30), (50,50), (70,70), (90,90), (110,110), (130,130), (150,150), (170,170), (190,190), (210,210), (230,230), (250,250),
                        # (270,270), (320,320), (350,350), (420,420)

                        #three round two

                        # (30, 30, 30), (50, 50, 50), (70, 70, 70), (90, 90, 90), (110, 110, 110), (130, 130, 130),
                        # (150, 150, 150), (170, 170, 170), (190, 190, 190), (210, 210, 210), (230, 230, 230),
                        # (250, 250, 250),
                        # (270, 270, 270), (320, 320, 320), (350, 350, 350), (420, 420, 420)
                        #ผสมรอบสอง
                        # (30,), (50,), (70,), (90,), (110,), (130,), (150,), (170,), (190,), (210,), (230,), (250,),
                        # (270,), (320,), (350,), (420),
                        # (30,30), (50,50), (70,70), (90,90), (110,110), (130,130), (150,150), (170,170), (190,190), (210,210), (230,230), (250,250),
                        # (270,270), (320,320), (350,350), (420,420),
                        # (30,30,30), (50,50,50), (70,70,70), (90,90,90), (110,110,110), (130,130,130), (150,150,150), (170,170,170), (190,190,190), (210,210,210), (230,230,230), (250,250,250),
                        # (270,270,270), (320,320,320), (350,350,350), (420,420,420)


                    ]
                }
            ]
            model = RandomizedSearchCV(mlp, params, cv=10, verbose=0)
            model.fit(x_train, y_train)
            print(f'Hyper parameter is {model.best_params_}')

            print('------------------')
            mlp_regressor = MLPRegressor(
                activation=model.best_params_['activation'],
                solver=model.best_params_['solver'],
                hidden_layer_sizes=model.best_params_['hidden_layer_sizes'],
                alpha=model.best_params_['alpha'],
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
            totalLisdiffer.append(sumthan1)

            if ref_point <= 9:
                print(f'Total Sum differential Grid{ref_point} : {sum(totalLisdiffer)}')
            print('Next ----------------------> Point', ref_point + 1)
except:
    a = 1

