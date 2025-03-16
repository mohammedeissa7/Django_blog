# Ec2 app Deployment

## ssh connection
**Set Permissions for the Key Pair File** :  `chmod 400 "temp-key.pem"`

**Connect to the Ec2 server using the ssh connection** : 
```bash
ssh -i "temp-key.pem" ec2-user@ec2-{your_IP}.compute-1.amazonaws.com
```

## Now you connect to your Amazon EC2 

- let's start using your server (ubuntu 2022) :

```bash
sudo ufw app list 
sudo ufw allow OpenSSH 
sudo ufw enable
sudo ufw status
sudo apt update
sudo apt install python3-venv python3-dev libpq-dev nginx curl virtualenv
```

- Move your App folder from your pc To the Ec2 instance :  
```bash
scp -i "temp-key.pem" -r "{your_dir}" ec2-user@{your_IP}.compute-1.amazonaws.com:~/Django_blog
```
And you will find your  project in **/home/ec2-user/{your_dir_name}**

And if you want to Find It yourself use this command to create `sudo find / -name "your_dir_name"`

- Python setup :
```bash
sudo apt install python3 python3-pip -y
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
```
now we will open settings.py to update the app settings:

`nano settings.py`

change ` ALLOWED_HOST = ['instance_IP']`

**recommend** : Make an elastic ip address because when you stop the instance and restart it will change the ip address


Add  `os.path.join(BASE_DIR, 'static')`

**Then save the folder**

***Don't forget to allow 8000/tcp connections to your security group in your instance***

after that run your local server :


```bash
python manage.py collectstatic
sudo ufw allow 8000
python manage.py runserver 0.0.0.0:8000
``` 
Access Your App Now : **http**://< public-ip-or-dns >:8000

Then run `deactivate`

- Let's install Gunicorn : 

```bash
sudo nano /etc/systemd/system/gunicorn.socket
```
Now you are in `/etc/systemd/system/gunicorn.socket`
```vim
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```vim
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/django_blog
ExecStart=/home/ubuntu/django_blog/env/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    django_blog.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
file /run/gunicorn.sock
sudo journalctl -u gunicorn.socket
curl --unix-socket /run/gunicorn.sock localhost
sudo systemctl status gunicorn
sudo systemctl deamon-reload
sudo systemctl restart gunicorn
```

- let's install nginx :

```bash
sudo nano /etc/nginx/sites-enabled/djangoblog
```

inside `/etc/nginx/sites-enabled/djangoblog` :

```vim
server {
    listen 80;
    server_name your_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/django_blog;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
**enable the site** :

```bash
sudo ln -s /etc/nginx/sites-available/djangoblog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```
## Access Your App Now : **http**://< public-ip-or-dns >
Now your application is running on ec2 but without css file 
to get access toi them 
```bash
sudo nano /etc/nginx/nginx.conf
``` 
and finally you will replace the user to Ubuntu

```bash
sudo systemctl restart nginx
```

## NOW WE HAVE THE SITE CORRECT ON EC2  >_<




