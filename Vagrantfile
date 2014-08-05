# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

SHELL = "#!/bin/bash
apt-get install -y --force-yes libblas-dev liblapack-dev gfortran
apt-get install -y --force-yes python3-pip python3-dev python3-scipy
(
	cd /wordgraph
	pip3 install distutils
	pip3 install -r requirements.txt
)

echo -e 'Done.\nRun `vagrant ssh` to get into the machine.\nThis directory is
mounted at /wordgraph. Run `sudo python3 setup.py install`.'
"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder ".", "/wordgraph"

  config.vm.provision :shell do |shell|
	shell.inline = SHELL
  end
end
