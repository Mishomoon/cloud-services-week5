# Cloud Services – Week 5

## Project Overview

This repository contains my Cloud Services Week 5 project.

In Week 5, I extended the multi-container application that was created during the previous week. The application is deployed on CSC Rahti using OpenShift.

The main goal of this week was to add and deploy an additional component while keeping the existing application working. I also worked with OpenShift Deployments, Services, Routes, container images, networking, configuration, testing and troubleshooting.

The application can be accessed through the public Rahti Route:

https://frontend-cloud-services-week5.2.rahtiapp.fi/

---

## Application Architecture

The Week 5 application is based on the multi-container architecture from Week 4.

The main components are:

- Frontend
- Backend
- MySQL database
- Additional Week 5 component
- OpenShift Services
- OpenShift Route

The general application flow is:

    Internet
       |
       v
    OpenShift Route
       |
       v
    Frontend
       |
       v
    Backend
       |
       +----------------+
       |                |
       v                v
     MySQL        Week 5 component

Each application component runs in its own container and is managed by OpenShift.

The frontend is exposed through the public Rahti Route. The backend communicates with the other services through the internal OpenShift network.

---

## Deployment on Rahti

The application was deployed to CSC Rahti using OpenShift.

The deployment uses OpenShift resources such as:

- Deployments
- Pods
- Services
- Routes
- ConfigMaps and/or Secrets where needed

The application was checked using OpenShift CLI commands.

For example:

    oc get pods

This command was used to check whether the application pods were running correctly.

Services were checked with:

    oc get svc

Deployments were checked with:

    oc get deployment

The public Route was checked with:

    oc get route

These commands helped verify that the different parts of the application were correctly deployed.

---

## Containers

Each application component runs inside a container.

The containers provide an isolated environment for the application services. OpenShift manages the containers through Pods and Deployments.

The frontend container is responsible for serving the web application.

The backend container provides the application/API functionality.

The MySQL container provides the database used by the application.

The additional Week 5 component is deployed independently so that it can be managed separately from the other components.

---

## OpenShift Services

OpenShift Services provide stable internal access to the application components.

Instead of connecting directly to a Pod IP address, other components can communicate with a Service.

This is important because Pod IP addresses can change when Pods are recreated.

The application therefore uses OpenShift networking to allow the different containers to communicate with each other.

For example, the backend can communicate with internal services using their Service names instead of depending on temporary Pod IP addresses.

---

## Public Route

The frontend is exposed through an OpenShift Route.

The public application can be accessed here:

https://frontend-cloud-services-week5.2.rahtiapp.fi/

The Route makes it possible to access the application from a web browser without directly exposing the individual Pods.

---

## Testing

After deployment, I tested the application through the public Rahti URL.

I also checked the status of the application using OpenShift commands.

Important commands used during testing included:

    oc get pods

    oc get svc

    oc get deployment

    oc get route

The purpose of these tests was to verify that:

- the Pods were running
- the Deployments were available
- the Services existed
- the Route was available
- the application could be accessed through the browser
- the different application components could communicate with each other

---

## Troubleshooting

When problems occurred, I used OpenShift commands to investigate them.

For example, Pod information can be inspected with:

    oc describe pod <pod-name>

Container logs can be viewed with:

    oc logs <pod-name>

The Deployment status can be checked with:

    oc rollout status deployment/<deployment-name>

These commands make it possible to find configuration problems, container errors and deployment issues.

Checking the Pods first is useful because it quickly shows whether a component is Running, Pending, restarting or failing.

---

## Security and Reliability

Security and reliability are important when deploying applications in a cloud environment.

Credentials and other sensitive information should not be stored directly in source code or committed to GitHub.

Secrets can be used for sensitive configuration instead of placing passwords or tokens directly into application files.

The application should also use the internal OpenShift network for communication between services whenever possible.

Another important reliability consideration is that Pods can be recreated by OpenShift. The application should therefore not depend on a specific Pod IP address.

Using Services provides a stable way for components to communicate even when Pods are replaced.

---

## Problems Encountered

During the Week 5 work, deployment and configuration issues were investigated using OpenShift.

The main troubleshooting approach was:

1. Check the Pods.

       oc get pods

2. Check the Services.

       oc get svc

3. Check the Deployment.

       oc get deployment

4. Inspect a problematic Pod.

       oc describe pod <pod-name>

5. Check container logs.

       oc logs <pod-name>

6. Check the rollout status.

       oc rollout status deployment/<deployment-name>

This helped identify whether a problem was related to the container, deployment, networking or configuration.

---

## What I Learned

During Week 5, I learned more about deploying multi-container applications using OpenShift and Rahti.

I learned how:

- Pods run containers in OpenShift
- Deployments manage application Pods
- Services provide stable internal networking
- Routes expose applications publicly
- OpenShift can recreate Pods
- containerized services communicate through the OpenShift network
- `oc` commands can be used to inspect and troubleshoot applications
- logs can be used to investigate application problems
- cloud applications need to consider security and reliability

I also gained more practical experience working with a real application deployed in a cloud environment rather than only running the containers locally.

---

## Project Structure

The repository contains the files needed for the Week 5 application and its deployment.

The project includes the application source code, container configuration and OpenShift-related configuration used during the assignment.

The GitHub repository provides the complete project files and allows the implementation to be reviewed.

---

## Live Application

The deployed Week 5 application is available here:

https://frontend-cloud-services-week5.2.rahtiapp.fi/

---

## GitHub Repository

The complete Week 5 project is available in this GitHub repository:

https://github.com/Mishomoon/cloud-services-week5

The repository contains the source code and configuration files used for the Week 5 project.

---

## Conclusion

Week 5 extended the previous multi-container application by adding another independently deployed component.

The application was deployed to CSC Rahti using OpenShift and tested through the public Route.

Through this assignment, I gained practical experience with containers, OpenShift Deployments, Pods, Services, Routes, networking, troubleshooting, security and reliability.

The final application is available through the public Rahti URL, and the complete project is available in the GitHub repository.
