import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return MySQLdb.connect(
        host=os.getenv("MYSQL_HOST", "gondola.proxy.rlwy.net"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "LPibeCJDBWxROkNbNaAtDYrvfyXBKIyz"),
        database=os.getenv("MYSQL_DATABASE", "railway"),
        port=int(os.getenv("MYSQL_PORT", 35908)),
        )
