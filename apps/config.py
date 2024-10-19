from pydantic_settings import BaseSettings,SettingsConfigDict



class Settings(BaseSettings):

    
    model_config = SettingsConfigDict(
        env_file='apps\.env',
        #case_sensitive=True
    )

    database_hostname: str
    database_username: str
    database_password: str
    database_name: str
    database_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()      