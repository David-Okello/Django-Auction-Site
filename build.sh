

# Ensure pip is installed
python3.9 -m ensurepip --upgrade

# Install Python dependencies
python3.9 -m pip install --upgrade pip
python3.9 -m pip install -r requirements.txt

# Run Django migrations
echo "Making Migrations ..."
python3.9 manage.py makemigrations --noinput
echo "Applying Migrations ..."
python3.9 manage.py migrate --noinput

# Collect static files
echo "Collecting Static Files ..."
python3.9 manage.py collectstatic --noinput --clear
