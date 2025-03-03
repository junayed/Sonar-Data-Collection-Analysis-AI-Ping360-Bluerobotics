#!/usr/bin/env python3

# ping360_data_processing.py
# This script uses the Blue Robotics Ping360 scanning sonar to collect and process sonar data.

"""
Author: Md Junayed Hasan
Teams: Bryan Bourdin, Hamid Reza Farhadi
Context: Using bluerobotics Ping360 sonar, we have collected the underwater sonar data.
This module heavily relies on the documentation and APIs provided by Blue Robotics for the Ping360 sonar.

"""

from brping import Ping360
from pathlib import Path
import csv
import re
from datetime import datetime, time


def calculate_v_sound(T, S, D):
    """
    Calculate the speed of sound in water based on temperature, salinity, and depth.
    
    Args:
        T (float): Water temperature in °C
        S (float): Salinity in PSU (Practical Salinity Units)
        D (float): Depth in meters
    
    Returns:
        float: Speed of sound in m/s
        
        
    This Equation is inspired by
    http://resource.npl.co.uk/acoustics/techguides/soundseawater/underlying-phys.html
    https://bluerobotics.com/learn/speed-of-sound-in-water-calculator/
    This is more simplified version, as the purpose is to test on simulated environment
    
    The details about it will be relased when the research findings are available
    """
    return 1410 + 4.21 * T - 0.037 * T**2 + 1.10 * S + 0.018 * D


def calculate_sample_distance(max_range, number_of_samples):
    """
    Calculate the distance between each sonar sample.
    
    Args:
        max_range (float): Maximum sonar range in meters
        number_of_samples (int): Number of sonar samples
    
    Returns:
        float: Distance per sample in meters
    """
    return max_range / number_of_samples


def calculate_sample_period(sample_distance, v_sound):
    """
    Calculate the sample period based on the sample distance and speed of sound.
    
    Args:
        sample_distance (float): Distance between each sample in meters
        v_sound (float): Speed of sound in m/s
    
    Returns:
        float: Sample period in nanoseconds
    """
    return sample_distance / (v_sound * 12.5 * 10**-9)


def setup_ping360(p, number_of_samples, sample_period, gain, transmit_duration, transmit_frequency):
    """
    Configure the Ping360 sonar settings.
    
    Args:
        p (Ping360): Instance of the Ping360 class
        number_of_samples (int): Number of samples to set
        sample_period (float): Sample period in nanoseconds
        gain (int): Gain setting (0 = low, 1 = normal, 2 = high)
        transmit_duration (int): Transmit duration in microseconds
        transmit_frequency (int): Transmit frequency in kHz
    """
    p.set_number_of_samples(number_of_samples)
    p.set_sample_period(int(sample_period))
    p.set_gain_setting(gain)
    p.set_transmit_duration(transmit_duration)
    p.set_transmit_frequency(transmit_frequency)


def extract_and_format_data(input_path):
    """
    Extract and format sonar data from the raw output file.
    
    Args:
        input_path (Path): Path to the raw data file
    
    Returns:
        list: A list of lists, each containing angle and intensity values
    """
    with input_path.open("r") as file:
        lines = file.read().splitlines()

    data_detection = '- data:'
    angle_detection = '- angle:'
    data_vector = []

    for element in lines:
        if angle_detection in element:
            angle = re.sub(angle_detection, "", element)

        if data_detection in element:
            element = re.sub(data_detection, "", element)
            element = re.sub("[\[\]' ]", "", element)
            h = element.split(",")
            h = [str(int(data, 16)) for data in h]
            h.insert(0, angle)
            data_vector.append(h)

    return data_vector


def save_data_to_csv(output_path, header, data_vector):
    """
    Save formatted data to a CSV file.
    
    Args:
        output_path (Path): Path to the output CSV file
        header (list): List containing the header names
        data_vector (list): Formatted data as a list of lists
    """
    with output_path.open("w") as out:
        csv_writer = csv.writer(out, delimiter=";")
        csv_writer.writerow(header)
        for sample in data_vector:
            csv_writer.writerow(sample)


# Define the paths directly
output_directory = Path("Deine your path")
output_directory.mkdir(parents=True, exist_ok=True)

# Define parameters
T = 16  # Water Temperature
S = 0  # Salinity - clean water is 0
D = 0.15  # Depth, the position of the sensor from the surface of the water
max_range = 2  # Maximum range in meters
number_of_samples = 1200  # Number of samples needed
G = 1  # Gain setting
transmit_duration = 16 # Transmit duration for a single acoustic ping
transmit_frequency = 1000

# Initialize Ping360 sonar
p = Ping360()
p.connect_serial("COM4", 115200)
p.initialize()

v_sound = calculate_v_sound(T, S, D)
sample_distance = calculate_sample_distance(max_range, number_of_samples)
sample_period = calculate_sample_period(sample_distance, v_sound)

setup_ping360(p, number_of_samples, sample_period, G, transmit_duration, transmit_frequency)

# Collect sonar data
data_vector = []
now = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
raw_output_path = output_directory / f"{now}.csv"

with raw_output_path.open("w") as out:
    csv_writer = csv.writer(out)
    for x in range(150, 251):
        response = p.transmitAngle(x)
        data = response.unpack_msg_data
        data_vector.append(data)
    csv_writer.writerow(data_vector)

# Extract and format data
data_vector = extract_and_format_data(raw_output_path)
results_output_path = output_directory / f"{now}_Results.csv"
header = ["Angle (gradian)", "Intensity (0-255)"]
save_data_to_csv(results_output_path, header, data_vector)
