"""
Hello World 程式
這是你的第一個 MicroPython 程式
"""

# 在 Thonny 的 Shell 中會顯示這個訊息
print("Hello, Pico!")
print("歡迎來到 MicroPython 的世界！")

# 顯示一些系統資訊
import sys
print(f"Python 版本: {sys.version}")

# 顯示 Pico 的唯一 ID
import machine
import ubinascii

unique_id = ubinascii.hexlify(machine.unique_id()).decode()
print(f"Pico 唯一 ID: {unique_id}")

print("\n程式執行完成！")
