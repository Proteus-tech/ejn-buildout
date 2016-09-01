ejn.applicants4funding
======================

How to use
----------

* Create custom Dexterity TTW types
* Activate the "EJN funding" behavior
* *before* start creating those content types, change the type base class (see below)

How to change Dexterity base class
----------------------------------

* Go to ZMI -> ``portal_types`` tool
* Select the TTW created dexterity types
* In the "Content type class" field change the class dotted name to
  ``ejn.applicants4funding.content.FundingReqBase``
* Save

**Note**: this will not change base class for already created contents (a type migration is needed in that case)
