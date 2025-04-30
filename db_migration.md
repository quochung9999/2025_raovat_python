# Database Setup and Superuser Creation for Classifieds Project

This document provides instructions for setting up the PostgreSQL database and creating a superuser account for the Classifieds Django project. These steps assume PostgreSQL is already installed on the system.

## 1. Install PostgreSQL and Dependencies

If PostgreSQL is not already installed, follow the instructions in the existing `postgresql_migration_plan.md` file to install it.

## 2. Create PostgreSQL Database and User

Execute the following commands in your terminal to create the database and user with the necessary privileges. You may need to enter your system password when prompted for `sudo`.

```bash
sudo -u postgres psql -c "CREATE DATABASE raovat_db;"
sudo -u postgres psql -c "CREATE USER raovat_user WITH PASSWORD 'cn2025_Hung@@';"
sudo -u postgres psql -c "ALTER ROLE raovat_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE raovat_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE raovat_user SET timezone TO 'UTC';"
sudo -u postgres psql -d raovat_db -c "GRANT ALL PRIVILEGES ON DATABASE raovat_db TO raovat_user;"
sudo -u postgres psql -d raovat_db -c "GRANT CREATE ON SCHEMA public TO raovat_user;"
```

**Note:** Use `'cn2025_Hung@@'` as the password for the `raovat_user`.

## 3. Install PostgreSQL Adapter

Navigate to your project's root directory (`/home/aaa/Documents/Linode_local/2025_raovat_python`) and install the `psycopg2-binary` package within your Python virtual environment:

```bash
cd /home/aaa/Documents/Linode_local/2025_raovat_python
# Activate your virtual environment if you are using one
# source venv/bin/activate # Example activation command
pip install psycopg2-binary
```

## 4. Update Django Settings

Ensure your `classified_project/settings.py` file is configured to use the PostgreSQL database with the credentials you set in Step 2. The `DATABASES` setting should look like this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'raovat_db',
        'USER': 'raovat_user',
        'PASSWORD': 'cn2025_Hung@@',  # Use the password you set
        'HOST': 'localhost',
        'PORT': '',  # Leave empty to use default port (5432)
    }
}
```

**Note:** Make sure the `PASSWORD` value matches the password you set for `raovat_user` in Step 2.

## 5. Apply Database Migrations

From the project's root directory, run the following command to apply the database migrations:

```bash
cd /home/aaa/Documents/Linode_local/2025_raovat_python
python3 manage.py migrate
```

## 6. Create Superuser Account

To create a superuser account for accessing the Django admin site and having full privileges, run the following command:

```bash
cd /home/aaa/Documents/Linode_local/2025_raovat_python
python3 manage.py createsuperuser
```

Follow the prompts to enter a username, email address, and password for the superuser.

**Note:** A superuser account was created with the following credentials:
- Username: `kevin9999`
- Email: `kevinle224466@gmail.com`
- Password: `Hung889900@@`

To create another superuser, run the `python3 manage.py createsuperuser` command again and use the following credentials:
- Username: `quochung9999`
- Email: `quochung9999@gmail.com`
- Password: `Hung889900@@`

After completing these steps, your project should be connected to the PostgreSQL database, and you will have superuser accounts to manage the application.
