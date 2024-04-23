import pandas as pd
import numpy as np
from plot_heat import plotHeat

from datetime import date


def convert_data(df, split_date, split_date2, minutes, set):
    print(f'\n-----------------------------------------------------------------\n')
    df['Timestamp'] = df['Timestamp'].astype(str).map(lambda x: x[:19:])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df[df['Timestamp'] >= split_date]
    df = df[df['Timestamp'] <= split_date2]

    return df.reset_index()


def select_Time(df, day, month):
    minutes = 5
    # month = '10'
    while True:
        try:
            default_start = input("Input Start Time (example: 08:00): ")
            default_end = input("Input End Time (example: 18:00): ")
            start_1 = default_start
            end_1 = default_end
            print(f"01{start_1}/{end_1}")

            # day = '8'
            day_begin = day
            date_end = day
            # date_end = int(day + 1)

            print(df.head().to_string())
            split_date = f"2024-{month}-{day_begin} {start_1}:00"
            split_date2 = f"2024-{month}-{date_end} {end_1}:00"
            new_data = convert_data(df, split_date, split_date2, minutes, "Test")
            print(f'\n Data at {split_date} \n {new_data.to_string()}')
            new_data.reset_index()
            csv_path = f"C:\\Users\\user\\Desktop\\Microclimate\\Source_Code\\RawData\\{day}_{month}_2024_MeetingRoom_Data.csv"
            # บันทึกเป็น CSV ที่ตำแหน่งที่กำหนดเอง
            new_data.to_csv(csv_path, index=False, header=True)

            return merge_anemometer(new_data, day, month, default_start, default_end)
        except Exception as e:
            print('Error in select_Time\n', e)
            pass


def merge_anemometer(new_data, day, month, default_start, default_end):
    # Merge Anemometer file
    while True:
        try:
            if (input("Do you want to merge anemometer csv? (Answer: y/n)\n")) == 'y':
                print(('|||| Merge Anemometer ||||'))

                point = []  # Array ที่จะเก็บชื่อไฟล์ Anemometer หลัง Merge ข้อมูลไว้
                point_number = []  # Array ที่จะเก็บตัวเลขตำแหน่งของ Anemometer ไว้
                loop = int(input("Anemometer: How many file You want to merge?\n"))
                for i in range(loop):
                    print(point)
                    original_filename = f'{input("Input Anemometer filename (not included .csv) ")}'  # Edit original filename
                    output_filename = f'merged_{original_filename}.csv'  # Edit Output filename

                    # Read the original CSV file
                    df = pd.read_csv(
                        f"C:\\Users\\user\\Desktop\\Microclimate\\Source_Code\\RawData\\{original_filename}.csv")

                    # Combine 'Time' and 'Date' columns and convert to datetime
                    df['Date'] = pd.to_datetime(df['Time'] + ' ' + df['Date'], format='mixed')  #TODO remove 'format' later

                    df.set_index('Date', inplace=True)

                    # Drop unnecessary columns
                    df = df.drop(columns=['RecNo', 'Time'])

                    # resampled data
                    # df = df.resample('5Min').agg({'MeaValue' : 'mean', 'Temperature': 'mean'})
                    df = df.resample('5Min').agg({'MeaValue': 'mean'})
                    #
                    # interval = (df['Date'] >= start) & (df['Date'] <= end)

                    df = df[(df.index.time >= pd.Timestamp(default_start).time()) & (df.index.time <= pd.Timestamp(default_end).time())]

                    # Set the path to save the output file
                    save_to_path = f'C:\\Users\\user\\Desktop\\Microclimate\\Source_Code\\OutputData\\{output_filename}'

                    print(df)
                    point.append(output_filename)
                    print(f'Output File: {point}')

                    if input("Add anemometer dataframe to main csv file? (answer: y/n)\n") == 'y':
                        output_column_name = int(input("Input the output column name (P..._AirVelocity_Mean): "))
                        while output_column_name < 1 or output_column_name > 4:
                            print("Anemometer has only 4 point")
                            output_column_name = int(input("Input the output column name (P..._AirVelocity_Mean): "))
                        df.to_csv(save_to_path, header=True, index=True)
                        input("Merged file saved. \nPlease Check the output file and then Input anything to continue.... ")
                        export_df = pd.read_csv(
                            f'C:\\Users\\user\\Desktop\\Microclimate\\Source_Code\\OutputData\\{output_filename}')
                        new_data[f'P{output_column_name}_AirVelocity_Mean'] = export_df['MeaValue']
                    print(new_data)

                    # Save merged Anemomter DataFrame to a new CSV file
                    # new_data.to_csv('C:\\Users\\user\\Desktop\\Microclimate\\Source_Code\\OutputData\\new_data.csv',
                    #                 header=True, index=True)
            return process_csv(new_data, day, month)
        except Exception as e:
            print('Error in merge_anemometer\n', e)
            pass


def process_csv(new_data, day, month):
    # for i in range(len(anemometer_point)):  # Loop เพื่อเพิ่มข้อมูลจาก Anemometer ทั้ง 4 จุด
    #     df = pd.read_csv(f'C:\\Users\\user\\Desktop\\Microclimate\\Source_Code\\OutputData\\{anemometer_point[i]}')
    #     new_data[f'P{i+1}_AirVelocity_Mean'] = df['MeaValue']

    # Process csv (insert more column etc.)
    input_column = ['People', 'Curtain_State', 'Light_Bulb_State', 'Weather', 'Window_State', 'Door_State', 'AC_State', 'AC_1_Filter', 'AC_2_Filter', 'AC_3_Filter','AC_4_Filter','Thermostat']
    while True:
        try:
            # TODO uncomment later
            while True:
                if (input("Input any value to exit (leave blank to continue Interval Input FN): ") != ""): break
                choice = int(input(
                    f"Select Column\n 1.{input_column[0]} \n 2.{input_column[1]} \n 3.{input_column[2]} \n 4.{input_column[3]}  \n 5.{input_column[4]} \n 6.{input_column[5]} \n 7.{input_column[6]} \n 8.{input_column[7]} \n 9.{input_column[8]} \n 10.{input_column[9]} \n 11.{input_column[10]} \n 12.{input_column[11]}  \n 13. Input 0 to exit \n "))
                if choice == 0: break
                if choice <= -1 or choice > len(input_column) : pass
                start = pd.to_datetime(
                    f'2024-{month}-{day} {input(f"Input Start Time for column {input_column[choice - 1]} (example: 12:00): ")}')
                end = pd.to_datetime(
                    f'2024-{month}-{day} {input(f"Input End Time for column {input_column[choice - 1]} (example: 01:00): ")}')

                interval = (new_data['Timestamp'] >= start) & (new_data['Timestamp'] <= end)

                value = input(f'Input Value for column {input_column[choice - 1]} (input "s" to exit): ')
                if value == 's': break
                new_data.loc[interval, input_column[choice - 1]] = value

            filename = f'{day}_{month}_2024_MeetingRoom_Data'
            # Step 1: Drop 'Timestamp' column
            # df_without_timestamp = new_data.drop(columns=['Timestamp', 'index'])
            # print(df_without_timestamp.dtypes)
            # Step 2: Calculate the mean of each column
            # mean_values = df_without_timestamp.mean()

            # # Step 3: Fill NaN values with mean
            # df_without_timestamp.fillna(value=mean_values)

            # Step 4: Add 'Timestamp' column back in the first position
            # df_without_timestamp.insert(0, 'Timestamp', new_data['Timestamp'])

            # print(df_without_timestamp.to_string())

            # export to csv
            new_data.to_csv(f'C:\\Users\\user\\Desktop\\Microclimate\\Source_Code\\OutputData\\filled_nan_{filename}.csv', index=False, header=True)
            # print(df_without_timestamp)
            # plotHeat(df_without_timestamp, day, month)       #TODO Uncomment Later
            print("CSV file exported.")
            break
        except Exception as e:
            print('Error in process_csv\n', e)
            pass
