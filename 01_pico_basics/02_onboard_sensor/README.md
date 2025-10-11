# 內建感測器範例

## 學習目標

- 理解 ADC（類比數位轉換）的概念
- 學習讀取 Pico 內建溫度感測器
- 掌握資料處理和格式化技巧
- 理解物件導向程式設計基礎

## 硬體需求

- Raspberry Pi Pico / Pico W
- USB 連接線

## 程式說明

### 1. temperature.py - 基本溫度讀取

最簡單的溫度感測器讀取程式。

**重要概念：**

**ADC（Analog-to-Digital Converter）**
- 將類比訊號轉換為數位值
- Pico 有 5 個 ADC 通道（ADC0-ADC4）
- ADC4 連接到內建溫度感測器
- 解析度：16 位元（0-65535）

**溫度轉換公式：**
```python
# 1. 讀取 ADC 值（0-65535）
adc_value = sensor.read_u16()

# 2. 轉換為電壓（0-3.3V）
voltage = adc_value * (3.3 / 65535)

# 3. 根據資料手冊公式轉換為溫度
temperature = 27 - (voltage - 0.706) / 0.001721
```

**執行步驟：**
1. 在 Thonny 中開啟 `temperature.py`
2. 執行程式
3. 觀察溫度讀數
4. 試著用手握住 Pico，觀察溫度變化

**注意事項：**
- 這是晶片溫度，不是環境溫度
- 正常範圍約 25-35°C
- 執行程式或充電時溫度會上升

### 2. sensor_reader.py - 感測器讀取類別

使用物件導向方式封裝感測器功能。

**類別設計：**
```python
class SensorReader:
    def __init__(self):
        # 初始化感測器
        
    def read_temperature(self):
        # 讀取當前溫度
        
    def get_average_temperature(self):
        # 取得平均溫度
        
    def get_sensor_data(self):
        # 取得完整資料
```

**資料平滑處理：**
- 保留最近 5 筆讀數
- 計算平均值減少雜訊
- 追蹤最小值和最大值

**執行步驟：**
1. 執行 `sensor_reader.py`
2. 觀察資料如何累積
3. 注意平均值比單次讀數更穩定

**練習：**
- 修改 `max_history` 改變平滑程度
- 加入中位數計算
- 實作溫度變化率計算

### 3. data_formatter.py - 資料格式化

將感測器資料格式化為標準 JSON 格式。

**JSON 資料格式：**
```json
{
    "device_id": "pico_001",
    "unique_id": "e66118605b3c5628",
    "device_type": "pico_w",
    "timestamp": 12345,
    "sensor_type": "temperature",
    "value": 28.5,
    "unit": "celsius"
}
```

**為什麼需要格式化？**
- 標準化資料結構
- 便於網路傳輸
- 易於其他系統解析
- 包含完整的元資料

**執行步驟：**
1. 執行 `data_formatter.py`
2. 觀察格式化的輸出
3. 注意 JSON 字串格式

**客製化：**
```python
# 修改裝置 ID
formatter = DataFormatter(device_id="my_pico_01")
```

## 重要概念

### ADC 基礎

**什麼是 ADC？**
- 將連續的類比訊號轉換為離散的數位值
- Pico 的 ADC 是 12 位元（但讀取時擴展為 16 位元）
- 參考電壓：3.3V

**ADC 通道：**
- ADC0: GPIO 26
- ADC1: GPIO 27
- ADC2: GPIO 28
- ADC3: GPIO 29（Pico W 用於 WiFi）
- ADC4: 內建溫度感測器

**使用方法：**
```python
import machine

# 初始化 ADC
adc = machine.ADC(pin_number)

# 讀取值
value = adc.read_u16()  # 0-65535
```

### 資料平滑技術

**為什麼需要平滑？**
- 感測器讀數會有雜訊
- 單次讀數可能不準確
- 平滑可以提高穩定性

**常用方法：**

1. **移動平均（Moving Average）**
```python
average = sum(history) / len(history)
```

2. **加權平均（Weighted Average）**
```python
# 最新的資料權重較高
weighted_avg = (old * 0.7) + (new * 0.3)
```

3. **中位數濾波（Median Filter）**
```python
median = sorted(history)[len(history)//2]
```

### JSON 格式

**什麼是 JSON？**
- JavaScript Object Notation
- 輕量級資料交換格式
- 易於人類閱讀和機器解析

**Python 中使用 JSON：**
```python
import json

# 字典轉 JSON 字串
data = {"key": "value"}
json_str = json.dumps(data)

# JSON 字串轉字典
data = json.loads(json_str)
```

## 實用技巧

### 溫度監控

建立簡單的溫度監控系統：

```python
def monitor_temperature(threshold=30):
    """監控溫度，超過閾值時警告"""
    reader = SensorReader()
    
    while True:
        temp = reader.read_temperature()
        
        if temp > threshold:
            print(f"警告！溫度過高: {temp:.2f}°C")
            # 可以加入 LED 閃爍或蜂鳴器
        else:
            print(f"溫度正常: {temp:.2f}°C")
        
        time.sleep(1)
```

### 資料記錄

記錄溫度資料到檔案：

```python
def log_temperature(filename="temp_log.txt"):
    """記錄溫度到檔案"""
    formatter = DataFormatter()
    
    with open(filename, "a") as f:
        data = formatter.get_json_string()
        f.write(data + "\n")
```

## 常見問題

### Q: 溫度讀數不準確？

**原因和解決方法：**
1. **這是晶片溫度，不是環境溫度**
   - 晶片溫度通常比環境溫度高 5-10°C
   - 如需測量環境溫度，使用外接感測器（如 DHT22）

2. **USB 供電導致溫度上升**
   - 使用電池供電可以降低溫度
   - 等待幾分鐘讓溫度穩定

3. **程式執行導致溫度上升**
   - 密集運算會產生熱量
   - 加入適當的延遲

### Q: ADC 讀數跳動很大？

**解決方法：**
1. 使用資料平滑
2. 增加讀取次數取平均
3. 加入硬體濾波電容（外接感測器時）

### Q: 如何校準溫度感測器？

**校準步驟：**
1. 使用標準溫度計測量實際溫度
2. 記錄 Pico 讀數
3. 計算偏移量
4. 在程式中加入校正：
```python
temperature = raw_temperature + calibration_offset
```

### Q: 時間戳記不正確？

**說明：**
- Pico 沒有 RTC（即時時鐘）
- `time.time()` 返回開機後的秒數
- 實際應用中需要從 NTP 伺服器同步時間
- 後續課程會教如何透過 WiFi 取得正確時間

## 練習題

### 練習 1：溫度警報系統

實作一個溫度警報系統：
- 設定高溫和低溫閾值
- 超過閾值時 LED 閃爍
- 顯示警告訊息

### 練習 2：溫度趨勢分析

擴展 SensorReader 類別：
- 計算溫度變化率（每分鐘上升/下降多少度）
- 預測未來溫度
- 偵測異常變化

### 練習 3：資料視覺化

將溫度資料以圖表方式顯示：
- 記錄最近 60 秒的溫度
- 在 Shell 中繪製簡單的文字圖表
- 提示：使用 `*` 或 `#` 字元

範例輸出：
```
30°C |****
29°C |*******
28°C |**********
27°C |*******
26°C |****
```

### 練習 4：多感測器整合

如果有外接感測器（如 DHT22）：
- 同時讀取內建和外接感測器
- 比較晶片溫度和環境溫度
- 計算溫度差異

## 檢核清單

完成本單元後，你應該能夠：

- [ ] 理解 ADC 的工作原理
- [ ] 讀取內建溫度感測器
- [ ] 實作資料平滑處理
- [ ] 使用類別封裝功能
- [ ] 格式化資料為 JSON
- [ ] 處理感測器雜訊
- [ ] 記錄和分析感測器資料

## 下一步

完成感測器讀取後，繼續學習：
- [按鈕輸入](../03_button_input/README.md) - 處理使用者輸入
- [MQTT 通訊](../../03_mqtt_communication/README.md) - 傳送資料到網路

## 參考資源

- [Pico 資料手冊](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)
- [RP2040 資料手冊](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf)
- [MicroPython ADC 文件](https://docs.micropython.org/en/latest/library/machine.ADC.html)
- [JSON 格式說明](https://www.json.org/)
