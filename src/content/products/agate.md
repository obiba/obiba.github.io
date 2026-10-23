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

Agate provides user services to the OBiBa software stack: authentication, user profile management and notifications, for the declared applications such as [Opal](/applications/opal/) and [Mica](/applications/mica/).

Agate aims to be a lightweight but highly secure central authentication server: simple to install, administer and integrate with OBiBa applications, and able to delegate authentication to your institution's identity provider.

![From Agate, an administrator manages users, groups and applications](/img/agate-server-home.png)

## Features

**Applications.** Declared applications use Agate as their user registry and notification service. Each application authenticates with a secret key. An identified application can authenticate a user, get their profile, and email all users or a group of users with access to it. Applications' requests on a user are tracked as tickets.

**Single sign-on.** Agate is an [OAuth2 and OpenID Connect provider](https://agatedoc.obiba.org/en/latest/oauth2-api/index.html): OBiBa applications and any third-party client can sign users in through Agate, with authorization code, resource owner password and OpenID Connect flows.

**Realms.** Authentication can be delegated to external identity providers while the user profile stays in Agate: OpenID Connect (Keycloak, institutional providers...), LDAP, Active Directory and SQL databases. Groups can be mapped from the identity provider's claims at each sign-in.

**Users and groups.** Users belong to groups, and application access is granted per user or per group. A user can be added by an administrator, or submit a join request from Agate or the Mica sign-up page (protected by [Google reCAPTCHA](https://www.google.com/recaptcha)), reviewed by an administrator. Passwords (first password and recovery) are handled by email between the user and Agate, with no administrator action. The user profile attributes can be extended.

**Security.**

- Two-factor authentication with an authenticator app, that can be enforced for all users, including those of external realms.
- Argon2id password hashing, configurable password policy, login ban after repeated failures, and re-authentication for sensitive operations.
- Encryption keys and certificates managed from the administration pages.

**Notifications.** Emails (account confirmation, password reset, two-factor code, registration review, and the applications' own notifications) are HTML [FreeMarker](https://freemarker.apache.org/) templates, edited and previewed from the web interface, localized per language, with fallback templates shared between applications.

**Automation.** The [obiba-agate](https://pypi.org/project/obiba-agate/) Python client and the REST web services allow scripting user, group and application management.

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
