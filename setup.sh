#!/bin/bash

# Install required packages
sudo apt-get update
sudo apt-get install -y git curl apt-transport-https ca-certificates gnupg-agent software-properties-common gettext-base

# Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Copy the .env.example file to .env
cp .env.example .env

# Enable memory overcommit
if ! grep -q "vm.overcommit_memory = 1" /etc/sysctl.conf; then
  echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf
fi

# Apply the changes without rebooting
sudo sysctl -p

echo "Server setup complete."

# Funktion zur Überprüfung und Bereinigung der Eingabe
clean_input() {
  echo "$1" | sed -e 's/[\/&|]/-/g' -e 's/!/\\!/g'
}
echo "Do you want to add the info for the .env file now? (Y/n)"
read answer
if [[ "$answer" =~ ^([yY][eE][sS]|[yY])*$ ]]; then
  read -p "DJANGO_SECRET_KEY: " django_secret_key
  echo "Enter your domain (e.g., nadooit.de) without HTTPS or WWW:"
  read -p "DOMAIN: " domain
  read -p "ACME_DEFAULT_EMAIL: " acme_default_email
  read -p "MYSQL_ROOT_PASSWORD: " mysql_root_password
  read -p "MYSQL_DATABASE: " mysql_database
  read -p "MYSQL_USER: " mysql_user
  read -p "MYSQL_PASSWORD: " mysql_password

  # Clean inputs
  django_secret_key=$(clean_input "$django_secret_key")
  domain=$(clean_input "$domain")
  acme_default_email=$(clean_input "$acme_default_email")
  mysql_root_password=$(clean_input "$mysql_root_password")
  mysql_database=$(clean_input "$mysql_database")
  mysql_user=$(clean_input "$mysql_user")
  mysql_password=$(clean_input "$mysql_password")

  # Prepare environment variables for init-db.sql generation
  export MYSQL_ROOT_PASSWORD MYSQL_DATABASE MYSQL_USER MYSQL_PASSWORD

  # Generate init-db.sql from template
  envsubst < init-db.template.sql > ./init-db.sql

  # Automatically add https:// to the domain for DJANGO_CSRF_TRUSTED_ORIGINS and include both root and www
  DJANGO_CSRF_TRUSTED_ORIGINS="https://$domain,https://www.$domain"

  # Update .env with MySQL and other environment variables
  sed -i "s/DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=$django_secret_key/" .env
  sed -i "s/DJANGO_CSRF_TRUSTED_ORIGINS=.*/DJANGO_CSRF_TRUSTED_ORIGINS=\"$DJANGO_CSRF_TRUSTED_ORIGINS\"/" .env
  sed -i "s/ACME_DEFAULT_EMAIL=.*/ACME_DEFAULT_EMAIL=$acme_default_email/" .env
  sed -i "s/MYSQL_ROOT_PASSWORD=.*/MYSQL_ROOT_PASSWORD=$mysql_root_password/" .env
  sed -i "s/MYSQL_DATABASE=.*/MYSQL_DATABASE=$mysql_database/" .env
  sed -i "s/MYSQL_USER=.*/MYSQL_USER=$mysql_user/" .env
  sed -i "s/MYSQL_PASSWORD=.*/MYSQL_PASSWORD=$mysql_password/" .env
  sed -i "s/DJANGO_DEBUG=1/DJANGO_DEBUG=0/" .env


  echo "Building the Docker images..."
  docker-compose -f docker-compose-deploy.yml build
  docker-compose -f docker-compose-deploy.yml up -d

  # Wait for MySQL to initialize (consider a smarter wait mechanism)
  echo "Waiting for MySQL to initialize..."
  sleep 30 # Adjust the sleep time as necessary

  # Cleanup init-db.sql after MySQL has started and executed the file
  #rm -f ./init-db.sql
  echo "init-db.sql has been removed for security."

  echo "Running migrations..."
  docker-compose -f docker-compose-deploy.yml run --rm app python manage.py migrate

  echo "Creating superuser..."
  docker-compose -f docker-compose-deploy.yml run --rm app python manage.py createsuperuser

  echo "Starting the server..."
  docker-compose -f docker-compose-deploy.yml up -d
fi

echo "The .env file has been updated with the provided information."
echo "If you chose not to update the .env file, follow the setup instructions in the documentation."

# Ask if a cron job for SSL certificate renewal should be added
echo "Do you want to add a cron job for automatic SSL certificate renewal with Let's Encrypt? (Y/n)"
read add_cron
if [[ "$add_cron" =~ ^([yY][eE][sS]|[yY])*$ ]]; then
  # Add Certbot PPA
  sudo add-apt-repository ppa:certbot/certbot
  sudo apt-get update
  # Install Certbot
  sudo apt-get install -y certbot
  # Setup cron job
  (crontab -l 2>/dev/null; echo "0 3 * * * /usr/bin/docker-compose -f $HOME/NADOO-IT/docker-compose-deploy.yml run --rm certbot renew --quiet && /usr/bin/docker-compose -f $HOME/NADOO-IT/docker-compose-deploy.yml restart nginx") | crontab -
  echo "Cron job for SSL certificate renewal has been added."
fi

echo "Setup completed."
