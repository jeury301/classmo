echo "Killing server..."
sudo lsof -t -i tcp:80 | xargs kill -9
