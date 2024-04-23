import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import cv2
from matplotlib import colors
from matplotlib.patches import Rectangle

def plotHeat(data):
    timestamps = data['Timestamp'].unique()

    save_directory = f"C:\\Users\\user\\Desktop\\Microclimate\\Heatindex"
    os.makedirs(save_directory, exist_ok=True)
    count = 1

    for timestamp in timestamps:
        current_data = data[data['Timestamp'] == timestamp].iloc[0]

        heatmap_data = np.array([
            [current_data['Grid3_Heat_Index'], current_data['Grid6_Heat_Index'], current_data['Grid9_Heat_Index']],
            [current_data['Grid2_Heat_Index'], current_data['Grid5_Heat_Index'], current_data['Grid8_Heat_Index']],
            [current_data['Grid1_Heat_Index'], current_data['Grid4_Heat_Index'], current_data['Grid7_Heat_Index']],
        ]).astype(float)

        color_list = ['#FFFFFF', '#87CEEB', '#32CD32', '#FFFF00', '#FFA500', '#FF0000']
        bounds = [0, 22, 27, 33, 40, 52]

        cmap = colors.ListedColormap(color_list)
        norm = colors.BoundaryNorm(bounds, cmap.N, clip=True)

        sns.set(font_scale=1)
        fig, ax = plt.subplots(figsize=(16, 9))
        plt.tick_params(axis='both', which='major', labelsize=10, labelbottom=False, bottom=False, top=False,
                        labeltop=True)

        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap=cmap, norm=norm, xticklabels=['G3', 'G6', 'G9'],
                    yticklabels=['G3', 'G2', 'G1'], cbar=True, ax=ax)

        # Custom colors and borders
        for i in range(len(heatmap_data)):
            for j in range(len(heatmap_data[i])):
                cell_value = heatmap_data[i][j]
                cell_color = cmap(norm([cell_value]))[0]
                ax.add_patch(Rectangle((j, i), 1, 1, fill=True, facecolor=cell_color, edgecolor='White', linewidth=4))

        fig.subplots_adjust(top=0.9)  # ระยะห่างจาก title ไปยังกราฟ
        fig.suptitle(f'Meeting Room {timestamp}', fontsize=16, ha='center')

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

# data01 = pd.read_csv(f"D:\\jsontocsv\\RawData\\MeetingRoom\\csvData\\4_11_2024_MeetingRoom_HeatIndex.csv")
data01 = pd.read_csv(f"C:\\Users\\user\\Desktop\\Microclimate\\data_heatindex.csv")
plotHeat(data01)







#
# heatmap_data = np.array([
#             [33.14, 31.85, 29.24],
#             [31.56, 25.38, 27.98],
#             [30.12, 27.52, 26.60],
#         ]).astype(float)
#
# color_list = ['#87CEEB', '#32CD32', '#FFFF00', '#FFA500', '#FF0000']
# bounds = [0, 22, 27, 33, 40]
#
# cmap = colors.ListedColormap(color_list)
# norm = colors.BoundaryNorm(bounds, cmap.N, clip=True)
#
# sns.set(font_scale=1)
# fig, ax = plt.subplots(figsize=(16, 9))
#
# plt.rcParams['font.family'] = 'TH SarabunPSK'
# plt.rcParams['font.size'] = 40
#
# plt.tick_params(axis='both', which='major', labelsize=40, labelbottom=False, bottom=False, top=False,
#                 labeltop=True)
#
#
# sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap=cmap, norm=norm, xticklabels=['ID3', 'ID6', 'ID9'],
#             yticklabels=['ID3', 'ID2', 'ID1 (Ref)'], cbar=True, ax=ax ).collections[0].colorbar.ax.tick_params(labelsize=40)
#
# plt.xticks(fontname='TH SarabunPSK', fontsize=40)
# plt.yticks(fontname='TH SarabunPSK', fontsize=40, rotation=0)
#
# # Custom colors and borders
# for i in range(len(heatmap_data)):
#     for j in range(len(heatmap_data[i])):
#         cell_value = heatmap_data[i][j]
#         cell_color = cmap(norm([cell_value]))[0]
#         ax.add_patch(Rectangle((j, i), 1, 1, fill=True, facecolor=cell_color, edgecolor='White', linewidth=4))
#
# fig.subplots_adjust(top=0.85)  # ระยะห่างจาก title ไปยังกราฟ
# fig.suptitle(f'Meeting Room ', fontsize=50, ha='center')
# plt.show()
# # plt.clf()