# SQLite to PostgreSQL Migration Plan

This document outlines the detailed steps to migrate your Django application from SQLite to PostgreSQL.

## 1. Install PostgreSQL

First, install PostgreSQL and its dependencies:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Verify the installation:

```bash
sudo systemctl status postgresql
```

## 2. Create PostgreSQL Database and User

Create a database and user for your Django application:

```bash
# Connect to PostgreSQL as the postgres user
sudo -u postgres psql

# Create database and user (run these commands in the PostgreSQL shell)
CREATE DATABASE raovat_db;
CREATE USER raovat_user WITH PASSWORD 'your_secure_password';

# Set encoding, isolation level, and timezone
ALTER ROLE raovat_user SET client_encoding TO 'utf8';
ALTER ROLE raovat_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE raovat_user SET timezone TO 'UTC';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE raovat_db TO raovat_user;

# Exit PostgreSQL shell
\q
```

## 3. Install PostgreSQL Adapter for Python

Install the PostgreSQL adapter in your virtual environment:

```bash
cd /var/www/2025_raovat_python
source venv/bin/activate
pip install psycopg2-binary
```

## 4. Update Django Settings

Modify the `settings.py` file to use PostgreSQL instead of SQLite:

```python
# Before (SQLite configuration)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# After (PostgreSQL configuration)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'raovat_db',
        'USER': 'raovat_user',
        'PASSWORD': 'your_secure_password',  # Use a strong password
        'HOST': 'localhost',
        'PORT': '',  # Leave empty to use default port (5432)
    }
}
```

## 5. Migrate Data from SQLite to PostgreSQL

There are two main approaches to migrate the data:

### Option 1: Using Django's dumpdata and loaddata commands

This approach uses Django's built-in tools to export data from SQLite and import it into PostgreSQL:

```bash
# Activate virtual environment
cd /var/www/2025_raovat_python
source venv/bin/activate

# Create a backup of your SQLite database
cp db.sqlite3 db.sqlite3.backup

# Dump data from SQLite (excluding contenttypes and permissions to avoid conflicts)
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data_dump.json

# Update settings.py to use PostgreSQL (as shown above)

# Apply migrations to the new PostgreSQL database
python manage.py migrate

# Load the dumped data into PostgreSQL
python manage.py loaddata data_dump.json

# Create a superuser if needed
python manage.py createsuperuser
```

### Option 2: Using pgloader (a specialized migration tool)

pgloader is a tool specifically designed for database migrations:

```bash
# Install pgloader
sudo apt install pgloader

# Run the migration (adjust paths as needed)
pgloader sqlite:///var/www/2025_raovat_python/db.sqlite3 postgresql://raovat_user:your_secure_password@localhost/raovat_db
```

## 6. Verify the Migration

After migrating the data, verify that everything was transferred correctly:

```bash
# Connect to PostgreSQL
sudo -u postgres psql -d raovat_db

# List tables
\dt

# Check row counts for important tables (adjust table names as needed)
SELECT COUNT(*) FROM auth_user;
SELECT COUNT(*) FROM listings_listing;  # Adjust table name based on your model

# Exit PostgreSQL shell
\q
```

## 7. Update Application Configuration

Restart the Gunicorn service to apply the changes:

```bash
sudo systemctl restart gunicorn_raovat
```

## 8. Test the Application

Access the application through the browser or using curl to verify it's working correctly with PostgreSQL:

```bash
curl http://45.56.68.95
```

Check that:
- The homepage loads correctly
- You can log in with existing credentials
- All listings and data are present
- You can create new listings

## 9. Backup Strategy for PostgreSQL

Set up regular backups for your PostgreSQL database:

```bash
# Create a backup script
cat > /var/www/backup_db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/www/db_backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p $BACKUP_DIR
pg_dump -U raovat_user -d raovat_db -h localhost -F c -f $BACKUP_DIR/raovat_db_$TIMESTAMP.dump
find $BACKUP_DIR -type f -mtime +7 -name "*.dump" -delete
EOF

# Make the script executable
chmod +x /var/www/backup_db.sh

# Set up a cron job to run daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /var/www/backup_db.sh") | crontab -
```

## 10. Troubleshooting

If you encounter issues during or after the migration:

1. **Database Connection Issues**:
   - Check PostgreSQL is running: `sudo systemctl status postgresql`
   - Verify connection settings in `settings.py`
   - Ensure the PostgreSQL user has proper permissions

2. **Missing Data**:
   - Compare record counts between SQLite and PostgreSQL
   - Check for errors in the migration logs

3. **Application Errors**:
   - Check Gunicorn logs: `sudo journalctl -u gunicorn_raovat`
   - Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`

## Benefits of PostgreSQL over SQLite

This migration provides several advantages:

1. **Concurrency**: PostgreSQL handles multiple simultaneous connections much better than SQLite
2. **Performance**: Better performance for larger datasets and complex queries
3. **Scalability**: Can handle growing data and user loads
4. **Advanced Features**: Full-text search, JSON support, and many other advanced features
5. **Reliability**: Better data integrity and crash recovery
6. **Security**: More robust user authentication and authorization options

## Rollback Plan

If you need to revert to SQLite:

1. Restore the original SQLite database:
   ```bash
   cp db.sqlite3.backup db.sqlite3
   ```

2. Revert the changes in `settings.py` to use SQLite again

3. Restart the Gunicorn service:
   ```bash
   sudo systemctl restart gunicorn_raovat