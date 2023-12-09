from pydantic import BaseModel, HttpUrl, EmailStr, SecretStr
from typing import List, Dict


class GameCommonParams(BaseModel):
    respawn_request: HttpUrl
    server_url: HttpUrl


class PlayerParams(BaseModel):
    resources_to_collect: List[str]
    instance: HttpUrl
    signature: str
    resource_request_template: HttpUrl
    cookie: str
    profile_dir: str
    nickname: str
    username: EmailStr
    password: SecretStr
    srv: str


class AppConfig(BaseModel):
    common_params: GameCommonParams
    users: Dict[str, PlayerParams]
