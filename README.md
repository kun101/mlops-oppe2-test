# MLOps OPPE-2 Quick Reference (Fraud Detection)

> **Purpose**  
> Fast lookup during exam. Commands and facts only.  
> Stack: FastAPI + Docker + GitHub Actions + GKE + DVC + MLflow + Locust + OpenTelemetry  
> Project: `sixth-sequencer-473212-e7`  
> Namespace: `fraud-ml`

---

## 1. Live Prediction Endpoint (MOST IMPORTANT)

**Endpoint**
POST http://34.46.192.132/predict

cpp
Copy code

**Test**
```bash
curl -X POST http://34.46.192.132/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Time": 1,
    "V1": 0, "V2": 0, "V3": 0, "V4": 0,
    "V5": 0, "V6": 0, "V7": 0, "V8": 0,
    "V9": 0, "V10": 0, "V11": 0, "V12": 0,
    "V13": 0, "V14": 0, "V15": 0,
    "V16": 0, "V17": 0, "V18": 0,
    "V19": 0, "V20": 0, "V21": 0,
    "V22": 0, "V23": 0, "V24": 0,
    "V25": 0, "V26": 0, "V27": 0,
    "V28": 0,
    "Amount": 100
  }'
Expected:

json
Copy code
{ "prediction": 0, "probability": 0.xxx }
2. FastAPI + OpenTelemetry (Deliverable: Observability)
Requirement

Custom span around model inference

Key code

python
Copy code
with tracer.start_as_current_span("model_predict"):
    prob = model.predict_proba(X)[0][1]
Verify traces

bash
Copy code
kubectl logs deployment/fraud-api -n fraud-ml
Look for:

less
Copy code
Span(name="model_predict", ...)
3. Docker & Artifact Registry
Artifact Registry repo

bash
Copy code
us-central1-docker.pkg.dev/sixth-sequencer-473212-e7/fraud-detection-repo
Exam-safe push (latest tag)

bash
Copy code
docker build -t us-central1-docker.pkg.dev/sixth-sequencer-473212-e7/fraud-detection-repo/fraud-detection-api:latest .
docker push us-central1-docker.pkg.dev/sixth-sequencer-473212-e7/fraud-detection-repo/fraud-detection-api:latest
4. Kubernetes Core Commands
Check service & external IP

bash
Copy code
kubectl get svc -n fraud-ml
Check pods

bash
Copy code
kubectl get pods -n fraud-ml
Expected:

sql
Copy code
1/1 Running
Restart deployment

bash
Copy code
kubectl rollout restart deployment fraud-api -n fraud-ml
Fix ImagePullBackOff quickly

bash
Copy code
kubectl set image deployment/fraud-api \
  fraud-api=us-central1-docker.pkg.dev/sixth-sequencer-473212-e7/fraud-detection-repo/fraud-detection-api:latest \
  -n fraud-ml
5. HPA (Autoscaling)
Check HPA

bash
Copy code
kubectl get hpa -n fraud-ml
kubectl describe hpa fraud-api-hpa -n fraud-ml
Watch scaling

bash
Copy code
kubectl get pods -n fraud-ml -w
6. Load Testing (Locust)
Start Locust

bash
Copy code
locust -f locustfile.py --host=http://34.46.192.132 --web-host=127.0.0.1
UI access

Vertex AI Workbench → Open Port → 8089

Test parameters

yaml
Copy code
Users: 200–500
Spawn rate: 10
7. DVC (Data Versioning)
Health check

bash
Copy code
dvc status
Expected:

vbnet
Copy code
Data and pipelines are up to date.
List remotes

bash
Copy code
dvc remote list
Verify GCS objects

bash
Copy code
gsutil ls gs://oppe-2-dvc-sixth-sequencer
⚠️ Do NOT use:

bash
Copy code
dvc list gs://...
8. Data Poisoning (Deliverable 3)
Poisoned datasets

bash
Copy code
data/v0/poisoned_2_percent.csv
data/v0/poisoned_8_percent.csv
data/v0/poisoned_20_percent.csv
Generate poisoned data

bash
Copy code
python scripts/poison.py
Train & log MLflow runs

bash
Copy code
python scripts/train_poisoned_mlflow.py
9. MLflow
Start server

bash
Copy code
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root gs://oppe-2-mlflow-sixth-sequencer \
  --host 0.0.0.0 \
  --port 5000
UI

cpp
Copy code
http://136.116.2.17:5000
Expected:

3 runs

param: poisoning_level

metric: f1_score

10. GitHub Actions / CI-CD
Workflow

bash
Copy code
.github/workflows/mlops_pipeline.yml
Push everything

bash
Copy code
git add .
git commit -m "feat: complete end-to-end MLOps fraud pipeline"
git push origin main
Verify

GitHub → Actions → green check

11. Common Fixes
Editor stuck (kubectl edit)

bash
Copy code
export EDITOR=nano
kubectl edit deployment fraud-api -n fraud-ml
ImagePullBackOff

bash
Copy code
kubectl set image deployment/fraud-api fraud-api=...:latest -n fraud-ml
kubectl rollout restart deployment fraud-api -n fraud-ml
Locust UI not opening

Use Workbench port forwarding for 8089

