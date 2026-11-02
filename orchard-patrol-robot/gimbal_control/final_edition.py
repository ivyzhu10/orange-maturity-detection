# coding: UTF-8
import time
import serial
import threading
from udp_service import UdpService

# 全局变量
angle_x = None
angle_y = None
angle_lock = threading.Lock()  # 添加锁来保证线程安全


def parse_command(servo_angle_x, servo_angle_y):
    # 构建指令字节序列
    # 假设指令格式为 [0x55, 0x55, 包长度, 指令类型, 舵机数量, 0xE8, 舵机编号, 角度高字节, 角度低字节]
    # 例如: [0x55, 0x55, 0x0B, 0x03, 0x02, 0xE8, 0x01, 高字节, 低字节, 0x02, 高字节, 低字节]
    command_length = 7 + 2 * 2  # 2舵机，每个舵机需要2个额外字节
    command_x = [
        0x55, 0x55, 0x08, 0x03, 0x01, 0x00, 0x00,
        0x01, servo_angle_x & 0xFF, (servo_angle_x >> 8) & 0xFF,
        0x02, servo_angle_y & 0xFF, (servo_angle_y >> 8) & 0xFF
    ]
    command_y = [
        0x55, 0x55, 0x08, 0x03, 0x01, 0x00, 0x00,
        0x02, servo_angle_y & 0xFF, (servo_angle_y >> 8) & 0xFF
    ]
    bytes_command_x = bytes(command_x)
    bytes_command_y = bytes(command_y)
    return bytes_command_x, bytes_command_y


def angle_to_servo_value(angle):
    """将陀螺仪的角度值转换为舵机的角度值。
    
    Args:
        angle (float): 陀螺仪的角度值，范围从 -180 到 180 度。
        
    Returns:
        int: 舵机的角度值，范围从 0 到 1000。
    """
    # 将角度值扩大100倍
    scaled_angle = angle * 100
    # 映射到舵机角度值范围
    servo_value = int((scaled_angle + 18000) / 360 * 1000 / 100)
    return servo_value


# 数据更新时会调用此方法 This method will be called when data is updated
def updateData(DeviceModel):
    global angle_x, angle_y, angle_lock
    
    with angle_lock:
        # 获得X轴加速度 Obtain X-axis acceleration
        angle_x = DeviceModel.get("AngleX")
        angle_y = DeviceModel.get("AngleY")


# 示例程序主入口 Example program main entrance
if __name__ == '__main__':
    port = 'COM4'
    baudrate = 9600  # 根据实际的波特率调整
    # 打开串口
    ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
    
    # UDP服务 UDP service
    server = UdpService(1399, updateData)
    server.start()
    
    while True:
            if angle_x is not None and angle_y is not None:
                servo_angle_x = angle_to_servo_value(angle_x)
                servo_angle_y = angle_to_servo_value(angle_y)
                print('servo_angle_x:', servo_angle_x)
                print('servo_angle_y:', servo_angle_y)
                ser.write(parse_command(servo_angle_x, servo_angle_y))
                # print("serial data sent successfully")
                
                angle_x = None
                angle_y = None
                time.sleep(0.08)

                
        
    


