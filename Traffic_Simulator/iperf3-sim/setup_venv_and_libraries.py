import os
import subprocess
import sys


def create_virtualenv(env_name="venv"):
    """Create a virtual environment."""
    if not os.path.exists(env_name):
        print(f"Creating virtual environment: {env_name}")
        subprocess.check_call([sys.executable, "-m", "venv", env_name])
    else:
        print(f"Virtual environment {env_name} already exists.")


def get_installed_packages(env_name="venv"):
    """Get a set of installed packages witpython -m pytest test_setup_venv_and_libraries.py --cov=setup_venv_and_libraries --cov-report=term
    hout versions using pip freeze."""
    pip_path = (
        os.path.join(env_name, "Scripts", "pip")
        if os.name == "nt"
        else os.path.join(env_name, "bin", "pip")
    )
    try:
        output = subprocess.check_output([pip_path, "freeze"], text=True)
        installed_packages = {
            line.split("==")[0].strip().lower() for line in output.splitlines()
        }
        return installed_packages
    except subprocess.CalledProcessError:
        print("Error retrieving installed packages.")
        sys.exit(1)


def check_and_install_dependencies(
    env_name="venv", requirements_file="requirements.txt"
):
    """Check and install dependencies only if not already installed."""
    pip_path = (
        os.path.join(env_name, "Scripts", "pip")
        if os.name == "nt"
        else os.path.join(env_name, "bin", "pip")
    )
    print("Checking dependencies...")

    # Read requirements.txt
    if not os.path.exists(requirements_file):
        print(f"Requirements file {requirements_file} not found. Please create one.")
        sys.exit(1)

    with open(requirements_file, "r") as req_file:
        required_packages = {
            line.strip().split("==")[0].lower() for line in req_file.readlines()
        }

    # Get currently installed packages
    installed_packages = get_installed_packages(env_name)

    # Identify missing packages
    missing_packages = required_packages - installed_packages

    # Install only missing packages
    if missing_packages:
        print(f"Installing missing dependencies: {missing_packages}")
        # subprocess.check_call([pip_path, "install", "--upgrade", "pip"])  # Upgrade pip
        subprocess.check_call([pip_path, "install"] + list(missing_packages))
    else:
        print("All dependencies are already installed.")


def activate_virtualenv(env_name="venv"):
    """Activate the virtual environment."""
    activate_script = (
        os.path.join(env_name, "Scripts", "activate")
        if os.name == "nt"
        else os.path.join(env_name, "bin", "activate")
    )
    print(
        f"To activate the virtual environment, run:\n source {activate_script}"
        if os.name != "nt"
        else f"To activate the virtual environment, run:\n {activate_script}"
    )
    print(f"To deactivate the virtual environment, run:\n deactivate")


if __name__ == "__main__":
    env_name = "venv"
    requirements_file = "requirements.txt"

    # Step 1: Create Virtual Environment
    create_virtualenv(env_name)

    # Step 2: Check and Install Dependencies
    check_and_install_dependencies(env_name, requirements_file)

    # Step 3: Notify User to Activate the Environment
    activate_virtualenv(env_name)

    print(
        "\nSetup is complete. You can now run your script using the virtual environment."
    )
