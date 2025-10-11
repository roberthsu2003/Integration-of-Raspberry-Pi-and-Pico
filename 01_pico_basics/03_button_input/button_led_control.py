"""
按鈕控制 LED
綜合練習：使用按鈕控制 LED 的不同模式

功能：
- 短按：切換 LED 開關
- 長按：切換 LED 閃爍模式
"""

import machine
import time

class ButtonController:
    """按鈕控制器類別"""
    
    def __init__(self, button_pin, led_pin="LED"):
        """初始化控制器"""
        self.button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.led = machine.Pin(led_pin, machine.Pin.OUT)
        
        # 狀態變數
        self.led_state = False  # LED 開關狀態
        self.blink_mode = False  # 閃爍模式
        self.last_press_time = 0
        self.long_press_time = 1000  # 長按時間（毫秒）
    
    def check_button(self):
        """
        檢查按鈕狀態並處理
        
        返回:
            str: "short" 表示短按，"long" 表示長按，None 表示無動作
        """
        # 按鈕被按下
        if self.button.value() == 0:
            press_start = time.ticks_ms()
            
            # 等待按鈕放開
            while self.button.value() == 0:
                time.sleep(0.01)
            
            # 計算按下時間
            press_duration = time.ticks_diff(time.ticks_ms(), press_start)
            
            # 防彈跳延遲
            time.sleep(0.05)
            
            # 判斷是短按還是長按
            if press_duration > self.long_press_time:
                return "long"
            else:
                return "short"
        
        return None
    
    def toggle_led(self):
        """切換 LED 開關"""
        self.led_state = not self.led_state
        if self.led_state:
            self.led.on()
            print("LED 開啟")
        else:
            self.led.off()
            print("LED 關閉")
    
    def toggle_blink_mode(self):
        """切換閃爍模式"""
        self.blink_mode = not self.blink_mode
        if self.blink_mode:
            print("進入閃爍模式")
        else:
            print("離開閃爍模式")
            self.led.off()
    
    def update(self):
        """更新控制器狀態（在主迴圈中呼叫）"""
        # 檢查按鈕
        button_action = self.check_button()
        
        if button_action == "short":
            print("偵測到短按")
            if not self.blink_mode:
                self.toggle_led()
        
        elif button_action == "long":
            print("偵測到長按")
            self.toggle_blink_mode()
        
        # 處理閃爍模式
        if self.blink_mode:
            self.led.toggle()
            time.sleep(0.3)

# 主程式
if __name__ == "__main__":
    print("按鈕 LED 控制程式")
    print("=" * 40)
    print("短按：切換 LED 開關")
    print("長按（1秒以上）：切換閃爍模式")
    print("按 Ctrl+C 停止程式")
    print("=" * 40)
    print()
    
    # 建立控制器
    controller = ButtonController(button_pin=15)
    
    try:
        while True:
            controller.update()
            time.sleep(0.01)
    
    except KeyboardInterrupt:
        print("\n程式已停止")
        controller.led.off()
