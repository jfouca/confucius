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
guide covers only the installation of Confucius itself and its dependencies.

Installation on a Debian-based OS
------------

This guide uses SQLite for the installation, since it's very easy to install and perfect for development
or testing purposes. You can use your favourite RDBMS, but you'll need to make some minor changes
to `settings.py` (please refer to the [dedicated Django documentation](https://docs.djangoproject.com/en/1.3/ref/settings/#databases)).

"|PATH|" designates the exact location where you will extract Confucius, eg : `/home/www`

By convention, commands preceded by `#` must be executed as `root`.

    # apt-get install apache2 libapache2-mod-wsgi python-pip libsqlite3-0
    # pip install Django==1.3.1
    # cd |PATH|
    PATH# wget http://www.confuciusproject.com/confucius_rc2.tar.gz
    PATH# tar xzf confucius_rc2.tar.gz
    PATH# cd confucius_wrapper
    PATH/confucius_wrapper# python manage.py syncdb

You will be prompted to create a superuser. Please do so.
Your username doesn't matter but you must use a correct email address (Confucius will use it to log you in).

    |PATH|/confucius_wrapper# chmod 755 -R . && chown www-data:www-data -R .

Then you will need to configure an Apache VirtualHost, you can use this sample (`/etc/apache2/sites-available/default`) :

    <VirtualHost *:80>
        Alias /media/ |PATH|/confucius_wrapper/media/
        Alias /static/ |PATH|/confucius_wrapper/static/
        
        <Directory |PATH|/confucius_wrapper/static>
            Order deny,allow
            Allow from all
        </Directory>
        
        <Directory |PATH|/confucius_wrapper/media>
            Order deny,allow
            Allow from all
        </Directory>
        
        WSGIScriptAlias / |PATH|/confucius_wrapper/confucius.wsgi
        WSGIDaemonProcess confucius user=www-data group=www-data processes=1 threads=10
        WSGIProcessGroup confucius
    </VirtualHost>

The restart Apache :

    # /etc/init.d/apache2 restart

Everything should work smoothly. The first thing you should do is go to `/admin` to set up your first conference.
Your username is your email, therefore use your *email* to log in.

Original developers
-------------------

- [Nicolas Bazire](/nbazire)
- [Ana Maria Faighel](/anouchka)
- [Lucas Fernandes](/lferna05)
- [Jérémy Foucault](/jfouca)
- [Yann Gauche](/yanng)
- [Raphaël Germon](/rgermon)
- [Yann Lemaulf](/ylemaulf)
