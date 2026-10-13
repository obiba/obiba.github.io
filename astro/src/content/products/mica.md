---
name: Mica
title: Publish with Mica
tagline: "Web data portals to describe studies, networks and variables, with real-time Opal queries."
order: 5
icon: /img/icon-mica.png
docs: https://micadoc.obiba.org
github: https://github.com/obiba/mica2
demo: https://mica-demo.obiba.org
---

## What is Mica?

Mica creates data web portals for large-scale epidemiological studies and multiple-study consortia.

Mica gives studies scientifically robust data visibility and a web presence without significant IT effort: structured descriptions of consortia and studies, annotated and searchable data dictionaries, and data access request management.

## Features

**Network identification and listing.** A standardized way to describe networks and the studies that constitute them.

**Study catalogue.**

- Default study description characteristics, customizable to specific requirements.
- Longitudinal study designs, with data collection events, sub-populations and recruitment timelines.

**Datasets.**

- A standard menu for data resources.
- Faceted variable search.
- Detailed dataset descriptions, with a comprehensive dictionary of the variables.

Mica does not store any record-level data. For studies using [Opal](/products/opal/) as their secured database, a distributed query engine gives authorized researchers real-time aggregated reports on the number of participants with specific characteristics, and summary statistics on each variable. No individual-level data passes through Mica, yet researchers can assess whether a dataset suits their needs.

**Data access management.** Editable forms to handle access requests electronically:

- Present the data access policy.
- Manage data access requests from submission to approval.
- Extend the default request form.
- Present the data access committee members.

**Administration.** Administer the portal from the website itself, and define permissions on any kind of content.

## Download

Mica is a stand-alone Java web server application; it does not need a container such as Tomcat or Jetty. The Debian and RPM packages are strongly recommended, as they greatly simplify installation and upgrades.

- **Debian / Ubuntu**: use the [Debian package repository](/pages/pkg/).
- **Fedora / RHEL**: use the [RPM package repository](/pages/rpm/).
- **Other platforms**: download the zip distribution from the [GitHub releases](https://github.com/obiba/mica2/releases).

See the [installation guide](https://micadoc.obiba.org/en/latest/admin/installation.html) and the [configuration guide](https://micadoc.obiba.org/en/latest/admin/configuration.html).

## Try Mica

Have a look at the [demo site](https://mica-demo.obiba.org).

Administration pages:

- Administrator: `administrator` / `password`
- Content editor: `editor` / `P@ssw0rd`
- Content reviewer: `reviewer` / `P@ssw0rd`

Data access pages:

- Data access officer: `dao` / `P@ssw0rd`
- Regular user: `user1` / `P@ssw0rd`
