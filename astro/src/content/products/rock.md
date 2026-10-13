---
name: Rock
title: Analyze with Rock
tagline: "A lightweight R server, the computing backend of Opal and DataSHIELD."
order: 3
docs: https://rockdoc.obiba.org
github: https://github.com/obiba/rock
---

## What is Rock?

Rock is OBiBa's [R](https://www.r-project.org/) analysis server. It manages R server analysis sessions and is the computation engine of [Opal](/products/opal/).

## Features

Rock provides a REST API to execute R operations on the server side, in a stateful R session. Rock servers can be discovered or can self-register to build clusters for distributed computations.

- **REST API**: see [rockr](https://github.com/obiba/rockr) for an R client.
- **Stateful R sessions**, based on [Rserve](https://www.rforge.net/Rserve/).
- **Secure**, thanks to [RAppArmor](https://cran.r-project.org/package=RAppArmor).
- **Scalable**, with service discovery and self-registration.

Being interoperable and reusable, Rock follows the [FAIR principles](https://www.go-fair.org/fair-principles/) for reproducible science. Read the [Rock introduction](https://rockdoc.obiba.org/en/latest/introduction.html) for more details.

## Download

Rock is a Java application and runs on any platform with a Java virtual machine.

- **Debian / Ubuntu**: use the [Debian package repository](/pages/pkg/).
- **Fedora / RHEL**: use the [RPM package repository](/pages/rpm/).
- **Docker**: images give a reproducible R environment; see [Docker image installation](https://rockdoc.obiba.org/en/latest/admin/installation.html#docker-image-installation).

Packages are also on the [GitHub releases](https://github.com/obiba/rock/releases) page. See the [installation guide](https://rockdoc.obiba.org/en/latest/admin/installation.html) and the [configuration guide](https://rockdoc.obiba.org/en/latest/admin/configuration.html).

## Try Rock

The [demo server](https://rock-demo.obiba.org) is accessible with the [rockr](https://github.com/obiba/rockr) R package:

- `administrator` / `password`
