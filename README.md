CONFUCIUS [![Build Status](https://secure.travis-ci.org/keepitsimpl/confucius.png?branch=development)](http://travis-ci.org/keepitsimpl/confucius)
=================================================================================================================================================

Preliminary notes
-----------------

Confucius is a student project developed in 3 weeks and a half by 7 students.
Because of the academic context and so little time, it hasn't been audited nor
fully tested and SHOULD NOT be used in production.


If you have some experience with the technologies used (Django, jQuery, Bootstrap), you might find some methods, functions or instructions unusuals.
Please do not hesitate to contribute to Confucius by improving our code quality and therefore, maintainability.


What is Confucius?
------------------

Confucius is a [Conference Management System](https://en.wikipedia.org/wiki/Conference_management_system).
It was designed to handle the rather complex workflow of submission, review
and selection processes typical of academic conferences.

Requirements
------------

Confucius requires Django 1.3+ (which itself requires Python 2.4+), access to a RDBMS (such as MySQL or PostgreSQL), and a
web server (the simplest is to deploy it with Apache and mod\_wsgi).

Installation on a Debian-based OS
------------

    # aptitude install apache2 libapache2-mod-wsgi python-pip

If your RDBMS is MySQL :

    # aptitude install python-mysql

If your RDBMS is PostgreSQL :

    # aptitude install python-psycopg2

    # wget https://github.com/keepitsimpl/confucius/zipball/development -O confucius.zip
    # unzip confucius.zip && rm confucius.zip
    # mv keepitsimpl-confucius-* confucius_wrapper && cd confucius_wrapper
    confucius_wrapper# pip install -r requirements.txt --use-mirrors

Original developers
-------------------

- [Nicolas Bazire](/nbazire)
- [Ana Maria Faighel](/anouchka)
- [Lucas Fernandes](/lferna05)
- [Jérémy Foucault](/jfouca)
- [Yann Gauche](/yanng)
- [Raphaël Germon](/rgermon)
- [Yann Lemaulf](/ylemaulf)
