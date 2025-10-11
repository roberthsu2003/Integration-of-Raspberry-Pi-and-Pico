"""
按鈕防彈跳處理
處理按鈕的機械彈跳問題，確保準確的按鈕事件偵測

什麼是彈跳（Bounce）？
當按鈕被按下或放開時，機械接點會快速震動，
產生多次開關訊號，這稱為「彈跳」。
"""

import machine
import time

class Button:
    """
    按鈕類別，包含防彈跳功能
    """
    
    def __init__(self, pin, debounce_time=50):
        """
        初始化按鈕
        
        參數:
            pin: GPIO 腳位編號
            debounce_time: 防彈跳時間（毫秒）
        """
        self.button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.debounce_time = debounce_time
        self.last_time = 0
        self.last_state = 1  # 初始狀態（未按下）
    
    def is_pressed(self):
        """
        檢查按鈕是否被按下（有防彈跳）
        
        返回:
            bool: True 表示按鈕被按下
        """
        current_state = self.button.value()
        current_time = time.ticks_ms()
        
        # 檢查是否超過防彈跳時間
        if time.ticks_diff(current_time, self.last_time) > self.debounce_time:
            # 偵測到狀態變化（從 1 變成 0）
            if self.last_state == 1 and current_state == 0:
                self.last_state = current_state
                self.last_time = current_time
                return True
            
            self.last_state = current_state
        
        return False
    
    def wait_for_press(self):
        """等待按鈕被按下"""
        while not self.is_pressed():
            time.sleep(0.01)
    
    def wait_for_release(self):
        """等待按鈕被放開"""
        while self.button.value() == 0:
            time.sleep(0.01)

# 示範使用
if __name__ == "__main__":
    print("按鈕防彈跳示範")
    print("每次按下按鈕會計數一次")
    print("按 Ctrl+C 停止程式")
    print()
    
    # 建立按鈕物件
    button = Button(15)
    
    # 初始化 LED
    led = machine.Pin("LED", machine.Pin.OUT)
    
    # 計數器
    count = 0
    
    try:
        while True:
            # 檢查按鈕是否被按下
            if button.is_pressed():
                count += 1
                print(f"按鈕被按下 {count} 次")
                
                # LED 閃爍表示偵測到按鈕
                led.on()
                time.sleep(0.1)
                led.off()
            
            time.sleep(0.01)
    
    except KeyboardInterrupt:
        print(f"\n程式已停止，總共按了 {count} 次")
        led.off()
