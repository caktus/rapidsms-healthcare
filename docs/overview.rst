Project Overview
====================================

As the name implies rapidsms-healthcare aims to solve a problem with storing healthcare related
data for RapidSMS deployments. Currently there is no canonical data model for storing
patient or healthcare worker data in RapidSMS. This means that each deployment tends
to create its own model for this data. Applications that are then built to use this
data are tied to the model which hurts the reusability of these applications.

At the same time with development of external electronic medicial record systems
such as OpenMRS, future deployments may choose to use these solutions rather than
storing data via the Django ORM. So rather than try to create a canonical representation
of the data, this project intends to create a seperation between the storage and
access of the data. Applications which need to access or store patient data
will do so through a common API without knowledge of the storage allowing the same
code to be used in a deployment which uses the ORM and another which uses OpenMRS.


Goals
------------------------------------

The development of rapidsms-healthcare is still in the very early stages but the
primary goals for both the current and future work are

- Client API for storing and retriving patient and provider records
- Default storage backend using the Django ORM
- Additional storage backend using OpenMRS
- Documentation guide/standards for creating additional storage backends
- Suite of applications known to work with this patient API


Related Projects
------------------------------------

There two current projects which attempt to provider flexible data models for
patient records

- https://github.com/unicefuganda/rapidsms-healthmodels
- https://github.com/ewheeler/rapidsms-people-app

While the flexibility is helpful for a singular deployment, it contributes to the
difficulty when trying to create applications which can be used on a broad set of
deployments.
