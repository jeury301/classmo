# running make migrations
./migrate.sh

# run script to create groups
cat setup_scripts/group_creation.py | python3 manage.py shell

# run script to create an admin account
cat setup_scripts/super_user_creation.py | python3 manage.py shell
