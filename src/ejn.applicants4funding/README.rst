ejn.applicants4funding
======================

How to configure
----------------

* Create new custom Dexterity TTW types (as many as needed)
* Activate the "EJN funding" behavior
* *Before* start creating those content types, change the type base class (see below)
* Create as many as needed PFG, and remember to fill the "EJN funding category" field
* For every form involved:
  * Create a new uwosh.pfg.d2c adapter
  * Configure the adapter to create a "Funding request" content type

How to use
----------

Every user can now create new dexterity types normally, but only one content per type is allowed; creating more that one will trigger an exception.
In the content view he will see a link of links to form that are configured with the current type.

How to change Dexterity base class
----------------------------------

* Go to ZMI -> ``portal_types`` tool
* Select the TTW created dexterity types
* In the "Content type class" field change the class dotted name to
  ``ejn.applicants4funding.content.FundingReqBase``
* Save

**Note**: this will not change base class for already created contents (a type migration is needed in that case)
