from fastapi import FastAPI, WebSocket, Depends, HTTPException # type: ignore
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from starlette.websockets import WebSocketDisconnect # type: ignore
from system_metrics import get_system_metrics
from database import insert_metrics, init_db, get_history, register_user, get_username_by_username
from security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from ai_engine import CPUPredictor, prepare_data, train_model
from pydantic import BaseModel
import logging
import jwt
import asyncio

logger = logging.getLogger(__name__)


class UserCreate(BaseModel):
    username: str
    password: str

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
init_db()
insert_metrics("00:00:00", 0.0, 0.0, 0.0)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if not username:
            raise HTTPException(status_code=401, detail="Geçersiz kimlik bilgileri")
            
        return {"username": username, "role": role}
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş bilet")

async def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Bu kapıdan sadece Adminler geçebilir!")
    
    return current_user

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = get_system_metrics()
            insert_metrics(data["timestamp"], data["cpu_usage"], data["memory_usage"], data["disk_usage"])
            await websocket.send_json(data)
            await asyncio.sleep(0.5)
        except WebSocketDisconnect:
            print("Client disconnected")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            import traceback
            traceback.print_exc()
            break

@app.get("/api/history")
async def get_metrics_history(current_user: dict = Depends(require_admin)):
    history = get_history()
    return [
        {
            "timestamp": row[1],
            "cpu_usage": row[2],
            "memory_usage": row[3],
            "disk_usage": row[4]
        }
        for row in history
    ]

@app.post("/api/register")
async def register(user: UserCreate):
    hashed_password = hash_password(user.password)
    try:
        register_user(user.username, hashed_password)
        return {"message": "User registered successfully"}
    except Exception as e:
        logger.error(f"Kayıt hatası: {e}")
        return {"error": "Bir hata oluştu, lüften tekrar deneyin"}


@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_in_db = get_username_by_username(form_data.username)
    if not user_in_db:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
    is_password_valid = verify_password(form_data.password, user_in_db[2])
    if not is_password_valid:
        raise HTTPException(status_code=401, detail="Hatalı şifre")
    token = create_access_token(data={"sub": form_data.username, "role": user_in_db[3]})
    return {"access_token": token, "token_type": "bearer"}
        
