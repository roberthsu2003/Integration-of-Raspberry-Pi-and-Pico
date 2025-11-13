"""
WiFi 配置檔案
請修改此檔案中的 WiFi 設定

安全提示：
- 不要將此檔案上傳到公開的 Git 儲存庫
- 建議將此檔案加入 .gitignore
"""

# WiFi 設定
WIFI_SSID = "your_wifi_ssid"        # 你的 WiFi 名稱
WIFI_PASSWORD = "your_wifi_password"  # 你的 WiFi 密碼

# MQTT Broker 設定
MQTT_BROKER = "192.168.1.100"  # Raspberry Pi 的 IP 位址
MQTT_PORT = 1883
MQTT_CLIENT_ID = "pico_001"    # 此 Pico 的唯一識別碼

# 裝置資訊
DEVICE_ID = "pico_001"
DEVICE_NAME = "Temperature Sensor 1"
DEVICE_LOCATION = "classroom_a"
