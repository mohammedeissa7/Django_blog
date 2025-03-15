# Ec2 app Deployment

## ssh connection
**Set Permissions for the Key Pair File** :  `chmod 400 "temp-key.pem"`

**Connect to the Ec2 server using the ssh connection** : 
```bash
ssh -i "temp-key.pem" ec2-user@ec2-{your_IP}.compute-1.amazonaws.com
```

## Now you connect to your Amazon EC2 

- let's start using your server (Amazone Linux 2023) :

```bash
sudo bash 
cd
sudo apt-get update
```

- Setting The Hostname :
```bash
hostnamectl set-hostname {your_hostname}
nano /etc/hosts
```
You now in /etc/hosts : add *your instance* IP and *{your_hostname}* under *localhost* Then **ctrl+x** and **Y** and Enter

- Adding User :

```bash

sudo useradd -m <user_name>
sudo passwd <user_name>
sudo usermod -aG sudo <user_name>
su - <user_name>

```
- Use firewalld (Recommended ubuntu) : 
```bash
sudo apt update
sudo apt install ufw
sudo ufw status
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 8000/tcp
sudo ufw status numbered
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

Add  `os.path.join(BASE_DIR, 'static')`

**Then save the folder**

***Don't forget to allow 8000/tcp connections to your security group in your instance***

after that run your local server :


```bash
python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000
``` 
Access Your App Now : **http**://< public-ip-or-dns >:8000

- Let's install Apache : 

```bash
# Step 1: Update package list and install Apache
sudo apt update
sudo apt install apache2 -y

# Step 2: Start Apache
sudo systemctl start apache2

# Step 3: Enable Apache to start on boot
sudo systemctl enable apache2

# Step 4: Check Apache status
sudo systemctl status apache2
```
check if it  works  through https://< your_instance_ip >

-  Configure Apache for Django:

