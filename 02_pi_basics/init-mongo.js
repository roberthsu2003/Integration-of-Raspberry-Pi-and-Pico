// MongoDB 初始化腳本
// 這個腳本會在 MongoDB 容器首次啟動時執行

// 切換到 iot_data 資料庫
db = db.getSiblingDB('iot_data');

// 建立一般使用者（非管理員）
db.createUser({
  user: 'iot_user',
  pwd: 'iot_password',
  roles: [
    {
      role: 'readWrite',
      db: 'iot_data'
    }
  ]
});

// 建立 sensor_data 集合
db.createCollection('sensor_data');

// 建立 devices 集合
db.createCollection('devices');

// 為 sensor_data 建立索引（提升查詢效能）
db.sensor_data.createIndex({ "device_id": 1 });
db.sensor_data.createIndex({ "timestamp": -1 });
db.sensor_data.createIndex({ "device_id": 1, "timestamp": -1 });

// 為 devices 建立索引
db.devices.createIndex({ "device_id": 1 }, { unique: true });

// 插入範例裝置資料
db.devices.insertMany([
  {
    device_id: "pico_001",
    device_name: "Temperature Sensor 1",
    device_type: "pico_w",
    location: "classroom_a",
    status: "active",
    created_at: new Date(),
    last_seen: new Date()
  },
  {
    device_id: "pico_002",
    device_name: "Temperature Sensor 2",
    device_type: "pico_w",
    location: "classroom_b",
    status: "active",
    created_at: new Date(),
    last_seen: new Date()
  }
]);

// 插入範例感測器資料
db.sensor_data.insertMany([
  {
    device_id: "pico_001",
    device_type: "pico_w",
    timestamp: new Date(),
    sensor_type: "temperature",
    value: 25.5,
    unit: "celsius",
    location: "classroom_a"
  },
  {
    device_id: "pico_002",
    device_type: "pico_w",
    timestamp: new Date(),
    sensor_type: "temperature",
    value: 26.2,
    unit: "celsius",
    location: "classroom_b"
  }
]);

print('MongoDB 初始化完成！');
print('已建立資料庫: iot_data');
print('已建立使用者: iot_user');
print('已建立集合: sensor_data, devices');
print('已插入範例資料');
