"""
按鈕中斷處理
使用中斷（Interrupt）方式處理按鈕輸入，更有效率

什麼是中斷？
中斷允許程式在特定事件發生時立即執行特定的程式碼，
而不需要持續輪詢（polling）檢查狀態。
"""

import machine
import time

# 全域變數
button_pressed = False
press_count = 0

def button_handler(pin):
    """
    按鈕中斷處理函式
    當按鈕狀態改變時會被呼叫
    
    參數:
        pin: 觸發中斷的 Pin 物件
    """
    global button_pressed, press_count
    
    # 簡單的防彈跳：檢查按鈕是否真的被按下
    if pin.value() == 0:
        button_pressed = True
        press_count += 1

# 初始化按鈕
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# 設定中斷：當按鈕狀態從 HIGH 變成 LOW 時觸發
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_handler)

# 初始化 LED
led = machine.Pin("LED", machine.Pin.OUT)

print("按鈕中斷示範")
print("按下按鈕會觸發中斷")
print("主程式可以執行其他任務")
print("按 Ctrl+C 停止程式")
print()

try:
    # 主迴圈可以執行其他任務
    while True:
        # 檢查是否有按鈕事件
        if button_pressed:
            button_pressed = False  # 重置旗標
            
            print(f"偵測到按鈕按下！（第 {press_count} 次）")
            
            # LED 閃爍
            led.on()
            time.sleep(0.2)
            led.off()
        
        # 主程式可以執行其他任務
        # 例如：顯示計時器
        print(f"運行時間: {time.time():.1f} 秒", end="\r")
        time.sleep(0.1)

except KeyboardInterrupt:
    print(f"\n程式已停止，總共按了 {press_count} 次")
    led.off()
