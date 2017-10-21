Ansible Deployment Script
=========================

The deployment scripts are great and all, but they still left me `ssh`ing in a
lot to tweak things. However, if I (the tweaker-in-chief) disappear,
administrators still need to make changes to the site, so I wrote this Ansible
script to take care of that.

 1. In the AWS console, create an Amazon EC2 medium instance with [Debian
    Stretch][1]. I gave it 32GiB of storage.
 2. Still in the AWS console, edit the security group to open up TCP ports 80
    and 443.
 3. Save the ssh key for the instance to `~/.ssh/id_rsa_ghu` or whatever.
    `chmod` it to 600 or something decent, and then add the following to
    `~/.ssh/config`:

        Host ghu
            User admin
            HostName IP_ADDRESS_HERE
            Port 22
            IdentityFile ~/.ssh/id_rsa_ghu
            IdentitiesOnly yes

 4. Now you should be able to ssh into the machine with `ssh ghu`, so create a
    modest inventory file `hosts` with one line: `ghu`:

        $ printf 'ghu\n' >hosts

 5. Finally, you can run the playbook with:

        $ ansible-playbook --ask-vault-pass -i hosts ghu.yml

    If you don't have the vault password, you can generate a new vault by
    deleting `secrets.yml` and creating another by running `ansible-vault
    create secrets.yml`, and then adding the following contents to the vault:

        vault_postgresql_password: POSTGRES_PASSWORD_HERE

 6. Set up Jenkins

You can re-run `ansible-playbook` with the command line shown above whenever
you want to update stuff on the server.

[1]: https://wiki.debian.org/Cloud/AmazonEC2Image
