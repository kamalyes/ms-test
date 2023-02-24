import time
import jwt

from fastapi import APIRouter, Depends

from app.curl.awen.kerberos import KerberosDao
from app.schema.kerberos import EnvironmentSchema, KerberosSchema
from app.service import Permission

router = APIRouter()


@router.post("/awtoken/generate", summary="生成阿闻后台token")
async def generate_awen_token(request: KerberosSchema, oauth=Depends(Permission())):
  return await KerberosDao.generate_awen_token(request)
  