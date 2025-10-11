"""
感測器資料發布程式
整合感測器讀取和 MQTT 發布

功能：
- 讀取 Pico 內建溫度感測器
- 定時發布資料到 MQTT Broker
- 自動重連機制
- 錯誤處理和日誌
"""

import machine
import time
from mqtt_client import PicoMQTTClient
from wifi_manager import WiFiManager
from wifi_config import (
    WIFI_SSID, WIFI_PASSWORD,
    MQTT_BROKER, MQTT_PORT, MQTT_CLIENT_ID,
    DEVICE_ID, DEVICE_LOCATION
)

class SensorPublisher:
    """
    感測器發布者類別
    
    整合感測器讀取和 MQTT 發布功能
    """
    
    def __init__(self, device_id, location=None, publish_interval=5):
        """
        初始化發布者
        
        參數:
            device_id: 裝置 ID
            location: 位置
            publish_interval: 發布間隔（秒）
        """
        self.device_id = device_id
        self.location = location
        self.publish_interval = publish_interval
        
        # 初始化溫度感測器
        self.sensor = machine.ADC(4)
        
        # WiFi 和 MQTT 客戶端（稍後初始化）
        self.wifi = None
        self.mqtt = None
        
        # 統計資訊
        self.publish_count = 0
        self.error_count = 0
    
    def read_temperature(self):
        """
        讀取溫度感測器
        
        返回:
            float: 溫度值（攝氏）
        """
        try:
            # 讀取 ADC 值
            adc_value = self.sensor.read_u16()
            
            # 轉換為電壓
            voltage = adc_value * (3.3 / 65535)
            
            # 轉換為溫度
            temperature = 27 - (voltage - 0.706) / 0.001721
            
            return temperature
        
        except Exception as e:
            print(f"讀取溫度失敗: {e}")
            return None
    
    def setup(self):
        """
        設定 WiFi 和 MQTT 連接
        
        返回:
            bool: 設定是否成功
        """
        print("=" * 50)
        print("感測器發布者啟動中...")
        print("=" * 50)
        
        # 1. 連接 WiFi
        print("\n[1/2] 連接 WiFi...")
        self.wifi = WiFiManager(WIFI_SSID, WIFI_PASSWORD)
        
        if not self.wifi.wait_for_connection(max_retries=3):
            print("✗ WiFi 連接失敗")
            return False
        
        print("✓ WiFi 連接成功")
        
        # 2. 連接 MQTT Broker
        print("\n[2/2] 連接 MQTT Broker...")
        self.mqtt = PicoMQTTClient(
            client_id=MQTT_CLIENT_ID,
            broker=MQTT_BROKER,
            port=MQTT_PORT
        )
        
        if not self.mqtt.connect():
            print("✗ MQTT 連接失敗")
            return False
        
        print("✓ MQTT 連接成功")
        
        print("\n" + "=" * 50)
        print("設定完成！開始發布資料...")
        print("=" * 50)
        
        return True
    
    def publish_sensor_data(self):
        """
        讀取並發布感測器資料
        
        返回:
            bool: 發布是否成功
        """
        try:
            # 讀取溫度
            temperature = self.read_temperature()
            
            if temperature is None:
                print("✗ 無法讀取溫度")
                self.error_count += 1
                return False
            
            # 發布資料
            success = self.mqtt.publish_sensor_data(
                device_id=self.device_id,
                sensor_type="temperature",
                value=temperature,
                unit="celsius",
                location=self.location
            )
            
            if success:
                self.publish_count += 1
                print(f"[{self.publish_count}] 溫度: {temperature:.2f}°C")
                return True
            else:
                self.error_count += 1
                return False
        
        except Exception as e:
            print(f"✗ 發布資料時發生錯誤: {e}")
            self.error_count += 1
            return False
    
    def check_connections(self):
        """
        檢查並維護連接
        
        返回:
            bool: 連接是否正常
        """
        # 檢查 WiFi
        if not self.wifi.is_connected():
            print("⚠ WiFi 連接中斷，嘗試重新連接...")
            if not self.wifi.connect():
                return False
        
        # 檢查 MQTT
        if not self.mqtt.connected:
            print("⚠ MQTT 連接中斷，嘗試重新連接...")
            if not self.mqtt.connect():
                return False
        
        return True
    
    def print_statistics(self):
        """列印統計資訊"""
        print("\n" + "=" * 50)
        print("統計資訊:")
        print(f"  成功發布: {self.publish_count} 次")
        print(f"  發生錯誤: {self.error_count} 次")
        if self.publish_count > 0:
            success_rate = (self.publish_count / (self.publish_count + self.error_count)) * 100
            print(f"  成功率: {success_rate:.1f}%")
        print("=" * 50)
    
    def run(self):
        """
        執行主迴圈
        
        持續讀取感測器並發布資料
        """
        # 設定連接
        if not self.setup():
            print("設定失敗，程式結束")
            return
        
        # 主迴圈
        try:
            while True:
                # 檢查連接狀態
                if not self.check_connections():
                    print("連接檢查失敗，等待 10 秒後重試...")
                    time.sleep(10)
                    continue
                
                # 發布感測器資料
                self.publish_sensor_data()
                
                # 等待下次發布
                time.sleep(self.publish_interval)
        
        except KeyboardInterrupt:
            print("\n\n程式已停止")
            self.print_statistics()
            
            # 清理資源
            if self.mqtt:
                self.mqtt.disconnect()
            if self.wifi:
                self.wifi.disconnect()
        
        except Exception as e:
            print(f"\n程式發生錯誤: {e}")
            self.print_statistics()

# ============================================================================
# 主程式
# ============================================================================

if __name__ == "__main__":
    # 建立發布者
    publisher = SensorPublisher(
        device_id=DEVICE_ID,
        location=DEVICE_LOCATION,
        publish_interval=5  # 每 5 秒發布一次
    )
    
    # 執行
    publisher.run()
