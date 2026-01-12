#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2 as cv
import sys
import os

# 导入 app.py 中的 GestureRecognizer 类
# 确保当前目录在 PYTHON PATH 中
sys.path.append(os.getcwd())
try:
    from app import GestureRecognizer
except ImportError as e:
    print(f"无法导入 app.py. 请确保此脚本与 app.py 在同一目录下。\n错误信息: {e}")
    sys.exit(1)

def main():
    # 1. 初始化摄像头
    # 如果有多个摄像头，尝试更改索引 0, 1...
    cap_device = 0
    cap = cv.VideoCapture(cap_device)
    
    if not cap.isOpened():
        print(f"无法打开摄像头 (Device {cap_device})")
        return

    # 设置分辨率（可选，与 app.py 保持一致）
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 540)

    # 2. 初始化手势识别器
    print("正在初始化手势识别模型...")
    try:
        recognizer = GestureRecognizer()
    except Exception as e:
        print(f"模型初始化失败: {e}")
        return
        
    print("初始化完成。按 'ESC' 键退出程序。")

    # 手势ID名称映射 (参考 app.py 的定义)
    GESTURE_NAMES = {
        0: "Open (张开)",
        1: "Close (握拳)",
        2: "Pointer (指)",
        3: "OK",
        4: "Paper (布)",
        5: "Rock (石头)",
        6: "Scissors (剪刀)",
        -1: "None (未识别)"
    }

    try:
        while True:
            # 3. 读取帧
            ret, frame = cap.read()
            if not ret:
                print("\n无法读取视频帧")
                break

            # 4. 获取手势ID
            # flip=True 表示会对图像进行镜像翻转，符合一般摄像头自拍习惯
            gesture_id = recognizer.get_gesture(frame, flip=True)

            # 5. 打印到命令行
            # 使用 \r 和 end='' 来在同一行刷新输出，避免大量刷屏
            name = GESTURE_NAMES.get(gesture_id, "Unknown")
            print(f"\r当前检测到的手势 ID: {gesture_id} -> {name}        ", end="", flush=True)

            # (可选) 显示画面，方便对准摄像头查看效果
            # get_gesture 内部使用镜像后的图像进行识别，这里我们也显示镜像后的图像
            display_image = cv.flip(frame, 1)
            
            # 在画面上绘制ID
            cv.putText(display_image, f"ID: {gesture_id} ({name.split(' ')[0]})", (10, 50), 
                       cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)
            
            cv.imshow('Gesture ID Runner', display_image)

            # 按 ESC 退出
            key = cv.waitKey(10)
            if key == 27:
                break

    except KeyboardInterrupt:
        pass
    finally:
        print("\n\n程序已退出。")
        cap.release()
        cv.destroyAllWindows()

if __name__ == '__main__':
    main()
