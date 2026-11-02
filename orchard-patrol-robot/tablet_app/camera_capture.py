import sys
import os
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        # 定义定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # 初始化摄像头
        self.cap = cv2.VideoCapture(0)

        # 确保图像保存文件夹存在
        self.image_folder = 'images'
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

        # 初始化用户界面
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Camera App')
        self.setGeometry(0, 0, 1920, 1080)  # 修改为2560x1600

        # 创建布局
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)  # 移除外边距

        # 添加一个标签用于显示摄像头画面
        self.label = QLabel(self)
        vbox.addWidget(self.label)

        # 创建水平布局放置按钮
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)  # 移除外边距

        # 创建退出按钮并连接信号槽
        self.exit_btn = QPushButton('quit', self)
        self.exit_btn.clicked.connect(self.close)

        # 创建拍照按钮并连接信号槽
        self.snap_btn = QPushButton('snap', self)
        self.snap_btn.clicked.connect(self.take_snapshot)

        # 使用 addStretch() 来添加弹性空间，把按钮推向左右两边
        hbox.addWidget(self.snap_btn)
        hbox.addStretch(1)  # 再次添加可拉伸的空间，把拍照按钮推向右边
        hbox.addWidget(self.exit_btn)
        hbox.addStretch(1)  # 这将创建一个可拉伸的空间，把退出按钮推向左边

        # 将水平布局添加到垂直布局的最后，使其位于窗口底部
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # 开始定时器以更新画面
        self.timer.start(30)  # 每30ms刷新一次

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(self.width(), self.height() - self.snap_btn.height(), aspectRatioMode=True)
            self.label.setPixmap(QPixmap.fromImage(p))

    def take_snapshot(self):
        ret, frame = self.cap.read()
        if ret:
            now = datetime.now().strftime("%Y%m%d") #string format time
            files = [f for f in os.listdir(self.image_folder) if f.startswith(now)]
            count = len(files) + 1
            filename = f"{self.image_folder}/{now}_{count:03d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved snapshot as {filename}")

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera_app = CameraApp()
    camera_app.show()
    sys.exit(app.exec_())