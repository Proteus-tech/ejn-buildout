collective.registrationcaptcha
==============================

Add a captcha field to the @@register form for anonymous users to secure
it from spam bots.

It depends on ``plone.app.discussion`` and uses its captcha abstaction
facilities.

In order to use a captcha widget, you have to install one - whether
by depending on the ``captchawidgets`` extra of this package or by installing
``plone.formwidget.captcha``, ``plone.formwidget.recaptcha`` (not functional at
time of this writing) or ``collective.z3cform.norobots``.

Then you have to configure plone.app.discussion to use a captcha widget. You
don't need to enable commenting on your site for this to work.


Installation on Plone 4.3
-------------------------

You will need to pin the version of plone.app.users to 2.1.0.

plone.app.users 2.2.x is Plone 5 only.
