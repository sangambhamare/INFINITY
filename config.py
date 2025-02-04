import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '21038175e1ecaf5abba836607a163f20'
