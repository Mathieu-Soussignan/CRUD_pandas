from src import *
import os 
from werkzeug.security import generate_password_hash, check_password_hash

def test_hash_password():
    password = "test_password"
    hashed_password = generate_password_hash(password)
    assert hashed_password != password
    assert check_password_hash(hashed_password, password) # = true