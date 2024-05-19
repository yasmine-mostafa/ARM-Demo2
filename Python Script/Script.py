import serial
import time
from datetime import datetime

# Configure the serial connection
Pressed = 'L'
Not_Pressed = 'H'
Led_ON ='O'
Led_OFF = 'F'
Trail = 0
ser = serial.Serial(
    port='COM7',  # Replace with your COM port
    baudrate=9600,  # Set your baud rate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Function to send a command over UART
def send_command(command):
    ser.write(command.encode())
    print(f"Sent command: {command}")

# Function to receive a response from the STM32
def receive_response():
    time.sleep(0.5)  # Wait for STM32 to respond
    response = ser.readline().decode('utf-8').strip()
    if response:
        print(f"Received response: {response}")
    return response

# Main program
with open("test_log.txt", "w") as logfile:
    while Trail < 6:
        if ser.isOpen():
            print("Serial port is open.")
            #to Get Pin Status
            send_command('S') 
            response = receive_response()
            time.sleep(0.5)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if response == Pressed:
                #Led ON
                send_command('O')
                response = receive_response()
                if response == Led_ON:
                    logfile.write(f"{timestamp}: Test case {Trail+1}: Pressed, Command: Led_ON, Response: Led_ON, Result: Pass\n")
                    print("Test case pass.")
                else:
                    logfile.write(f"{timestamp}: Test case {Trail+1}: Pressed, Command: Led_ON, Response: Led_ON, Result: Fail\n")
                    print("Test case fail.")
            elif response == Not_Pressed:
                send_command('F')
                response = receive_response()
                if response == Led_OFF:
                    logfile.write(f"{timestamp}: Test case {Trail+1}: Not Pressed, Command: Led_OFF, Response: Led_OFF, Result: Pass\n")
                    print("Test case pass.")
                else:
                    logfile.write(f"{timestamp}: Test case {Trail+1}: Not Pressed, Command: Led_OFF, Response: Led_OFF, Result: Fail\n")
                    print("Test case fail.")
            time.sleep(5)
        Trail += 1