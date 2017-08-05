FLAWLESS ODOO SETUP GUIDE
=========================

The following guide was summarized from;

https://www.linode.com/docs/websites/cms/install-odoo-10-on-ubuntu-16-04

Update Server
-------------
.. code-block::

    sudo apt update && sudo apt upgrade

Configure Firewall for odoo port
--------------------------------

.. code-block::

    sudo ufw allow ssh
    sudo ufw allow 8069/tcp
    sudo ufw enable

Install postgreSQL database and other dependencies
--------------------------------------------------

.. code-block::

    sudo apt-get install git python-pip postgresql postgresql-server-dev-9.5 python-all-dev python-dev python-setuptools libxml2-dev libxslt1-dev libevent-dev libsasl2-dev libldap2-dev pkg-config libtiff5-dev libjpeg8-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev liblcms2-utils libwebp-dev tcl8.6-dev tk8.6-dev python-tk libyaml-dev fontconfig

Configure postgres user
-----------------------

.. code-block::

    sudo su - postgres
    createuser odoo -U postgres -dRSP

Make ODOO user, configure log location and clone odoo
------------------------------------------------------

.. code-block::

    sudo adduser --system --home=/opt/odoo --group odoo
    sudo mkdir /var/log/odoo
    sudo git clone https://www.github.com/odoo/odoo --depth 1 --branch 10.0 --single-branch /opt/odoo

Install Odoo's Python dependencies
----------------------------------

.. code-block::

    sudo pip install -r /opt/odoo/doc/requirements.txt
    sudo pip install -r /opt/odoo/requirements.txt

Install Less CSS via nodejs and npm
-----------------------------------

.. code-block::

    sudo curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
    sudo apt install -y nodejs
    sudo npm install -g less less-plugin-clean-css


Install Stable Wkhtmltopdf Version
----------------------------------
.. code-block::

    cd /tmp
    sudo wget https://downloads.wkhtmltopdf.org/0.12/0.12.1/wkhtmltox-0.12.1_linux-trusty-amd64.deb
    sudo dpkg -i wkhtmltox-0.12.1_linux-trusty-amd64.deb
    sudo cp /usr/local/bin/wkhtmltopdf /usr/bin
    sudo cp /usr/local/bin/wkhtmltoimage /usr/bin

Odoo Server Configuration
-------------------------

.. code-block::

    sudo cp /opt/odoo/debian/odoo.conf /etc/odoo-server.conf

- put this in odoo-server.conf

.. code-block::

    [options]
    admin_passwd = admin
    db_host = False
    db_port = False
    db_user = odoo
    db_password = FALSE
    addons_path = /opt/odoo/addons
    ;Uncomment the following line to enable a custom log
    logfile = /var/log/odoo/odoo-server.log
    xmlrpc_port = 8069

[OPTIONAL] Create an Odoo Service
----------------------------------

.. code-block::

    sudo touch /lib/systemd/system/odoo-server.service

- Include the following text in that file

.. code-block::

    [Unit]
    Description=Odoo Open Source ERP and CRM
    Requires=postgresql.service
    After=network.target postgresql.service

    [Service]
    Type=simple
    PermissionsStartOnly=true
    SyslogIdentifier=odoo-server
    User=odoo
    Group=odoo
    ExecStart=/opt/odoo/odoo-bin --config=/etc/odoo-server.conf --addons-path=/opt/odoo/addons/
    WorkingDirectory=/opt/odoo/
    StandardOutput=journal+console

    [Install]
    WantedBy=multi-user.target


Change File Ownership and Permissions
-------------------------------------

.. code-block::

    sudo chmod 755 /lib/systemd/system/odoo-server.service
    sudo chown root: /lib/systemd/system/odoo-server.service
    sudo chown -R odoo: /opt/odoo/
    sudo chown odoo:root /var/log/odoo
    sudo chown odoo: /etc/odoo-server.conf

Test the Server
---------------

.. code-block::

    sudo systemctl start odoo-server
    sudo systemctl status odoo-server
    sudo journalctl -u postgresql
    sudo systemctl stop odoo-server


Enable Odoo Service
-------------------

.. code-block::

    sudo systemctl enable odoo-server

- Restart server and check that it starts again

.. code-block::

    sudo journalctl -u odoo-server

Some additional things that are nice
------------------------------------

Disable and re-enable sleep
___________________________

.. code-block::

    sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
    sudo systemctl unmask sleep.target suspend.target hibernate.target hybrid-sleep.target
