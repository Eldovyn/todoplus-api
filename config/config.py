from dotenv import load_dotenv
import os

load_dotenv()

mongodb = os.getenv("MONGODB")
mongodb_url = os.getenv("MONGODB_URL")
secret_key = os.getenv("SECRET_KEY")
