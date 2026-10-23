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

Mica gives studies scientifically robust data visibility and a web presence without significant IT effort: structured descriptions of networks, studies and harmonization initiatives, annotated and searchable data dictionaries, and data access request management. Mica stores no record-level data: it works with [Opal](/applications/opal/) for the data dictionaries and summary statistics, and with [Agate](/applications/agate/) for the users.

## Features

**Catalogue.** Documents specific to the epidemiological domain, with their relationships:

- Networks of studies.
- Individual studies, with populations and data collection events, and harmonization initiatives.
- Collected datasets and harmonization protocols, with their variables, data schema and harmonized variables.
- Research projects conducted with the data.

The description forms are customizable, and documents are annotated with taxonomies (such as the [Maelstrom Research](https://www.maelstrom-research.org/) classification), either manually or inferred from their variables.

**Search.** A faceted search engine, that combines criteria across document types: for instance, variables about alcohol in studies that collected biosamples and belong to a network. Variables, studies and networks can be collected in a cart, compared, and downloaded as CSV.

**Data summaries.** For studies using Opal as their secured database, a distributed query engine gives authorized researchers real-time aggregated reports on the number of participants with specific characteristics, and summary statistics on each variable. No individual-level data passes through Mica. Data dictionaries can also be provided as Excel or SPSS files, without an Opal server.

**Data access management.** Electronic handling of access requests, from submission to approval:

- Forms designed by the administrator: main application, preliminary, feasibility, amendment and end-user agreement forms, with attached files and a selection of requested variables.
- Configurable workflow (review and conditional approval steps), with email notifications at each status change.
- Collaborators, private comments for the data access committee, and a history of each request.
- Research projects reporting what was done with the data.

**Publication flow.** Every document and file goes through draft, review and publication states, with permissions separating editors from reviewers, revision history and comments.

**Web portal.** The public pages are [FreeMarker](https://freemarker.apache.org/) templates that can be customized, extended or overridden, with a theme based on [AdminLTE](https://adminlte.io/), custom pages, translations and multilingual content.

**Security.** Authentication delegated to Agate (two-factor authentication, OpenID Connect realms, roles mapped from Agate groups), permissions on any document, sign-up protected by [Google reCAPTCHA](https://www.google.com/recaptcha).

**Automation.** The [micar](https://cran.r-project.org/package=micar) R package, the [obiba-mica](https://pypi.org/project/obiba-mica/) Python client and the REST web services allow exploring the published content and scripting administration tasks. Search engines (Elasticsearch, OpenSearch), table and taxonomy sources are plugins.

## Download

Mica is a stand-alone Java web server application. The Debian and RPM packages are strongly recommended, as they greatly simplify installation and upgrades.

- System packages
  - **Debian / Ubuntu**: use the [Debian package repository](/pkg/).
  - **Fedora / RHEL**: use the [RPM package repository](/rpm/).
  - **Other platforms**: download the zip distribution from the [GitHub releases](https://github.com/obiba/mica2/releases).
- Containers
  - **Docker**: use image from [Docker hub repository](https://hub.docker.com/r/obiba/mica)

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
