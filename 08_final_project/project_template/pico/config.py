"""
配置檔案 - 請根據你的環境修改這些設定
"""

# 裝置設定
DEVICE_ID = "pico_student_01"  # 修改為你的裝置 ID
DEVICE_NAME = "學生專題裝置"

# WiFi 設定（如果使用 Pico W）
WIFI_SSID = "your_wifi_ssid"      # 修改為你的 WiFi 名稱
WIFI_PASSWORD = "your_password"    # 修改為你的 WiFi 密碼

# MQTT 設定
MQTT_BROKER = "192.168.1.100"      # 修改為你的 Pi IP 位址
MQTT_PORT = 1883
MQTT_TOPIC_PREFIX = "student/sensors"

# 資料發送間隔（秒）
PUBLISH_INTERVAL = 5

# 感測器設定
SENSOR_CONFIG = {
    "temperature": {
        "enabled": True,
        "unit": "celsius"
    },
    # 在此加入其他感測器設定
}
