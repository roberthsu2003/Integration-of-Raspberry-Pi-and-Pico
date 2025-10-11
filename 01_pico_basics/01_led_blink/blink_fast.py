"""
快速閃爍 LED
練習：調整閃爍頻率

學生可以修改 delay_time 變數來改變閃爍速度
"""

import machine
import time

# 初始化內建 LED
led = machine.Pin("LED", machine.Pin.OUT)

# 設定延遲時間（秒）
# 練習：試著改變這個值，看看 LED 閃爍速度的變化
delay_time = 0.2  # 0.2 秒 = 200 毫秒

print(f"LED 快速閃爍程式（延遲: {delay_time} 秒）")
print("按 Ctrl+C 停止程式")

try:
    while True:
        led.on()
        time.sleep(delay_time)
        led.off()
        time.sleep(delay_time)

except KeyboardInterrupt:
    print("\n程式已停止")
    led.off()
