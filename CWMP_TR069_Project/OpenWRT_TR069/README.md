### Compiling, Building and Deploying TR069 with OpenWRT
-------------------------------------------------------------------------------
	1) git clone https://github.com/openwrt/openwrt openwrt_tr069
	2) cd openwrt_tr069
	3) sudo apt install binutils bzip2 diff find flex gawk gcc-6+ getopt grep install libc-dev libz-dev make4.1+ perl python3.6+ rsync subversion unzip which
	4) ./scripts/feeds update -a
	5) ./scripts/feeds install -a
	6) Copy the easycwmp.zip file into package/ folder and unzip it as $ unzip easycwmp.zip
	7) Copy the libmicroxml.zip file into package/libs folder and unzip it as $ unzip libmicroxml.zip
	8) make menuconfig
		--> Select target as X86
		--> Select all Luci Themes
		--> Select easycwmp under Utilties Menu
		--> Select libmicroxml under Librairies
		--> Save and Exit
	9) make -j1 V=s
	10) You will get compilation error during linking.
		Please compare cwmp.h, cwmp.c and xml.c file and merge the changes at build_dir/target-i386_pentium4_musl/easycwmp/easycwmp-1.8.6/src/
	Note: Prerequisite files needed during compilation: easycwmp.zip, libmicroxml.zip, cwmp.h, cwmp.c and xml.c
	11) Deploy the openWRT image in VBox and Change the N/W setting as Host Only Adapter and Bridge Adapter
----------------------------------------------------------------------------------------------------------------

### Run the openWRT with TR-069 and Configure EasyCWMP for genieacs server
------------------------------------------------------------------------------
	uci show easycwmp
	uci set easycwmp.@acs[0].url='http://192.168.1.8:7547'
	uci set easycwmp.@acs[0].username='admin'
	uci set easycwmp.@acs[0].password='admin'
	uci commit
	uci show easycwmp
	/etc/init.d/easycwmpd start

