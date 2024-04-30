Linux deploy
sudo apt-get update
git clone https://github.com/Bachbui179/finalProject
sudo apt install python3-pip -y
sudo apt-get install python3-venv -y
python3 -m venv env
source env/bin/activate

sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
sudo apt install pkg-config
pip install mysqlclient

#go to files that contain manage.py
cd projectFinal 
python3 manage.py shell
  from django.core.management.utils import get_random_secret_key
  print(get_random_secret_key())
  exit()
  
#copy the secret key that generated 
#paste the key
export SECRET_KEY="your_secret_key_value"

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
