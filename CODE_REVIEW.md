# CODE_REVIEW.md

## 1. Code Style Conventions

- Before committing code, run the following commands to ensure consistent linting and formatting:
  ```bash
  pip install pre-commit
  pre-commit install
  ```

* Configuration and deployment files (`docker-compose`, Grafana configs, `.env`, etc.) must be placed under the `container/` folder.

* Each sub-service should be organized under `services/` with the following structure:

  ```
  services/<service_name>/
  ├── app/              # API endpoints or worker interfaces
  ├── config/           # Pydantic-based configuration, read from `.env`
  ├── schema/           # Input/output schemas for the service
  ├── src/              # Main source code
  ├── test/             # Unit tests for modules + API tests for `app/`
  ├── requirements.txt  # Dependencies
  ├── .env              # Environment variables for the service
  └── Dockerfile        # Build instructions for the service
  ```

* Sub-services must be **tested individually** and verified before being integrated into the main `container/docker-compose.yaml`.

---

## 2. Testing & CI

- Run local development and test pipeline using:

  ```bash
  bash scripts/dev.sh
  ```

- Ensure all tests in the `tests/` folder pass.

- CI should build containers and run tests automatically before merging.

---

## 3. Current Limitations

- Chat streaming is not yet supported.
- Chat history is not yet persisted.
- Booking service is not implemented.

---

## 4. Future Improvements

- **Monitoring**: Integrate Prometheus to track service resource usage.
- **Task Management**: Use a message queue (e.g., Celery) to handle long-running tasks.
- **Scalability**: Auto-scale AI services using Ray Serve.
- **User Experience**: Add streaming token responses for real-time chat.
- **LLM Integration**: Support multiple large language model (LLM) backends
- **Agent**: Use an LLM-based agent to determine tasks, with each service acting as a tool
