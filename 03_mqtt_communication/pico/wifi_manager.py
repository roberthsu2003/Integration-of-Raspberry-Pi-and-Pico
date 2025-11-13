"""
WiFi 連接管理模組
處理 Pico W 的 WiFi 連接

功能：
- WiFi 連接
- 連接狀態檢查
- 自動重連
- 錯誤處理
"""

import network
import time
import machine

class WiFiManager:
    """
    WiFi 管理器類別
    
    負責 WiFi 連接和狀態管理
    """
    
    def __init__(self, ssid, password, timeout=10):
        """
        初始化 WiFi 管理器
        
        參數:
            ssid: WiFi 名稱
            password: WiFi 密碼
            timeout: 連接逾時時間（秒）
        """
        self.ssid = ssid
        self.password = password
        self.timeout = timeout
        
        # 初始化 WLAN 介面
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        
        # LED 指示（選用）
        self.led = machine.Pin("LED", machine.Pin.OUT)
    
    def connect(self):
        """
        連接到 WiFi
        
        返回:
            bool: 連接是否成功
        """
        # 如果已經連接，直接返回
        if self.wlan.isconnected():
            print("已經連接到 WiFi")
            return True
        
        print(f"正在連接到 WiFi: {self.ssid}")
        
        # 開始連接
        self.wlan.connect(self.ssid, self.password)
        
        # 等待連接
        start_time = time.time()
        while not self.wlan.isconnected():
            # LED 閃爍表示正在連接
            self.led.toggle()
            time.sleep(0.5)
            
            # 檢查逾時
            if time.time() - start_time > self.timeout:
                print("WiFi 連接逾時")
                self.led.off()
                return False
        
        # 連接成功
        self.led.on()
        print("WiFi 連接成功！")
        self.print_network_info()
        return True
    
    def disconnect(self):
        """中斷 WiFi 連接"""
        if self.wlan.isconnected():
            self.wlan.disconnect()
            print("已中斷 WiFi 連接")
        self.led.off()
    
    def is_connected(self):
        """
        檢查是否已連接
        
        返回:
            bool: 是否已連接
        """
        return self.wlan.isconnected()
    
    def get_ip(self):
        """
        取得 IP 位址
        
        返回:
            str: IP 位址，如果未連接則返回 None
        """
        if self.wlan.isconnected():
            return self.wlan.ifconfig()[0]
        return None
    
    def print_network_info(self):
        """列印網路資訊"""
        if self.wlan.isconnected():
            config = self.wlan.ifconfig()
            print("=" * 40)
            print("網路資訊:")
            print(f"  IP 位址: {config[0]}")
            print(f"  子網路遮罩: {config[1]}")
            print(f"  閘道: {config[2]}")
            print(f"  DNS: {config[3]}")
            print("=" * 40)
    
    def wait_for_connection(self, max_retries=3):
        """
        等待連接，支援重試
        
        參數:
            max_retries: 最大重試次數
        
        返回:
            bool: 連接是否成功
        """
        for attempt in range(max_retries):
            print(f"連接嘗試 {attempt + 1}/{max_retries}")
            
            if self.connect():
                return True
            
            if attempt < max_retries - 1:
                print(f"等待 5 秒後重試...")
                time.sleep(5)
        
        print("WiFi 連接失敗，已達最大重試次數")
        return False
    
    def reconnect_if_needed(self):
        """
        如果連接中斷，自動重新連接
        
        返回:
            bool: 是否已連接
        """
        if not self.is_connected():
            print("偵測到 WiFi 連接中斷，嘗試重新連接...")
            return self.connect()
        return True

# ============================================================================
# 使用範例
# ============================================================================

if __name__ == "__main__":
    # 匯入配置
    from wifi_config import WIFI_SSID, WIFI_PASSWORD
    
    # 建立 WiFi 管理器
    wifi = WiFiManager(WIFI_SSID, WIFI_PASSWORD)
    
    # 連接到 WiFi
    if wifi.wait_for_connection():
        print("WiFi 連接成功！")
        print(f"IP 位址: {wifi.get_ip()}")
        
        # 保持連接
        try:
            while True:
                # 檢查連接狀態
                if wifi.is_connected():
                    print("WiFi 連接正常")
                else:
                    print("WiFi 連接中斷")
                    wifi.reconnect_if_needed()
                
                time.sleep(10)
        
        except KeyboardInterrupt:
            print("\n程式已停止")
            wifi.disconnect()
    else:
        print("無法連接到 WiFi")
