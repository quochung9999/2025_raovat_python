#!/bin/bash

# Create dbdump directory if it doesn't exist
mkdir -p dbdump

# Set database credentials
export PGDATABASE="raovat_db"
export PGUSER="raovat_user"
export PGPASSWORD="cn2025_Hung@@"
# Set database host and port (modify if needed)
export PGHOST="localhost" # Replace with remote host if necessary
export PGPORT="5432" # Replace with remote port if necessary

# Generate timestamp for filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DUMP_FILE="dbdump/raovat_db_${TIMESTAMP}.sql"

# Dump the database
pg_dump -Fc -v -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE > "$DUMP_FILE"

# Check if the dump was successful
if [ $? -eq 0 ]; then
  echo "Database dump successful. Saved to $DUMP_FILE"
else
  echo "Database dump failed."
  exit 1
fi
