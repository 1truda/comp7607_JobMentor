import uuid
# unique_id = uuid.uuid3(0xbc3dc497)
# print(unique_id)


from datetime import datetime

# Getting the current date and time
current_time = datetime.now()

# Getting the timestamp
timestamp = current_time.timestamp()

print("Current time:", current_time)
print("Timestamp:", timestamp)

x="2024-11-23 12:00:00"
x=datetime.timestamp(datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
print(x)