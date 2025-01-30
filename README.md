# Svelte Linux Dashboard for Orange Pi Zero 2W

A lightweight Svelte-based system monitoring dashboard for the Orange Pi Zero 2W. This dashboard provides real-time insights into CPU, memory, network usage, disk statistics, and basic system information. The backend is powered by Python's `psutil` library.

## Features

- **CPU Monitoring**: View real-time CPU usage and temperature.
- **Memory Usage**: Track available and used RAM.
- **Network Statistics**: Monitor upload/download speeds and active connections.
- **Disk Usage**: Display available and used disk space.
- **Basic System Info**: Get details about the system, including OS version and uptime.

## Tech Stack

- **Frontend**: Svelte (for a lightweight and reactive UI)
- **Backend**: Python with `psutil` (for fetching system stats)
- **Server**: FastAPI (serves API endpoints for frontend data retrieval)

## Installation & Setup

### Prerequisites

- Orange Pi Zero 2W (or similar SBC running Linux)
- Python 3 installed
- Node.js and npm installed

### Backend Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/Karniverse/svelte-orangepizero2w-dashboard.git
   cd orangepi-dashboard/backend
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install required dependencies:
   ```sh
   pip install fastapi psutil
   ```
4. Run the backend server:
   ```sh
   python backend/server.py
   ```

### Frontend Setup

1. Install dependencies:
   ```sh
   npm install
   ```
2. Start the Svelte app:
   ```sh
   npm run dev
   ```

## Usage

- Access the dashboard via your browser at `http://localhost:5173/`.
- Ensure the backend server is running to fetch system statistics.

## Roadmap

- [ ] Add historical data tracking
- [ ] Implement dark mode
- [ ] Expand support for additional SBCs
- [ ] Create a Docker container for easier deployment

## Contributing

Feel free to fork and submit pull requests to improve the project!

## License

This project is licensed under the MIT License.

## Author

Created by **Karniverse**. Reach out for collaboration or suggestions!



code references:
https://stackoverflow.com/questions/42471475/fastest-way-to-get-system-uptime-in-python-in-linux
https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/