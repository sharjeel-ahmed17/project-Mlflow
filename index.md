Build and run again:
docker build -t ship .
docker run -p 8000:8000 --env-file .env ship
If this works, you know 100% that the problem is just the MLflow Model Name/Registry, not Docker.

register model
Ship_Fuel_Consumption_Model

docker tag ship sharjeelahmed017/ship:latest

To get your application running on Kubernetes, follow these steps:

### 1. Create the MLflow Secrets

Since the `deployment.yaml` references `mlflow-secrets`, you must create this secret in your cluster so the app can connect to DagsHub. Run this command (replacing the placeholders):

```bash
kubectl create secret generic mlflow-secrets \
  --from-literal=tracking_uri='YOUR_MLFLOW_TRACKING_URI' \
  --from-literal=username='YOUR_DAGS_HUB_USERNAME' \
  --from-literal=password='YOUR_DAGS_HUB_TOKEN'
```

### 2. Deploy to Kubernetes

Apply the manifest files created in the `k8s` directory:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 3. Verify the Deployment

Check the status of your pods and service:

```bash
# Check pods status
kubectl get pods

# Get the external IP of the LoadBalancer
kubectl get service ship-fuel-prediction-service
```

### 4. Test the API

Once you have the External IP, you can test the prediction endpoint:

```bash
curl http://<EXTERNAL_IP>/predict -X POST -d '{"ship_type": "Bulk Carrier", "month": "January", "distance": 1000, "fuel_type": "HFO", "weather_conditions": "Clear", "engine_efficiency": 0.85}'
```

**Would you like me to help you write a script to automate the secret creation or a health check probe for the deployment?**

## minikube

Setting up Minikube is a great way to run a local Kubernetes cluster. Since you are using **WSL2** (based on your previous terminal output), the setup requires a few specific steps to ensure the Linux environment can communicate with the Kubernetes VM.

Here is the step-by-step guide to setting up Minikube on Windows with WSL2.

### 1. Prerequisites

Ensure you have the following installed:

- **Docker Desktop** (already installed, as you have a Docker Hub image).
- Ensure **WSL2** is updated (`wsl --update` in PowerShell).

---

### 2. Install kubectl (The CLI Tool)

If you haven't installed the Kubernetes CLI yet, run this in your WSL2 terminal:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### 3. Install Minikube

Run the official installation script in your WSL2 terminal:

```bash
curl -LO https://minikube.sigs.k8s.io/kubernetes-driver-installer/minikube/minikube-installer.sh
sudo bash minikube-installer.sh
```

### 4. Start Minikube (WSL2 Specific)

Since you have Docker Desktop installed, you should use the **docker driver**. This is the most stable way to run Minikube in WSL2.

Run this command to start the cluster:

```bash
minikube start --driver=docker
```

**If it fails with a permission error**, you may need to run it with `sudo` or add your user to the docker group:
`sudo usermod -aG docker $USER && newgrp docker`

### 5. Verify the Setup

Once it starts, verify that `kubectl` is pointing to Minikube:

```bash
kubectl cluster-info
```

You should see a message saying: `Kubernetes control plane is running`.

---

### 6. Deploy Your Project

Now that the cluster is running, you can execute the steps we discussed earlier:

**Step A: Create the secret**

**Step B: Apply your manifests**

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 7. Accessing your App (Minikube Tunnel)

In standard Kubernetes (Cloud), a `LoadBalancer` gives you a real IP. In Minikube, it stays `<pending>`. To get the IP on your local machine, run this in a **separate terminal window** and keep it open:

```bash
minikube tunnel
```

Then, you can get the IP using:

```bash
kubectl get service ship-fuel-prediction-service
```

**Let me know if you run into any errors during the `minikube start` process!**
