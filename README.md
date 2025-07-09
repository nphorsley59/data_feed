# data_feed

Microservice to collect articles from medical journals.

## Data sources

### PubMed Central (PMC)

PMC is a free, full-text archive of biomedical and life sciences journals. It is a subset of PubMed.

*PMC Open Access Subset [Internet]. Bethesda (MD): National Library of Medicine. 2003 - [cited YEAR MONTH DAY]. Available from https://pmc.ncbi.nlm.nih.gov/tools/openftlist/.*

*Comeau DC, Wei CH, Islamaj Doğan R, and Lu Z. PMC text mining subset in BioC: about 3 million full text articles and growing, Bioinformatics, btz070, 2019.*

## Docker

Docker is used to manage the development environment and to emulate services.

To connect to your Docker development server:

1. Start the container in detached mode with `docker compose up -d <service_name>`
2. Enter the container with `docker compose exec <service_name> bash`

If you suspect a build is outdated:

1. Rebuild the container with `docker compose build --no-cache <service_name>`

## Poetry

Poetry is used to manage the Python environment in the development container. Poetry commands should generally be run on the development server.

- Show what is installed with `poetry show`
- Add a new library with `poetry add <library_name>@<version>`
- Remove an existing library with `poetry remove <library_name>`
- Reinstall requirements by rebuilding the development container
