# OBiBa Website
#### Open Source Software for BioBanks
### License [GPL3](http://www.gnu.org/copyleft/gpl.html#gnu-license)

## Directories

### Website Structure

In order to have clean URLs, each section of the site has its own directory under pages. For example the link to Opal
page will be:

    http://obiba.github.io/pages/products/opal

Under each section folder there is an index.html file which serves as including sub-section templates. Here is Opal's
index file:

    ---
    layout: product
    wiki: http://wiki.obiba.org/display/OPALDOC/Home
    download: http://download.obiba.org/opal/stable/
    github: http://github.com/obiba/opal
    demo: http://wiki.obiba.org/pages/viewpage.action?pageId=22544438
    title: Store with Opal
    ---
    {% include JB/setup %}
    {% include themes/bootstrap/section.html icon="fa-info-circle" sectionTitle="What is Opal?" sectionBody="themes/bootstrap/opal/what.html" %}
    {% include themes/bootstrap/section.html icon="fa-cogs" sectionTitle="Features" sectionBody="themes/bootstrap/opal/features.html" %}

The section between the three dashes is the page YAML configuration used by the corresponding template files:

* **layout**: name of the page layout used by this page
* **wiki**, **download**, **github**, **demo**: are the icons in each product page (aligned to the right)
* **title**: The title on top of the page

As an example, a template file such as *product.html* can access the download key as follows:

    page.download

The first include is useful if Jekyll Bootstrap functionality is required.
The last two include files are actually including the content of the page.

As a general rule, each main page uses templates (partials) to make the edition simpler and more organized. As it can be
seen, the Opal's intro and feature pages are divided into two separate template files.

All template files are under <strong>_includes/themes/bootstrap/</strong>, you can have a look at each to get some ideas how they use
the YAML settings and the Liquid template codes.

Currently there are four general layouts:

* **default**: the main container layout
* **page**: for all non-product pages
* **product**: for product only pages
* **post**: for posts that are not currently used

All data files are placed under <strong>_data</strong> files:

* **jobs**: list of job postings
* **news**: list of news
* **partners**: list of partners
* **post**: list of sponsors

### Website Development

You need the following tools:

* **ruby**
* **ruby-dev**
* **nodejs**
* **grunt**
* **jekyll**

To start the development follow these steps:

* open two Terminal TABs or windows
* in the first one run:


    $>grunt

* in the second run:


    $> jekyll serve -w

To view the website locally go to [http://localhost:4000](http://localhost:4000)

You can change the port alternativaly by adding a **-port <number>** to the **jeckyll** commandline:


    $>jekyll serve -w -port 4001


### Website Issues

You can always log bugs and improvements using our [JIRA](http://jira.obiba.org/) under the project **OBiBa Website**
