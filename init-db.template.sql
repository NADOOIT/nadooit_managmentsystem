CREATE USER '{{MYSQL_USER}}'@'%' IDENTIFIED BY '{{MYSQL_PASSWORD}}';
ALTER USER '{{MYSQL_USER}}'@'%' IDENTIFIED WITH mysql_native_password BY '{{MYSQL_PASSWORD}}';
GRANT ALL PRIVILEGES ON {{MYSQL_DATABASE}}.* TO '{{MYSQL_USER}}'@'%';
FLUSH PRIVILEGES;
