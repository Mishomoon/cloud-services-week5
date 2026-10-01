# Cloud Services – Week 5: Redis cache and visitor counter

This is my Week 5 project. I took my Week 4 app (Nginx frontend, Flask backend, MySQL) on CSC Rahti and added **Redis** as a new component. The backend uses Redis for a visitor counter.

- Live app: https://frontend-cloud-services-week5.2.rahtiapp.fi
- The full documentation (Part A answers and screenshots) is on the same page.

## Architecture

```text
User -> Rahti Route -> Nginx frontend -> Flask/Gunicorn backend -> Redis (visitor counter)
                                                                -> MySQL (database + PVC)
```

Redis runs in its own pod with its own Deployment and Service. It is not inside the backend container. It has no Route, so only the backend can reach it inside the cluster.

## What I added in Week 5

| File | What it does |
|---|---|
| `rahti/redis-deployment.yaml` | Redis Deployment (Redis image, 1 replica, port 6379) |
| `rahti/redis-service.yaml` | Service named `redis` on port 6379 |
| `rahti/configmap.yaml` | Backend config, including `REDIS_HOST=redis` |
| `backend/requirements.txt` | Added the `redis` Python package |
| `backend/app.py` | New `/api/visitor` endpoint |

## How the visitor counter works

The backend connects to Redis using the Service name:

```python
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
```

Each request to `/api/visitor` runs `redis_client.incr("visitor_count")` and returns the new number as JSON, for example `{"visits": 5}`. The backend gets `REDIS_HOST` from the ConfigMap (`envFrom` with `backend-config`), so no values are hard-coded in the code.

## Evidence

Screenshots are in `frontend/screenshots-week5/`.

| What | File |
|---|---|
| Deployments and pods (frontend, backend, MySQL, Redis all running) | `Week 5 Deployment Status.png` |
| Services, including Redis on 6379 | `week5-services.png` |
| Redis running as its own Deployment | `week5-redis-deployment.png` |
| Redis host in the ConfigMap | `configmap.yaml.png` |
| Redis package in requirements | `requirements.txt.png` |
| Visitor counter test | `visitor count.png` |

## Problems I had

**1. Redis permission error.** Redis could not save its RDB file in `/data` and the backend got errors. Redis is only used as a cache here, so I turned off RDB saving and append-only mode. (`redis-error.png`)

**2. Rahti CPU quota.** When I updated the Redis Deployment, the new pod would not start because the project had already used its 4 CPUs and the new pod asked for another 500m. The old Redis pod kept running, so the problem was the quota and not the Service. **[TODO: write how you fixed it]** (`CPU-quota.png`)

**3. ImagePullBackOff on the frontend.** The frontend pod could not pull its image because the image tag was missing on Docker Hub. I pushed the image again (`mishmoon/frontend:1.8`) and updated the Deployment. After that the pod started.

## If this went to production

- **Redis loses its data on restart.** The visitor counter starts again from zero when the Redis pod is recreated. That is fine for a counter in this course project, but important data must stay in MySQL, which uses persistent storage.
- **Cache invalidation.** If cached data comes from MySQL, it can get old. I would use a TTL or delete the key when the data changes.
- **Reliability.** One Redis replica is fine here. In production I would add monitoring and a more resilient Redis setup.
- **Security.** Redis is only reachable through an internal Service. A Web Application Firewall would go in front of the Route, which is the only public entry point. No passwords are committed to this repository. **[TODO: write where the MySQL password is stored, e.g. a Secret]**
- **Link to Part A.** YAML (Part A) is the format of all my manifests. Keeping credentials on the backend (Part A, AI platforms) is the same rule I would follow for any API key I added later.

## Repository structure

```text
backend/        Flask app (app.py, Dockerfile, requirements.txt)
db/init/        MySQL init script
frontend/       Nginx frontend and screenshots-week5/
rahti/          Kubernetes/OpenShift YAML files
docker-compose.dev.yml, docker-compose.prod.yml
```

## Cleanup

These Rahti resources are temporary course resources. I will remove them after peer review.
