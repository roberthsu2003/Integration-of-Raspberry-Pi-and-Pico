# 環境設定指南

本文件提供完整的環境設定步驟，包括 Raspberry Pi 和 Raspberry Pi Pico 的配置。

## 目錄

- [Raspberry Pi 設定](#raspberry-pi-設定)
- [Raspberry Pi Pico 設定](#raspberry-pi-pico-設定)
- [軟體安裝](#軟體安裝)
- [環境驗證](#環境驗證)

## Raspberry Pi 設定

### 1. 作業系統安裝

1. 下載 [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. 選擇 "Raspberry Pi OS (64-bit)" 或 "Raspberry Pi OS (32-bit)"
3. 將映像檔寫入 microSD 卡
4. 在寫入前，點擊設定圖示配置：
   - 設定主機名稱
   - 啟用 SSH
   - 設定使用者名稱和密碼
   - 配置 WiFi（如果使用無線網路）

### 2. 首次啟動

1. 將 microSD 卡插入 Raspberry Pi
2. 連接電源啟動
3. 透過 SSH 連接或直接使用螢幕鍵盤

```bash
# 從其他電腦 SSH 連接
ssh pi@raspberrypi.local
# 或使用 IP 位址
ssh pi@192.168.1.100
```

### 3. 系統更新

```bash
# 更新套件清單
sudo apt update

# 升級已安裝的套件
sudo apt upgrade -y

# 重新啟動（建議）
sudo reboot
```

## 軟體安裝

### 1. Python 環境

```bash
# 檢查 Python 版本（應該是 3.9 或更高）
python3 --version

# 安裝 pip
sudo apt install python3-pip -y

# 安裝虛擬環境工具
sudo apt install python3-venv -y
```

### 2. Docker 和 Docker Compose

```bash
# 安裝 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 將當前使用者加入 docker 群組
sudo usermod -aG docker $USER

# 登出後重新登入使群組變更生效
# 或執行以下命令
newgrp docker

# 驗證 Docker 安裝
docker --version

# 安裝 Docker Compose
sudo apt install docker-compose -y

# 驗證 Docker Compose 安裝
docker-compose --version
```

### 3. MQTT Broker (Mosquitto)

```bash
# 安裝 Mosquitto
sudo apt install mosquitto mosquitto-clients -y

# 啟動 Mosquitto 服務
sudo systemctl start mosquitto

# 設定開機自動啟動
sudo systemctl enable mosquitto

# 檢查服務狀態
sudo systemctl status mosquitto
```

### 4. Python 套件

建立專案虛擬環境：

```bash
# 進入專案目錄
cd ~/pi-pico-integration

# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate

# 安裝必要套件
pip install fastapi uvicorn pymongo paho-mqtt python-multipart
pip install pyserial  # 用於 UART/USB 通訊
```

建立 requirements.txt：

```bash
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
pymongo==4.6.0
paho-mqtt==1.6.1
python-multipart==0.0.6
pyserial==3.5
pydantic==2.5.0
EOF

# 使用 requirements.txt 安裝
pip install -r requirements.txt
```

### 5. 開發工具

```bash
# 安裝文字編輯器
sudo apt install vim nano -y

# 安裝 Git（通常已預裝）
sudo apt install git -y

# 安裝網路工具
sudo apt install net-tools -y
```

## Raspberry Pi Pico 設定

### 1. 安裝 MicroPython 韌體

1. 下載最新的 [MicroPython 韌體](https://micropython.org/download/rp2-pico-w/)
   - 選擇 "Raspberry Pi Pico W" 版本
   - 下載 `.uf2` 檔案

2. 安裝韌體到 Pico：
   - 按住 Pico 上的 BOOTSEL 按鈕
   - 將 Pico 透過 USB 連接到電腦
   - Pico 會顯示為 USB 儲存裝置
   - 將 `.uf2` 檔案拖曳到 Pico 磁碟機
   - Pico 會自動重新啟動

### 2. 安裝 Thonny IDE

在 Raspberry Pi 上：

```bash
# Thonny 通常已預裝，如果沒有：
sudo apt install thonny -y
```

在 Windows/Mac/Linux 上：
- 從 [Thonny 官網](https://thonny.org/) 下載安裝

### 3. 配置 Thonny

1. 開啟 Thonny
2. 點擊右下角的直譯器選擇
3. 選擇 "MicroPython (Raspberry Pi Pico)"
4. 選擇正確的 USB 連接埠

### 4. 測試連接

在 Thonny 的 Shell 中輸入：

```python
>>> print("Hello, Pico!")
Hello, Pico!

>>> import machine
>>> led = machine.Pin("LED", machine.Pin.OUT)
>>> led.on()
>>> led.off()
```

如果 LED 能夠開關，表示連接成功。

### 5. 安裝 MQTT 函式庫到 Pico

在 Thonny 中：

1. 點擊 "Tools" > "Manage packages"
2. 搜尋 "umqtt.simple"
3. 點擊安裝

或手動安裝：

```python
# 在 Thonny Shell 中執行
import upip
upip.install('umqtt.simple')
```

## 網路配置

### 1. WiFi 設定（Raspberry Pi）

如果在安裝時沒有配置 WiFi：

```bash
# 編輯 wpa_supplicant 配置
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

# 加入以下內容
network={
    ssid="你的WiFi名稱"
    psk="你的WiFi密碼"
}

# 重新啟動網路服務
sudo systemctl restart dhcpcd
```

### 2. 固定 IP 位址（選用）

```bash
# 編輯 dhcpcd 配置
sudo nano /etc/dhcpcd.conf

# 在檔案末尾加入
interface wlan0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8

# 重新啟動
sudo reboot
```

### 3. 檢查網路連接

```bash
# 檢查 IP 位址
ip addr show

# 測試網路連接
ping -c 4 google.com

# 檢查開放的連接埠
sudo netstat -tulpn
```

## MQTT Broker 配置

### 1. 基本配置

```bash
# 建立配置檔
sudo nano /etc/mosquitto/conf.d/custom.conf

# 加入以下內容
listener 1883
allow_anonymous true
```

### 2. 重新啟動服務

```bash
sudo systemctl restart mosquitto
```

### 3. 測試 MQTT

開啟兩個終端視窗：

終端 1（訂閱者）：
```bash
mosquitto_sub -h localhost -t test/topic
```

終端 2（發布者）：
```bash
mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"
```

如果終端 1 顯示 "Hello MQTT"，表示 MQTT 運作正常。

## MongoDB 設定

### 1. 使用 Docker 啟動 MongoDB

```bash
# 建立資料目錄
mkdir -p ~/mongodb/data

# 啟動 MongoDB 容器
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v ~/mongodb/data:/data/db \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:latest

# 檢查容器狀態
docker ps
```

### 2. 測試 MongoDB 連接

```bash
# 進入 MongoDB Shell
docker exec -it mongodb mongosh -u admin -p password

# 在 MongoDB Shell 中
> show dbs
> exit
```

## 環境驗證

### 1. 執行驗證腳本

```bash
# 確保在專案目錄中
cd ~/pi-pico-integration

# 啟動虛擬環境
source venv/bin/activate

# 執行驗證腳本
python tools/verify_setup.py
```

### 2. 手動檢查清單

- [ ] Raspberry Pi 可以連接網路
- [ ] Python 3.9+ 已安裝
- [ ] Docker 和 Docker Compose 已安裝
- [ ] MongoDB 容器正在運行
- [ ] Mosquitto MQTT Broker 正在運行
- [ ] Pico 已安裝 MicroPython 韌體
- [ ] Thonny 可以連接到 Pico
- [ ] Pico 可以連接 WiFi（稍後在課程中設定）

### 3. 測試各項服務

```bash
# 測試 MQTT
python tools/test_mqtt.py --broker localhost --port 1883

# 測試 MongoDB
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://admin:password@localhost:27017/'); print('MongoDB OK')"

# 測試 Docker
docker ps
```

## 常見問題

### Q: Docker 安裝後無法執行

A: 確保已將使用者加入 docker 群組並重新登入：
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Q: Mosquitto 無法啟動

A: 檢查配置檔是否有語法錯誤：
```bash
sudo mosquitto -c /etc/mosquitto/mosquitto.conf -v
```

### Q: Thonny 找不到 Pico

A: 
1. 確認 USB 線材支援資料傳輸（不是只有充電功能）
2. 檢查 USB 連接埠權限：`sudo chmod 666 /dev/ttyACM0`
3. 重新安裝 MicroPython 韌體

### Q: MongoDB 容器無法啟動

A: 檢查連接埠是否被佔用：
```bash
sudo netstat -tulpn | grep 27017
```

### Q: Pico 無法連接 WiFi

A: 確認使用的是 Pico W（有 WiFi 功能），不是一般的 Pico。

## 下一步

環境設定完成後，請參考：
- [SCHEDULE.md](SCHEDULE.md) - 查看詳細課程安排
- [01_pico_basics/README.md](01_pico_basics/README.md) - 開始第一個模組

## 需要協助？

如果遇到設定問題，請參考：
- [resources/troubleshooting.md](resources/troubleshooting.md)
- 或向講師尋求協助
