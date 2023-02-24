import time
import jwt
from app.core.handler.execres import ValidException
from app.core.handler.jsonres import MsResponse

from app.curl import MsModelWrapper
from app.schema.kerberos import KerberosSchema
from config import MsAppConfig


@MsModelWrapper(KerberosSchema)
class KerberosDao():

    @classmethod
    async def generate_awen_token(cls, request: KerberosSchema):
        """
        { "mobile": 18176699611,"name": "yu","userno": "U_3B63GEA","exp": 1677577765}
  """
        valid_env_array_, env_ = {1: "sit", 2: "uat"}, request.env
        if env_ in valid_env_array_.keys():
            private_key_path = f"{MsAppConfig.CONF_PATH}/{valid_env_array_.get(env_)}_private_key.pem"
            claims = {
                "mobile": request.mobile,
                "name": request.name,
                "userno": request.user_no
            }
            offset_time = 72 * 60 * 60
            exp = int(time.time()) + offset_time
            claims['exp'] = exp
            # print("\nsecret-----------\n"+secret + "\nclaims---------"+str(claims));
            secret = open(private_key_path, "rb").read()
            token = jwt.encode(claims, secret, algorithm='RS256')
            return MsResponse.success(token, message=private_key_path)
        else:
            raise ValidException
