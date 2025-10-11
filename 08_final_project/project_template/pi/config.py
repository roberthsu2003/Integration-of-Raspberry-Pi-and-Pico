"""
Pi 端配置檔案
"""

import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# API 設定
API_PORT = int(os.getenv("API_PORT", "8000"))

# MongoDB 設定
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "student_project")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "sensor_data")

# MQTT 設定
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPICS = os.getenv("MQTT_TOPICS", "student/sensors/#").split(",")

# 日誌設定
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
