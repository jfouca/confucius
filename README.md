CONFUCIUS [![Build Status](https://secure.travis-ci.org/keepitsimpl/confucius.png?branch=development)](http://travis-ci.org/keepitsimpl/confucius)
=================================================================================================================================================

Preliminary notes
-----------------

Confucius is a student project developed in 3 weeks and a half by 7 students.
Because of the academic context and so little time, it hasn't been audited nor
fully tested (yet) and SHOULD NOT be used in production.

We -the students- put a strong focus on releasing all features planned initially because
our final evaluation would only assess "what" we managed to do, not "how" we did it.
Code quality, maintainability, and good development practices such as branching, documenting,
testing and continuous integration were never part of the evaluation.

Therefore, the code is functionnal but as it grew became very difficult to read and maintain, even
for us. Before even considering a public release a full set of tests should be written, and
the code should be completely documented and undergo some heavy refactoring.

Only one of us was familiar with all the technologies used (Django, jQuery, Bootstrap),
if you have some experience with those you might find some methods, functions or instructions horrifying.
Please bear in mind that all of this was done in less than 4 weeks by 7 people including 6 who
didn't know the first thing about generic views, method chaining or unobstrusive Javascript.

While this is absolutely not an excuse for writing crappy code, it should be noted that we are
fully aware of the nowhere-near-production-ready state of this project, we just didn't have the
time to correct it (yet).

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

### Requirements installation

    # aptitude install apache2 libapache2-mod-wsgi python-pip
    # pip install -r requirements.txt --use-mirrors

If your RDBMS is MySQL :

    # aptitude install python-mysql

If your RDBMS is PostgreSQL :

    # aptitude install python-psycopg2


Original developers
-------------------

- [Nicolas Bazire](/nbazire)
- [Ana Maria Faighel](/anouchka)
- [Lucas Fernandes](/lferna05)
- [Jérémy Foucault](/jfouca)
- [Yann Gauche](/yanng)
- [Raphaël Germon](/rgermon)
- [Yann Lemaulf](/ylemaulf)
