# orange-maturity-detection
Remote controlled patrol vehicle for orchards with Mecanum wheels, an IMU controlled gimbal camera, and real time YOLO fruit ripeness detection and counting.
# Orchard Patrol Robot

An unmanned patrol vehicle that helps farmers monitor fruit orchards remotely, built as a Regeneron science fair project.

## Why
Checking an orchard by hand is slow, tiring, and easy to get wrong. On a 100 hectare farm, it can take five workers ten hours to look over every tree for ripeness, pests, and disease. With this vehicle, one operator can run the same patrol from a tablet in about 3 hours.

## Features
- **Omnidirectional movement:** Mecanum wheels let the vehicle move sideways and turn in place between narrow plant rows.
- **IMU controlled gimbal camera:** A Raspberry Pi 4B reads gyroscope data from a WiFi IMU and maps the Z axis to a yaw servo and the Y axis to a pitch servo through a serial servo driver. The operator tilts their hand and the camera follows.
- **Fruit ripeness detection and counting:** An object detection model, trained on 286 images I labeled by hand in LabelImg, finds oranges, sorts them into ripe and unripe, and counts them frame by frame.
- **Live video:** A 5GHz wireless video module streams footage straight to the operator's tablet.
- **Field data collection:** The operator can capture close up images of pests and disease, building a dataset for future models.

## Hardware
Raspberry Pi 4B, WiFi IMU module, two serial bus servos (240° range, 0.3° accuracy), USB to TTL converter, Mecanum wheel chassis, 5GHz wireless video transmitter and receiver, tablet, and a joystick and tablet mount I designed in SolidWorks and 3D printed.

## Model comparison
Fruits take up only a tiny part of each tree image, which makes small object detection the main challenge. I trained two single stage detectors and one two stage detector on the same dataset and compared them:

| Model | Size (MB) | Params | Precision | Recall | mAP@.5 |
|---|---|---|---|---|---|
| YOLOv5s | 14.0 | 7.4M | 0.74 | 0.51 | 0.51 |
| YOLOv8s | 21.5 | 11.1M | 0.78 | 0.59 | 0.58 |
| Faster R-CNN | 167 | 41M | 0.82 | 0.65 | 0.63 |

Faster R-CNN was the most accurate, but the YOLO models are a fraction of the size and much faster, which matters when the model has to run in real time on a tablet in the field.

## Testing
- **Gimbal control:** Rotating the IMU clockwise or counterclockwise turned the yaw servo in sync, and tilting it moved the pitch servo from horizontal up to vertical.
- **Live detection:** With oranges of different ripeness placed in front of the camera, the model running on the tablet detected, classified, and counted them correctly.

## Future work
- Higher resolution, interference resistant video transmission
- A pest and disease detection model trained on a larger dataset
- GPS tracking to find the vehicle in large fields
- Drones scanning from above while the vehicle inspects up close
- Adapting the platform to other crops like apples and grapes
