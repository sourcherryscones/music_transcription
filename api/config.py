import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI')
    ALLOWED_EXTENSIONS={"wav","mp3", "m4a"}
    UPLOAD_FOLDER='./api/storage_temp'
    UPLOAD_FOLDER_OUTPUT='./storage_temp'
    OUTPUT_FOLDER='../output_cautious'
