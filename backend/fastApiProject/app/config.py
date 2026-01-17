from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # 基本设置
    APP_NAME: str = "WanderWise"
    DEBUG: bool = False

    # Mysql
    MYSQL_CONNECTION_STRING: str = "mysql+pymysql://user:123456@localhost:3306/wanderwise"

    # Elasticsearch设置
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_INDEX_PREFIX: str = "wanderwise_"

    # 外部API
    # 建议通过 .env 提供真实值（避免把 key 提交到 repo）
    GOOGLE_MAPS_API_KEY: str = ""
    DEEP_SEEK_API_KEY: str = ""


@lru_cache()
def get_settings():
    """创建设置单例，避免重复加载"""
    return Settings()
