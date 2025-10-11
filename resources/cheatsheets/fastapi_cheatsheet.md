# FastAPI 速查表

快速參考 FastAPI 常用功能和模式。

## 基礎設定

### 建立應用程式
```python
from fastapi import FastAPI

app = FastAPI(
    title="IoT API",
    description="物聯網資料收集 API",
    version="1.0.0"
)
```

### 啟動伺服器
```bash
# 開發模式（自動重載）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 生產模式
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 路由定義

### GET 請求
```python
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# 查詢參數
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### POST 請求
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: str = None

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}
```

### PUT 請求
```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}
```

### DELETE 請求
```python
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}
```

## 資料模型

### Pydantic 模型
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SensorData(BaseModel):
    device_id: str = Field(..., description="裝置 ID")
    device_type: str = Field(default="pico_w")
    timestamp: str
    sensor_type: str
    value: float
    unit: str
    location: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "device_id": "pico_001",
                "device_type": "pico_w",
                "timestamp": "2025-10-11T10:30:00Z",
                "sensor_type": "temperature",
                "value": 25.5,
                "unit": "celsius",
                "location": "classroom_a"
            }
        }
```

### 資料驗證
```python
from pydantic import validator

class SensorData(BaseModel):
    value: float
    
    @validator('value')
    def validate_temperature(cls, v):
        if v < -50 or v > 100:
            raise ValueError('溫度超出有效範圍')
        return v
```

## 回應模型

### 標準回應
```python
from typing import Any

class Response(BaseModel):
    status: str
    data: Any = None
    message: str = ""

@app.get("/data", response_model=Response)
async def get_data():
    return Response(
        status="success",
        data={"items": []},
        message="資料查詢成功"
    )
```

### 狀態碼
```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    pass
```

## 錯誤處理

### HTTPException
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )
    return items[item_id]
```

### 自訂例外處理器
```python
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": exc.message}
    )
```

## 依賴注入

### 基本依賴
```python
from fastapi import Depends

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db = Depends(get_db)):
    return db.get_items()
```

### 類別依賴
```python
class CommonQueryParams:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    return {"skip": commons.skip, "limit": commons.limit}
```

## 中介軟體

### CORS 設定
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應限制來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 自訂中介軟體
```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## 背景任務

### 簡單背景任務
```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_log, f"Email sent to {email}")
    return {"message": "Notification sent"}
```

## 檔案上傳

### 上傳檔案
```python
from fastapi import File, UploadFile

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "size": len(contents)
    }
```

## 靜態檔案

### 提供靜態檔案
```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

## 模板

### Jinja2 模板
```python
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "title": "Dashboard"}
    )
```

## WebSocket

### WebSocket 端點
```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message: {data}")
    except:
        pass
```

## 資料庫整合

### MongoDB 範例
```python
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List

# 連接資料庫
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.iot_data
collection = db.sensor_data

@app.post("/data/")
async def create_data(data: SensorData):
    result = await collection.insert_one(data.dict())
    return {"id": str(result.inserted_id)}

@app.get("/data/", response_model=List[SensorData])
async def read_data(limit: int = 10):
    cursor = collection.find().limit(limit)
    data = await cursor.to_list(length=limit)
    return data
```

### PyMongo 範例（同步）
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.iot_data
collection = db.sensor_data

@app.post("/data/")
def create_data(data: SensorData):
    result = collection.insert_one(data.dict())
    return {"id": str(result.inserted_id)}

@app.get("/data/")
def read_data(limit: int = 10):
    data = list(collection.find().limit(limit))
    # 轉換 ObjectId 為字串
    for item in data:
        item['_id'] = str(item['_id'])
    return data
```

## 測試

### 測試客戶端
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test", "price": 10.5}
    )
    assert response.status_code == 200
```

## 文件

### 自動文件
```python
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc

# 自訂文件 URL
app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 隱藏端點
@app.get("/hidden", include_in_schema=False)
async def hidden_route():
    return {"message": "This is hidden"}
```

## 設定管理

### 環境變數
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "IoT API"
    mongodb_url: str
    mqtt_broker: str
    
    class Config:
        env_file = ".env"

settings = Settings()

@app.get("/info")
async def info():
    return {"app_name": settings.app_name}
```

### .env 檔案
```
MONGODB_URL=mongodb://localhost:27017
MQTT_BROKER=localhost
```

## 日誌

### 設定日誌
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.get("/items/")
async def read_items():
    logger.info("Reading items")
    return {"items": []}
```

## 效能優化

### 快取
```python
from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()

@app.get("/settings")
async def settings():
    return get_settings()
```

### 非同步操作
```python
import asyncio

@app.get("/slow")
async def slow_operation():
    # 使用 asyncio 進行非同步操作
    await asyncio.sleep(1)
    return {"message": "Done"}
```

## 安全性

### API 金鑰
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != "secret-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.get("/secure")
async def secure_endpoint(api_key: str = Depends(verify_api_key)):
    return {"message": "Secure data"}
```

## 常用指令

```bash
# 安裝 FastAPI
pip install fastapi uvicorn

# 安裝額外套件
pip install python-multipart  # 表單和檔案上傳
pip install jinja2            # 模板
pip install python-jose       # JWT
pip install passlib           # 密碼雜湊

# 執行伺服器
uvicorn main:app --reload

# 產生 requirements.txt
pip freeze > requirements.txt
```

## 實用技巧

### 健康檢查端點
```python
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

### 版本控制
```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/items")
async def get_items_v1():
    return {"version": "1.0"}

@v2_router.get("/items")
async def get_items_v2():
    return {"version": "2.0"}

app.include_router(v1_router)
app.include_router(v2_router)
```

## 參考資源

- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [FastAPI GitHub](https://github.com/tiangolo/fastapi)
- [Pydantic 文件](https://pydantic-docs.helpmanual.io/)
- [Uvicorn 文件](https://www.uvicorn.org/)
