---
layout: ../layouts/Page.astro
title: RPM package repository
description: Install and upgrade OBiBa software on Fedora, RHEL and derivatives with yum or dnf.
---

OBiBa's RPM package repository automates installation and upgrades. Add the repository:

```sh
wget https://www.obiba.org/assets/obiba-rpm.repo -O obiba-rpm.repo
sudo mv obiba-rpm.repo /etc/yum.repos.d/
```

Check that it was added:

```sh
yum repolist | grep obiba
```

On RHEL derivatives (CentOS, Rocky Linux, AlmaLinux…), also install `epel-release`: it provides some required packages, such as `R`.

## Opal

```sh
sudo yum install opal-server
```

R server configured for Opal:

```sh
sudo yum install rock
sudo service rock restart
```

Opal Python client:

```sh
sudo yum install python3-pip libcurl4-openssl-dev libssl-dev
sudo pip install obiba-opal
```

See the [Opal documentation](https://opaldoc.obiba.org).

## Mica

```sh
sudo yum install mica2
```

Mica Python client:

```sh
sudo yum install python3-pip libcurl4-openssl-dev libssl-dev
sudo pip install obiba-mica
```

See the [Mica documentation](https://micadoc.obiba.org).

## Agate

```sh
sudo yum install agate
```

Agate Python client:

```sh
sudo yum install python3-pip libcurl4-openssl-dev libssl-dev
sudo pip install obiba-agate
```

See the [Agate documentation](https://agatedoc.obiba.org).

## Individual packages

The `.rpm` of a specific version is available from each application's releases page: [Opal](https://github.com/obiba/opal/releases), [Mica](https://github.com/obiba/mica2/releases), [Agate](https://github.com/obiba/agate/releases), [Rock](https://github.com/obiba/rock/releases).

The Debian equivalent is the [Debian package repository](/pkg/).
