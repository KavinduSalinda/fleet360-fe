#!/usr/bin/env python
"""
Setup script for Fleet360 Django project
"""

import os
import sys
import subprocess


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e.stderr}")
        return False


def main():
    print("Fleet360 Django Project Setup")
    print("=" * 40)
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("\nCreating virtual environment...")
        if not run_command('python -m venv venv', 'Virtual environment creation'):
            sys.exit(1)
    
    # Activate virtual environment and install requirements
    if os.name == 'nt':  # Windows
        activate_cmd = 'venv\\Scripts\\activate'
        pip_cmd = 'venv\\Scripts\\pip'
        python_cmd = 'venv\\Scripts\\python'
    else:  # Unix/Linux/Mac
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
        python_cmd = 'venv/bin/python'
    
    # Install requirements
    if not run_command(f'{pip_cmd} install -r requirements.txt', 'Installing requirements'):
        sys.exit(1)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\nCreating .env file from template...")
        if os.path.exists('env.example'):
            import shutil
            shutil.copy('env.example', '.env')
            print("✓ .env file created from env.example")
            print("⚠️  Please edit .env file with your database credentials")
        else:
            print("✗ env.example file not found")
    
    # Run migrations
    if not run_command(f'{python_cmd} manage.py makemigrations', 'Creating migrations'):
        sys.exit(1)
    
    if not run_command(f'{python_cmd} manage.py migrate', 'Running migrations'):
        sys.exit(1)
    
    # Populate initial data
    if not run_command(f'{python_cmd} manage.py populate_data', 'Populating initial data'):
        print("⚠️  Initial data population failed, but continuing...")
    
    print("\n" + "=" * 40)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your MySQL database credentials")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Run the development server: python manage.py runserver")
    print("4. Access admin interface at: http://localhost:8000/admin/")
    print("5. API endpoints are available at: http://localhost:8000/api/")


if __name__ == '__main__':
    main()
