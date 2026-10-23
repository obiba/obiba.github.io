---
layout: ../layouts/Page.astro
title: User stories
description: How large-scale epidemiological projects use OBiBa software.
---

These stories illustrate different uses of OBiBa software in large-scale epidemiological projects.

## The Canadian Partnership for Tomorrow Project

The [Canadian Partnership for Tomorrow Project](https://canpath.ca/) (CPTP, now CanPath) is a long-term research initiative on cancer. It consists of five large Canadian prospective studies, which recruited 300,000 participants nationwide between 2009 and 2012.

The [Onyx](https://github.com/obiba/onyx) application was initially created to collect CPTP baseline data. Developed and configured by a team of 10 OBiBa developers, Onyx was deployed in dozens of assessment centers across Canada. With Onyx, participants signed an electronic consent form, answered multiple questionnaires and had physical measurements taken with several medical instruments. Barcoded biological samples were also tracked with Onyx.

In 2014, the collaboration entered a new phase with [Maelstrom Research](https://www.maelstrom-research.org/), whose mandate was to harmonize the data collected by the five cohorts and build the national data repository with [Opal](/applications/opal/) and [Mica](/applications/mica/).

## The Canadian Longitudinal Study on Aging

The [Canadian Longitudinal Study on Aging](https://www.clsa-elcv.ca/) (CLSA) is a good example of a productive collaboration between a large-scale study and OBiBa. The CLSA follows approximately 50,000 men and women for at least 20 years, collecting information on the changing biological, medical, psychological, social, lifestyle and economic aspects of their lives.

CLSA and OBiBa worked closely to develop the functionality required by CLSA protocols and data management procedures in Onyx and [Opal](/applications/opal/): a graphical questionnaire editor, integration of new medical imaging devices, video and sound recording in cognitive tests, and more.

Onyx was deployed in 10 data collection centers across Canada, and used by nurses on laptops for home interviews. Data collected by Onyx was imported daily into a central Opal repository at McMaster University in Hamilton, then incrementally exported to the CLSA analysis center's Opal at McGill University in Montreal for curation and analysis. As of September 2014, CLSA's Opal databases stored more than 4.5 terabytes of data.

The CLSA data portal is powered by [Mica](/applications/mica/).

![CLSA data flow between Onyx and Opal](/img/clsa-flow.png)

## Data harmonization and federation in BioSHaRE

BioSHaRE shows how OBiBa software creates a federated database that enables advanced analysis without disclosing any individual-level data.

[BioSHaRE](https://www.maelstrom-research.org/network/bioshare-eu) was a European project to standardize and harmonize data from some of the largest biobanks in Europe. More than 160 data elements from 13 European biobanks were harmonized by [Maelstrom Research](https://www.maelstrom-research.org/), and the harmonized datasets were stored on [Opal](/applications/opal/) servers.

The 13 databases were securely federated through the [Mica-based BioSHaRE website](https://www.maelstrom-research.org/network/bioshare-eu) and the [DataSHIELD](/applications/datashield/) R client, creating a distributed dataset on more than 650,000 European subjects. Authorized researchers can run distributed queries and statistical analyses on harmonized data hosted on geographically dispersed Opal servers:

- **Mica queries** retrieve data summaries and descriptive statistics in real time for each biobank: counts, minimums, maximums, means, standard deviations, contingency tables.
- **DataSHIELD** runs more advanced real-time analyses, such as generalized linear model fitting.

In both cases, no individual-level data is ever transferred or disclosed to researchers, protecting the subjects' privacy. See the [publication](https://doi.org/10.1186/1742-7622-10-12) for details.

![The BioSHaRE federated database connects Opal databases from European cohorts](/img/bioshare-federation-map.png)
