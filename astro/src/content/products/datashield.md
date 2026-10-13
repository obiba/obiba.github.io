---
name: DataSHIELD
title: Analyze with DataSHIELD
tagline: "Federated analysis across studies without sharing individual-level data."
order: 4
icon: /img/icon-datashield.png
docs: https://datashield.ac.uk/
---

## What is DataSHIELD?

Some research projects need to pool data from several studies to get sample sizes large enough to detect interactions. Ethical and legal constraints often prevent sharing individual-level data across studies.

[DataSHIELD](https://datashield.ac.uk) addresses this: it enables advanced statistical analysis of individual-level data from several sources *without pooling the data together*.

In collaboration with the DataSHIELD team at Newcastle University, OBiBa built the software infrastructure required to run DataSHIELD analyses securely on data stored in [Opal](/products/opal/). See the [Opal R and DataSHIELD user guide](https://opaldoc.obiba.org/en/latest/r-user-guide/) for implementation details.

## Features

With DataSHIELD in Opal, studies can:

- Create large virtual pooled datasets from multiple harmonized study datasets and run analyses such as linear regressions.
- Install and manage DataSHIELD R packages from the [OBiBa CRAN repository](https://cran.obiba.org).
- Set fine-grained user permissions on the tables and variables available for DataSHIELD analysis.
- Set up authentication certificates between DataSHIELD clients and Opal.

A real deployment is described in the [BioSHaRE user story](/stories/).
