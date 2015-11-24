EJN buildout
============

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
