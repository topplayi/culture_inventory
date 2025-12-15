# 读.env
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./store.db"  # 默认值，可被 .env 覆盖

    class Config:
        env_file = ".env"  # 项目根目录下的 .env
        case_sensitive = False


settings = Settings()  # 单例，全局导入
