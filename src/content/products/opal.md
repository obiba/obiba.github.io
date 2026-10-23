---
name: Opal
title: Store and document data with Opal
tagline: "OBiBa's core data management application, to import, transform, describe and analyze data."
order: 2
icon: /img/icon-opal.png
docs: https://opaldoc.obiba.org
github: https://github.com/obiba/opal
demo: https://opal-demo.obiba.org
---

## What is Opal?

Opal is OBiBa's core data management application. This server application provides all the necessary tools to import, transform, describe and share data. Participant identifiers are kept apart from the data and managed at import and export time.

**Analysis.** Thanks to its integration with [R](https://www.r-project.org/), complex statistical analysis and reports can be performed. The implementation of [DataSHIELD](/applications/datashield/) allows advanced statistical analysis across multiple studies *without sharing or disclosing any individual-level data*.

**Integration.** Studies using Opal can import data collected with [Amber](/applications/amber/) directly from the Amber server, and build web data portals with [Mica](/applications/mica/) that query Opal for real-time aggregated reports. Secured REST web services allow automating server management and accessing data from [R](https://cran.r-project.org/package=opalr), [Python](https://pypi.org/project/obiba-opal/) or any web-capable tool.

![Opal federated analysis](/img/opal-federated.png)

## Features

**Data warehouse.**

- Projects hold tables of any entity type (participant, sample, instrument...) and value type, including dates, binaries and geographic points, lines and polygons.
- Data are stored in MySQL, MariaDB, PostgreSQL or MongoDB. A project can also be created with its own database, managed by Opal.
- Import from CSV, SPSS, SAS, Stata, Excel, SQL, REDCap, LimeSurvey, Amber or another Opal server; incremental imports; export to CSV, Opal archive or SQL.
- Query tables with SQL through the web services, and look an entity up across tables.

**Data dictionary and harmonization.**

- Variables with categories and multilingual attributes, annotated with taxonomies such as the [Maelstrom Research](https://www.maelstrom-research.org/) classification.
- Views: virtual tables of derived variables, with a JavaScript derivation library, user-friendly recoding, versioned scripts and instant summary statistics.
- Full text variable search across projects.

**Resources.** Give R/DataSHIELD sessions access to remote big or complex datasets and computing units without importing data: only the location and credentials are stored. See the [resourcer](https://github.com/obiba/resourcer) R package.

**R and DataSHIELD.**

- Computations are delegated to [Rock](/applications/rock/) R servers, that can be clustered for load balancing and declined in profiles (different R versions and packages).
- DataSHIELD packages, allowed methods and options are managed per profile, with usage quotas, audit and metrics.
- R Markdown reports and analysis plugins (data validation) run on the R server.

**Privacy, confidentiality and security.**

- Multiple identifiers per participant, kept in a database distinct from the data; data imported or exported with a research project's own identifiers.
- Password, certificate, personal access token, OpenID Connect, LDAP/Active Directory and [Agate](/applications/agate/) authentication; two-factor authentication.
- Permissions down to the variable level, summary statistics privacy threshold, PKI-based data encryption.

**Administration.** Centralized file system with access controls and SFTP, plugins (search, data sources, VCF genotypes store, analysis), persistent task history, storage safeguards, and OpenTelemetry export of logs, traces and metrics.

![Opal privacy: the same participant has different IDs, all managed by Opal](/img/opal-privacy.png)

## Download

Opal is a stand-alone Java web server application.

- System packages
  - **Debian / Ubuntu**: use the [Debian package repository](/pkg/).
  - **Fedora / RHEL**: use the [RPM package repository](/rpm/).
  - **Other platforms**: download the zip distribution from the [GitHub releases](https://github.com/obiba/opal/releases).
- Containers
  - **Docker**: use image from [Docker hub repository](https://hub.docker.com/r/obiba/opal)
  - **Helm charts**: use [OBiBa Helm charts](https://github.com/obiba/helm-charts) 

See the [installation guide](https://opaldoc.obiba.org/en/latest/admin/installation.html) and the [configuration guide](https://opaldoc.obiba.org/en/latest/admin/configuration.html).

## Try Opal

Have a look at the [demo site](https://opal-demo.obiba.org) with one of these credentials:

- Administrator: `administrator` / `password`
- DataSHIELD users: `dsuser`, `dsuser1`, `dsuser2`, `dsuser3` / `P@ssw0rd`
