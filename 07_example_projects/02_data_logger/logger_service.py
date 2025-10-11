"""
資料記錄服務
持續監聽 MQTT 訊息並記錄到 MongoDB
"""

import json
import logging
from datetime import datetime
import paho.mqtt.client as mqtt
import pymongo

# 設定
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/#"
MONGO_URI = "mongodb://admin:password123@localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "sensor_logs"

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_logger.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataLogger:
    """資料記錄器類別"""
    
    def __init__(self):
        """初始化記錄器"""
        self.db = None
        self.collection = None
        self.record_count = 0
        self.error_count = 0
        self.connect_database()
    
    def connect_database(self):
        """連接到 MongoDB"""
        try:
            client = pymongo.MongoClient(MONGO_URI)
            self.db = client[MONGO_DB]
            self.collection = self.db[MONGO_COLLECTION]
            
            # 建立索引
            self.collection.create_index([("timestamp", -1)])
            self.collection.create_index([("device_id", 1), ("timestamp", -1)])
            
            logger.info(f"已連接到 MongoDB: {MONGO_DB}.{MONGO_COLLECTION}")
        except Exception as e:
            logger.error(f"MongoDB 連接失敗: {e}")
            raise
    
    def validate_data(self, data):
        """驗證資料"""
        required_fields = ["device_id", "sensor_type", "value", "timestamp"]
        for field in required_fields:
            if field not in data:
                return False, f"缺少必要欄位: {field}"
        return True, None
    
    def log_data(self, data):
        """記錄資料到資料庫"""
        try:
            # 加入記錄時間
            data["logged_at"] = datetime.now().isoformat()
            
            # 儲存到資料庫
            self.collection.insert_one(data)
            self.record_count += 1
            
            logger.info(
                f"[{self.record_count}] 已記錄: {data['device_id']} - "
                f"{data['sensor_type']}: {data['value']}"
            )
            return True
        except Exception as e:
            self.error_count += 1
            logger.error(f"記錄失敗: {e}")
            return False
    
    def on_connect(self, client, userdata, flags, rc):
        """MQTT 連接回調"""
        if rc == 0:
            logger.info(f"已連接到 MQTT Broker")
            client.subscribe(MQTT_TOPIC)
            logger.info(f"已訂閱主題: {MQTT_TOPIC}")
        else:
            logger.error(f"MQTT 連接失敗，代碼: {rc}")
    
    def on_message(self, client, userdata, msg):
        """MQTT 訊息回調"""
        try:
            payload = msg.payload.decode('utf-8')
            data = json.loads(payload)
            
            # 驗證資料
            is_valid, error_msg = self.validate_data(data)
            if not is_valid:
                logger.error(f"資料驗證失敗: {error_msg}")
                self.error_count += 1
                return
            
            # 記錄資料
            self.log_data(data)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失敗: {e}")
            self.error_count += 1
        except Exception as e:
            logger.error(f"處理訊息時發生錯誤: {e}")
            self.error_count += 1
    
    def print_statistics(self):
        """印出統計資訊"""
        logger.info("=" * 50)
        logger.info("資料記錄統計")
        logger.info(f"成功記錄: {self.record_count} 筆")
        logger.info(f"錯誤次數: {self.error_count} 次")
        logger.info("=" * 50)
    
    def run(self):
        """啟動記錄服務"""
        logger.info("=" * 50)
        logger.info("資料記錄服務啟動")
        logger.info("=" * 50)
        logger.info(f"MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
        logger.info(f"訂閱主題: {MQTT_TOPIC}")
        logger.info(f"資料庫: {MONGO_DB}.{MONGO_COLLECTION}")
        logger.info("-" * 50)
        
        # 建立 MQTT 客戶端
        client = mqtt.Client(client_id="data_logger")
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            logger.info("開始記錄資料...")
            client.loop_forever()
        except KeyboardInterrupt:
            logger.info("\n正在停止服務...")
            self.print_statistics()
        except Exception as e:
            logger.error(f"服務錯誤: {e}")
        finally:
            client.disconnect()
            logger.info("服務已停止")

def main():
    """主程式"""
    logger_service = DataLogger()
    logger_service.run()

if __name__ == "__main__":
    main()
