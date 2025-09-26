# RAS Lab 2 - Dobot Magician Lite End Effector Control

## 📁 Repository Structure

```
lab_2_code/
├── README.md                    # Project documentation (to be added)
├── get_robot_position.py        # Robot position retrieval utility
├── pydobot_gripper.py          # Gripper end effector control script
├── pydobot_port.py             # Port communication handler
├── pydobot_suction.py          # Suction cup end effector control script
├── pyproject.toml              # Python project configuration
└── uv.lock                     # UV package manager lock file
```

## 🎯 Project Overview

This repository contains control scripts for operating the Dobot Magician Lite robotic arm with two different end effectors:
- **Suction Cup**: For picking up flat, smooth objects
- **Gripper**: For grasping objects with adjustable grip strength

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Dobot Magician Lite robotic arm
- USB connection to the robot

### Installation
```bash
git clone https://github.com/anirudh97asu/lab_2_code.git
cd lab_2_code
uv sync  # Install dependencies using UV package manager
# OR using pip:
pip install pydobot
```

### Basic Usage
```python
# Suction cup operation
python pydobot_suction.py

# Gripper operation
python pydobot_gripper.py

# Get current robot position
python get_robot_position.py
```

## 📋 Main Components

### Core Scripts
- **`pydobot_suction.py`** - Main control script for suction cup end effector operations
- **`pydobot_gripper.py`** - Main control script for gripper end effector operations  
- **`get_robot_position.py`** - Utility script for retrieving current robot position coordinates
- **`pydobot_port.py`** - Port communication management and connection handling

### Configuration Files
- **`pyproject.toml`** - Python project configuration using modern packaging standards
- **`uv.lock`** - UV package manager lock file ensuring reproducible builds

### Dependencies
- `pydobot` - Python library for Dobot Magician Lite control
- Additional dependencies managed through UV package manager

## 🎥 Demonstration Videos

### Suction Cup End Effector
- **Platform**: YouTube Shorts
- **Link**: [https://youtube.com/shorts/zYZhu5pHMZQ](https://youtube.com/shorts/zYZhu5pHMZQ)
- **Content**: Full cycle demonstration with timing display

### Gripper End Effector
- **Platform**: YouTube Shorts
- **Link**: [https://youtube.com/shorts/u3Fqj_t1XtY](https://youtube.com/shorts/u3Fqj_t1XtY)
- **Content**: Full cycle demonstration showing rotational adjustments

## 📖 Documentation

- Complete setup instructions and usage examples coming soon
- API reference for all control functions
- Troubleshooting guide for common connection and operational issues

## 🔧 Development Tools

This project uses modern Python tooling:
- **UV Package Manager**: Fast, reliable dependency resolution and virtual environment management
- **pyproject.toml**: Standard Python project configuration
- **Modular Design**: Separate scripts for different end effector types and utilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📚 References

1. Dobot Magician Lite User Manual, Dobot Technology, 2023
2. [Python 3.8 Documentation](https://docs.python.org/3.8/), Python Software Foundation, 2024
3. [Pydobot Library Documentation](https://pypi.org/project/pydobot/), 2024

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏫 Academic Context

This project is part of RAS (Robotics and Autonomous Systems) Lab 2, focusing on end effector control and manipulation tasks using the Dobot Magician Lite platform.

---

**Repository**: [https://github.com/anirudh97asu/lab_2_code](https://github.com/anirudh97asu/lab_2_code)
