"""
Configuration file for database connection.
Update these settings to match your PostgreSQL installation.
"""
import os

# Database configuration
# Update these values to match your PostgreSQL setup
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "rental_system"
DB_USER = "postgres"
DB_PASSWORD = "peacemaker360"  # Your PostgreSQL password

# Construct database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Alternative: You can also set these as environment variables
# DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
