import torch
import cv2

# 加载YOLOv5模型
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='E:/Youxun_Projects/4.经济林巡视智能无人车/yolov5-5.0_test0802/runs/train/exp10/weights/best.pt')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='E:/Youxun_Projects/4.经济林巡视智能无人车/yolov5-5.0_test0802/runs/train/exp10/weights/best.pt')
# 打开摄像头
cap = cv2.VideoCapture(0)  # 0代表默认的摄像头，如果有多个摄像头可以尝试1, 2等

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
    
    # 显示结果
    result_frame = results.render()[0]
    cv2.imshow('Orange Detection', result_frame)
    
    # 按'q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()