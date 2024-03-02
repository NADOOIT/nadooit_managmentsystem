#!/bin/bash

# Install required packages
sudo apt-get update
sudo apt-get install -y git curl apt-transport-https ca-certificates gnupg-agent software-properties-common

# Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone the repository
git clone git@github.com:NADOOIT/NADOO-IT.git

# Change to the project directory
cd NADOO-IT

# Copy the .env.example file to .env
cp .env.example .env

# Enable memory overcommit
if ! grep -q "vm.overcommit_memory = 1" /etc/sysctl.conf; then
  echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf
fi

# Apply the changes without rebooting
sudo sysctl -p

echo "Server setup complete."

echo "Do you want to add the info for the .env file now? (y/n)"
read answer
if [ "$answer" = "y" ]; then
  read -p "DJANGO_SECRET_KEY: " django_secret_key
  read -p "DOMAIN (for DJANGO_CSRF_TRUSTED_ORIGINS): " domain
  read -p "ACME_DEFAUT_EMAIL: " acme_default_email
  # Removed the CockroachDB setup as we're focusing on MySQL
  read -p "MYSQL_ROOT_PASSWORD: " mysql_root_password
  read -p "MYSQL_DATABASE: " mysql_database
  read -p "MYSQL_USER: " mysql_user
  read -p "MYSQL_PASSWORD: " mysql_password
  read -p "NADOOIT__API_KEY: " nadooit_api_key
  read -p "NADOOIT__USER_CODE: " nadooit_user_code

  # Update .env with MySQL and other environment variables
  sed -i "s/your_secret_key/$django_secret_key/" .env
  sed -i "s/your_domain/$domain/" .env
  sed -i "s/your_email/$acme_default_email/" .env
  sed -i "s/MYSQL_ROOT_PASSWORD/$mysql_root_password/" .env
  sed -i "s/MYSQL_DATABASE/$mysql_database/" .env
  sed -i "s/MYSQL_USER/$mysql_user/" .env
  sed -i "s/MYSQL_PASSWORD/$mysql_password/" .env
  sed -i "s/your_nadooit_api_key/$nadooit_api_key/" .env
  sed -i "s/your_nadooit_user_code/$nadooit_user_code/" .env
  sed -i "s/DJANGO_DEBUG=1/DJANGO_DEBUG=0/" .env
  
  echo "Building the Docker images..."
  docker-compose -f docker-compose.deploy.yml build
  docker-compose -f docker-compose.deploy.yml run --rm certbot /opt/certify-init.sh

  echo "Running migrations..."
  docker-compose -f docker-compose.deploy.yml run --rm app python manage.py migrate

  echo "Creating superuser..."
  docker-compose -f docker-compose.deploy.yml run --rm app python manage.py createsuperuser

  echo "Starting the server..."
  docker-compose -f docker-compose.deploy.yml up -d
fi

echo "The .env file has been updated with the provided information."
echo "If you chose not to update the .env file, follow the setup instructions in the documentation."
