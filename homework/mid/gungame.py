import cv2
import torch
import numpy as np
from mss import mss
from ultralytics import YOLO
import matplotlib.pyplot as plt
import pyautogui  # 用於控制滑鼠
from pynput.mouse import Listener  # 用於監聽滑鼠事件
import keyboard  # 用於監聽鍵盤事件

# 載入模型
model = YOLO("yolov8n-pose.pt")

# 設定螢幕截圖範圍為螢幕中心
sct = mss()

# 獲取螢幕解析度
screen_width = sct.monitors[1]['width']
screen_height = sct.monitors[1]['height']

# 設定截圖區域大小，並將其置中
monitor_width = 800
monitor_height = 600
monitor = {
    "top": (screen_height - monitor_height) // 2,
    "left": (screen_width - monitor_width) // 2,
    "width": monitor_width,
    "height": monitor_height
}

# 用來儲存每個物體的中心點
centers = []

# 儲存滑鼠左鍵是否按下的狀態
mouse_pressed = False

# 控制滑鼠移動是否啟用
mouse_control_enabled = False

# 用來處理滑鼠事件
def on_click(x, y, button, pressed):
    global mouse_pressed
    if button.name == 'left':  # 監聽滑鼠左鍵
        mouse_pressed = pressed  # 當滑鼠左鍵按下時，設置為 True，放開時設置為 False

# 開啟監聽滑鼠左鍵事件
listener = Listener(on_click=on_click)
listener.start()

# 當按下特定鍵時啟動或關閉滑鼠控制
def on_keyboard_event():
    global mouse_control_enabled
    if keyboard.is_pressed('ctrl+q'):  # 按下 Ctrl+Q 開啟滑鼠控制
        mouse_control_enabled = True
        print("滑鼠控制啟動")
    elif keyboard.is_pressed('ctrl+b'):  # 按下 Ctrl+B 關閉滑鼠控制
        mouse_control_enabled = False
        print("滑鼠控制關閉")

def detect_and_display():
    global mouse_pressed  # 在函數中使用全域變數
    global mouse_control_enabled  # 控制是否啟用滑鼠控制
    plt.ion()  # 啟用 Matplotlib 的互動模式
    fig, ax = plt.subplots(figsize=(10, 6))

    while True:
        # 截取畫面
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        # 進行目標物件偵測
        results = model.predict(source=img_rgb, conf=0.5, verbose=False)

        # 繪製偵測結果
        annotated_img = results[0].plot()

        detections = results[0].keypoints  # YOLOv8 的人體架構檢測
        centers.clear()  # 清空之前的目標點

        # 確認是否有檢測結果
        if detections is not None and len(detections) > 0:
            for keypoints in detections:
                list_p = keypoints.data.tolist()

                # 確保 list_p 不為空且包含有效數據
                if list_p and len(list_p[0]) >= 5:  # 確保有至少 5 個點
                    for i in range(5):  # 遍歷鼻子、左眼、右眼、左耳、右耳
                        if list_p[0][i][0] != 0 and list_p[0][i][1] != 0:  # 如果座標不是 (0, 0)
                            # 轉換為螢幕的絕對座標
                            abs_x = int(list_p[0][i][0] + monitor["left"])
                            abs_y = int(list_p[0][i][1] + monitor["top"])
                            
                            # 將座標加入中心列表
                            centers.append((abs_x, abs_y))
                            
                            # 打印結果並停止檢查
                            # print(f"掃描到 {i}: ({abs_x}, {abs_y})")
                            break
        else:
            print("沒有偵測到物體")




        # 使用 Matplotlib 顯示圖片
        ax.clear()
        ax.imshow(cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB))
        ax.axis("off")
        plt.pause(0.001)  # 更新圖像

        # 持續監聽按鍵來控制滑鼠
        on_keyboard_event()

        # 當滑鼠左鍵持續按下時，找到最近的物體並移動滑鼠
        if mouse_control_enabled and mouse_pressed:  # 如果滑鼠控制啟動並且按住左鍵
            if centers:  # 確保有物體偵測
                # 取得當前滑鼠位置
                mouse_x, mouse_y = pyautogui.position()

                # 計算滑鼠到每個物體中心的距離
                min_dist = float("inf")
                nearest_center = None
                for center in centers:
                    dist = np.sqrt((mouse_x - center[0]) ** 2 + (mouse_y - center[1]) ** 2)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_center = center

                if nearest_center is not None:
                    # 將滑鼠移動到最近的物體中心
                    pyautogui.moveTo(nearest_center[0], nearest_center[1])
                    print("hit")
        
        # 檢查是否按下 Ctrl + S 退出程式
        if keyboard.is_pressed('ctrl+s'):
            print("按下 Ctrl+S，程式結束")
            break

    plt.close()

if __name__ == "__main__":
    detect_and_display()

# video :https://www.youtube.com/watch?v=jtCwLwYphJU&ab_channel=AriesCheng%28%E5%90%B3%E4%B8%9E%E6%81%A9%29