import json
import pandas as pd
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import time

client = ModbusTcpClient('127.0.0.1')

CRANE_X_ADDRESS = 1
CRANE_Y_ADDRESS = 2
CRANE_VACUUM_ADDRESS = 3

def read_input(address):
    result = client.read_holding_registers(address, 1)
    return result.registers[0]

def write_output(address, value):
    result = client.write_register(address, value)
    print(f"Successfully wrote {value} to address {address}")

def execute_commands_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Iterate through each action in the JSON file
    for action in data['actions']:
        if 'vacuum' in action:
            # Set vacuum state
            vacuum_state = action['vacuum']
            write_output(CRANE_VACUUM_ADDRESS, vacuum_state)
            print(f"Vacuum set to {vacuum_state}")
        elif 'setX' in action and 'setY' in action:
            # Set X and Y positions
            x_value = action['setX']
            y_value = action['setY']
            write_output(CRANE_X_ADDRESS, x_value)
            write_output(CRANE_Y_ADDRESS, y_value)
            print(f"Crane moved to X: {x_value}, Y: {y_value}")
        

        time.sleep(1)

if __name__ == "__main__":
    try:
        client.connect()

        json_file = 'crane_commands.json'
        
        execute_commands_from_json(json_file)

    except ModbusException as e:
        print(f"Modbus error: {e}")
    finally:
        client.close()
