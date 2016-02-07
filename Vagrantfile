#-*- mode: ruby -*-
#vi: set ft=ruby :

Vagrant.require_plugin 'vagrant-aws'
Vagrant.require_plugin 'vagrant-omnibus'


Vagrant.configure('2') do |config|
    config.vm.box = "dummy"
    config.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"
    config.vm.network "public_network"
    config.vm.network "private_network",ip: "192.168.56.10", virtualbox__intnet: "vboxnet0"
    config.vm.network "forwarded_port", guest: 80, host: 80
    config.vm.define "localhost" do |l|
            l.vm.hostname = "localhost"
    end

    config.vm.provider :aws do |aws, override|
        aws.access_key_id = "AKIAI2N4FSELVI4JUX5Q"
        aws.secret_access_key = "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"
        aws.keypair_name = "credenciales"
        aws.ami = "ami-5189a661"
        aws.region = "us-west-2"
        aws.security_groups = "default"
        aws.instance_type = "t2.micro"
        override.ssh.username = "ubuntu"
        override.ssh.private_key_path = "./credenciales.pem"
    end

    config.vm.provision "ansible" do |ansible|
        ansible.sudo = true
        ansible.playbook = "playbook.yml"
        ansible.verbose = "v"
        ansible.host_key_checking = false
  end
end
