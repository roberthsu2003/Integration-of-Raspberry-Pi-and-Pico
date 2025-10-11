"""
基本 UART 通訊範例
示範 Pico 的 UART 發送和接收

硬體連接：
- TX (GPIO 0) → RX (Pi)
- RX (GPIO 1) → TX (Pi)
- GND → GND
"""

import machine
import time

# 初始化 UART
# UART 0: TX=GPIO 0, RX=GPIO 1
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

print("UART 基本通訊範例")
print("Baudrate: 9600")
print("TX: GPIO 0, RX: GPIO 1")
print("-" * 40)

# 發送測試訊息
def send_message(message):
    """
    發送訊息
    
    參數:
        message: 要發送的訊息（字串）
    """
    uart.write(message + '\n')
    print(f"發送: {message}")

# 接收訊息
def receive_message():
    """
    接收訊息
    
    返回:
        str: 接收到的訊息，如果沒有則返回 None
    """
    if uart.any():
        data = uart.read()
        if data:
            message = data.decode('utf-8').strip()
            print(f"接收: {message}")
            return message
    return None

# 主程式
print("\n開始通訊...")
print("按 Ctrl+C 停止")
print()

try:
    count = 0
    while True:
        # 發送訊息
        count += 1
        send_message(f"Hello from Pico #{count}")
        
        # 等待並接收回應
        time.sleep(0.5)
        receive_message()
        
        # 等待下次發送
        time.sleep(2)

except KeyboardInterrupt:
    print("\n程式已停止")
