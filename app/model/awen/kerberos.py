import time
import jwt

from app.curl.awen.kerberos import KerberosDao
from app.schema.kerberos import KerberosSchema


class Kerberos():
    async def generate_awen_token(request: KerberosSchema):
       return await KerberosDao.generate_awen_token(request)
