import torch
import cv2
import numpy as np

# 加载YOLOv5模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path='E:/Youxun_Projects/4.经济林巡视智能无人车/yolov5-5.0_test0802/runs/train/exp10/weights/best.pt')

# 假设模型输出的类别标签是 'red_orange' 和 'green_orange'
print("model.names: ", model.names)
class_labels = model.names  # 获取模型的类别标签

# 打开摄像头
# cap = cv2.VideoCapture('rtsp://192.168.144.25:8554/main.264')  # 0代表默认的摄像头，如果有多个摄像头可以尝试1, 2等
# cap.set(cv2.CAP_PROP_FPS, 10)  # 尝试将帧率设置为10fps
cap = cv2.VideoCapture(1)

while True:
    # 读取帧
    ret, frame = cap.read()
    if not ret:
        print("无法获取帧")
        break
    
    # 转换为RGB格式，因为YOLOv5期望的是RGB图像
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 进行预测
    results = model(frame_rgb)
    
    # 初始化计数器
    red_orange_count = 0
    green_orange_count = 0
    
    # 遍历检测结果，统计不同颜色的橘子数量
    for detection in results.xyxy[0]:  # xyxy表示边界框坐标
        class_index = int(detection[-1].item())  # 类别索引
        class_name = class_labels[class_index]  # 类别名称
        
        if class_name == 'orange':
            red_orange_count += 1
        elif class_name == 'green_orange':
            green_orange_count += 1
    
    # 渲染结果
    result_frame = results.render()[0]
    
    # 将渲染后的图像从RGB转换回BGR，以便使用OpenCV显示
    result_frame_bgr = cv2.cvtColor(result_frame, cv2.COLOR_RGB2BGR)
    
    # 在图像上显示统计结果
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (10, 30)
    font_scale = 1
    color = (255, 0, 0)  # 蓝色
    thickness = 2
    
    text = f'Red Oranges: {red_orange_count}, Green Oranges: {green_orange_count}'
    result_frame_bgr = cv2.putText(result_frame_bgr, text, org, font, font_scale, color, thickness, cv2.LINE_AA)
    
    # 显示结果
    cv2.imshow('Orange Detection', result_frame_bgr)
    
    # 按'q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()

print(f"最终统计结果 - 红色橘子: {red_orange_count}, 绿色橘子: {green_orange_count}")