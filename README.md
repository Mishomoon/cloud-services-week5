# Cloud Services – Week 5

## Overview

This project is the Week 5 continuation of the Cloud Services application developed during Week 4.

The main goal of Week 5 was to extend the existing application with **Redis caching** and a **visitor counter**, while keeping the application running as a multi-container application in Rahti.

The project contains a frontend, backend, MySQL database, and Redis service. The application is deployed using Kubernetes/OpenShift resources in Rahti.

The Week 5 work also includes Kubernetes configuration, Redis deployment and service configuration, environment variables, resource limits, and documentation screenshots.

---

## Technologies Used

- Docker
- Docker Hub
- Kubernetes
- OpenShift / Rahti
- Redis
- MySQL
- Flask
- Python
- Nginx
- Git
- GitHub
- PowerShell
- YAML

---

## Application Architecture

The application consists of four main services:

```text
                    User
                      |
                      v
                 Nginx Frontend
                      |
                      v
                 Flask Backend
                  /         \
                 /           \
                v             v
             MySQL          Redis
            Database       Cache / Counter
```

### Frontend

The frontend is served by Nginx.

It provides the web interface and communicates with the Flask backend.

### Backend

The backend is a Flask application running with Gunicorn.

The backend communicates with:

- MySQL for database operations
- Redis for the visitor counter

### MySQL

MySQL is used as the application's database.

The database stores the application data and continues to use persistent storage through Kubernetes persistent volume configuration.

### Redis

Redis was introduced in Week 5.

Redis is used as an in-memory data store and is used in this project for the visitor counter.

---

## Week 5 Main Task

The main new feature in Week 5 was adding Redis to the existing application.

The backend connects to Redis using the Redis hostname provided through the environment.

The backend uses the Redis `INCR` operation to increase the visitor count whenever the visitor endpoint is requested.

The relevant backend endpoint is:

```text
/api/visitor
```

The endpoint increases the Redis counter and returns the current number of visits.

Example response:

```json
{
  "visits": 5
}
```

Every request to the endpoint increases the counter.

---

## Redis Configuration

Redis was added as a separate Kubernetes/OpenShift workload.

The project contains:

```text
rahti/redis-deployment.yaml
rahti/redis-service.yaml
```

The Redis Deployment creates the Redis Pod.

The Redis Service provides a stable network name that the backend can use to communicate with Redis.

The backend uses:

```text
REDIS_HOST=redis
```

so that the backend can find the Redis service inside the Kubernetes cluster.

### Redis Deployment

The Redis deployment is defined in:

```text
rahti/redis-deployment.yaml
```

The Deployment is responsible for creating and maintaining the Redis Pod.

The Redis container uses a Redis image and exposes the Redis port:

```text
6379
```

The Redis Deployment was tested in the Week 5 Rahti project.

The Redis Pod was checked with:

```bash
oc get pods
```

The expected result is that the Redis Pod is running.

Example:

```text
redis-xxxxxxxxxx-xxxxx   1/1   Running   0
```

### Redis Service

The Redis Service is defined in:

```text
rahti/redis-service.yaml
```

The Service provides internal cluster networking for Redis.

The backend does not need to know the Redis Pod IP address.

Instead, it connects to:

```text
redis:6379
```

Kubernetes/OpenShift resolves the service name `redis` to the Redis service.

This makes communication between the backend and Redis easier and more reliable.

### Backend Redis Connection

The Flask backend creates a Redis client using the Redis hostname:

```python
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)
```

The default Redis hostname is:

```text
redis
```

The Redis port is:

```text
6379
```

The backend therefore communicates with the Redis Kubernetes Service rather than directly connecting to a Redis Pod.

---

## Visitor Counter

The visitor counter is implemented using Redis.

The endpoint is:

```text
/api/visitor
```

The backend uses:

```python
redis_client.incr("visitor_count")
```

The `INCR` operation increases the Redis value by one.

The current value is then returned to the frontend as JSON.

Example:

```json
{
  "visits": 1
}
```

After another request:

```json
{
  "visits": 2
}
```

This demonstrates that Redis is being used to maintain the visitor count.

---

## Kubernetes / Rahti Resources

The project contains several Kubernetes/OpenShift YAML files.

Important files include:

```text
rahti/backend-deployment.yaml
rahti/backend-service.yaml
rahti/configmap.yaml

rahti/frontend-deployment.yaml
rahti/frontend-service.yaml

rahti/mysql-deployment.yaml
rahti/mysql-pvc.yaml
rahti/mysql-service.yaml

rahti/redis-deployment.yaml
rahti/redis-service.yaml
```

These files define the application's workloads and networking resources.

### ConfigMap

The backend configuration is stored using a Kubernetes ConfigMap.

The configuration includes environment variables needed by the backend.

The backend Deployment uses:

```yaml
envFrom:
  - configMapRef:
      name: backend-config
```

This allows the backend container to receive its configuration without hard-coding all configuration values directly into the application code.

The Redis hostname is configured so that the backend can connect to the Redis Service.

### Resource Limits

Resource configuration was also used in the Week 5 deployment.

For example, CPU and memory settings can be specified for containers.

Resource limits help prevent a container from using unlimited cluster resources.

The project includes documentation screenshots showing the resource configuration and deployment status.

---

## Docker

The application uses Docker containers.

The frontend uses an Nginx-based container.

The backend uses a Python-based container running Flask through Gunicorn.

Docker images were built locally and pushed to Docker Hub.

Example image naming:

```text
mishmoon/frontend
mishmoon/backend
```

Version tags were used to identify different application versions.

### Docker Hub

The Docker images are stored in Docker Hub so that Rahti can pull the images when creating the application Pods.

For example:

```text
mishmoon/frontend:1.8
```

was used for the Week 5 frontend deployment.

The image was pushed using:

```bash
docker push mishmoon/frontend:1.8
```

After pushing the image, the OpenShift deployment was updated to use the new image.

---

## Deployment to Rahti

The application was deployed to the CSC Rahti environment.

The project used OpenShift commands through the `oc` command-line tool.

Useful commands include:

```bash
oc get pods
```

to see the running Pods.

```bash
oc get services
```

to see the Kubernetes/OpenShift Services.

```bash
oc get deployments
```

to see the Deployments.

```bash
oc describe pod <pod-name>
```

to inspect a Pod and its events.

These commands were used to troubleshoot the deployment and verify that the application was running correctly.

---

## Troubleshooting

During the Week 5 deployment, the frontend initially showed an `ImagePullBackOff` state.

The Pod description showed that the cluster initially could not find the requested image manifest.

The image was then pushed again to Docker Hub and the frontend Deployment was updated to use the correct image version.

After updating the Deployment, the frontend Pod started successfully.

The final status showed all main application components running.

Example:

```text
backend    1/1   Running
frontend   1/1   Running
mysql      1/1   Running
redis      1/1   Running
```

This confirmed that the application components were running in Rahti.

---

## Week 5 Frontend

The frontend was updated to show the Week 5 application.

The frontend includes documentation and screenshots related to the Week 5 work.

The Week 5 screenshot files are stored in:

```text
frontend/screenshots-week5/
```

The screenshots include evidence related to:

- Redis deployment
- Redis service
- Redis configuration
- Redis error troubleshooting
- CPU quota
- Requirements
- Week 5 deployment status
- Visitor count
- Week 5 services

---

## Screenshots

The project contains documentation screenshots in:

```text
frontend/screenshots-week5/
```

Important screenshots include:

```text
CPU-quota.png
Week 5 Deployment Status.png
configmap.yaml.png
redis-deployment.png
redis-error.png
redis-service.png
requirements.txt.png
visitor count.png
week5-redis-deployment.png
week5-services.png
```

These screenshots document the configuration, deployment, troubleshooting, and final state of the Week 5 application.

---

## Verification

The following checks were used to verify the application.

### Check Pods

```bash
oc get pods
```

This shows whether the application Pods are running.

### Check Deployments

```bash
oc get deployments
```

This shows the current Deployments and their replica status.

### Check Services

```bash
oc get services
```

This shows the services used for internal and external communication.

### Inspect a Pod

```bash
oc describe pod <pod-name>
```

This can be used to inspect:

- container image
- Pod status
- environment configuration
- events
- image pull errors
- container state

### Visitor Counter Test

The visitor counter can be tested through the deployed application.

The backend endpoint is:

```text
/api/visitor
```

Each request increases the Redis counter.

For example:

```text
First request  → visits: 1
Second request → visits: 2
Third request  → visits: 3
```

This demonstrates that Redis is being used by the backend.

---

## Project Structure

The main project structure is:

```text
cloud-services-week5/
│
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── db/
│   └── init/
│       └── 01-init.sql
│
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── nginx.conf
│   └── screenshots-week5/
│       ├── CPU-quota.png
│       ├── Week 5 Deployment Status.png
│       ├── configmap.yaml.png
│       ├── redis-deployment.png
│       ├── redis-error.png
│       ├── redis-service.png
│       ├── requirements.txt.png
│       ├── visitor count.png
│       ├── week5-redis-deployment.png
│       └── week5-services.png
│
├── rahti/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── configmap.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── mysql-deployment.yaml
│   ├── mysql-pvc.yaml
│   ├── mysql-service.yaml
│   ├── redis-deployment.yaml
│   └── redis-service.yaml
│
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── package-lock.json
└── .gitignore
```

---

## Main Week 5 Learning Outcomes

During Week 5, the application was extended with Redis and Kubernetes configuration.

The main things demonstrated were:

- Running Redis as a separate container/workload
- Connecting Flask to Redis
- Using Redis for a visitor counter
- Creating a Redis Deployment
- Creating a Redis Service
- Using ConfigMaps for configuration
- Building and pushing Docker images
- Updating Kubernetes/OpenShift Deployments
- Troubleshooting image pull problems
- Checking Pods and Services in Rahti
- Documenting the deployment with screenshots

---

## Final Result

The final Week 5 application contains:

```text
Frontend
   ↓
Backend
   ↓
 ┌───────────────┐
 │               │
MySQL          Redis
Database       Visitor Counter
```

The application was successfully containerized and deployed to Rahti.

The frontend was accessible through the Rahti route, while the backend communicated internally with MySQL and Redis through Kubernetes/OpenShift Services.

The Week 5 implementation provides the foundation for the next Cloud Services tasks, where the application can be extended with additional cloud-native functionality.

---

## Repository

GitHub repository:

https://github.com/Mishomoon/cloud-services-week5

## Deployment URL

Week 5 frontend:

https://frontend-cloud-services-week5.2.rahtiapp.fi

---

## Conclusion

Week 5 extended the previous cloud application by introducing Redis and a Redis-based visitor counter.

The project demonstrates how multiple containerized services can communicate inside a Kubernetes/OpenShift environment.

The final application consists of a frontend, Flask backend, MySQL database, and Redis service. Docker images are stored in Docker Hub and the application is deployed to CSC Rahti.

The project also includes Kubernetes configuration files, deployment evidence, troubleshooting screenshots, and documentation of the Week 5 implementation.
