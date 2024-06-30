from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(None, description='Логин')
    token: str = Field(None, description='Токен')
    old_password: str = Field(None, description='Старый пароль')
    new_password: str = Field(None, description='Новый пароль')
