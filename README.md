# Ticketbot

<p align="center">
  <img src="assets/ticketbot.png" alt="Ticketbot Logo" width="200"/>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/release/python-390/">
    <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python 3.9+">
  </a>
  <a href="https://docs.docker.com/compose/">
    <img src="https://img.shields.io/badge/docker-compose-blue?logo=docker" alt="Docker Compose">
  </a>
  <a href="https://pre-commit.com/">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit" alt="pre-commit">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/tien02/ticketbot" alt="License">
  </a>
</p>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture & Structure](#architecture--structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)

---

## Overview

Ticketbot is a booking ticket chatbot designed to process user requests and store relevant information in an SQL database. It’s built with modular services for better organization and maintainability.

---

## Features

- FAQ from the database.
- Interact with a booking relational database through natural language.
- Accept booking requests in natural language.
- Support audio and image inputs.
- Validate and log tickets in SQL.
- Modular architecture for scalability.

---

## Architecture & Structure

Please have a look at [CODE_REVIEW.md](CODE_REVIEW.md).

---

## Prerequisites

- Docker & Docker Compose
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- `pip install pre-commit` (ensure code formatting and linting)

---

## Setup & Installation

1. **Configure environment**

   - Copy `.env.example` to `.env` in each service directory.
   - Update environment variables as needed (e.g., database URLs, API keys).

2. **Run server**

   - Development server:

     ```bash
     bash scripts/dev.sh
     ```

   - Production server:
     ```bash
     bash scripts/prod.sh
     ```

---

## Usage

- Interact with the chatbot via API endpoints. Example (adjust URL as needed):
  ```bash
  curl -X POST http://localhost:8080/process \
    -F "user_id=U001" \
    -F "message=Tôi muốn đặt vé đi thành phố Hồ Chí Minh"
  ```

* View Grafana logs at `http://localhost:3000`

---

## Testing

- Each service includes unit tests under `services/<service_name>/test/`.
- Test the end-to-end service with scripts in the `test/` directory. Run the following command to insert the dummy data:

```bash
python test/insert_test_data.py
```

---

## Future Enhancements

- Add **chat streaming** support.
- Implement **chat history persistence**.
- Integrate **Prometheus** for resource monitoring.
- Use a **message queue** (Celery or similar) for async tasks.
- Enable **auto-scaling** of AI model services (e.g., Ray Serve).
- Support **token stream responses** for real-time user interaction.
