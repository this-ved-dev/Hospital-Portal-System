# Hospital Management System

A comprehensive web-based Hospital Management System built with Flask that allows doctors and patients to manage appointments, share medical information, and communicate effectively.

## Features

- **User Authentication**
  - Separate registration and login for doctors and patients
  - Secure password handling
  - Profile management with image upload

- **Doctor Features**
  - Create and manage medical blogs
  - View and manage patient appointments
  - Update patient diagnoses
  - Profile management with specialization details

- **Patient Features**
  - Book appointments with doctors
  - View medical blogs
  - Track appointment status
  - Update personal information

- **Blog System**
  - Create, edit, and delete medical blogs
  - Share medical information and updates
  - View all published blogs

- **Appointment Management**
  - Book appointments
  - Track appointment status
  - View appointment history
  - Update appointment details

## Prerequisites

- pyenv (Python version manager)
  - Windows: Install using [pyenv-win](https://github.com/pyenv-win/pyenv-win)
  - Linux/MacOS: Install using [pyenv](https://github.com/pyenv/pyenv)
- pip (Python package installer)

## Installation

1. **Install pyenv**
   - **Windows**:
     ```bash
     # Open PowerShell as Administrator and set execution policy
     Set-ExecutionPolicy RemoteSigned
     # Type 'Y' when prompted

     # Install pyenv-win
     Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
     ```
     After installation, restart your terminal and verify:
     ```bash
     pyenv --version
     ```

   - **Linux/MacOS**:
     ```bash
     # Using curl
     curl https://pyenv.run | bash
     ```
     Add to your shell configuration file (~/.bashrc, ~/.zshrc, etc.):
     ```bash
     export PATH="$HOME/.pyenv/bin:$PATH"
     eval "$(pyenv init -)"
     eval "$(pyenv virtualenv-init -)"
     ```

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Hospital_Management
   ```

3. **Install Python 3.11 using pyenv**
   ```bash
   # Install Python 3.11
   pyenv install 3.11.0

   # Set local Python version
   pyenv local 3.11.0
   ```

4. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv hospital-env #Windows
   pyenv virtualenv 3.11.0 hospital-env #Linux/MacOS

   # Activate virtual environment
   hospital-env\Scripts\activate #Windows
   pyenv activate hospital-env #Linux/MacOS
   ```

5. **Install the project and dependencies**
   ```bash
   # Install in editable mode with development dependencies
   pip install -e ".[dev]"
   ```

6. **Set up environment variables**
   Create a `.env` file in the root directory with the following content:
   ```
   FLASK_APP=hospital_flask
   FLASK_ENV=development
   SECRET_KEY=<your-secret-key>
   SQLALCHEMY_DATABASE_URI=sqlite:///hospital.db
   SQLALCHEMY_TRACK_MODIFICATIONS=False
   ```

7. **Initialize the database**
   ```bash
   flask shell
   ```
   In the Flask shell:
   ```python
   from hospital_flask import db
   db.create_all()
   exit()
   ```

## Development

The project uses several development tools to maintain code quality:

- **Code Formatting**: Black and isort for consistent code style
- **Type Checking**: mypy for static type checking
- **Linting**: flake8 for code linting
- **Testing**: pytest for unit and integration tests

To run the development tools:

```bash
# Format code
black .
isort .

# Type checking
mypy .

# Linting
flake8

# Run tests
pytest
```

## Running the Application

1. **Run the Flask application**
   ```bash
   flask run
   ```

2. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

## Project Structure

```
Hospital_Management/
├── hospital_flask/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── profile_pics/
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       └── ...
├── pyproject.toml
├── .python-version
├── run.py
└── README.md
```

## Database Models

- **User (Doctor)**
  - Basic information (name, email, password)
  - Professional details (occupation, specialization)
  - Profile image
  - Blog and appointment relationships

- **UserPatient**
  - Basic information (name, email, password)
  - Personal details (age, gender)
  - Profile image
  - Appointment relationships

- **Blog**
  - Title and content
  - Author relationship
  - Timestamp

- **Appointment**
  - Doctor and patient relationships
  - Appointment date and time
  - Status and diagnosis
  - Symptoms

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please ensure your code follows our style guidelines:
- Use Black for code formatting
- Follow type hints with mypy
- Pass all tests
- Update documentation as needed


## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- Flask and its extensions for the web framework
- SQLAlchemy for database management