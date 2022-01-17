<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/interlink-project/interlinker-collaborative-editor">
    <img src="images/logo.png" alt="Logo" width="172" height="80">
  </a>

  <h3 align="center">Collaborative editor interlinker</h3>

  <p align="center">
    Interlinker that allows multiple users to collaborate on real-time documents using Etherpad technology
    <br />
    <a href="https://interlink-project.eu/"><strong>View Interlink project »</strong></a>
    <br />
    <br />
    <a href="https://github.com/interlink-project/interlinker-collaborative-editor/issues">Report Bug</a>
    ·
    <a href="https://github.com/interlink-project/interlinker-collaborative-editor/issues">Request Feature</a>
  </p>
</div>

<!-- ABOUT THE INTERLINKER -->
## About the Interlinker

![Screen Shot](images/screenshot.png)

This interlinker is intended to be a wrapper for the Etherpad open source tool. It consists of an API (developed with FastAPI) that acts as a proxy with Etherpad's own API (https://etherpad.org/doc/v1.8.4/), so that the specification of the project's interlinkers is followed and the agreed standard methods are provided.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

* Install [docker-compose](https://docs.docker.com/compose/install/) to run this project.

### Installation

1. Build the containers

   ```sh
   make devbuild
   ```

   or 
   ```sh
   make devbuild
   ```

1. Run the containers in solo version

   ```sh
   make solo
   ```
   or
   ```sh
   docker-compose -f docker-compose.devsolo.yml --env-file=.env.solo up -d
   ```
1. Run the containers in integrated version

    ```sh
   make integrated
   ```
   or
   ```sh
   docker-compose -f docker-compose.devintegrated.yml up -d
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

DOMAIN:
  * **Solo mode:** localhost:8456
  * **Integrated mode:** localhost/etherwrapper
### Docs

>  http://DOMAIN/docs

### Asset instantiation

>  POST to http://DOMAIN/api/v1/assets/

### Asset retrieval

>  GET to http://DOMAIN/api/v1/assets/{id}

### Editing interface

>  GET to http://DOMAIN/api/v1/assets/{id}/gui


<p align="right">(<a href="#top">back to top</a>)</p>