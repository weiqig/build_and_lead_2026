## Project Description

This project implements a local ETL (Extract, Transform, Load) pipeline designed to process raw job listing data into a clean, structured format stored in a relational database (jobs.db).

The pipeline follows a simplified Medallion Architecture, organizing data into progressive layers of quality:

- Bronze Layer (Extract): Raw data ingestion from the 0_source directory.

- Silver Layer (Transform): Data cleaning and processing, including removal of HTML noise and normalization of fields.

- Gold Layer (Load): Structured and validated data loaded into a relational database.
Objective

The goal is to build a robust and idempotent pipeline that:

    - Extracts raw job data
    - Cleans and processes it into readable text
    - Structures it into a consistent schema
    - Loads it into jobs.db

Final database schema:

```sh
source_id | job_title | company | description | tech_stack
```

A key success criterion is ensuring that the description field contains clean, human-readable text rather than raw HTML.

## Architecture Overview

The pipeline follows a standard ETL flow:

[SOURCE] → [EXTRACT] → [CLEAN / PROCESS] → [LOAD] → [DATABASE]

### Key Components

Extractor (Bronze):
- Reads raw files from 0_source
- Handles ingestion in a consistent format

Processing Layer (Silver):
- Cleans HTML from descriptions
- Normalizes text and fields
- Extracts relevant metadata (e.g., tech stack)

Storage Layer (Gold):
- Writes structured data into jobs.db
- Ensures schema consistency

Orchestrator (main.py):
- Coordinates the full pipeline
- Ensures repeatable (idempotent) runs
- Design Considerations

### Idempotency

The pipeline is designed to produce consistent results across multiple runs without duplicating or corrupting data.

### Data Quality

Validation and cleaning occur before loading to ensure:

    - No raw HTML in descriptions
    - Structured, queryable data
    - Consistent schema adherence

## Instructions
1. Environment Setup

    Must include a .python-version file with the following content:

        3.14

    Include the required dependencies:

        uv 0.8.*
        ruff 0.15.*
        pydantic 2.13.*

    Install dependencies:
    ```sh
    uv sync
    ```

2. Run the Pipeline

    To execute each pipline separately:
    ```sh
    uv run python main.py <command>
    ```

    availble commands include:
    - ingest - extracts *.html from *.mhtml files from ( 0_source > 1_bronze )
    - process - process and clean html data into .json (1_bronze > 2_silver)
    - load - load json data into jobs.db (2_silver > 3_gold)
    - profile - provide a detailed output of database information (3_gold)

    To execute the full ETL pipeline:
    ```sh
    uv run python main.py all
    ```

    This will:
    - Extract raw data from 0_source/
    - Clean and process the data
    - Load the results into jobs.db

3. Verify Output

    After running the pipeline:

    A jobs.db SQLite database should be created.
    It will contain a single table with the following schema:
    ```sh
    source_id | job_title | company | description | tech_stack
    ```

    You can inspect it using:
    ```sh
    sqlite3 jobs.db
    ```

    Example query:
    ```sh
    SELECT * FROM jobs LIMIT 5;
    ```

## Notes
All dependencies are pinned to exact versions to ensure reproducibility.
Code is formatted using ruff.
The pipeline is designed to be modular and extensible for future stages (e.g., analytics, APIs).