# This script perform the following action:
# - It run makemigrations by calling migrate.sh
# - It cleans up the database (optional)
# - It creates the groups neccesary for classmo i.e.:Students, Instructors
# - It create an admin account with credentials: admin:12345
# - It loads the db with initial data:
#   - Initial Subjects
#   - Initial Locations
#   - Initial Instructors
#   - Initial Sessions
#   - Initial Discussion
#
# Last updated on: 03/31/18

# running make migrations
./migrate.sh

# cleaning up db (optional)
./clean_db.sh

# run script to create groups
cat setup_scripts/group_creation.py | python3 manage.py shell

# run script to create an admin account
cat setup_scripts/super_user_creation.py | python3 manage.py shell

# run script to create initial data
cat setup_scripts/test_data_creation_yoga.py | python3 manage.py shell

