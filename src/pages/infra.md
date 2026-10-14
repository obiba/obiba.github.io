---
layout: ../layouts/Page.astro
title: Infrastructure
description: How OBiBa software is built, packaged, distributed and documented.
---

Our development workflow follows agile principles with continuous integration. To keep the maintenance of the development infrastructure low, we rely on software-as-a-service offers.

## Issue tracking

Each application or library has its issue tracker in its GitHub repository: [Opal](https://github.com/obiba/opal/issues), [Mica](https://github.com/obiba/mica2/issues), [Agate](https://github.com/obiba/agate/issues), [Rock](https://github.com/obiba/rock/issues), [Amber](https://github.com/obiba/amber/issues)…

## Continuous integration

[GitHub Actions](https://github.com/features/actions) builds and tests each commit, pull request and tag.

## Repositories

The Maven, Debian and RPM package repositories are hosted on [JFrog Artifactory](https://obiba.jfrog.io). Installation instructions:

- [Debian package repository](/pkg/)
- [RPM package repository](/rpm/)

Debian, RPM and zip packages can also be downloaded from the GitHub releases pages: [Opal](https://github.com/obiba/opal/releases), [Mica](https://github.com/obiba/mica2/releases), [Agate](https://github.com/obiba/agate/releases), [Rock](https://github.com/obiba/rock/releases)…

Other distribution channels:

- **R packages**: on [CRAN](https://cran.r-project.org/).
- **Python packages**: on [PyPI](https://pypi.org/search/?q=obiba), e.g. [obiba-opal](https://pypi.org/project/obiba-opal/).
- **Plugins**: the plugins index and service plugin interfaces (SPI) are in the [plugins repository](https://plugins.obiba.org/).
- **Docker images**: on [Docker Hub](https://hub.docker.com/u/obiba/).
- **Helm charts**: on [OBiBa Helm Charts repository](https://github.com/obiba/helm-charts)

## Documentation

The online documentation is hosted by [Read the Docs](https://readthedocs.org/): [Opal](https://opaldoc.obiba.org), [Mica](https://micadoc.obiba.org), [Agate](https://agatedoc.obiba.org), [Rock](https://rockdoc.obiba.org), [Amber](https://amberdoc.obiba.org).
