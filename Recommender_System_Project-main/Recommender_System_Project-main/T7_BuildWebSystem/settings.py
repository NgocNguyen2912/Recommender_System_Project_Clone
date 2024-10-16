# Import libraries:
import bcrypt

# MongoDB address:
MONGODB_HOST = 'mongodb://localhost:27017/'
MONGODB_ATLAS = ''
password = 'dsa123456'
uri = f"mongodb+srv://DSA_Project:dsa123456@cluster0.gdtn4g6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Common password:
TMP_PASSWORD = bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode().encode()
