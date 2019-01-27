import os


class Config():
    DEBUG = False
    TESTING = False
    SECRET = os.getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True
    url = os.getenv("DB_URL")


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    url = os.getenv("TEST_URL")


class StagingConfig(Config):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig
}

secret_key = Config.SECRET
db_url = DevelopmentConfig.url
test_url = TestingConfig.url
