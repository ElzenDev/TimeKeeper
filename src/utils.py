from datetime import datetime

now = datetime.now()

time_str = "2025-09-23 17:51:55.907123"

new_time = now.fromisoformat(time_str)

print(new_time)