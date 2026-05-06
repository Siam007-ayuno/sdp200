# SafeZone - Varsity Project

SafeZone is a Python desktop application (built with Tkinter) connected to a MySQL database. It helps users search or select an area to view its safety level and report safety issues.

## Tech Stack
- **Language**: Python 3
- **GUI**: Tkinter (ttk)
- **Database**: MySQL

## Prerequisites
- Python 3.x installed
- MySQL Server installed and running

## Setup Instructions for VS Code

1. **Clone or Extract** the project folder.
2. **Open** the folder in **VS Code**.
3. **Set up the Database**:
   - Open your MySQL Workbench or command line client.
   - Run the provided `database.sql` script to create the database, tables, and insert sample data.
4. **Configure Database Credentials**:
   - In `db.py`, update the `host`, `user`, and `password` inside the `Database.__init__` method to match your local MySQL configuration. Default uses `root` and an empty password `""`.
5. **Install Dependencies**:
   - Open a terminal in VS Code (`Ctrl + ~`).
   - Run the following command:
     ```bash
     pip install -r requirements.txt
     ```
6. **Run the Application**:
   - In the terminal, run:
     ```bash
     python main.py
     ```

## Features
- **Dashboard**: View safety summary for an area.
- **Explore Areas**: List of all areas and their current status.
- **Report an Area**: Submit a report about an incident in a specific area.
- **View Reports**: Check recent reports for any area.
- **Admin**: Basic login tab for admin users (username: `admin`, password: `admin123`).
