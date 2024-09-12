class Settings:
    VECTOR_DB_PATH = r'./chromadb'
    DEFAULT_COLLECTION = r'langchain'

    LOG_FORMAT = r'%(asctime)s [%(name)s] %(filename)s:%(lineno)d:%(funcName)s [%(levelname)s] %(message)s'
    LOG_DATE_FORMAT = r'%Y-%m-%d %H:%M:%S'
    LOG_LEVEL = 'info'
