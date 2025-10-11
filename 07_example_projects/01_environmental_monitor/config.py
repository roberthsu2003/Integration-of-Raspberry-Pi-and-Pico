"""
環境監測系統配置檔案
"""

# MQTT 設定
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/environment/#"
MQTT_CLIENT_ID = "env_monitor"

# MongoDB 設定
MONGO_URI = "mongodb://admin:password123@localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "environmental_data"

# 監測設定
PUBLISH_INTERVAL = 300  # Pico 發布間隔（秒）
DATA_RETENTION_DAYS = 30  # 資料保留天數

# 異常檢測閾值
TEMP_MIN = 15  # 最低溫度（°C）
TEMP_MAX = 35  # 最高溫度（°C）
TEMP_CHANGE_THRESHOLD = 5  # 溫度變化閾值（°C/小時）
SENSOR_TIMEOUT = 900  # 感測器無回應超時（秒，15分鐘）

# API 設定
API_HOST = "0.0.0.0"
API_PORT = 8000

# 裝置設定
DEFAULT_DEVICE_ID = "pico_env_001"
DEFAULT_LOCATION = "classroom_a"
