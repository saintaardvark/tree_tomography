#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import serial
import re
import sys


# Function to read data from the serial port
def read_serial_data(port, baudrate):
    ser = serial.Serial(port, baudrate, timeout=1)
    data = []

    # Regular expression to match the expected format
    pattern = re.compile(r"^interval=\d{1,5}, rzf=[01]{8}$")

    try:
        while True:
            line = (
                ser.readline().decode("utf-8").strip()
            )  # Read a line from the serial port
            print(line)
            if line and pattern.match(line):  # If the line matches the expected format
                print("found one!")
                data.append(line)
    except KeyboardInterrupt:
        print("Stopping data collection.")
    finally:
        ser.close()

    return data


# Function to parse the data
def parse_data(data):
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


# Main function
def main():
    # Serial port configuration
    port = "/dev/ttyACM0"  # Change this to your serial port
    baudrate = 115200  # Change this to your baud rate

    print("Reading data from serial port...")
    data = read_serial_data(port, baudrate)

    # Parse the collected data
    ticks, sensor_states = parse_data(data)

    # Get the number of sensors
    num_sensors = sensor_states.shape[1]

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set the y-axis to flow downwards
    ax.invert_yaxis()

    # Set the x-axis limits
    ax.set_xlim(0, num_sensors - 1)

    # Set the y-axis limits
    ax.set_ylim(
        max(ticks), 0
    )  # Set the limits to have 0 at the top and max tick at the bottom

    # Set the x-ticks to represent sensor indices
    ax.set_xticks(range(num_sensors))
    ax.set_xticklabels(range(num_sensors))

    # Plot the data
    for i, tick in enumerate(ticks):
        for sensor_index in range(num_sensors):
            if sensor_states[i][sensor_index] == 1:
                ax.plot(sensor_index, tick, "ro")  # Plot a red dot for active sensors

    # Set labels
    ax.set_xlabel("Sensors")
    ax.set_ylabel("Ticks (inverted)")

    # Show the plot
    plt.title("Sensor Input Over Time")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
