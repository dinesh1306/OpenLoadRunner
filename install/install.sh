#! /bin/bash
PARENT_DIR=../../
yum install python3
pip3 install pyinstaller
/usr/local/bin/pyinstaller ../cmds/load_runner
cp build/load_runner/load_runner /usr/bin/
load_runner_dir=
if [ -d /var/spool/LoadRunner ]
then
	old_dir=old_LoadRunner$(date +"%m%d%Y")
	echo "Moving old directory to ${old_dir}"
	mv /var/spool/LoadRunner /var/spool/${old_dir}
else
	echo "Load runner directory not exists"
	echo "creating LoadRunner directory ..."
	mkdir /var/spool/LoadRunner
fi

svr_name=mysqld
svr_cmd=$(which service)
service ${svr_name} start
if [ $? -eq 0 ]
then
	echo "$svr_name started successfully"
else
	echo "failed to start $svr_name"
fi 

# Creating user and password for mysql database
echo "### Please provide mysql database password"
read password

echo "### Mysql password is ${password}"
mysql_cnf="$(cat <<-EOF
[client]
user = root
password = ${password}
EOF
)"

if [ -f ~/.my.cnf ]
then
	echo "Mysql configuration file already present."
	echo "Not creating Mysql configuration file."
else
	echo "Mysql configuration file not present."
	echo "Creating Mysql configuration file."
	echo "${mysql_cnf}" > ~/.my.cnf
	service ${svr_name} restart
fi
