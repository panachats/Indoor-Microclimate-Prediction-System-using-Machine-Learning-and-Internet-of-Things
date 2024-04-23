from metpy.calc import heat_index
from metpy.units import units
import pandas as pd


# def convert(data):
#     heat_index_data = {'Timestamp': data['Timestamp']}  # เก็บ Timestamp ในคอลัมน์ใหม่
#     for i in range(1, 10):
#         temp_col = f'Grid{i}_InTemp_Mean'
#         hum_col = f'Grid{i}_InHumi_Mean'
#
#         temp_values = data[temp_col].values * units.degC
#         rel_hum_values = data[hum_col] / 100
#         rounded_hum_values = round(rel_hum_values, 2)
#
#         heat_index_values = []
#         print('____' * 20)
#         print(f'Grid{i}_InTemp_Mean -> Grid{i}_InHumi_Mean')
#         for temp, rounded_hum in zip(temp_values, rounded_hum_values):
#             print(f"{temp}, {rounded_hum}")
#             heat = heat_index(temp, rounded_hum, mask_undefined=False)
#             heat_in_celsius = float(heat.to(units.degC).magnitude)
#
#             print(f'Heat Index: {round(heat_in_celsius,2)}')
#             heat_index_values.append(round(heat_in_celsius,2))
#
#         # สร้างคอลัมน์ใหม่ใน heat_index_data ตาม Grid
#         grid_col_name = f'Grid{i}_Heat_Index'
#         heat_index_data[grid_col_name] = heat_index_values
#
#     # สร้าง DataFrame ใหม่จาก heat_index_data
#     heat_index_df = pd.DataFrame(heat_index_data)
#
#     # บันทึก DataFrame ลงในไฟล์ CSV
#     print(heat_index_df)
#     if(input("Include outdoor and other parameters? \nAnswer y/n: ") == 'y'):
#         out_convert(data,heat_index_df)
#         return 0
#     csv_path = "C:\\Users\\user\\Desktop\\Microclimate\\data_heatindex.csv"
#     # csv_path = "D:\\jsontocsv\\RawData\\MeetingRoom\\csvData\\MeetingRoom_HeatIndex.csv"
#     heat_index_df.to_csv(csv_path, index=False) #TODO Uncomment
#     return 0

def convert(data):
    heat_index_data = {'Timestamp': data['Timestamp']}  # เก็บ Timestamp ในคอลัมน์ใหม่
    for i in range(1, 10):
        temp_col = f'Grid{i}_InTemp_Mean'
        hum_col = f'Grid{i}_InHumi_Mean'

        temp_values = data[temp_col].values * units.degC
        rel_hum_values = data[hum_col] / 100
        rounded_hum_values = round(rel_hum_values, 2)

        heat_index_values = []
        print('____' * 20)
        print(f'Grid{i}_InTemp_Mean -> Grid{i}_InHumi_Mean')
        for temp, rounded_hum in zip(temp_values, rounded_hum_values):
            print(f"{temp}, {rounded_hum}")
            heat = heat_index(temp, rounded_hum, mask_undefined=False)
            heat_in_celsius = float(heat.to(units.degC).magnitude)

            print(f'Heat Index: {round(heat_in_celsius,2)}')
            heat_index_values.append(round(heat_in_celsius,2))

        # สร้างคอลัมน์ใหม่ใน heat_index_data ตาม Grid
        grid_col_name = f'Grid{i}_Heat_Index'
        heat_index_data[grid_col_name] = heat_index_values

    mid_grid = [5,8] # Grid on the table list
    for i in mid_grid:
        temp_values = data[f'Grid{i}Mid_Temperature_Mean'].values * units.degC
        rel_hum_values = data[f'Grid{i}Mid_Humidity_Mean'] / 100
        rounded_hum_values = round(rel_hum_values, 2)

        heat_index_values = []
        print('____' * 20)
        print(f'Grid{i}_InTemp_Mean -> Grid{i}_InHumi_Mean')
        for temp, rounded_hum in zip(temp_values, rounded_hum_values):
            print(f"{temp}, {rounded_hum}")
            heat = heat_index(temp, rounded_hum, mask_undefined=False)
            heat_in_celsius = float(heat.to(units.degC).magnitude)

            print(f'Heat Index: {round(heat_in_celsius, 2)}')
            heat_index_values.append(round(heat_in_celsius, 2))

        # สร้างคอลัมน์ใหม่ใน heat_index_data ตาม Grid
        grid_col_name = f'Grid{i}Mid_Heat_Index'
        heat_index_data[grid_col_name] = heat_index_values
    # สร้าง DataFrame ใหม่จาก heat_index_data
    heat_index_df = pd.DataFrame(heat_index_data)

    # บันทึก DataFrame ลงในไฟล์ CSV
    print(heat_index_df)
    # if(input("Include outdoor and other parameters? \nAnswer y/n: ") == 'y'):
    xyz = True
    if xyz:
        out_convert(data,heat_index_df)
        return 0
    csv_path = "C:\\Users\\user\\Desktop\\Microclimate\\data_heatindex.csv"
    # csv_path = "D:\\jsontocsv\\RawData\\MeetingRoom\\csvData\\MeetingRoom_HeatIndex.csv"
    heat_index_df.to_csv(csv_path, index=False) #TODO Uncomment
    return 0

def out_convert(data, heat_index_df):
    heat_index_data = {'Curtain_State': data['Curtain_State'],
                       'Weather': data['Weather'],
                       'Window_State': data['Window_State'],
                       'Door_State': data['Door_State'],
                       'AC_State': data['AC_State']}  # เก็บ Timestamp ในคอลัมน์ใหม่
    for i in range(1, 5):
        out_temp_col = f'Out{i}_Temp_Mean'
        out_hum_col = f'Out{i}_Humi_Mean'

        temp_values = data[out_temp_col].values * units.degC
        rel_hum_values = data[out_hum_col] / 100
        rounded_hum_values = round(rel_hum_values, 2)

        heat_index_values = []
        print('____' * 20)
        print(f'Out{i}_Temp_Mean -> Out{i}_Humi_Mean')
        for temp, rounded_hum in zip(temp_values, rounded_hum_values):
            print(f"{temp}, {rounded_hum}")
            heat = heat_index(temp, rounded_hum, mask_undefined=False)
            heat_in_celsius = float(heat.to(units.degC).magnitude)

            print(f'Heat Index: {round(heat_in_celsius,2)}')
            heat_index_values.append(round(heat_in_celsius,2))

        # สร้างคอลัมน์ใหม่ใน heat_index_data ตาม Grid
        grid_col_name = f'Out{i}_Heat_Index'
        heat_index_data[grid_col_name] = heat_index_values

    # สร้าง DataFrame ใหม่จาก heat_index_da ta
    new_df = pd.DataFrame(heat_index_data)
    print(new_df)
    # heat_index_df = heat_index_df.append(new_df, ignore_index=True)
    # merged_df = heat_index_df.join(new_df)
    # merged_df = pd.concat([heat_index_df, new_df], axis=1)
    merged_df = pd.concat([heat_index_df, new_df], axis=1, join='inner')
    print(merged_df)
    # บันทึก DataFrame ลงในไฟล์ CS
    csv_path = "C:\\Users\\user\\Desktop\\Microclimate\\data_heatindex.csv"
    merged_df.to_csv(csv_path, index=False)   #TODO Uncomment


# def convert(data):
#     heat_index_data = {'Timestamp': data['Timestamp']}  # เก็บ Timestamp ในคอลัมน์ใหม่
#     for i in range(1, 5):
#         temp_col = f'Out{i}_Temp_Mean'
#         hum_col = f'Out{i}_Humi_Mean'
#
#         temp_values = data[temp_col].values * units.degC
#         rel_hum_values = data[hum_col] / 100
#         rounded_hum_values = round(rel_hum_values, 2)
#
#         heat_index_values = []
#         print('____' * 20)
#         print(f'Out{i}_Temp_Mean -> Out{i}_Humi_Mean')
#         for temp, rounded_hum in zip(temp_values, rounded_hum_values):
#             print(f"{temp}, {rounded_hum}")
#             heat = heat_index(temp, rounded_hum, mask_undefined=False)
#             heat_in_celsius = float(heat.to(units.degC).magnitude)
#
#             print(f'Heat Index: {heat_in_celsius}')
#             heat_index_values.append(heat_in_celsius)
#
#         # สร้างคอลัมน์ใหม่ใน heat_index_data ตาม Grid
#         grid_col_name = f'Out{i}_Heat_Index'
#         heat_index_data[grid_col_name] = heat_index_values
#
#     # สร้าง DataFrame ใหม่จาก heat_index_data
#     heat_index_df = pd.DataFrame(heat_index_data)
#
#     # บันทึก DataFrame ลงในไฟล์ CSV
#     csv_path = "D:\\jsontocsv\\RawData\\MeetingRoom\\csvData\\OutMeetingRoom_HeatIndex.csv"
#     heat_index_df.to_csv(csv_path, index=False)


data01 = pd.read_csv("C:\\Users\\user\\Desktop\\Microclimate\\data.csv")
# data01 = pd.read_csv("D:\\jsontocsv\\RawData\\MeetingRoom\\csvData\\data.csv")
convert(data01)
