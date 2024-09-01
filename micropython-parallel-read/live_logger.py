#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import serial
import re
import time
import threading

PATTERN = re.compile(r"^interval=\d{1,10}, rzf=[01]{8}$")


# Function to read data from the serial port
def read_serial_data(ser, pattern, data_buffer):
    while True:
        line = (
            ser.readline().decode("utf-8").strip()
        )  # Read a line from the serial port
        print(line)
        if line and pattern.match(line):  # If the line matches the expected format
            print("Found one!")
            data_buffer.append(line)


# Function to parse the data def parse_data(data):
    ticks = []
    sensor_states = []

    for line in data:
        parts = line.split(", ")
        tick = int(parts[0].split("=")[1])
        rzf = parts[1].split("=")[1]

        ticks.append(tick)
        sensor_states.append(
            [int(bit) for bit in rzf[::-1]]
        )  # Reverse to match sensor index

    return ticks, np.array(sensor_states)


# Function to update the plot
def update_plot(ax, all_ticks, all_sensor_states):
    ax.clear()  # Clear the previous plot
    num_sensors = 8  # Assuming 8 sensors
    ax.set_xlim(0, num_sensors - 1)
    if all_ticks:
        ax.set_ylim(max(all_ticks), 0)  # Update y-limits
    ax.set_xticks(range(num_sensors))
    ax.set_xticklabels(range(num_sensors))
    ax.invert_yaxis()  # Invert y-axis to have 0 at the top
    ax.set_xlabel("Sensors")
    ax.set_ylabel("Ticks (inverted)")
    plt.title("Sensor Input Over Time")
    plt.grid()

    # Plot the data
    for i, tick in enumerate(all_ticks):
        for sensor_index in range(num_sensors):
            if all_sensor_states[i][sensor_index] == 1:
                ax.plot(sensor_index, tick, "ro")  # Plot a red dot for active sensors

    plt.draw()  # Update the plot
    plt.pause(0.1)  # Pause to allow the plot to update

# Function to parse the data
def parse_data(data):
    ticks = []
    sensor_states = []
    
    for line in data:
        parts = line.split(", ")
        tick = int(parts[0].split("=")[1])
        rzf = parts[1].split("=")[1]
        
        ticks.append(tick)
        sensor_states.append([int(bit) for bit in rzf[::-1]])  # Reverse to match sensor index

    return ticks, np.array(sensor_states)    

# Main function
def main():
    # Serial port configuration
    port = "/dev/ttyACM0"  # Change this to your serial port
    baudrate = 115200  # Change this to your baud rate


    # Regular expression to match the expected format
    pattern = PATTERN

    # Set up the serial connection
    ser = serial.Serial(port, baudrate, timeout=1)

    # Create a figure and axis for the plot
    fig, ax = plt.subplots()
    num_sensors = 8  # Assuming 8 sensors
    ax.set_xlim(0, num_sensors - 1)
    ax.set_ylim(0, 0)  # Initial y-limits will be updated later
    ax.set_xticks(range(num_sensors))
    ax.set_xticklabels(range(num_sensors))
    ax.invert_yaxis()  # Invert y-axis to have 0 at the top
    ax.set_xlabel("Sensors")
    ax.set_ylabel("Ticks (inverted)")
    plt.title("Sensor Input Over Time")
    plt.grid()

    # Initialize empty data
    all_ticks = []
    all_sensor_states = []
    data_buffer = []

    # Start the data reading thread
    data_thread = threading.Thread(
        target=read_serial_data, args=(ser, pattern, data_buffer), daemon=True
    )
    data_thread.start()
    try:
        while True:
            # Check if there is new data to process
            if data_buffer:
                new_data = data_buffer.copy()  # Copy the current data
                data_buffer.clear()  # Clear the buffer for new data
                ticks, sensor_states = parse_data(new_data)
                all_ticks.extend(ticks)
                all_sensor_states.extend(sensor_states)

            # Update the plot every 10 seconds
            update_plot(ax, all_ticks, all_sensor_states)
            time.sleep(10)  # Wait for 10 seconds before the next update

    except KeyboardInterrupt:
        print("Stopping data collection.")
    finally:
        ser.close()
        plt.close(fig)  # Close the plot window

    

if __name__ == "__main__":
    main()
