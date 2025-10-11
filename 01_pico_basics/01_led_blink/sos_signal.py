"""
SOS 訊號程式
練習：實作摩斯密碼 SOS 訊號

SOS 摩斯密碼：
S = ... (三短)
O = --- (三長)
S = ... (三短)
"""

import machine
import time

# 初始化內建 LED
led = machine.Pin("LED", machine.Pin.OUT)

# 定義時間單位（秒）
SHORT = 0.2  # 短訊號（點）
LONG = 0.6   # 長訊號（劃）
PAUSE = 0.2  # 訊號間隔
LETTER_PAUSE = 0.6  # 字母間隔
WORD_PAUSE = 1.4    # 單字間隔

def blink(duration):
    """
    讓 LED 閃爍指定的時間
    
    參數:
        duration: 閃爍持續時間（秒）
    """
    led.on()
    time.sleep(duration)
    led.off()
    time.sleep(PAUSE)

def send_s():
    """發送字母 S (三短)"""
    print("S", end="")
    for _ in range(3):
        blink(SHORT)
    time.sleep(LETTER_PAUSE)

def send_o():
    """發送字母 O (三長)"""
    print("O", end="")
    for _ in range(3):
        blink(LONG)
    time.sleep(LETTER_PAUSE)

def send_sos():
    """發送完整的 SOS 訊號"""
    print("發送 SOS: ", end="")
    send_s()  # S
    send_o()  # O
    send_s()  # S
    print()  # 換行
    time.sleep(WORD_PAUSE)

# 主程式
print("SOS 訊號程式")
print("按 Ctrl+C 停止程式")
print()

try:
    while True:
        send_sos()
        time.sleep(2)  # 每次 SOS 後等待 2 秒

except KeyboardInterrupt:
    print("\n程式已停止")
    led.off()
