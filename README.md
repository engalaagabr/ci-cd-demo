# FastAPI CI/CD

Minimal FastAPI app with Docker, Ruff, pytest, and GitHub Actions.

## Quick start

Use Python 3.14:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Or run with Docker:

```sh
docker compose up --build
```

Open [the app](http://localhost:8000/) or [API docs](http://localhost:8000/docs).

## Development

```sh
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
```

<details>
<summary>Apply lint fixes and formatting</summary>

```sh
python -m ruff check --fix .
python -m ruff format .
```

Ruff settings live in [pyproject.toml](pyproject.toml).

</details>

## CI/CD

GitHub Actions checks linting, formatting, and tests before building the Docker
image. Successful pushes and pull requests targeting `main` publish to GitHub
Container Registry, regardless of the default branch.

<details>
<summary>Workflow details</summary>

- [CI](.github/workflows/ci.yml) also checks PRs targeting `dev` and supports manual runs.
- [CD](.github/workflows/cd.yml) publishes `latest` and commit-specific image tags.
  Both push and PR publishing update `latest`.
- Fork PRs normally cannot publish with the default read-only token.
- Server deployment is configured separately.

</details>
