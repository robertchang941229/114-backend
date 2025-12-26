from dotenv import load_dotenv
load_dotenv
from fastapi import FASTAPI,Depends,HTTPException,status
from pydantic import BaseModel
from google_oauth import vertify_google_id_token,exchange_code_for_tokens
from auth_utils import create_access_token, get_current_user_email

app=FASTAPI(title="資工系 114-Backen 示範專案")

class TockenRequest(BaseModel):
    id_tocken:str



class CodeRequest(BaseModel):
    code:str
    redirect_uri:str





@app.post("/auth/google/code",summary="[架構A] 用 Code 快取 JWT")
async def google_auth_with_code(request:CodeRequest):

    tokens=exchange_code_for_tokens(request.code,request.redirect_uri)

    google_id_token=tokens.get("id_token")
    if not google_id_token:
        raise HTTPException(status_code=400,detail="Google 帳號為提供Email")
    
    user_info = vertify_google_id_token(google_id_token)
    user_email = user_info.get("email")
    
    access_token=create_access_token(data={"sub":user_email})

    return {
        "access_tocken":access_token,
        "token_type":"bearer",
        "user":{
            "name":user_info.get("name"),
            "email":user_email,
            "picture":user_info.get("picture")


        },
        "google_access_token":tokens.get("access_token")
    }


@app.post("/auth/google",summary="[架構B]用ID Token換取JWT")
async def google_auth(request:TockenRequest):

    user_info=vertify_google_id_token(request.id_token)

    user_email=user_info.get("email")


