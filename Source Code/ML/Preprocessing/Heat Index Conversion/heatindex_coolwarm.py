import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import cv2

def plotHeat(data):
    timestamps = data['Timestamp'].unique()

    save_directory = f"C:\\Users\\user\\Desktop\\Microclimate\\Heatindex_coolwarm"
    os.makedirs(save_directory, exist_ok=True)
    count = 1

    for timestamp in timestamps:
        current_data = data[data['Timestamp'] == timestamp].iloc[0]

        heatmap_data = np.array([
            [current_data['Grid3_Heat_Index'], current_data['Grid6_Heat_Index'], current_data['Grid9_Heat_Index']],
            [current_data['Grid2_Heat_Index'], current_data['Grid5_Heat_Index'], current_data['Grid8_Heat_Index']],
            [current_data['Grid1_Heat_Index'], current_data['Grid4_Heat_Index'], current_data['Grid7_Heat_Index']],
        ]).astype(float)


        print(f'\nHumid: {heatmap_data}')

        print(type(heatmap_data[0][0]))
        # print(heatmap_data)
        #
        sns.set(font_scale=1)
        fig, ax1= plt.subplots(1,figsize=(16, 9))
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap='coolwarm',
                    xticklabels=['G3', 'G6', 'G9'],

                    yticklabels=['G3', 'G2', 'G1'],
                    linewidths=4, linecolor='white', cbar=True, ax=ax1, vmax=27, vmin=23)
                    # linewidths=4, linecolor='white', cbar=True, ax=ax1, vmax=40, vmin=23)
        ax1.set_title(f'Meeting Room Heatindex {timestamp}', fontsize=16, ha='center')
        ax1.xaxis.tick_top()

        fig.subplots_adjust(top=0.9)  # ระยะห่างจาก title ไปยังกราฟ
        # fig.suptitle(f'Meeting Room {timestamp}', fontsize=16, ha='center')

        save_path = f'{save_directory}\\heatindex_{count}.png'
        plt.savefig(save_path)
        count += 1
        plt.clf()

    print(f"บันทึกรูป heatindex สำหรับวันที่: {[f'heatindex_{count}.png' for count in range(1, count)]}")
    return createVideo(save_directory, timestamps)

def createVideo(save_directory, timestamps):
        # กำหนดชื่อไฟล์วิดีโอ
        video_filename = f"{save_directory}\\heatindex_video.mp4"

        # โค้ดสร้างวิดีโอจากไฟล์รูปภาพ
        image_files = [os.path.join(save_directory, f'heatindex_{i}.png') for i in range(1, len(timestamps) + 1)]
        first_image = cv2.imread(image_files[0])
        height, width, layers = first_image.shape
        size = (width, height)

        out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'mp4v'), 6, size)

        for image_file in image_files:
            img = cv2.imread(image_file)
            out.write(img)

        out.release()

        print(f'สร้างวิดีโอ {video_filename} เรียบร้อยแล้ว')
        return video_filename

# data01 = pd.read_csv(f"D:\\jsontocsv\\RawData\\MeetingRoom\\csvData\\4_11_2024_[8-15]_MeetingRoom_HeatIndex.csv")
data01 = pd.read_csv("C:\\Users\\user\\Desktop\\Microclimate\\data_heatindex.csv")
plotHeat(data01)
