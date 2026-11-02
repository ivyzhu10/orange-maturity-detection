import threading
import queue
import time
import torch
import cv2
import numpy as np

# 加载YOLOv5模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path='E:/Youxun_Projects/4.经济林巡视智能无人车/yolov5-5.0_test0802/runs/train/exp10/weights/best.pt')

# 假设模型输出的类别标签是 'red_orange' 和 'green_orange'
class_labels = model.names  # 获取模型的类别标签

# 创建队列用于在线程间传递数据
frame_queue = queue.Queue(maxsize=5)  # 设置最大队列大小以防止内存占用过多
result_queue = queue.Queue()

def read_frames(cap, frame_queue):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法获取帧")
            break
        
        # 转换为RGB格式，因为YOLOv5期望的是RGB图像
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 如果队列已满，则移除最老的元素
        if frame_queue.full():
            try:
                frame_queue.get_nowait()  # 移除最老的帧
            except queue.Empty:
                pass
        
        frame_queue.put(frame_rgb)

        # 添加一个小的延迟以避免过度消耗CPU资源
        time.sleep(0.03)  # 根据需要调整此值

def process_frames(model, frame_queue, result_queue):
    while True:
        if not frame_queue.empty():
            frame_rgb = frame_queue.get()
            
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
            
            result_queue.put(result_frame_bgr)

def display_results(result_queue):
    while True:
        if not result_queue.empty():
            result_frame_bgr = result_queue.get()
            # 显示结果
            cv2.imshow('Orange Detection', result_frame_bgr)
            
            # 按'q'键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    # 打开摄像头
    cap = cv2.VideoCapture('rtsp://192.168.144.25:8554/main.264')
    
    # 启动线程
    threads = []
    threads.append(threading.Thread(target=read_frames, args=(cap, frame_queue)))
    threads.append(threading.Thread(target=process_frames, args=(model, frame_queue, result_queue)))
    threads.append(threading.Thread(target=display_results, args=(result_queue,)))

    # 设置线程为守护线程，这样主线程结束时它们也会自动结束
    for t in threads:
        t.daemon = True
        t.start()

    # 主线程等待所有子线程完成（实际上这里会一直运行直到用户终止程序）
    for t in threads:
        t.join()

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()