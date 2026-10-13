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

Opal is OBiBa's core data management application. This server application provides all the necessary tools to import, transform and describe data. Subject identifiers can also be managed at data import and export time.

**Analysis.** Thanks to its integration with [R](https://www.r-project.org/), complex statistical analysis and reports can be performed. The implementation of [DataSHIELD](/products/datashield/) allows advanced statistical analysis across multiple studies *without sharing or disclosing any individual-level data*.

**Integration.** Studies using Opal can securely import data collected with [Amber](/products/amber/), and build web data portals with [Mica](/products/mica/) that query Opal for real-time aggregated reports. Secured REST web services allow automating server management (Python command line tools) and accessing data from R, Python or any web-capable tool.

![Opal federated analysis](/img/opal-federated.png)

## Features

- **Data warehouse**: unlimited number of variables; MongoDB, MySQL, MariaDB and PostgreSQL backends; import and export CSV, SPSS, SAS, Stata and SQL; incremental imports; any type of entity and value; SQL API.
- **Resources**: give R/DataSHIELD sessions access to remote big or complex datasets and computing units, without importing data. See the [resourcer](https://github.com/obiba/resourcer) R package.
- **Views and derived variables**: virtual tables of derived variables, a JavaScript library for derivations, user-friendly recoding, instant summary statistics.
- **Privacy, confidentiality and security**: PKI-based data encryption, certificate, password, token and OpenID Connect authentication, multiple identifiers per participant in a distinct database, permissions down to the variable level.
- **File system**: centralized file management with access controls.
- **R interface**: R server monitoring and secured data access from R.

![Opal privacy: the same participant has different IDs, all managed by Opal](/img/opal-privacy.png)

## Download

Opal is a stand-alone Java web server application; it does not need a container such as Tomcat or Jetty.

- **Debian / Ubuntu**: use the [Debian package repository](/pages/pkg/).
- **Fedora / RHEL**: use the [RPM package repository](/pages/rpm/).
- **Other platforms**: download the zip distribution from the [GitHub releases](https://github.com/obiba/opal/releases).

See the [installation guide](https://opaldoc.obiba.org/en/latest/admin/installation.html) and the [configuration guide](https://opaldoc.obiba.org/en/latest/admin/configuration.html).

## Try Opal

Have a look at the [demo site](https://opal-demo.obiba.org) with one of these credentials:

- Administrator: `administrator` / `password`
- DataSHIELD users: `dsuser`, `dsuser1`, `dsuser2`, `dsuser3` / `P@ssw0rd`
