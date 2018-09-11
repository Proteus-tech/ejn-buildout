EJN buildout
============
Prequisite:
  $ sudo apt-get install varnish
  $ sudo apt-get install python-docutils
  $ sudo apt-get install libncurses5-dev libncursesw5-dev
  $ sudo apt-get install -y pkg-config
  $ sudo apt-get install libpcre3 libpcre3-dev libedit-dev
Bootstrap::

  $ cp buildout.cfg.sample buildout.cfg
  $ pip install -r requirements.txt
  $ buildout

For production::

  $ cp buildout.cfg.sample buildout.cfg
  $ sed -i -e 's/development/production/' buildout.cfg
  $ pip install -r requirements.txt
  $ buildout

Then make a supervisord init file and launch it.

DEV3:
ssh root@159.89.191.228
bin/instance1 start
bin/instance1 stop