# ALYVON Rental Management System

A desktop application for managing rental items, customers, and transactions using Python, PostgreSQL, and Tkinter.

## Features

- **Dashboard**: Overview of total items, customers, and active rentals
- **Rental Management**: Create new rentals with customer and item selection
- **Inventory Management**: View and manage rental items
- **Customer Management**: View customer information
- **Reports**: Track active rentals and mark items as returned

## Prerequisites

1. **Python 3.7+** - Download from [python.org](https://python.org)
2. **PostgreSQL** - Download from [postgresql.org](https://postgresql.org)
3. **Tkinter** - Usually comes with Python

## Installation Steps

### 1. Install PostgreSQL

1. Download and install PostgreSQL from [postgresql.org](https://postgresql.org)
2. During installation, set a password for the 'postgres' user (remember this password)
3. Make sure PostgreSQL service is running

### 2. Install Python Dependencies

Open Command Prompt or PowerShell in the project directory and run:

```bash
pip install -r requirements.txt
```

### 3. Setup Database

Run the database setup script:

```bash
python setup_database.py
```

This will:
- Create the 'rental_system' database
- Create all necessary tables
- Add sample rental items

### 4. Run the Application

```bash
python rental_manager.py
```

## Database Configuration

The application connects to PostgreSQL using these default settings:
- Host: localhost
- Port: 5432
- Database: rental_system
- Username: postgres
- Password: password

To change these settings, edit the `DATABASE_URL` in `database.py`.

## Usage

### Creating a New Rental

1. Go to the "New Rental" tab
2. Enter customer information (name and phone)
3. Select an item from the dropdown
4. Enter quantity and number of rental days
5. Click "Create Rental"

### Managing Inventory

1. Go to the "Inventory" tab to view all items
2. Click "Add New Item" to add new rental items
3. View available quantities for each item

### Viewing Reports

1. Go to the "Reports" tab to see active rentals
2. Select a rental and click "Mark as Returned" when items are returned

## Sample Data

The system comes with sample rental items:
- Chairs (50 available) - $5.00/day
- Tables (20 available) - $15.00/day
- Projectors (10 available) - $25.00/day
- Sound Systems (5 available) - $30.00/day

## Troubleshooting

### Database Connection Issues
- Make sure PostgreSQL is running
- Check that the password is correct
- Verify the database was created successfully

### Application Won't Start
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Make sure Python and Tkinter are properly installed

### Permission Issues
- Run Command Prompt as Administrator if needed

## Support

If you encounter any issues, check:
1. PostgreSQL is running and accessible
2. All Python dependencies are installed
3. Database was created successfully
4. Python and Tkinter are working properly
