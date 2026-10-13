---
title: "Infrastructure Migration"
date: "2018-06-29"
summary: "Repositories, development pipeline"
---

<p>We have migrated our infrastructure from self-hosted servers to software-as-a-service (saas) open source software offers:</p>

<ul>
		<li>Source code, issue management and release packages are in <a href="https://github.com/obiba/" target="_blank">GitHub </a>,
		</li>
		<li>Continuous integration is performed by <a href="https://travis-ci.org/obiba" target="_blank">Travis-ci </a>,
		</li>
		<li>Snapshot maven artifacts are in <a href="https://obiba.jfrog.io" target="_blank">JFrog Artifactory repositories </a>,
		</li>
		<li>Released maven artifacts and debian/rpm packages are in <a href="https://bintray.com/obiba/maven" target="_blank">JFrog Bintray repositories </a>,
		</li>
		<li>Documentations are hosted by <a href="https://readthedocs.org/" target="_blank">Read the Docs </a>.
		</li>
	</ul>

<p>As a consequence <b>system administrators must update Debian and/or RPM package repositories references</b>: see the <a href="/pkg/">Debian repository</a> and <a href="/rpm/">RPM repository</a> instructions.</a>

<p>See also the <a href="/infra/">Infrastructure description</a> for more details.</p>
