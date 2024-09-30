import BAC0

# Initialize BACnet network
bacnet = BAC0.lite()

# Define the object type and instance you want to read
object_type = 'analogInput'  # Example: 'analogInput', 'binaryOutput', etc.
object_instance = 1  # Replace with the instance number you want to read

# Create the BACnet address and object identifier
object_id = f'{object_type}.{object_instance}'

# Replace with the BACnet device address you want to query
device_address = '192.168.1.100'  # IP address of your BACnet device

# Construct the full BACnet object identifier
full_object_id = f'{device_address}/{object_id}'

try:
    # Read the value from the BACnet device
    result = bacnet.read(full_object_id)
    print(f'Read value: {result}')
except Exception as e:
    print(f'Error reading value: {e}')
