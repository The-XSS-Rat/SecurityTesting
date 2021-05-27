#!/bin/bash
echo "Enter the user name: "  
read userName 

mkdir /home/$userName
chmod 767 /home/$userName/

sudo useradd -g Commands -d /home/$userName $userName
echo "$userName ALL=(ALL) NOPASSWD:/usr/bin/apt-get install *" >> /etc/sudoers

echo -e "test\ntest\n" | passwd $userName > /dev/null 2>&1 && echo " User account has been created." || echo " ERR -- User account creation failed!"

echo "ssh $userName@45.79.218.21 - password is 'test' please change it ASAP"
