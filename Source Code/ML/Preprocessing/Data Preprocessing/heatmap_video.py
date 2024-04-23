import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import cv2

def plotHeat(data):
    timestamps = data['Timestamp'].unique()

    save_directory = f"C:\\Users\\user\\Desktop\\Microclimate\\Heatmap"
    os.makedirs(save_directory, exist_ok=True)
    count = 1

    for timestamp in timestamps:
        current_data = data[data['Timestamp'] == timestamp].iloc[0]

        heatmap_data = np.array([
            [current_data['Grid3_InTemp_Mean'], current_data['Grid6_InTemp_Mean'], current_data['Grid9_InTemp_Mean'],current_data['Out4_Temp_Mean']],
            [current_data['Grid2_InTemp_Mean'], current_data['Grid5_InTemp_Mean'], current_data['Grid8_InTemp_Mean'],current_data['Out4_Temp_Mean']],
            [current_data['Grid1_InTemp_Mean'], current_data['Grid4_InTemp_Mean'], current_data['Grid7_InTemp_Mean'],current_data['Out3_Temp_Mean']],
            [current_data['Out1_Temp_Mean'], current_data['Out1_Temp_Mean'], current_data['Out2_Temp_Mean'],current_data['Out3_Temp_Mean']],
        ]).astype(float)


        heatmap_data2 = np.array([
            [current_data['Grid3_InHumi_Mean'], current_data['Grid6_InHumi_Mean'], current_data['Grid9_InHumi_Mean'],
             current_data['Out4_Humi_Mean']],
            [current_data['Grid2_InHumi_Mean'], current_data['Grid5_InHumi_Mean'], current_data['Grid8_InHumi_Mean'],
             current_data['Out4_Humi_Mean']],
            [current_data['Grid1_InHumi_Mean'], current_data['Grid4_InHumi_Mean'], current_data['Grid7_InHumi_Mean'],
             current_data['Out3_Humi_Mean']],
            [current_data['Out1_Humi_Mean'], current_data['Out1_Humi_Mean'], current_data['Out2_Humi_Mean'],
             current_data['Out3_Humi_Mean']],
        ]).astype(float)

        # print(type(heatmap_data[0][0]))
        # print(heatmap_data)
        #
        sns.set(font_scale=1)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(32, 9))
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap='coolwarm',
                    xticklabels=['G3', 'G6', 'G9', 'Outdoor2'],
                    yticklabels=['G3', 'G2', 'G1', 'Outdoor1'],
                    linewidths=2, linecolor='white', cbar=True, ax=ax1, vmax=27, vmin=22)
        ax1.set_title(f'Meeting Room Temperature(°C) {timestamp}', fontsize=16, ha='center')
        ax1.xaxis.tick_top()

        sns.heatmap(heatmap_data2, annot=True, fmt=".2f", cmap='coolwarm',
                    xticklabels=['G3', 'G6', 'G9', 'Outdoor2'],
                    yticklabels=['G3', 'G2', 'G1', 'Outdoor1'],
                    linewidths=2, linecolor='white', cbar=True, ax=ax2, vmax=90, vmin=60)
        ax2.set_title(f'Meeting Room Humidity(%) {timestamp}', fontsize=16, ha='center')
        ax2.xaxis.tick_top()

        fig.subplots_adjust(top=0.9)  # ระยะห่างจาก title ไปยังกราฟ
        # fig.suptitle(f'Meeting Room {timestamp}', fontsize=16, ha='center')

        save_path = f'{save_directory}\\heatmap_{count}.png'
        plt.savefig(save_path)
        count += 1
        plt.clf()

    print(f"บันทึกรูป heatmap สำหรับวันที่: {[f'heatmap_{count}.png' for count in range(1, count)]}")
    plotMidHeat(data) #TODO Uncomment
    return createVideo(save_directory, timestamps)

def plotMidHeat(data):
    timestamps = data['Timestamp'].unique()

    save_directory = f"C:\\Users\\user\\Desktop\\Microclimate\\Heatmap\\Middle_Bottom_Grid"
    os.makedirs(save_directory, exist_ok=True)
    count = 1

    for timestamp in timestamps:
        current_data = data[data['Timestamp'] == timestamp].iloc[0]

        heatmap_data_temp = np.array([
            [current_data['Grid5Mid_Temperature_Mean'], current_data['Grid8Mid_Temperature_Mean']],
            [current_data['Grid5_InTemp_Mean'], current_data['Grid8_InTemp_Mean']],
        ]).astype(float)

        heatmap_data_humi = np.array([
            [current_data['Grid5Mid_Humidity_Mean'], current_data['Grid8Mid_Humidity_Mean']],
            [current_data['Grid5_InHumi_Mean'], current_data['Grid8_InHumi_Mean']],
        ]).astype(float)

        # print(type(heatmap_data[0][0]))
        # print(heatmap_data)
        #
        sns.set(font_scale=1)
        # fig, ax1 = plt.subplots(1, 2, figsize=(32, 9))
        fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(32, 9))    # 1 Axis
        sns.heatmap(heatmap_data_temp, annot=True, fmt=".2f", cmap='coolwarm',
                    xticklabels=['Mid G5', 'Mid G8'],
                    yticklabels=['G5', 'G8'],
                    linewidths=2, linecolor='white', cbar=True, ax=ax1, vmax=34, vmin=26)
        ax1.set_title(f'Middle Grid Temperature(°C) {timestamp}', fontsize=16, ha='center')
        ax1.xaxis.tick_top()

        sns.heatmap(heatmap_data_humi, annot=True, fmt=".2f", cmap='coolwarm',
                    xticklabels=['Mid G5', 'Mid G8'],
                    yticklabels=['G5', 'G8'],
                    linewidths=2, linecolor='white', cbar=True, ax=ax2, vmax=100, vmin=20)
        ax2.set_title(f'Middle Grid Humidity(%) {timestamp}', fontsize=16, ha='center')
        ax2.xaxis.tick_top()


        fig.subplots_adjust(top=0.9)  # ระยะห่างจาก title ไปยังกราฟ
        # fig.suptitle(f'Meeting Room {timestamp}', fontsize=16, ha='center')

        save_path = f'{save_directory}\\heatmap_{count}.png'
        plt.savefig(save_path)
        count += 1
        plt.clf()

    print(f"บันทึกรูป heatmap สำหรับวันที่: {[f'heatmap_{count}.png' for count in range(1, count)]}")
    return createVideo(save_directory, timestamps)


def createVideo(save_directory, timestamps):
        # กำหนดชื่อไฟล์วิดีโอ
        video_filename = f"{save_directory}\\heatmap_video.mp4"

        # โค้ดสร้างวิดีโอจากไฟล์รูปภาพ
        image_files = [os.path.join(save_directory, f'heatmap_{i}.png') for i in range(1, len(timestamps) + 1)]
        first_image = cv2.imread(image_files[0])
        height, width, layers = first_image.shape
        size = (width, height)

        out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'mp4v'), 6, size)

        for image_file in image_files:
            img = cv2.imread(image_file)
            out.write(img)

        out.release()

        print(f'สร้างวิดีโอ {video_filename} เรียบร้อยแล้ว')
        return 0



data01 = pd.read_csv(f"C:\\Users\\user\\Desktop\\Microclimate\\data.csv")
plotHeat(data01)
