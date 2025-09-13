# toggl2db

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A simple Flask-based tool to fetch projects and time entries from **Toggl Track** and store them in a local PostgreSQL database.

This project uses **Toggl API v9**. For details, see the [Toggl API documentation](https://engineering.toggl.com/docs/).

## Features

- Import projects and time entries from Toggl.
- Store data locally using PostgreSQL.
- Built-in web interface to view monthly reports:
  - Navigate by month and year.
  - Sync data from Toggl for the selected month.
  - Export report as CSV or copy to clipboard.

## Requirements

- PostgreSQL **13+**
- Either Docker & Docker Compose or Python **3.10+**

Docker is recommended.

## Setup

### Clone repository  

```bash
git clone https://github.com/Jbdnr/toggl2db.git
cd toggl2db
```

### Configure environment

Create `.env` with database and Toggl credentials. `.env` file should be placed in the project root.

```env
TOGGL_API_KEY=your_toggl_api_key_here

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=example
DB_NAME=postgres
```

> [!NOTE]
> Your Toggl API key can be found at the bottom of your **User Profile** page.

## Run locally with Python

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the app

```bash
flask run
```

## Run with Docker

Build and start services with Docker Compose:

```bash
docker-compose up --build
```

## Usage

- Open the [web UI](http://localhost:5000/) in your browser
- Choose a month and year to view time entries
- Click **Sync** to fetch data from Toggl for that month
- Export reports as **CSV** or copy them to your clipboard

## License

[MIT](LICENSE)
