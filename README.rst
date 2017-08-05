Summary
=======

The cash register module is an Odoo module (Version 10.0) intended to improve
the experience of recording till counts. It provides the option to manually
count and enter the contents of a till, or simply provide a balance with rough
estimates of the contents while while randomly generating counts for the
remaining balance.


Requirements & Deployment
=========================

As this is an Odoo module, the minimum requirements are prescribed by those of
the Odoo framework. These requirements basically consist of some non-stock
python libraries and some (fairly recent) version of postgreSQL. For a flawless
guide on Odoo 10 server deployment please visit the following link;

https://www.linode.com/docs/websites/cms/install-odoo-10-on-ubuntu-16-04

With a properly configured base Odoo environment

1. Ensure that the configuration file includes the location of this module in
the "addons_path".
2. Run the Odoo server
3. Active *Developer Mode* via **Settings**
4. Refresh the browser, **Apps > Update Module List**
5. Install *cash_register*...
