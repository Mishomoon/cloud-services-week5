# Cloud Services – Week 5: Redis and a visitor counter

This is my Week 5 project. It is the Week 4 app (Nginx frontend, Flask/Gunicorn backend, MySQL) on CSC Rahti, with Redis added as a new part. The backend uses Redis for a visitor counter.

Live app: https://frontend-cloud-services-week5.2.rahtiapp.fi
GitHub: https://github.com/Mishomoon/cloud-services-week5

## Architecture

```text
User -> Rahti Route -> Nginx frontend -> Flask backend -> Redis (visitor counter)
                                                       -> MySQL (database)
```

Redis runs in its own pod with its own Deployment and Service. It is not inside the backend container. It has no Route, so only the backend can reach it.

## What I added

- `rahti/redis-deployment.yaml`: the Redis Deployment (Redis image, port 6379)
- `rahti/redis-service.yaml`: a Service named `redis` on port 6379
- `rahti/configmap.yaml`: the backend config, including `REDIS_HOST=redis`
- `backend/requirements.txt`: added the `redis` package
- `backend/app.py`: the new `/api/visitor` endpoint

## How the visitor counter works

The backend connects to Redis with the Service name, which it gets from the ConfigMap:

```python
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)
```

Every request to `/api/visitor` runs `redis_client.incr("visitor_count")` and returns the new number:

```json
{ "visits": 5 }
```

The backend gets its config with `envFrom` and the `backend-config` ConfigMap, so nothing is hard-coded.

## Problems I had

**Redis permission error.** Redis could not save its RDB file in `/data`, and the backend got errors. Redis is only a cache here, so I turned off RDB snapshots and append-only mode. (`redis-error.png`)

**CPU quota.** When I updated the Redis Deployment, the new pod would not start. My project had already used its 4 CPUs and the new pod asked for another 500m. The old Redis pod kept running, so the problem was the quota and not the Service. (`CPU-quota.png`)

**ImagePullBackOff.** The frontend pod could not pull its image because the tag was not on Docker Hub. I pushed `mishmoon/frontend:1.8` again and updated the Deployment, and then the pod started.

## Evidence

The screenshots are in `frontend/screenshots-week5/`:

- `Week 5 Deployment Status.png`: pods for frontend, backend, MySQL and Redis
- `week5-services.png`: services, including Redis on 6379
- `week5-redis-deployment.png`: Redis running as its own Deployment
- `configmap.yaml.png`: the Redis host in the ConfigMap
- `requirements.txt.png`: the Redis package
- `visitor count.png`: the visitor counter test

## If this went to production

- Redis loses its data when the pod restarts, so the counter starts from zero again. MySQL stays the main database because it uses persistent storage.
- Cached data can get old. I would use a TTL, or delete the key when the data in MySQL changes.
- One Redis replica is fine for a course project. Production would need monitoring and a better setup.
- Redis is only reachable through an internal Service, and no passwords are committed to this repo.

## Project structure

```text
backend/       Flask app (app.py, Dockerfile, requirements.txt)
db/init/       MySQL init script
frontend/      Nginx frontend and screenshots-week5/
rahti/         Kubernetes/OpenShift YAML files
docker-compose.dev.yml, docker-compose.prod.yml
```

I will remove the Rahti resources after the peer review.
