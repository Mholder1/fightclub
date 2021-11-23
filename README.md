# Try out fightclub

Try out this website for yourself through my server on AWS Elastic Beanstalk by following the link below

http://fightclub-env-1.eba-ippz5yfc.eu-west-2.elasticbeanstalk.com/

# To Debug in VS Code

In terminal window

sudo apt-get install libffi-dev

python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install flask
pip install flask_restful

pip3 install psycopg2
or
python -m pip install psycopg2

In VS Code
Ctrl Shift P - select python interpreter (venv one)
Run - Start Debugging - Flask - fightclub_api.py
In Browser go to http://127.0.0.1:5000/
