# coding: UTF-8
import time
import serial
import threading
import cv2
from udp_service import UdpService

# 全局变量
angle_pitch = None
angle_yaw = None
angle_lock = threading.Lock()  # 添加锁来保证线程安全


def parse_command(servo_angle_x, servo_angle_y):
    # 构建指令字节序列
    # 假设指令格式为 [0x55, 0x55, 包长度, 指令类型, 舵机数量, 0xE8, 舵机编号, 角度高字节, 角度低字节]
    # 例如: [0x55, 0x55, 0x0B, 0x03, 0x02, 0xE8, 0x01, 高字节, 低字节, 0x02, 高字节, 低字节]
    command_length = 7 + 2 * 2  # 2舵机，每个舵机需要2个额外字节
    command_x = [
        0x55, 0x55, 0x08, 0x03, 0x01, 0x00, 0x00,
        0x01, servo_angle_x & 0xFF, (servo_angle_x >> 8) & 0xFF
    ]
    command_y = [
        0x55, 0x55, 0x08, 0x03, 0x01, 0x00, 0x00,
        0x02, servo_angle_y & 0xFF, (servo_angle_y >> 8) & 0xFF
    ]
    bytes_command_x = bytes(command_x)
    bytes_command_y = bytes(command_y)
    return bytes_command_x, bytes_command_y


# def angle_to_servo_value(angle):
#     """将陀螺仪的角度值转换为舵机的角度值。
#
#     Args:
#         angle (float): 陀螺仪的角度值，范围从 -180 到 180 度。
#
#     Returns:
#         int: 舵机的角度值，范围从 0 到 1000。
#     """
#     # 将角度值扩大100倍
#     scaled_angle = angle * 100
#     # 映射到舵机角度值范围
#     servo_value = int((scaled_angle + 18000) / 360 * 1000 / 100)
#     return servo_value


def angle_to_servo_value(angle, min_angle, max_angle, min_value, max_value):
    # 将角度值乘以100以便处理小数点后的两位数字
    scaled_angle = int(angle * 100)
    
    # 确保角度值在有效范围内
    scaled_angle = max(min_angle * 100, min(max_angle * 100, scaled_angle))
    
    # 计算比例因子
    range_angle = max_angle * 100 - min_angle * 100
    range_value = max_value - min_value
    
    # 映射角度到舵机数值
    servo_value = int(((scaled_angle - min_angle * 100) / range_angle) * range_value + min_value)
    
    return servo_value

# 数据更新时会调用此方法 This method will be called when data is updated
def updateData(DeviceModel):
    global angle_pitch, angle_yaw, angle_lock

    with angle_lock:
        # 获得X轴加速度 Obtain X-axis acceleration
        angle_pitch = DeviceModel.get("AngleY")
        angle_yaw = DeviceModel.get("AngleZ")


# 示例程序主入口 Example program main entrance
if __name__ == '__main__':
    port = 'COM4'
    baudrate = 9600  # 根据实际的波特率调整
    # 打开串口
    ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)

    # UDP服务 UDP service
    server = UdpService(1399, updateData)
    server.start()

    cap = cv2.VideoCapture(1)

    while True:
        if angle_pitch is not None and angle_yaw is not None:
            # 舵机角度映射到舵机数值
            yaw_value = angle_to_servo_value(angle_yaw, -90, 90, 125, 875)
            pitch_value = angle_to_servo_value(-angle_pitch, -30, 30, 850, 300)
            # print('servo_angle_x:', servo_angle_x)
            # print('servo_angle_y:', servo_angle_y)
            a, b = parse_command(yaw_value, pitch_value)
            ser.write(b)         # 俯仰舵机
            ser.write(a)         # 偏航舵机
            # ser.write(parse_command(servo_angle_x, servo_angle_y))
            # print("serial data sent successfully")

            angle_pitch = None
            angle_yaw = None
            # 读取摄像头帧
            ret, frame = cap.read()
            if ret:
                # 显示帧
                cv2.imshow('Camera Feed', frame)
                # 按q键退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            time.sleep(0.08)
    #随时准备按q退出
    cap.release()
    cv2.destroyAllWindows()
    #停止调用，关闭窗口





