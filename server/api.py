from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import JWTError, jwt
from pydantic import BaseModel
from query import run_query
from typing import Union
import uvicorn

app = FastAPI()
# app = FastAPI(docs_url=None, redoc_url=None)

# OAuth2加密
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/token')
# 密码用一次性md5加密
pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")
# jwt用这个密钥、这个算法加密，密钥可以自己随便生成
SECRET_KEY = "fdc891e49e9f4d526b8fdd7d53bf0a8dd40035de30e7e9c3db4d1035e2e05d60"
ALGORITHM = "HS256"
# 过期时间30分钟
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 一个虚假的用户表（字典）
users_db = {
    'user01':{
        'username': 'user01',
        'password': '$1$Nyu4AoP1$trb8LJzUXrbroQB60Ha51.', #对应的明文密码是password
    }
}

# Token类
class Token(BaseModel):
    access_token:str
    token_type:str

# 用户类
class UserInDB(BaseModel):
    username:str
    password:str

# 校验密码是否与密文一致
def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

# 获取用户字典
def get_user(users_db, username:str):
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(**user_dict)

# 校验用户是否在表中、密码是否一致
def authenticate_user(users_db, username, password):
    user = get_user(users_db, username)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user

# 生成token
def generate_token(data:dict, expires_delta:Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 创建返回token的接口
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 创建一个get查询接口
@app.get('/xxqg')
async def query_qg(key:str, token:str = Depends(oauth2_schema)):
    return JSONResponse(run_query(key),headers={'content-type': 'application/json;charset=utf-8'})

# 创建一个post查询接口
@app.post('/xxqg')
async def query_qg(key:str = Form(...), token:str = Depends(oauth2_schema)):
    return JSONResponse(run_query(key),headers={'content-type': 'application/json;charset=utf-8'})

if __name__ == '__main__':
    uvicorn.run('api:app', host='localhost', port=8000, reload=False, workers=1)