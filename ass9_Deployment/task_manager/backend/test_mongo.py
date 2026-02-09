import asyncio
import os
from dotenv import load_dotenv
from config.database import check_mongo_connection

load_dotenv()

# NOTE: Avoid emojis in console output on Windows default encodings.
print(f"Connection String: {os.getenv('MONGO_URL')}")
print("Attempting connection...\n")

try:
    asyncio.run(check_mongo_connection())
except Exception as e:
    # Plain ASCII messages for Windows consoles
    print(f"\nError Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    
    msg = str(e).lower()
    if "authentication failed" in msg:
        print("\nHINT: Check these in MongoDB Atlas:")
        print("  1. Verify IP whitelist (add your IP or 0.0.0.0/0 for testing)")
        print("  2. Verify username/password are correct")
        print("  3. Ensure the user has access to the target database")
    elif "lookup" in msg or "timed out" in msg:
        print("\nHINT: Possible DNS/network issue – check internet and Atlas network access settings")
