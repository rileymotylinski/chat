from datetime import datetime

def log_message(body: str) -> str:
    print(f"[{str(datetime.now())}] {body}")