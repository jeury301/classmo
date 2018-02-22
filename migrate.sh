# usage: ./migrate.sh
# note: you might need to modify permissions of the file
#   chmod 755 migrate.sh

echo "Starting migration process..."
python3 manage.py makemigrations schedules
python3 manage.py makemigrations discussions
python3 manage.py migrate
