from auth import hash_password, verify_password

try:
    pwd = "mysecretpassword"
    hashed = hash_password(pwd)
    print(f"Hash: {hashed}")
    assert verify_password(pwd, hashed)
    print("Verification successful")
except Exception as e:
    print(f"Error: {e}")
