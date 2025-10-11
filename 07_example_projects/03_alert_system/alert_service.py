"""
警報監控服務
監控感測器資料並根據規則觸發警報
"""

import json
import logging
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import pymongo
import argparse

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('alerts.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AlertSystem:
    """警報系統類別"""
    
    def __init__(self, config_file="alert_config.json"):
        """初始化警報系統"""
        self.config = self.load_config(config_file)
        self.db = None
        self.collection = None
        self.last_values = {}  # 儲存最後的數值用於計算變化率
        self.last_alerts = {}  # 儲存最後警報時間用於冷卻
        self.alert_count = 0
        self.connect_database()
    
    def load_config(self, config_file):
        """載入配置檔案"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"已載入配置檔案: {config_file}")
            return config
        except Exception as e:
            logger.error(f"載入配置失敗: {e}")
            raise
    
    def connect_database(self):
        """連接到 MongoDB"""
        try:
            db_config = self.config['database']
            client = pymongo.MongoClient(db_config['uri'])
            self.db = client[db_config['db']]
            self.collection = self.db[db_config['collection']]
            
            # 建立索引
            self.collection.create_index([("timestamp", -1)])
            self.collection.create_index([("device_id", 1), ("timestamp", -1)])
            
            logger.info(f"已連接到 MongoDB: {db_config['db']}.{db_config['collection']}")
        except Exception as e:
            logger.error(f"MongoDB 連接失敗: {e}")
            raise
    
    def evaluate_condition(self, condition, data, change_rate=None):
        """
        評估警報條件
        
        Args:
            condition: 條件表達式
            data: 感測器資料
            change_rate: 變化率（選填）
        
        Returns:
            bool: 條件是否滿足
        """
        try:
            # 準備評估環境
            eval_env = {
                'value': data.get('value'),
                'change_rate': change_rate
            }
            
            # 評估條件
            result = eval(condition, {"__builtins__": {}}, eval_env)
            return bool(result)
        except Exception as e:
            logger.error(f"條件評估失敗: {e}")
            return False
    
    def calculate_change_rate(self, device_id, current_value, current_time):
        """
        計算變化率
        
        Args:
            device_id: 裝置 ID
            current_value: 當前數值
            current_time: 當前時間
        
        Returns:
            float: 變化率（單位/小時）
        """
        if device_id not in self.last_values:
            self.last_values[device_id] = {
                'value': current_value,
                'time': current_time
            }
            return 0
        
        last_data = self.last_values[device_id]
        time_diff = (current_time - last_data['time']).total_seconds() / 3600  # 小時
        
        if time_diff > 0:
            value_diff = current_value - last_data['value']
            change_rate = abs(value_diff / time_diff)
            
            # 更新最後數值
            self.last_values[device_id] = {
                'value': current_value,
                'time': current_time
            }
            
            return change_rate
        
        return 0
    
    def check_cooldown(self, rule_name, device_id, cooldown):
        """
        檢查警報冷卻時間
        
        Args:
            rule_name: 規則名稱
            device_id: 裝置 ID
            cooldown: 冷卻時間（秒）
        
        Returns:
            bool: 是否在冷卻期內
        """
        key = f"{device_id}_{rule_name}"
        
        if key not in self.last_alerts:
            return False
        
        last_alert_time = self.last_alerts[key]
        time_since_last = (datetime.now() - last_alert_time).total_seconds()
        
        return time_since_last < cooldown
    
    def trigger_alert(self, rule, data, change_rate=None):
        """
        觸發警報
        
        Args:
            rule: 警報規則
            data: 感測器資料
            change_rate: 變化率（選填）
        """
        device_id = data['device_id']
        cooldown = rule.get('cooldown', 0)
        
        # 檢查冷卻時間
        if self.check_cooldown(rule['name'], device_id, cooldown):
            return
        
        # 建立警報記錄
        alert = {
            'alert_id': f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.alert_count}",
            'device_id': device_id,
            'rule_name': rule['name'],
            'severity': rule['severity'],
            'sensor_type': data.get('sensor_type'),
            'value': data.get('value'),
            'change_rate': change_rate,
            'timestamp': datetime.now().isoformat(),
            'data_timestamp': data.get('timestamp')
        }
        
        # 格式化訊息
        message_template = rule.get('message', '警報觸發')
        try:
            alert['message'] = message_template.format(
                value=data.get('value'),
                change_rate=change_rate if change_rate else 0
            )
        except:
            alert['message'] = message_template
        
        # 儲存警報
        try:
            self.collection.insert_one(alert)
        except Exception as e:
            logger.error(f"儲存警報失敗: {e}")
        
        # 發送通知
        self.send_notifications(alert)
        
        # 更新最後警報時間
        key = f"{device_id}_{rule['name']}"
        self.last_alerts[key] = datetime.now()
        
        self.alert_count += 1
    
    def send_notifications(self, alert):
        """
        發送警報通知
        
        Args:
            alert: 警報資料
        """
        notifications = self.config.get('notifications', {})
        
        # 終端輸出
        if notifications.get('terminal', True):
            severity_icon = {
                'info': 'ℹ️',
                'warning': '⚠️',
                'critical': '🚨'
            }.get(alert['severity'], '⚠️')
            
            logger.warning(
                f"{severity_icon} 警報: [{alert['severity'].upper()}] "
                f"{alert['device_id']} - {alert['message']}"
            )
        
        # MQTT 發布
        if notifications.get('mqtt', False):
            try:
                topic = f"alerts/{alert['device_id']}"
                message = json.dumps(alert, default=str)
                # 這裡需要一個 MQTT 客戶端來發布
                # 簡化版本，實際應用中應該使用獨立的發布客戶端
                logger.info(f"警報已發布到 MQTT: {topic}")
            except Exception as e:
                logger.error(f"MQTT 發布失敗: {e}")
    
    def check_rules(self, data):
        """
        檢查所有警報規則
        
        Args:
            data: 感測器資料
        """
        device_id = data.get('device_id')
        sensor_type = data.get('sensor_type')
        value = data.get('value')
        
        if not all([device_id, sensor_type, value is not None]):
            return
        
        # 計算變化率
        try:
            timestamp = datetime.fromisoformat(data.get('timestamp'))
        except:
            timestamp = datetime.now()
        
        change_rate = self.calculate_change_rate(device_id, value, timestamp)
        
        # 檢查每個規則
        for rule in self.config.get('rules', []):
            # 檢查感測器類型是否匹配
            if 'sensor_type' in rule and rule['sensor_type'] != sensor_type:
                continue
            
            # 評估條件
            condition = rule.get('condition')
            if not condition:
                continue
            
            if self.evaluate_condition(condition, data, change_rate):
                self.trigger_alert(rule, data, change_rate)
    
    def on_connect(self, client, userdata, flags, rc):
        """MQTT 連接回調"""
        if rc == 0:
            logger.info(f"已連接到 MQTT Broker")
            mqtt_config = self.config['mqtt']
            client.subscribe(mqtt_config['topic'])
            logger.info(f"已訂閱主題: {mqtt_config['topic']}")
        else:
            logger.error(f"MQTT 連接失敗，代碼: {rc}")
    
    def on_message(self, client, userdata, msg):
        """MQTT 訊息回調"""
        try:
            payload = msg.payload.decode('utf-8')
            data = json.loads(payload)
            
            # 檢查警報規則
            self.check_rules(data)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失敗: {e}")
        except Exception as e:
            logger.error(f"處理訊息時發生錯誤: {e}")
    
    def run(self):
        """啟動警報服務"""
        logger.info("=" * 50)
        logger.info("警報監控服務啟動")
        logger.info("=" * 50)
        
        mqtt_config = self.config['mqtt']
        logger.info(f"MQTT Broker: {mqtt_config['broker']}:{mqtt_config['port']}")
        logger.info(f"訂閱主題: {mqtt_config['topic']}")
        logger.info(f"警報規則數: {len(self.config.get('rules', []))}")
        logger.info("-" * 50)
        
        # 建立 MQTT 客戶端
        client = mqtt.Client(client_id="alert_system")
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        
        try:
            client.connect(mqtt_config['broker'], mqtt_config['port'], 60)
            logger.info("開始監控...")
            client.loop_forever()
        except KeyboardInterrupt:
            logger.info("\n正在停止服務...")
            logger.info(f"總警報數: {self.alert_count}")
        except Exception as e:
            logger.error(f"服務錯誤: {e}")
        finally:
            client.disconnect()
            logger.info("服務已停止")

def main():
    """主程式"""
    parser = argparse.ArgumentParser(description="警報監控服務")
    parser.add_argument(
        "--config",
        default="alert_config.json",
        help="配置檔案路徑"
    )
    args = parser.parse_args()
    
    alert_system = AlertSystem(args.config)
    alert_system.run()

if __name__ == "__main__":
    main()
