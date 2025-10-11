"""
按鈕輸入處理
學習如何讀取按鈕狀態並處理輸入

硬體連接：
- 按鈕一端連接到 GPIO 15
- 按鈕另一端連接到 GND
- 使用內部上拉電阻
"""

import machine
import time

# 初始化按鈕（GPIO 15，使用內部上拉電阻）
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# 初始化 LED
led = machine.Pin("LED", machine.Pin.OUT)

print("按鈕輸入程式")
print("按下按鈕來控制 LED")
print("按 Ctrl+C 停止程式")
print()

try:
    while True:
        # 讀取按鈕狀態
        # 使用上拉電阻時：按下 = 0（LOW），放開 = 1（HIGH）
        button_state = button.value()
        
        if button_state == 0:  # 按鈕被按下
            led.on()
            print("按鈕按下 - LED 開啟")
        else:  # 按鈕放開
            led.off()
            print("按鈕放開 - LED 關閉")
        
        # 短暫延遲避免過度讀取
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n程式已停止")
    led.off()
