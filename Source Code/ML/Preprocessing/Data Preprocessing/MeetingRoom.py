import pandas as pd
import json
from SelectTimestamp import select_Time
def splitTime(data,day, month):
    # สร้าง List เพื่อเก็บ Timestamps และข้อมูลที่จะนำเข้า DataFrame
    timestamps = []
    data_list = []

    # วนลูปใน JSON เพื่อดึง Timestamp และข้อมูล
    for timestamp, values in data.items():
        # เพิ่ม Timestamp ลงใน List
        timestamps.append(pd.to_datetime(timestamp))
        # เพิ่มข้อมูลลงใน List
        data_list.append(values)

    # สร้าง DataFrame จาก List ของ Dictionary
    df = pd.DataFrame(data_list)

    # เพิ่มคอลัมน์ Timestamp ลงใน DataFrame
    df["Timestamp"] = timestamps

    return mapping_column(df,day, month)


# def drop_column(df,day, month):
    # columns_to_drop = ["Air1_FrontHumidity_Mean", "Air1_FrontHumidity_SD", "Air1_FrontTemperature_Mean","Air1_FrontTemperature_SD",
    #                     "Air1_UnderHumidity_Mean","Air1_UnderHumidity_SD","Air1_UnderTemperature_Mean","Air1_UnderTemperature_SD",
    #                     "Air2_FrontHumidity_Mean", "Air2_FrontHumidity_SD", "Air2_FrontTemperature_Mean","Air2_FrontTemperature_SD",
    #                     "Air2_UnderHumidity_Mean","Air2_UnderHumidity_SD","Air2_UnderTemperature_Mean","Air2_UnderTemperature_SD",
    #                     "Air3_FrontHumidity_Mean", "Air3_FrontHumidity_SD", "Air3_FrontTemperature_Mean","Air3_FrontTemperature_SD",
    #                     "Air3_UnderHumidity_Mean","Air3_UnderHumidity_SD","Air3_UnderTemperature_Mean","Air3_UnderTemperature_SD",
    #                     "Air4_FrontHumidity_Mean", "Air4_FrontHumidity_SD", "Air4_FrontTemperature_Mean","Air4_FrontTemperature_SD",
    #                     "Air4_UnderHumidity_Mean","Air4_UnderHumidity_SD","Air4_UnderTemperature_Mean","Air4_UnderTemperature_SD",
    #                     "Grid1_Array_Length","Grid2_Array_Length","Grid3_Array_Length","Grid4_Array_Length","Grid5_Array_Length",
    #                     "Grid6_Array_Length","Grid7_Array_Length","Grid8_Array_Length","Grid9_Array_Length",
    #                     "Outdoor1_Current1_Mean","Outdoor1_Current1_SD","Outdoor1_Current2_Mean","Outdoor1_Current2_SD",
    #                     "Outdoor2_Current1_Mean","Outdoor2_Current1_SD","Outdoor2_Current2_Mean","Outdoor2_Current2_SD",
    #                     "Outdoor1_Power1_Mean","Outdoor1_Power1_SD","Outdoor1_Power2_Mean","Outdoor1_Power2_SD"]
    # df = df.drop(columns=columns_to_drop, axis=1)
    # print(f"DROP DATA{df}")
    # return mapping_column(df,day, month)



def mapping_column(df,day, month):
    column_mapping = {
        "Grid1_Humidity_Mean": "Grid1_InHumi_Mean",
        "Grid1_Humidity_SD": "Grid1_InHumi_SD",
        "Grid1_Temperature_Mean": "Grid1_InTemp_Mean",
        "Grid1_Temperature_SD": "Grid1_InTemp_SD",

        "Grid2_Humidity_Mean": "Grid2_InHumi_Mean",
        "Grid2_Humidity_SD": "Grid2_InHumi_SD",
        "Grid2_Temperature_Mean": "Grid2_InTemp_Mean",
        "Grid2_Temperature_SD": "Grid2_InTemp_SD",

        "Grid3_Humidity_Mean": "Grid3_InHumi_Mean",
        "Grid3_Humidity_SD": "Grid3_InHumi_SD",
        "Grid3_Temperature_Mean": "Grid3_InTemp_Mean",
        "Grid3_Temperature_SD": "Grid3_InTemp_SD",

        "Grid4_Humidity_Mean": "Grid4_InHumi_Mean",
        "Grid4_Humidity_SD": "Grid4_InHumi_SD",
        "Grid4_Temperature_Mean": "Grid4_InTemp_Mean",
        "Grid4_Temperature_SD": "Grid4_InTemp_SD",

        "Grid5_Humidity_Mean": "Grid5_InHumi_Mean",
        "Grid5_Humidity_SD": "Grid5_InHumi_SD",
        "Grid5_Temperature_Mean": "Grid5_InTemp_Mean",
        "Grid5_Temperature_SD": "Grid5_InTemp_SD",

        "Grid6_Humidity_Mean": "Grid6_InHumi_Mean",
        "Grid6_Humidity_SD": "Grid6_InHumi_SD",
        "Grid6_Temperature_Mean": "Grid6_InTemp_Mean",
        "Grid6_Temperature_SD": "Grid6_InTemp_SD",

        "Grid7_Humidity_Mean": "Grid7_InHumi_Mean",
        "Grid7_Humidity_SD": "Grid7_InHumi_SD",
        "Grid7_Temperature_Mean": "Grid7_InTemp_Mean",
        "Grid7_Temperature_SD": "Grid7_InTemp_SD",

        "Grid8_Humidity_Mean": "Grid8_InHumi_Mean",
        "Grid8_Humidity_SD": "Grid8_InHumi_SD",
        "Grid8_Temperature_Mean": "Grid8_InTemp_Mean",
        "Grid8_Temperature_SD": "Grid8_InTemp_SD",

        "Grid9_Humidity_Mean": "Grid9_InHumi_Mean",
        "Grid9_Humidity_SD": "Grid9_InHumi_SD",
        "Grid9_Temperature_Mean": "Grid9_InTemp_Mean",
        "Grid9_Temperature_SD": "Grid9_InTemp_SD",

        "Outdoor1_Humidity1_Mean": "Out1_Humi_Mean",
        "Outdoor1_Humidity1_SD": "Out1_Humi_SD",
        "Outdoor1_Temperature1_Mean": "Out1_Temp_Mean",
        "Outdoor1_Temperature1_SD": "Out1_Temp_SD",

        "Outdoor1_Humidity2_Mean": "Out2_Humi_Mean",
        "Outdoor1_Humidity2_SD": "Out2_Humi_SD",
        "Outdoor1_Temperature2_Mean": "Out2_Temp_Mean",
        "Outdoor1_Temperature2_SD": "Out2_Temp_SD",

        "Outdoor2_Humidity1_Mean": "Out3_Humi_Mean",
        "Outdoor2_Humidity1_SD": "Out3_Humi_SD",
        "Outdoor2_Temperature1_Mean": "Out3_Temp_Mean",
        "Outdoor2_Temperature1_SD": "Out3_Temp_SD",

        "Outdoor2_Humidity2_Mean": "Out4_Humi_Mean",
        "Outdoor2_Humidity2_SD": "Out4_Humi_SD",
        "Outdoor2_Temperature2_Mean": "Out4_Temp_Mean",
        "Outdoor2_Temperature2_SD": "Out4_Temp_SD",

        "Grid5Mid_Humidity_Mean": "Grid5Mid_Humidity_Mean",
        "Grid5Mid_Humidity_SD": "Grid5Mid_Humidity_SD",
        "Grid5Mid_Temperature_Mean": "Grid5Mid_Temperature_Mean",
        "Grid5Mid_Temperature_SD": "Grid5Mid_Temperature_SD",

        "Grid8Mid_Humidity_Mean": "Grid8Mid_Humidity_Mean",
        "Grid8Mid_Humidity_SD": "Grid8Mid_Humidity_SD",
        "Grid8Mid_Temperature_Mean": "Grid8Mid_Temperature_Mean",
        "Grid8Mid_Temperature_SD": "Grid8Mid_Temperature_SD",

        "Outdoor1_Current1_Mean": "Out1_Current1_Mean",
        "Outdoor1_Current1_SD": "Out1_Current1_SD",

        "Outdoor1_Current2_Mean": "Out1_Current2_Mean",
        "Outdoor1_Current2_SD": "Out1_Current2_SD",

        "Outdoor2_Current1_Mean": "Out2_Current1_Mean",
        "Outdoor2_Current1_SD": "Out2_Current1_SD",

        "Outdoor2_Current2_Mean": "Out2_Current2_Mean",
        "Outdoor2_Current2_SD": "Out2_Current2_SD"
    }

    # if input("Include middle point in csv? Answer: y/n \n") == 'y':
    #     column_mapping.update({
    #         "Grid5Mid_Humidity_Mean": "Grid5Mid_Humidity_Mean",
    #         "Grid5Mid_Humidity_SD":"Grid5Mid_Humidity_SD",
    #         "Grid5Mid_Temperature_Mean":"Grid5Mid_Temperature_Mean",
    #         "Grid5Mid_Temperature_SD":"Grid5Mid_Temperature_SD",
    #
    #         "Grid8Mid_Humidity_Mean" : "Grid8Mid_Humidity_Mean",
    #         "Grid8Mid_Humidity_SD":"Grid8Mid_Humidity_SD",
    #         "Grid8Mid_Temperature_Mean":"Grid8Mid_Temperature_Mean",
    #         "Grid8Mid_Temperature_SD":"Grid8Mid_Temperature_SD"
    #
    #     })

    df = df.rename(columns=column_mapping)
    print(f"RENAME DATA{df}")
    return order_collumn(df,day, month)

def order_collumn(df,day, month):
    # เรียงลำดับคอลัมน์ตามลำดับที่ระบุ
    columns_order = [
        "Timestamp",
        "Grid1_InHumi_Mean", "Grid1_InTemp_Mean",
        "Grid2_InHumi_Mean", "Grid2_InTemp_Mean",
        "Grid3_InHumi_Mean", "Grid3_InTemp_Mean",
        "Grid4_InHumi_Mean", "Grid4_InTemp_Mean",
        "Grid5_InHumi_Mean", "Grid5_InTemp_Mean",
        "Grid6_InHumi_Mean", "Grid6_InTemp_Mean",
        "Grid7_InHumi_Mean", "Grid7_InTemp_Mean",
        "Grid8_InHumi_Mean", "Grid8_InTemp_Mean",
        "Grid9_InHumi_Mean", "Grid9_InTemp_Mean",
        "Out1_Humi_Mean", "Out1_Temp_Mean",
        "Out2_Humi_Mean", "Out2_Temp_Mean",
        "Out3_Humi_Mean", "Out3_Temp_Mean",
        "Out4_Humi_Mean", "Out4_Temp_Mean",

        "Grid1_InHumi_SD","Grid1_InTemp_SD",
        "Grid2_InHumi_SD","Grid2_InTemp_SD",
        "Grid3_InHumi_SD","Grid3_InTemp_SD",
        "Grid4_InHumi_SD","Grid4_InTemp_SD",
        "Grid5_InHumi_SD","Grid5_InTemp_SD",
        "Grid6_InHumi_SD","Grid6_InTemp_SD",
        "Grid7_InHumi_SD","Grid7_InTemp_SD",
        "Grid8_InHumi_SD","Grid8_InTemp_SD",
        "Grid9_InHumi_SD","Grid9_InTemp_SD",
        "Out1_Humi_SD","Out1_Temp_SD",
        "Out2_Humi_SD","Out2_Temp_SD",
        "Out3_Humi_SD","Out3_Temp_SD",
        "Out4_Humi_SD","Out4_Temp_SD",

        "Out1_Current1_Mean", "Out1_Current1_SD",
        "Out1_Current2_Mean","Out1_Current2_SD",

        "Out2_Current1_Mean","Out2_Current1_SD",
        "Out2_Current2_Mean","Out2_Current2_SD"
    ]

    if input("Include middle point in csv? Answer: y/n \n") == 'y':
        columns_order.extend([
            "Grid5Mid_Humidity_Mean",
            "Grid5Mid_Humidity_SD",
            "Grid5Mid_Temperature_Mean",
            "Grid5Mid_Temperature_SD",

            "Grid8Mid_Humidity_Mean",
            "Grid8Mid_Humidity_SD",
            "Grid8Mid_Temperature_Mean",
            "Grid8Mid_Temperature_SD"
        ])

    df = df[columns_order]
    print(f"ORDER DATA{df}")
    return select_Time(df, day, month)



day = int(input("Input your day of Convert to CSV: "))
month = int(input("Input your month of Convert to CSV: "))
# อ่าน JSON และแปลงเป็น DataFrame
with open(f"C:\\Users\\user\\Desktop\\Microclimate\\Source_Code\\RawData\\{day}_{month}_2024.json") as file:
    data = json.load(file)
splitTime(data, day, month)














