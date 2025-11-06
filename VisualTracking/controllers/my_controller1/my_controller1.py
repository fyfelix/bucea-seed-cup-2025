"""my_controller1 controller."""
from controller import Robot, Motor, Camera
import numpy as np
import cv2

# ---------------------------
# 创建机器人实例
# ---------------------------
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# ---------------------------
# 获取左右电机
# ---------------------------
left_motor = robot.getDevice('MotorLeft')
right_motor = robot.getDevice('MotorRight')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# ---------------------------
# 启用摄像头
# ---------------------------
camera = robot.getDevice('camera')
camera.enable(timestep)

# ---------------------------
# 主循环
# ---------------------------
max_speed = min(left_motor.getMaxVelocity(), right_motor.getMaxVelocity())

while robot.step(timestep) != -1:
    # 前进
    # left_motor.setVelocity(0.5*max_speed)
    # right_motor.setVelocity(0.5*max_speed)

    # 获取图像缓冲区
    image = camera.getImage()
    if image:
        width = camera.getWidth()
        height = camera.getHeight()

        # 将 Webots 图像转换为 numpy 数组
        img_array = np.frombuffer(image, np.uint8).reshape((height, width, 4))
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)

        # 上下翻转图像
        flipped_img = cv2.flip(img_bgr, 0)

        # 显示翻转后的图像
        cv2.imshow("Flipped Camera View", img_bgr)
        if cv2.waitKey(1) & 0xFF == 27:  # 按下 ESC 键退出显示窗口
            break

# 释放 OpenCV 窗口
cv2.destroyAllWindows()
