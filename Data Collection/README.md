
# Ping360 Sonar Data Processing

This repository provides a Python script to collect and process sonar data using the Blue Robotics Ping360 scanning sonar. The collected data can be used for various research and exploration purposes.

## Overview

**Ping360 Scanning Imaging Sonar**  
The Ping360 is a mechanical scanning sonar for navigation and imaging. It has a 50-meter (165-foot) range, a 300-meter (984-foot) depth rating, and an open-source software interface, making it a capable tool for ROV navigation and underwater acoustic imaging.

### Features
- **Range**: 50 meters (165 feet)
- **Depth Rating**: 300 meters (984 feet)
- **Open-Source Software Interface**

**Price**: $2,650.00

**Included Components**:
- Ping360 Sonar
- Connection Cables
- Software Interface

For more details, visit the [Blue Robotics Ping360 Product Page](https://bluerobotics.com/store/sensors-sonar-cameras/sonar/ping360-sensor-r1-rp/).

### Team Information

**Author**: Md Junayed Hasan  
**Teams**: Bryan Bourdin, Hamid Reza Farhadi

**Context**:  
Using Blue Robotics Ping360 sonar, we have collected underwater sonar data for our research initiatives. This module heavily relies on the documentation and APIs provided by Blue Robotics for the Ping360 sonar.

**Project Role**:  
As an ML Engineer and Tech Lead, my role is to justify the feasibility check as a Subject Matter Expert (SME) on sensor setup and data inspection based on DMBOK.

**Research Context**:  
Our experiment is part of ongoing research initiatives, and further details will be openly available when the manuscript/research findings are published.

## Getting Started

### Prerequisites

To use this module, you will need the following Python libraries:

- `brping` (Blue Robotics Ping Library)
- `pathlib` (Standard Library)
- `csv` (Standard Library)
- `re` (Standard Library)
- `datetime` (Standard Library)

Install the required Python package:

```bash
pip install brping
```

### Required Hardware
- **Blue Robotics Ping360 Scanning Sonar**  
  The sonar can be purchased from [Blue Robotics](https://bluerobotics.com/store/sensors-sonar-cameras/sonar/ping360-sensor-r1-rp/).

### Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/Sonar-Data-Collection-Analysis-AI-Ping360-Bluerobotics.git
    ```

2. **Connect the Sonar**:
   - Connect the sonar to your computer following the Blue Robotics Ping360 User Guide.

3. **Run the Script**:
   - Update the serial port in the script (`"COM4"` in Windows or `"/dev/ttyUSB0"` in Linux/Mac).
   - Update the `output_directory` path to your desired location.


4. **Inspect Results**:
   - The script will output raw and formatted data in CSV files in the specified directory.

## Project Structure

```
ping360-sonar-data-processing/
└── Data Collection
   ├── ping360.py
   ├── ping360_connection.py    # The main script for collecting and processing sonar data
   └── README.md                # This README file
```

## Documentation References
- [Blue Robotics GitHub - Ping Library](https://github.com/bluerobotics/ping-python)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
