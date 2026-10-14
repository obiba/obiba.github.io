---
name: Agate
title: Manage users with Agate
tagline: "Central user profile, authentication and 2FA server for the OBiBa applications."
order: 6
icon: /img/icon-agate.png
docs: https://agatedoc.obiba.org
github: https://github.com/obiba/agate
demo: https://agate-demo.obiba.org
---

## What is Agate?

Agate provides user services to the OBiBa software stack: authentication, user profile management and notifications, for the declared applications such as [Opal](/products/opal/) and [Mica](/products/mica/).

Agate aims to be a lightweight but highly secure central authentication server: simple to install, administer and integrate with OBiBa applications.

![From Agate, an administrator manages users, groups and applications](/img/agate-server-home.png)

## Features

**Applications.** Declared applications use Agate as their user registry and notification service. Each application authenticates with a secret key (see each application's documentation to register one). An identified application can authenticate a user, get their profile, and email all users or a group of users with access to it.

**Groups.** Users can belong to one or more groups. Application access can be granted per group: members inherit the group's application access.

**Users.** A user is authenticated and receives notification emails. A user can be added by an Agate administrator, or submit a join request from the Agate web interface or the Mica sign-up page (protected by [Google reCAPTCHA](https://www.google.com/recaptcha)). Users manage their personal information from Agate or from their Mica profile page. Passwords (first password and recovery) are handled by email between the user and Agate, with no administrator action.

**Email templates.** Notifications are HTML templates, so you can fully customize links, style and site policies.

**Administration.**

- Extend user profile attributes (applied to the join request form).
- Manage users, groups and applications.
- Manage user sessions: timeouts and activity tracking.

## Download

Agate is a stand-alone Java web server application. The Debian and RPM packages are strongly recommended, as they greatly simplify installation and upgrades.

- System packages
  - **Debian / Ubuntu**: use the [Debian package repository](/pkg/).
  - **Fedora / RHEL**: use the [RPM package repository](/rpm/).
  - **Other platforms**: download the zip distribution from the [GitHub releases](https://github.com/obiba/agate/releases).
- Containers
  - **Docker**: use image from [Docker hub repository](https://hub.docker.com/r/obiba/agate)

See the [installation guide](https://agatedoc.obiba.org/en/latest/admin/installation.html) and the [configuration guide](https://agatedoc.obiba.org/en/latest/admin/configuration.html).

## Try Agate

Have a look at the [demo site](https://agate-demo.obiba.org).

Administration pages:

- Administrator: `administrator` / `password`

Own user profile:

- Mica content editor: `editor` / `P@ssw0rd`
- Mica content reviewer: `reviewer` / `P@ssw0rd`
- Mica data access officer: `dao` / `P@ssw0rd`
- Mica regular user: `user1` / `P@ssw0rd`
