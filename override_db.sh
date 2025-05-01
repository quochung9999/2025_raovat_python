#!/bin/bash

# Set database credentials for restore
export PGDATABASE="raovat_db"
export PGUSER="raovat_user"
export PGPASSWORD="cn2025_Hung@@"
# Set database host and port (modify if needed)
export PGHOST="localhost" # Replace with remote host if necessary
export PGPORT="5432" # Replace with remote port if necessary

# Set the dump file to restore from
DUMP_FILE="dbdump/raovat_db_20250501_001519.sql"

# Check if the dump file exists
if [ ! -f "$DUMP_FILE" ]; then
  echo "Error: Dump file $DUMP_FILE not found."
  exit 1
fi

# Use postgres user for dropping and creating database
export PGUSER="postgres"
export PGPASSWORD="temp_password" # Temporary password set by the model

# Drop the existing database
echo "Dropping existing database $PGDATABASE..."
dropdb -h $PGHOST -p $PGPORT -U $PGUSER $PGDATABASE

# Create a new database
echo "Creating new database $PGDATABASE..."
createdb -h $PGHOST -p $PGPORT -U $PGUSER $PGDATABASE

# Restore the database using postgres user
echo "Restoring database from $DUMP_FILE using postgres user..."
pg_restore -v -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE "$DUMP_FILE"

# Check if the restore was successful
if [ $? -eq 0 ]; then
  echo "Database restore successful from $DUMP_FILE"
else
  echo "Database restore failed."
  exit 1
fi

# Change ownership of tables in public schema to raovat_user
echo "Changing ownership of tables in public schema to raovat_user..."
sudo -u postgres psql -d $PGDATABASE -c "SELECT 'ALTER TABLE public.' || tablename || ' OWNER TO raovat_user;' FROM pg_tables WHERE schemaname = 'public';" | grep '^ALTER ' | sudo -u postgres psql -d $PGDATABASE

# Change ownership of sequences in public schema to raovat_user
echo "Changing ownership of sequences in public schema to raovat_user..."
sudo -u postgres psql -d $PGDATABASE -c "SELECT 'ALTER SEQUENCE public.' || sequencename || ' OWNER TO raovat_user;' FROM pg_sequences WHERE schemaname = 'public';" | grep '^ALTER ' | sudo -u postgres psql -d $PGDATABASE
