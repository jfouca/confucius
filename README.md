CONFUCIUS [![Build Status](https://secure.travis-ci.org/keepitsimpl/confucius.png?branch=development)](http://travis-ci.org/keepitsimpl/confucius)
=================================================================================================================================================

Preliminary notes
-----------------

Confucius is a student project developed in 3 weeks and a half by 7 students.
Because of the academic context and so little time, it hasn't been audited nor
fully tested and therefore SHOULD NOT be used in production.

This is still a work in progress. Please feel free to participate and don't hesitate to make a pull request.

What is Confucius?
------------------

Confucius is a [Conference Management System](https://en.wikipedia.org/wiki/Conference_management_system).
It was designed to handle the rather complex workflow of submission, review
and selection processes typical of academic conferences.

Requirements
------------

Confucius requires Django 1.3+ (which itself requires Python 2.4+), access to a RDBMS (such as MySQL or PostgreSQL),
a working SMTP gateway and a web server (the simplest is to deploy it with Apache and mod\_wsgi).

Below are described the basic steps to get a proper installation working. Please note that this installation
guide covers only the installation of confucius itself and its dependencies.

Installation on a Debian-based OS
------------

"<path>" designates the exact location where you will extract Confucius, eg : /home/www/confucius\_wrapper

    # aptitude install apache2 libapache2-mod-wsgi python-pip
    # pip install pip install Django==1.3.1
    # cd <path>
    # wget http://www.confuciusproject.com/confucius_rc1.tar.gz
    # tar xzf confucius_rc1.tar.gz
    # cd confucius_wrapper
    confucius_wrapper# python manage.py syncdb

You will be prompted to create a superuser. Please do so and use a correct email address.

    confucius_wrapper# chmod 755 -R . && chown www-data:www-data

Then you will need to configure an Apache VirtualHost, you can use this sample (for instance /etc/apache2/sites-available/default) :
    <VirtualHost *:80>
        Alias /media/ <path>/media/
        Alias /static/ <path>/static/
        
        <Directory <path>/static>
            Order deny,allow
            Allow from all
        </Directory>
        
        <Directory <path>/media>
            Order deny,allow
            Allow from all
        </Directory>
        
        WSGIScriptAlias / <path>/confucius.wsgi
        WSGIDaemonProcess confucius user=www-data group=www-data processes=1 threads=10
        WSGIProcessGroup confucius
    </VirtualHost>

The restart Apache :

    # /etc/init.d/apache2 restart

Everything should work smoothly. The first thing you should do is go to /admin to set up your first conference.

Original developers
-------------------

- [Nicolas Bazire](/nbazire)
- [Ana Maria Faighel](/anouchka)
- [Lucas Fernandes](/lferna05)
- [Jérémy Foucault](/jfouca)
- [Yann Gauche](/yanng)
- [Raphaël Germon](/rgermon)
- [Yann Lemaulf](/ylemaulf)
