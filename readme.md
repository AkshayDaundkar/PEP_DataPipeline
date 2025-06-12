# 🌱 Energy Data Pipeline — Full Stack Project

This project simulates a real-time data pipeline on mock data for PEP renewable energy company, providing data ingestion, processing, storage, analytics, and a beautiful full-stack dashboard interface.

---

### Live link:- https://pep-datapipeline-frontend.onrender.com/

## Project Structure

```
PEP DATA ASSESSMENT/
├── backend/          # FastAPI, Lambda, DynamoDB, S3, Terraform
├── frontend/         # React + Vite + Tailwind Dashboard UI
```

---

## Backend Overview — `/backend`

### 🔹 `api/app.py` (FastAPI)

- `/simulate` — Uploads one file with energy data to S3
- `/file/{filename}` — Returns file content from S3
- `/records` — Fetches all processed records for a `site_id` from DynamoDB
- `/all-records` — Scans entire DynamoDB table (used for graphs)
- Includes CORS support for React frontend

### 🔹 `data/simulate_data.py`

- Generates random JSON for multiple sites:

  - `site_id`, `timestamp`, `energy_generated_kwh`, `energy_consumed_kwh`

- Uploads the file to S3
- Exposed to FastAPI via `/simulate`

### 🔹 `lambda/process_data.py`

- Lambda triggered by new S3 files
- Parses file → computes:

  - `net_energy_kwh = generated - consumed`
  - Flags `anomaly` if generated or consumed is negative

- Writes each entry to DynamoDB (`energy_data` table)

### 🔹 `terraform/`

- Provisions the entire backend infra:

  - `S3`, `DynamoDB`, `Lambda`, `IAM Roles`

- Key files:

  - `main.tf`, `outputs.tf`, `variables.tf`
  - `function.zip` for Lambda deployment
  - You have to run aws configure on Command Line & optionally have to Install AWS CLI And run this Commands
    This stores credentials in your AWS CLI config, and Terraform automatically uses them.
    ```bash
    aws configure
    -	AWS Access Key ID [None]: <your-access-key-id>
    -	AWS Secret Access Key [None]: <your-secret-access-key>
    -	Default region name [None]: us-east-1
    -	Default output format [None]: json
    ```

### 🔹 `visualization/app.py`

- Local Streamlit dashboard (optional)
- Superseded by frontend charts

## Real-Time Anomaly Alerting via AWS SNS

- **SNS Topic (`energy-anomaly-alerts`)** is created using Terraform.
- **Email subscription** for alerts is configured through a Terraform variable.
- **Lambda Function** is updated to publish an alert when:
  - `energy_generated_kwh < 0` or
  - `energy_consumed_kwh < 0`

### Setup Instructions

1. **Edit your `terraform.tfvars` file** and add:
   ```hcl
   alert_email = "your.email@example.com"
   ```

## \*\* If an anomaly is `present`, you’ll receive an email alert like:

###

![SNS Anomaly Alert in Mail](https://drive.google.com/file/d/1dbN-iH13BfYBzcqPmafkDe4j7PoAAFe2/view?usp=sharing)

```bash
Anomaly Detected!
Site: test-site-123
Timestamp: 2025-06-11T20:00:00Z
Generated: -10
Consumed: 20
```

###

---

## Frontend Overview — `/frontend`

### Built With:

- **React + Vite** for fast builds
- **Tailwind CSS** for clean design
- **Recharts** for visualization

### 📂 Folder Structure

```
src/
├── components/
│   ├── Extras/
│   │   ├── Sidebar.jsx
│   │   ├── SimulatePanel.jsx
│   ├── FileViewer/
│   │   ├── FileList.jsx
│   │   ├── FileViewer.jsx
│   ├── Charts/
│   │   ├── EnergyComparisonChart.jsx
│   │   ├── AnomalyDistributionChart.jsx
│   │   ├── EnergyTrendChart.jsx
│   ├── ProcessData/
│   │   ├── ProcessData.jsx
│   │   ├── ProcessedDataTable.jsx
├── pages/
│   ├── Files.jsx
│   ├── Graphs.jsx
├── App.jsx
├── index.css, main.jsx
```

### Features

#### Simulate Data

- Trigger one-time or continuous data uploads (every 2 minutes)
- Stores filenames and timestamps in localStorage
- Logs uploads and shows latest file

#### File Viewer

- Lists all generated files (from localStorage)
- View file content (fetched from backend `/file/<filename>`)

#### Graphs (Dynamic Visualization)

- Energy generated vs consumed (Bar chart)
- Anomalies per site (Bar chart)
- Net energy trend over time (Line chart)

#### Processed Data Viewer

- Input `site_id` to view all DynamoDB-processed records
- Table includes: `timestamp`, `generated`, `consumed`, `net`, `anomaly`
- Highlights anomaly rows

### ⚡ UI

- Sidebar layout inspired by Daxwell’s SmartBot
- Fully responsive, mobile-friendly layout
- Elegant cards, buttons, modals (Tailwind-based)

---

## 🛠️ Setup Instructions

### 1. Backend

```bash
cd backend
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate
pip install -r requirements.txt

# Start FastAPI
uvicorn api.app:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. Terraform Infra Setup

```bash
cd terraform
terraform init
terraform apply
```

Ensure AWS CLI is configured and credentials are active.

---

## Sample Flow

1. Simulate data → JSON file goes to S3
2. Lambda triggers → Data processed → Records saved to DynamoDB
3. Frontend:

   - See simulation logs
   - Browse file content
   - Analyze energy trends + anomalies

---

## Teardown Checklist

```bash
cd terraform
terraform destroy
```

- Delete S3 bucket contents
- Delete DynamoDB table
- Remove Lambda, IAM roles

---

## Notes

- Tailwind uses system font stack
- All charts auto-size
- Dynamically pulled data from backend
- Logs are stored in localStorage

---

## Future Enhancements

- Add user authentication (AWS Cognito or JWT)
- Export charts/records to CSV
- SNS/Email alerts for anomalies
- Date filters and dynamic queries
- CI/CD pipeline using GitHub Actions

---

## Author

Akshay Daundkar
Built for Private Energy Partners Assessment
2025
