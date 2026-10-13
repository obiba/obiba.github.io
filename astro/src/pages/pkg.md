---
layout: ../layouts/Page.astro
title: Debian package repository
description: Install and upgrade OBiBa software on Debian and Ubuntu with apt.
---

OBiBa's Debian package repository automates installation and upgrades. First add the signing key to your system:

```sh
curl -fsSL https://www.obiba.org/assets/obiba-pub.pem | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/obiba.gpg
```

Then add the OBiBa APT source:

```sh
echo 'deb https://obiba.jfrog.io/artifactory/debian-local all main' | sudo tee /etc/apt/sources.list.d/obiba.list
```

And update the local package index:

```sh
sudo apt-get update
```

## Opal

```sh
sudo apt-get install opal
```

R server configured for Opal:

```sh
sudo apt-get install rock
sudo service rock restart
```

Opal Python client:

```sh
sudo apt-get install pipx
pipx ensurepath
pipx install obiba-opal
```

See the [Opal documentation](https://opaldoc.obiba.org).

## Mica

```sh
sudo apt-get install mica2
```

Mica Python client:

```sh
sudo apt-get install pipx
pipx ensurepath
pipx install obiba-mica
```

See the [Mica documentation](https://micadoc.obiba.org).

## Agate

```sh
sudo apt-get install agate
```

Agate Python client:

```sh
sudo apt-get install pipx
pipx ensurepath
pipx install obiba-agate
```

See the [Agate documentation](https://agatedoc.obiba.org).

## Individual packages

The `.deb` of a specific version is available from each application's releases page: [Opal](https://github.com/obiba/opal/releases), [Mica](https://github.com/obiba/mica2/releases), [Agate](https://github.com/obiba/agate/releases), [Rock](https://github.com/obiba/rock/releases).

The RPM equivalent is the [RPM package repository](/rpm/).
