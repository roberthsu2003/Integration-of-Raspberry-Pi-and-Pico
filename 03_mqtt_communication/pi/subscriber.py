"""
MQTT 訂閱者主程式
整合 MQTT 客戶端和資料處理器

功能：
- 訂閱 MQTT 主題
- 接收感測器資料
- 儲存到資料庫
- 統計和監控
"""

import sys
import os
import time
import signal
from mqtt_client import PiMQTTClient
from data_handler import DataHandler

# 加入 FastAPI 應用程式路徑
sys.path.append(os.path.join(os.path.dirname(__file__), '../../02_pi_basics/fastapi_app'))

try:
    from database import DatabaseManager
    DB_AVAILABLE = True
except ImportError:
    print("警告：無法匯入 DatabaseManager")
    DB_AVAILABLE = False

class MQTTSubscriber:
    """
    MQTT 訂閱者類別
    
    整合 MQTT 訂閱和資料處理功能
    """
    
    def __init__(
        self,
        client_id: str = "pi_subscriber",
        broker: str = "localhost",
        port: int = 1883,
        use_database: bool = True
    ):
        """
        初始化訂閱者
        
        參數:
            client_id: MQTT 客戶端 ID
            broker: MQTT Broker 位址
            port: MQTT 連接埠
            use_database: 是否使用資料庫
        """
        self.client_id = client_id
        self.broker = broker
        self.port = port
        
        # 初始化資料庫管理器
        self.db = None
        if use_database and DB_AVAILABLE:
            try:
                self.db = DatabaseManager()
                print("✓ 資料庫連接成功")
            except Exception as e:
                print(f"✗ 資料庫連接失敗: {e}")
        
        # 初始化資料處理器
        self.data_handler = DataHandler(self.db)
        
        # 初始化 MQTT 客戶端
        self.mqtt_client = PiMQTTClient(
            client_id=client_id,
            broker=broker,
            port=port
        )
        
        # 運行狀態
        self.running = False
    
    def on_sensor_data(self, topic: str, data):
        """
        感測器資料回調函式
        
        參數:
            topic: MQTT 主題
            data: 訊息資料
        """
        self.data_handler.handle_message(topic, data)
    
    def setup(self) -> bool:
        """
        設定訂閱者
        
        返回:
            bool: 設定是否成功
        """
        print("=" * 60)
        print("MQTT 訂閱者啟動中...")
        print("=" * 60)
        
        # 連接到 MQTT Broker
        print(f"\n連接到 MQTT Broker: {self.broker}:{self.port}")
        if not self.mqtt_client.connect():
            print("✗ MQTT 連接失敗")
            return False
        
        # 訂閱主題
        print("\n訂閱主題...")
        self.mqtt_client.subscribe("sensors/#", self.on_sensor_data)
        
        print("\n" + "=" * 60)
        print("設定完成！開始接收資料...")
        print("=" * 60)
        print("\n提示：")
        print("  - 按 Ctrl+C 停止程式")
        print("  - 按 Ctrl+\\ 顯示統計資訊")
        print()
        
        return True
    
    def run(self):
        """
        執行訂閱者主迴圈
        """
        # 設定
        if not self.setup():
            print("設定失敗，程式結束")
            return
        
        # 設定信號處理
        signal.signal(signal.SIGQUIT, self._signal_handler)
        
        self.running = True
        
        try:
            # 主迴圈
            while self.running:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n程式已停止")
        
        finally:
            self.cleanup()
    
    def _signal_handler(self, signum, frame):
        """
        信號處理函式
        
        Ctrl+\ 顯示統計資訊
        """
        print("\n")
        self.print_statistics()
    
    def cleanup(self):
        """清理資源"""
        print("\n清理資源...")
        
        # 顯示統計
        self.print_statistics()
        
        # 中斷 MQTT 連接
        if self.mqtt_client:
            self.mqtt_client.disconnect()
        
        # 關閉資料庫連接
        if self.db:
            self.db.close()
        
        print("清理完成")
    
    def print_statistics(self):
        """列印統計資訊"""
        print("\n" + "=" * 60)
        print("統計資訊")
        print("=" * 60)
        
        # MQTT 統計
        mqtt_stats = self.mqtt_client.get_statistics()
        print("\nMQTT 客戶端:")
        print(f"  連接狀態: {'已連接' if mqtt_stats['connected'] else '未連接'}")
        print(f"  接收訊息: {mqtt_stats['message_count']} 則")
        print(f"  發生錯誤: {mqtt_stats['error_count']} 次")
        
        # 資料處理統計
        data_stats = self.data_handler.get_statistics()
        print("\n資料處理:")
        print(f"  處理訊息: {data_stats['processed']} 則")
        print(f"  成功儲存: {data_stats['saved']} 則")
        print(f"  發生錯誤: {data_stats['errors']} 次")
        print(f"  成功率: {data_stats['success_rate']:.1f}%")
        
        print("=" * 60)

# ============================================================================
# 主程式
# ============================================================================

def main():
    """主程式入口"""
    import argparse
    
    # 命令列參數
    parser = argparse.ArgumentParser(description='MQTT 訂閱者')
    parser.add_argument('--broker', default='localhost', help='MQTT Broker 位址')
    parser.add_argument('--port', type=int, default=1883, help='MQTT 連接埠')
    parser.add_argument('--client-id', default='pi_subscriber', help='客戶端 ID')
    parser.add_argument('--no-db', action='store_true', help='不使用資料庫')
    
    args = parser.parse_args()
    
    # 建立訂閱者
    subscriber = MQTTSubscriber(
        client_id=args.client_id,
        broker=args.broker,
        port=args.port,
        use_database=not args.no_db
    )
    
    # 執行
    subscriber.run()

if __name__ == "__main__":
    main()
