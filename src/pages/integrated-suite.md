---
layout: ../layouts/Page.astro
title: An integrated suite of applications
description: How OBiBa applications work together, for individual studies and study consortia.
---

OBiBa applications share common data models and interfaces, so data moves seamlessly and securely from one application to another. Together they give studies an integrated infrastructure that supports almost all their data management activities, for individual studies as well as study consortia.

## Individual study

An epidemiological study can take advantage of the whole OBiBa stack.

**Data collection.** [Amber](/applications/amber/) captures case report forms and participant interviews, with validation rules and skip logic that keep errors low. Collected data always comes with its data dictionary, derived from the form, so no information is lost when interpreting it. Amber data can be imported into [Opal](/applications/opal/), or extracted with the amberr R package.

**Data storage.** [Opal](/applications/opal/) stores data from Amber and from other sources: CSV, SPSS, SAS or Stata files, SQL databases. The data dictionary can be prepared before or after import. Derivation algorithms clean and quality-check the data, and participant data can be enriched with other information such as drug registries or geographical area metrics.

Opal also compartmentalizes participant identifiers for better privacy and to avoid data collusion: the same participant can have one ID in the collected data, another in Opal storage, and yet another in data exported to a research group.

**Data analysis.** Data stored in Opal can be exported in common file formats, or analyzed in [R](https://www.r-project.org/) through [Rock](/applications/rock/) servers for statistics, graphics and reports.

**Data publication.** [Mica](/applications/mica/) publishes data dictionaries and aggregated results. Its search lets researchers explore a study's variables and data profiles to find what matches their needs, and data access requests can be submitted and evaluated online.

**User management.** [Agate](/applications/agate/) provides a single user registry, authentication with two-factor support, and notifications across the applications.

## Study consortia

OBiBa supports data collection, harmonization and federation across studies:

- Data collected with Amber, or from other sources, is imported into study-specific Opal databases.
- Each study uses Opal views and derived variables to transform its data into a common, harmonized dataset.
- With Mica and Opal, the harmonized data is queried and analyzed using [DataSHIELD](/applications/datashield/) as a federated database, *without individual-level data ever leaving the host institutions*.

![From data collection to data federation via data harmonization in a study consortium](/img/opal-federated.png)

Real examples are described in the [CPTP and BioSHaRE user stories](/stories/). To set up your own federated infrastructure, see the [Opal R and DataSHIELD user guide](https://opaldoc.obiba.org/en/latest/r-user-guide/).
