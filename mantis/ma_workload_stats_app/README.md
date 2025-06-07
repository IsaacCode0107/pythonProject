# MA Workload Statistics Application

This project is a web application built using Flask that provides bi-weekly and monthly statistics of MA_WorkLoad by personnel and team. 

## Project Structure

```
ma_workload_stats_app
├── app
│   ├── __init__.py        # Initializes the Flask application and sets up configuration and routes
│   ├── models.py          # Defines data models for personnel and team workload statistics
│   ├── routes.py          # Contains route definitions for the web application
│   ├── services.py        # Includes business logic for processing workload data
│   └── templates
│       └── index.html     # Main HTML template for rendering statistics
├── requirements.txt       # Lists dependencies required for the project
├── config.py              # Contains configuration settings for the application
└── README.md              # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd ma_workload_stats_app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Configure the application:**
   Update the `config.py` file with your database connection details and any other necessary environment variables.

6. **Run the application:**
   ```
   flask run
   ```

## Usage

Once the application is running, you can access it in your web browser at `http://127.0.0.1:5000`. The main page will display the workload statistics, allowing you to view data by personnel and team for bi-weekly and monthly periods.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.