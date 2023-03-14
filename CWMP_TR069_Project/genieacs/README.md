## 1. Install node.js on Ubuntu(Only One Time)
--------------------------------------------------------------------------
	curl -sL https://deb.nodesource.com/setup_14.x -o nodesource_setup.sh
	sudo bash nodesource_setup.sh
	sudo apt install nodejs
	node -v

## 2. Install MongoDB on Ubuntu(Only One Time)
--------------------------------------------------------------------------

### 2.1 Install libssl1.1
	echo "deb http://security.ubuntu.com/ubuntu focal-security main" | sudo tee /etc/apt/sources.list.d/focal-security.list
	sudo apt-get update
	sudo apt-get install libssl1.1

### 2.2 Install MongoDB
	curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
	apt-key list
	echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
	sudo apt update
	sudo apt install mongodb-org
	sudo systemctl start mongod.service
	sudo systemctl status mongod
	sudo systemctl enable mongod
	mongo --eval 'db.runCommand({ connectionStatus: 1 })'

## 3. Install GenieACS on Ubuntu(Only One Time)
----------------------------------------------------------------------------------------
	http://docs.genieacs.com/en/latest/installation-guide.html#install-genieacs

	Warning:
		1) If 'sudo systemctl status genieacs-cwmp' not running and giving '/usr/bin/genieacs-cwmp' not found.
			then, execute $which genieacs-cwmp and change the 'ExecStart' path to '/usr/local/bin/genieacs-cwmp'
			Do, same for genieacs-nbi, genieacs-fs and genieacs-ui.
		2) Replace 'sudo chmod 600 /opt/genieacs/genieacs.env' to 'sudo chmod 666 /opt/genieacs/genieacs.env' before executing 				Generate a secure JWT secret command.
		3) Login in Window as http://<ubuntu-ip>:3000 and user as 'admin' and passwd as 'admin'
