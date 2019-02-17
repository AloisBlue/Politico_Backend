# config.py


class Configurations():
    """docstring for Configurations class."""
    DEBUG = False


class Develop(Configurations):
    """docstring for Develop environment."""
    DEBUG = True


class Testing(Configurations):
    """Testing environment"""
    DEBUG = True


class ProductionConfig(Configurations):
    """Production Configurations environment"""
    DEBUG = False


config = {
    'development': Develop,
    'testing': Testing,
    'production': ProductionConfig
    }

config = {
    'development': Develop,
    'testing': Testing,
    'production': ProductionConfig
}
