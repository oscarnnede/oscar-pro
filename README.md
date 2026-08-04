<<<<<<< HEAD
# Ledger — Budget Tracker

Personal expense tracker. FastAPI + PostgreSQL backend, React (Vite/Tailwind) frontend,
built to run in Docker/Kubernetes.

## Stack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Prometheus metrics at `/metrics`
- **Frontend**: React + Vite + Tailwind, served by nginx (proxies `/api` to backend)
- **Infra**: Dockerfiles per service, docker-compose for local dev, K8s manifests for deployment

## Local development (Docker Compose)
```bash
docker compose up --build
```
- Frontend: http://localhost:8080
- Backend API docs: http://localhost:8000/docs
- Postgres: localhost:5432 (user/pass: `budget`/`budget`)

Tables are created automatically on backend startup (no migration step needed for v1).

## Kubernetes deployment
1. Build and push images (or load into your cluster's local registry, e.g. `kind load docker-image`):
   ```bash
   docker build -t budget-tracker-backend:latest ./backend
   docker build -t budget-tracker-frontend:latest ./frontend
   ```
2. Update `k8s/10-postgres.yaml` secret with a real password before deploying anywhere non-local.
3. Apply manifests in order:
   ```bash
   kubectl apply -f k8s/00-namespace.yaml
   kubectl apply -f k8s/10-postgres.yaml
   kubectl apply -f k8s/20-backend.yaml
   kubectl apply -f k8s/30-frontend.yaml
   ```
4. Add `budget-tracker.local` to `/etc/hosts` pointing at your ingress controller's IP, or
   `kubectl port-forward svc/frontend 8080:80 -n budget-tracker` for quick access.

Includes:
- Backend HPA (CPU-based, 2–6 replicas)
- Liveness/readiness probes on backend (`/api/health`) and frontend
- Postgres as a StatefulSet with a PVC (swap for a managed DB in real production)

## API surface
- `GET/POST /api/categories`, `DELETE /api/categories/{id}`
- `GET/POST/PATCH/DELETE /api/expenses`
- `GET /api/expenses/summary/monthly?month=&year=`
- `GET /api/health`, `GET /metrics` (Prometheus)

## Next steps worth considering
- Alembic migrations once the schema needs to evolve
- Auth (even basic) if this leaves your home network
- CI pipeline: build/push images on tag, `kubectl apply` or move to Helm/ArgoCD
- Grafana dashboard against the `/metrics` endpoint
=======

