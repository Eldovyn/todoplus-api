from dotenv import load_dotenv
import os

load_dotenv()

mongodb = os.getenv("MONGODB")
mongodb_url = os.getenv("MONGODB_URL")
secret_key = os.getenv("SECRET_KEY")
todoplus_url = os.getenv("TODOLUS_URL")
reset_password = os.getenv("RESET_PASSWORD")
smtp_email = os.getenv("SMTP_EMAIL")
smtp_password = os.getenv("SMTP_PASSWORD")
smtp_host = os.getenv("SMTP_HOST")
smtp_port = os.getenv("SMTP_PORT")
