import serial
import time


potential_ports = [
    '/dev/cu.HC-05',
    '/dev/cu.HC-05-DevB',
    '/dev/tty.HC-05',
    '/dev/tty.HC-05-DevB'
]

# Try to connect to any available port
bluetooth = None
connected_port = None

print("Attempting to connect to HC-05...")
for port in potential_ports:
    try:
        print(f"Trying port: {port}")
        test = serial.Serial(port, 9600, timeout=1)
        bluetooth = test
        connected_port = port
        print(f"Successfully connected to {port}")
        break
    except Exception as e:
        print(f"Failed to connect to {port}: {e}")

if not bluetooth:
    print("Could not connect to any Bluetooth port!")
    print("Please check if the HC-05 module is paired with your Mac.")
    exit(1)

# Function to send commands with visual confirmation
def send_command(cmd):
    print(f"Sending command: {cmd}")
    bluetooth.write(cmd.encode())
    time.sleep(0.5)
    print(f"Command sent: {cmd}")

# Test LED control first (simplest test)
print("\nTESTING LED CONTROL")
print("The built-in LED should blink ON and OFF")
for i in range(3):
    print(f"\nTest {i+1}/3:")
    print("Turning LED ON")
    send_command('N')  # 'N' for ON
    time.sleep(1)
    
    print("Turning LED OFF")
    send_command('F')  # 'F' for OFF
    time.sleep(1)

print("\nTESTING MOTOR COMMANDS")
commands = [
    ('F', "Forward - 5 fingers up"),
    ('B', "Backward - All fingers down"),
    ('L', "Left - Middle finger up"),
    ('R', "Right - Index finger up"),
    ('S', "Stop - Thumb up")
]

for cmd, desc in commands:
    print(f"\nSending {desc} command: {cmd}")
    send_command(cmd)
    input("Press Enter to continue to next command...")

# Close the connection
bluetooth.close()
print("\nTest complete!")