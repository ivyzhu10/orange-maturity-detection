import serial
import struct

def send_command(yaw_angle, pitch_angle):
    # Map servo angles to servo values
    yaw_value = map_angle(yaw_angle, -90, 90, 125, 875)
    pitch_value = map_angle(pitch_angle, -30, 30, 850, 300)
    
    # Convert to byte format
    yaw_low_byte, yaw_high_byte = divmod(yaw_value, 256)
    pitch_low_byte, pitch_high_byte = divmod(pitch_value, 256)
    print("Yaw angle:", yaw_low_byte, yaw_high_byte)
    print("Pitch angle:", pitch_low_byte, pitch_high_byte)

    # Construct the complete command
    command = [
        0x55, 0x55,  # Frame header
        0x0B,        # Frame length
        0x03,        # Device ID
        0x02,        # Command type
        0x01,        # Sub-command/register address (yaw angle)
        yaw_low_byte, yaw_high_byte,  # Yaw angle
        0x02,        # Sub-command/register address (pitch angle)
        pitch_low_byte, pitch_high_byte,  # Pitch angle
        0x00         # Assuming checksum is 0x00
    ]
    
    # Send command
    # ser.write(command)
    
    # If needed, add code here to read the response from the lower computer
    # response = ser.read(ser.in_waiting)  # Read all available data
    # print("Received:", response.hex())  # Can be commented out or kept for debugging

def map_angle(angle, in_min, in_max, out_min, out_max):
    # Map angle to servo value
    return int((angle - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def angle_to_servo_value(angle, min_angle, max_angle, min_value, max_value):
    # Multiply angle by 100 to handle two decimal places
    scaled_angle = int(angle * 100)
    
    # Ensure the angle is within a valid range
    scaled_angle = max(min_angle * 100, min(max_angle * 100, scaled_angle))
    
    # Calculate scale factor
    range_angle = max_angle * 100 - min_angle * 100
    range_value = max_value - min_value
    
    # Map angle to servo value
    servo_value = int(((scaled_angle - min_angle * 100) / range_angle) * range_value + min_value)
    
    return servo_value

if __name__ == "__main__":
    # Define the angles to be sent
    yaw_angle = 45  # Example yaw angle
    pitch_angle = 15  # Example pitch angle
    
    # Send command
    ret = angle_to_servo_value(45.56, -90, 90, 125, 875)
    print(ret)
