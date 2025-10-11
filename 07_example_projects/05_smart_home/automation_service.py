"""
智慧家居自動化服務
根據感測器資料自動執行控制動作
"""

import json
import logging
from datetime import datetime
import paho.mqtt.client as mqtt
import pymongo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutomationService:
    """自動化服務類別"""
    
    def __init__(self, config_file="automation_rules.json"):
        self.config = self.load_config(config_file)
        self.last_actions = {}  # 記錄最後執行的動作（用於冷卻）
        self.mqtt_client = None
        
        # MongoDB 連接（用於記錄控制歷史）
        try:
            self.db_client = pymongo.MongoClient("mongodb://admin:password123@localhost:27017/")
            self.history_collection = self.db_client["iot_data"]["control_history"]
            logger.info("已連接到 MongoDB")
        except Exception as e:
            logger.warning(f"MongoDB 連接失敗: {e}，將不記錄歷史")
            self.db_client = None
            self.history_collection = None
    
    def load_config(self, config_file):
        """載入配置"""
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def evaluate_condition(self, condition, data):
        """評估條件"""
        try:
            temperature = data.get('value')
            return eval(condition, {"__builtins__": {}}, {"temperature": temperature})
        except:
            return False
    
    def send_control_command(self, device_id, action, rule_name=None):
        """發送控制命令"""
        topic = self.config['mqtt']['control_topic'].format(device_id=device_id)
        timestamp = datetime.now().isoformat()
        command = {"action": action, "timestamp": timestamp}
        
        self.mqtt_client.publish(topic, json.dumps(command))
        logger.info(f"✓ 已發送控制命令: {device_id} -> {action}")
        
        # 記錄到資料庫
        if self.history_collection is not None:
            try:
                self.history_collection.insert_one({
                    "device_id": device_id,
                    "action": action,
                    "rule_name": rule_name or "unknown",
                    "timestamp": timestamp
                })
            except Exception as e:
                logger.warning(f"記錄歷史失敗: {e}")
    
    def check_cooldown(self, rule_name, device_id, cooldown):
        """檢查冷卻時間"""
        key = f"{device_id}_{rule_name}"
        if key in self.last_actions:
            elapsed = (datetime.now() - self.last_actions[key]).total_seconds()
            return elapsed < cooldown
        return False
    
    def process_sensor_data(self, data):
        """處理感測器資料並執行自動化規則"""
        device_id = data.get('device_id')
        sensor_type = data.get('sensor_type')
        
        if sensor_type != 'temperature':
            return
        
        for rule in self.config['rules']:
            if self.evaluate_condition(rule['condition'], data):
                cooldown = rule.get('cooldown', 0)
                
                if not self.check_cooldown(rule['name'], device_id, cooldown):
                    logger.info(f"🤖 觸發規則: {rule['name']} - {rule['description']}")
                    self.send_control_command(device_id, rule['action'], rule['name'])
                    self.last_actions[f"{device_id}_{rule['name']}"] = datetime.now()
                break
    
    def on_connect(self, client, userdata, flags, rc):
        """MQTT 連接回調"""
        if rc == 0:
            logger.info("已連接到 MQTT Broker")
            client.subscribe(self.config['mqtt']['sensor_topic'])
            logger.info(f"已訂閱: {self.config['mqtt']['sensor_topic']}")
    
    def on_message(self, client, userdata, msg):
        """MQTT 訊息回調"""
        try:
            data = json.loads(msg.payload.decode('utf-8'))
            self.process_sensor_data(data)
        except Exception as e:
            logger.error(f"處理訊息失敗: {e}")
    
    def run(self):
        """啟動服務"""
        logger.info("=" * 50)
        logger.info("智慧家居自動化服務啟動")
        logger.info("=" * 50)
        
        mqtt_config = self.config['mqtt']
        self.mqtt_client = mqtt.Client(client_id="automation_service")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        
        try:
            self.mqtt_client.connect(mqtt_config['broker'], mqtt_config['port'], 60)
            logger.info("開始監控...")
            self.mqtt_client.loop_forever()
        except KeyboardInterrupt:
            logger.info("\n服務已停止")
        finally:
            self.mqtt_client.disconnect()
            if self.db_client:
                self.db_client.close()

if __name__ == "__main__":
    service = AutomationService()
    service.run()
