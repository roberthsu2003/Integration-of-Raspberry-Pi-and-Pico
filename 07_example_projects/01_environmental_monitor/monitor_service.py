"""
環境監測服務
訂閱 MQTT 訊息並儲存到 MongoDB，包含異常檢測功能
"""

import json
import logging
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import pymongo
from config import *

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnvironmentalMonitor:
    """環境監測服務類別"""
    
    def __init__(self):
        """初始化監測服務"""
        self.db = None
        self.collection = None
        self.last_temperature = None
        self.last_timestamp = None
        self.connect_database()
    
    def connect_database(self):
        """連接到 MongoDB"""
        try:
            client = pymongo.MongoClient(MONGO_URI)
            self.db = client[MONGO_DB]
            self.collection = self.db[MONGO_COLLECTION]
            
            # 建立索引以提升查詢效能
            self.collection.create_index([("device_id", 1), ("timestamp", -1)])
            self.collection.create_index([("timestamp", -1)])
            
            logger.info(f"已連接到 MongoDB: {MONGO_DB}.{MONGO_COLLECTION}")
        except Exception as e:
            logger.error(f"MongoDB 連接失敗: {e}")
            raise
    
    def validate_data(self, data):
        """
        驗證接收到的資料
        
        Args:
            data: 資料字典
            
        Returns:
            tuple: (是否有效, 錯誤訊息)
        """
        required_fields = ["device_id", "sensor_type", "value", "timestamp"]
        
        # 檢查必要欄位
        for field in required_fields:
            if field not in data:
                return False, f"缺少必要欄位: {field}"
        
        # 檢查溫度範圍
        if data["sensor_type"] == "temperature":
            value = data["value"]
            if not isinstance(value, (int, float)):
                return False, "溫度值必須是數字"
            
            if value < TEMP_MIN or value > TEMP_MAX:
                logger.warning(f"溫度超出正常範圍: {value}°C")
                # 不拒絕資料，但記錄警告
        
        return True, None
    
    def detect_anomalies(self, data):
        """
        檢測異常情況
        
        Args:
            data: 資料字典
            
        Returns:
            list: 異常訊息列表
        """
        anomalies = []
        
        if data["sensor_type"] != "temperature":
            return anomalies
        
        current_temp = data["value"]
        current_time = datetime.fromisoformat(data["timestamp"])
        
        # 檢查溫度範圍
        if current_temp < TEMP_MIN:
            anomalies.append(f"溫度過低: {current_temp}°C (最低: {TEMP_MIN}°C)")
        elif current_temp > TEMP_MAX:
            anomalies.append(f"溫度過高: {current_temp}°C (最高: {TEMP_MAX}°C)")
        
        # 檢查溫度變化率
        if self.last_temperature is not None and self.last_timestamp is not None:
            time_diff = (current_time - self.last_timestamp).total_seconds() / 3600  # 小時
            if time_diff > 0:
                temp_change = abs(current_temp - self.last_temperature)
                change_rate = temp_change / time_diff
                
                if change_rate > TEMP_CHANGE_THRESHOLD:
                    anomalies.append(
                        f"溫度變化過快: {change_rate:.2f}°C/小時 "
                        f"(閾值: {TEMP_CHANGE_THRESHOLD}°C/小時)"
                    )
        
        # 更新最後記錄
        self.last_temperature = current_temp
        self.last_timestamp = current_time
        
        return anomalies
    
    def save_data(self, data):
        """
        儲存資料到 MongoDB
        
        Args:
            data: 資料字典
            
        Returns:
            bool: 儲存是否成功
        """
        try:
            # 加入建立時間
            data["created_at"] = datetime.now().isoformat()
            
            # 儲存到資料庫
            result = self.collection.insert_one(data)
            logger.info(
                f"✓ 已儲存資料: {data['device_id']} - "
                f"{data['sensor_type']}: {data['value']}"
            )
            return True
        except Exception as e:
            logger.error(f"✗ 儲存失敗: {e}")
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
            # 解析 JSON 訊息
            payload = msg.payload.decode('utf-8')
            data = json.loads(payload)
            
            logger.info(f"收到訊息: {msg.topic}")
            
            # 驗證資料
            is_valid, error_msg = self.validate_data(data)
            if not is_valid:
                logger.error(f"資料驗證失敗: {error_msg}")
                return
            
            # 檢測異常
            anomalies = self.detect_anomalies(data)
            if anomalies:
                for anomaly in anomalies:
                    logger.warning(f"⚠️  異常檢測: {anomaly}")
            
            # 儲存資料
            self.save_data(data)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失敗: {e}")
        except Exception as e:
            logger.error(f"處理訊息時發生錯誤: {e}")
    
    def cleanup_old_data(self):
        """清理過期資料"""
        try:
            cutoff_date = datetime.now() - timedelta(days=DATA_RETENTION_DAYS)
            result = self.collection.delete_many({
                "timestamp": {"$lt": cutoff_date.isoformat()}
            })
            if result.deleted_count > 0:
                logger.info(f"已清理 {result.deleted_count} 筆過期資料")
        except Exception as e:
            logger.error(f"清理資料失敗: {e}")
    
    def run(self):
        """啟動監測服務"""
        logger.info("=" * 50)
        logger.info("環境監測服務啟動")
        logger.info("=" * 50)
        logger.info(f"MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
        logger.info(f"訂閱主題: {MQTT_TOPIC}")
        logger.info(f"資料庫: {MONGO_DB}.{MONGO_COLLECTION}")
        logger.info("-" * 50)
        
        # 建立 MQTT 客戶端
        client = mqtt.Client(client_id=MQTT_CLIENT_ID)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        
        try:
            # 連接到 MQTT Broker
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            
            # 開始監聽
            logger.info("開始監聽 MQTT 訊息...")
            client.loop_forever()
            
        except KeyboardInterrupt:
            logger.info("\n正在停止服務...")
        except Exception as e:
            logger.error(f"服務錯誤: {e}")
        finally:
            client.disconnect()
            logger.info("服務已停止")

def main():
    """主程式"""
    monitor = EnvironmentalMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
