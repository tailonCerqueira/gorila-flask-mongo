from dotenv import load_dotenv
load_dotenv(verbose=True)
import os

HOST=os.getenv("HOST")
PORT=os.getenv("PORT")
DB_URL=os.getenv("DB_URL")
DB_PORT=os.getenv("DB_PORT")
DB_COLLECTION=os.getenv("DB_COLLECTION")
