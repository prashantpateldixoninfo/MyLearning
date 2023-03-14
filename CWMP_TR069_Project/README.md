### Install the genieacs server from 
--------------------------------------------------
https://github.com/genieacs/genieacs

### Dowload the genieacs-sim and execute
=============================================
Configuration of GeniesACS-SIM for GENIEACS
=============================================
git clone https://github.com/genieacs/genieacs-sim
./genieacs-sim -s 654321 -u "http://192.168.1.8:7547"


### Run the openWRT with TR-069
=============================================
Configuration of EasyCWMP for GENIEACS
==========================================
uci show easycwmp
uci set easycwmp.@acs[0].url='http://192.168.1.8:7547'
uci set easycwmp.@acs[0].username='admin'
uci set easycwmp.@acs[0].password='admin'
uci commit
uci show easycwmp
/etc/init.d/easycwmpd start


### Document of TR-069 
https://cwmp-data-models.broadband-forum.org/
