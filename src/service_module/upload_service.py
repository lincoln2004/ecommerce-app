from fastapi import UploadFile, HTTPException

from dotenv import load_dotenv

import cloudinary
import cloudinary.uploader
import cloudinary.utils

from uuid import uuid4
import os

load_dotenv()

class DriveUploadService:
    
    def __init__(self):
        
        cloudinary.config( 
        cloud_name = os.getenv('REMOTE_STORAGE_NAME'), 
        api_key = os.getenv('REMOTE_STORAGE_IDENTITY'), 
        api_secret = os.getenv('REMOTE_STORAGE_KEY'),
        secure = True
        )
    
    def upload_file(self, file: UploadFile):
        
        try:
            result = cloudinary.uploader.upload(
                file.file, 
                folder="fastapi_uploads",
                public_id=str(uuid4())
            )
            
            if not result: raise Exception()
            
            if id := result.get('public_id'):
                return id
            
            raise Exception() 
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500)    
        
    def get_file(self, id):
        
        try:
            url, _ = cloudinary.utils.cloudinary_url(id, secure=True)
        
            if not url: raise Exception('file not found')
            
            return url
        except Exception as e:
            print(e) 
            
            raise HTTPException(status_code=500)   
        
    def delete_file(self, id):
        
        try:
            result = cloudinary.uploader.destroy(id)
            
            if result.get("result") == "ok":
                return True
            
            raise Exception()
        except Exception as e:
            
            print(e)
            raise HTTPException(status_code=500)
            