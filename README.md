# FastAPI CI/CD

## Local development

Use Python 3.14:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
uvicorn app.main:app --reload
```

Ruff handles linting, import sorting, and formatting, configured in
`pyproject.toml`. To apply lint fixes and format the code locally:

```sh
python -m ruff check --fix .
python -m ruff format .
```

CI checks linting and formatting without modifying files, following the
[Ruff GitHub Actions integration](https://docs.astral.sh/ruff/integrations/#github-actions).

Or start the app with `docker compose up --build`. The endpoint at
`http://localhost:8000/` returns `{"message": "Hello, World!"}`.

## GitHub Actions

- `.github/workflows/ci.yml` runs on pushes to `main`, pull requests targeting
  `main` or `dev` from any source branch, and manual dispatches. PR checks run when opened,
  updated with new commits, reopened, edited (including retargeting to `main`), or
  marked ready for review. It checks dependencies, runs Ruff lint and formatting
  checks, then runs pytest on Python 3.14,
  then builds the Docker image. New runs cancel older runs for the same ref.
- After CI succeeds for a push to `main` or a pull request targeting `main`,
  regardless of the repository's default branch, it calls
  `.github/workflows/cd.yml` to publish the image to GitHub Container Registry.
  Publishing runs for all PR events listed above. PRs targeting `dev` and manual
  CI runs do not publish images. Fork PRs normally receive a read-only
  `GITHUB_TOKEN`, so publishing from them requires additional repository permissions.
- Images are tagged `ghcr.io/<owner>/<repository>:latest` and
  `ghcr.io/<owner>/<repository>:sha-<full-commit-sha>`, with lowercase owner and
  repository names. Both push and PR publishing update `latest`. For PRs, the
  image contains GitHub's test merge commit. Use the commit tag to select a
  particular version.

Push this repository to GitHub with Actions enabled. Publishing uses the built-in
`GITHUB_TOKEN` with `packages: write`; no custom registry secret is needed. If the
container package already exists, ensure this repository has Actions write access
to it. See [GitHub's package publishing documentation](https://docs.github.com/en/packages/managing-github-packages-using-github-actions-workflows/publishing-and-installing-a-package-with-github-actions).

CD delivers a container image; deploying it to a running server requires a hosting
target and its deployment configuration. To run a published image locally:

```sh
docker run --rm -p 8000:8000 ghcr.io/<owner>/<repository>:sha-<full-commit-sha>
```

Authenticate to GHCR before pulling if the package is private.
