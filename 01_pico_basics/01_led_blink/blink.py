"""
LED 閃爍程式
控制 Pico W 內建的 LED 進行閃爍

硬體：Raspberry Pi Pico W
功能：讓內建 LED 以 1 秒間隔閃爍
"""

import machine
import time

# 初始化內建 LED
# Pico W 的內建 LED 連接到 "LED" 腳位
led = machine.Pin("LED", machine.Pin.OUT)

print("LED 閃爍程式開始")
print("按 Ctrl+C 停止程式")

try:
    # 無限迴圈
    while True:
        # 開啟 LED
        led.on()
        print("LED 開啟")
        time.sleep(1)  # 等待 1 秒
        
        # 關閉 LED
        led.off()
        print("LED 關閉")
        time.sleep(1)  # 等待 1 秒

except KeyboardInterrupt:
    # 當使用者按下 Ctrl+C 時執行
    print("\n程式已停止")
    led.off()  # 確保 LED 關閉
