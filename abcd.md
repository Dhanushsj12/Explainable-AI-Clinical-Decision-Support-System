# Explainable AI Clinical Decision Support System (XAI-CDSS)
## Comprehensive Technical Manual, Architectural Specification, and IEEE Conference Research Framework

---

## 1. Executive Summary & Project Overview

The **Explainable AI Clinical Decision Support System (XAI-CDSS)** is an enterprise-grade, medically grounded, multi-disease risk assessment platform designed to eliminate the **"black-box" dilemma** of artificial intelligence in healthcare. 

While conventional Machine Learning (ML) classifiers can achieve high predictive accuracy, their adoption in real-world clinical practice is hindered by opacity, lack of interpretability, and vulnerability to conflicting explanations. This system bridges the translational gap between machine learning algorithms and bedside clinicians by combining:

1. **Multi-Disease Predictive AI**: High-accuracy supervised classification models for **Heart Disease**, **Diabetes**, **Chronic Kidney Disease (CKD)**, and **Stroke Risk**.
2. **Triangulated Explainability (SHAP + LIME)**: Dual local interpretability engines that compute cooperative game-theoretic attribution (SHAP) alongside local surrogate perturbation (LIME).
3. **Explanation Reliability & Consistency Index (ERI)** *(Novelty Claim 1)*: A mathematical meta-metric that quantifies concordance between SHAP and LIME across feature overlap, sign directionality, and rank ordering.
4. **Dual-Tier Constrained Counterfactual Analysis Engine** *(Novelty Claim 2)*: A decision-support recourse engine that partitions model-generated hypothetical what-if simulations into **Tier 1 (Single-Biomarker $L_0=1$)** and **Tier 2 (Multi-Biomarker $L_0 \ge 2$, with $L_0=2$ demonstrated)** while strictly enforcing biological and demographic **immutability guardrails** (Age, Biological Sex locked). Crucially, these counterfactuals represent classifier decision-boundary explorations, not clinical prescriptions or treatment targets.
5. **Role-Based Access Control (RBAC) & Institutional Security**: A persistent SQLite-backed authorization layer supporting distinct workflows for **Admins**, **Doctors**, and **Clinical Staff**.
6. **Clinical Documentation & Audit Trail**: Real-time PDF medical dossier generation (ReportLab) and SQLite clinical case history logging.

---

## 2. System Architecture & Tech Stack

```
+-----------------------------------------------------------------------------------+
|                                  CLIENT TIER                                      |
|  React 19 + Vite + React Router 7 + Axios Interceptors                            |
|  Theme: Clinical Minimalist (Sky Blue #4aa9dc, Navy #102d4a, White #ffffff)      |
|                                                                                   |
|  [Admin Dashboard]          [Doctor CDSS Portal]          [Staff Intake Portal]   |
|   - User Management          - Patient Form                - Patient Form         |
|   - Role Promotion           - SHAP / LIME / ERI           - SHAP / LIME / ERI    |
|   - Institutional Stats      - Dual-Tier Counterfactuals   - Counterfactuals      |
|                              - Patient History / Archive   - PDF Dossier Export   |
|                              - PDF Dossier Export                                 |
+------------------------------------------+----------------------------------------+
                                           | HTTP / REST (JWT Bearer Auth)
                                           v
+-----------------------------------------------------------------------------------+
|                                  BACKEND API                                      |
|  Flask Application Server (0.0.0.0:5000)                                          |
|                                                                                   |
|  [/auth/*]           [/predict]               [/report]          [/history]       |
|  - login             - Model Execution        - PDF Generation   - Doctor-only    |
|  - signup            - SHAP Attributions      - ReportLab        - DB Query       |
|  - me                - LIME Attributions                                          |
|  - users (Admin)     - ERI Concordance        [/stats]                            |
|  - role (Admin)      - Dual-Tier CF Engine    - System Metrics                    |
+--------------------+---------------------+--------------------+-------------------+
                     |                     |                    |
                     v                     v                    v
+--------------------+---+   +-------------+------+   +---------+-------------------+
|      DATABASE LAYER    |   | MACHINE LEARNING   |   |   EXPLAINABILITY (XAI)      |
|  SQLite 3 Persistence  |   | Joblib Serialized  |   |                             |
|  - users.db            |   | - Heart (RF)       |   | - TreeExplainer (SHAP)      |
|    * id, email, role   |   | - Diabetes (DT/RF) |   | - LinearExplainer (SHAP)    |
|    * pwd_hash          |   | - CKD (RF)         |   | - LimeTabularExplainer      |
|  - predictions.db      |   | - Stroke (LogReg)  |   | - ERI Consensus Metric      |
|    * patient_id, risk  |   | - StandardScalers  |   | - Dual-Tier CF Engine       |
+------------------------+   +--------------------+   +-----------------------------+
```

### Technology Matrix

| Layer | Technologies Used | Primary Responsibilities |
| :--- | :--- | :--- |
| **Frontend UI** | React 19, Vite 8, React Router 7, Axios 1.19 | Responsive clinical UI, dynamic form input, multi-XAI charts, dual-tier counterfactual presentation, PDF triggers |
| **Styling** | Vanilla Modular CSS (`theme.css`) | Sky Blue (`#4aa9dc`), Navy Blue (`#102d4a`), Pure White (`#ffffff`), and Dark Ink palette; clinical typography |
| **Backend API** | Python 3.10+, Flask 3.x, Werkzeug | REST API endpoints, JWT token verification, dynamic CORS handling |
| **Security & Auth** | Flask-JWT-Extended, PBKDF2/SHA-256 | Role-based decorator (`@role_required`), token claims, session persistence |
| **Databases** | SQLite3 (`users.db`, `predictions.db`) | Relational storage for users, roles, password hashes, and clinical prediction history |
| **Machine Learning** | Scikit-learn, Joblib, NumPy, Pandas | Supervised classification models, standard scalers, median imputers, probability calibration |
| **Explainable AI** | SHAP (`shap`), LIME (`lime`) | Global/Local game-theoretic Shapley values, perturbation-based surrogate models |
| **Counterfactuals** | Custom Python Engine (`counterfactual_engine.py`) | Gradient-free, clinically constrained grid search with immutability filters |
| **Reporting** | ReportLab | Diagnostic summary PDF compiling patient data, risk score, top biomarkers, and recommendations |

---

## 3. Authentication & Role-Based Access Control (RBAC)

The application enforces a 3-tier Role-Based Access Control (RBAC) hierarchy.

### 3.1 Role Hierarchy & Permissions Matrix

| Feature / Action | System Administrator (`admin`) | Lead Doctor (`doctor`) | Clinical Staff (`staff`) |
| :--- | :---: | :---: | :---: |
| **User Management Portal** | Yes | No | No |
| **View All Registered Staff/Doctors** | Yes | No | No |
| **Promote Staff to Doctor** | Yes | No | No |
| **Demote Doctor to Staff** | Yes | No | No |
| **Execute Multi-Disease CDSS Assessment** | No | Yes | Yes |
| **Inspect SHAP & LIME Feature Attributions** | No | Yes | Yes |
| **View ERI Explanation Reliability Score** | No | Yes | Yes |
| **Inspect Dual-Tier Counterfactual Plans** | No | Yes | Yes |
| **Export Official PDF Clinical Report** | No | Yes | Yes |
| **Access Case Archive / Patient History** | No | **Yes** | **No (403 Forbidden)** |

### 3.2 Pre-Seeded Institutional Credentials

The SQLite database (`backend/users.db`) automatically seeds three institutional user accounts upon startup:

```
+-----------------------------------------------------------------------------------+
| ROLE               EMAIL                      PASSWORD          PERMISSIONS       |
+-----------------------------------------------------------------------------------+
| Administrator      admin@hospital.com         Admin@123         Manage users/roles|
| Lead Doctor        doctor@hospital.com        Doctor@123        Full CDSS + History|
| Clinical Staff     staff@hospital.com         Staff@123         Intake & Assessment|
+-----------------------------------------------------------------------------------+
```

> [!NOTE]
> Every time the backend launches, `auth_database.py` executes `seed_default_users()`. If these accounts are modified or missing, their credentials and roles are restored without altering custom user signups.

### 3.3 Auth Implementation Details

- **Token Mechanism**: Standard JSON Web Tokens (JWT) signed using HMAC-SHA256 (`JWT_SECRET_KEY`).
- **Token Claims**: Each token payload embeds `id`, `name`, `email`, and `role`.
- **Dynamic API Base URL**: `frontend/src/services/api.js` dynamically checks `window.location.hostname`. When accessing from `localhost` or `127.0.0.1`, it automatically communicates with `http://localhost:5000`, guaranteeing local database persistence.
- **Backend Route Guard**: Decorator `@role_required(*allowed_roles)` verifies both JWT validity and role claim.
- **Frontend Route Guard**: `<ProtectedRoute allowedRoles={[...]}>` redirects unauthorized attempts to `/unauthorized` or `/login`.

---

## 4. Database Architecture & Schemas

The system utilizes two independent SQLite databases to enforce clean domain separation:

### 4.1 Authentication Database (`backend/users.db`)

Table: `users`

```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

- **`password_hash`**: Stored using `werkzeug.security.generate_password_hash` (`pbkdf2:sha256`).
- **`role`**: Enforced constraint: `'admin'`, `'doctor'`, or `'staff'`.

### 4.2 Clinical Archive Database (`backend/predictions.db`)

Table: `prediction_history`

```sql
CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    patient_name TEXT,
    disease TEXT,
    prediction TEXT,
    probability REAL,
    risk_level TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

- Accessible **only** by authenticated users with the `doctor` role via `/history`.
- Stores audit history for medical-legal review and longitudinal tracking.

---

## 5. Machine Learning Disease Models

The CDSS supports four major clinical conditions across distinct pathophysiology domains:

```
+--------------------------------------------------------------------------------------------------+
| DISEASE          MODEL ARCHITECTURE             FEATURES   TARGET CLASSES     OPTIMIZATION       |
+--------------------------------------------------------------------------------------------------+
| Heart Disease    Random Forest Classifier       13         0: No / 1: Risk    StandardScaler     |
| Diabetes         Decision Tree / Random Forest  16         0: Neg / 1: Pos    StandardScaler     |
| Chronic Kidney   Random Forest Classifier       24         0: No / 1: CKD     StandardScaler     |
| Stroke Risk      Logistic Regression (Weighted) 10         0: No / 1: Stroke  Imputer + Tau=0.85 |
+--------------------------------------------------------------------------------------------------+
```

### 5.1 Heart Disease Module (13 Biomarkers)
- **Clinical Dataset**: Cleveland Heart Disease benchmark.
- **Biomarkers**:
  1. `age`: Age in years
  2. `sex`: Gender (1 = Male, 0 = Female)
  3. `cp`: Chest pain type (0: Typical Angina, 1: Atypical Angina, 2: Non-anginal, 3: Asymptomatic)
  4. `trestbps`: Resting blood pressure (mmHg)
  5. `chol`: Serum cholesterol (mg/dL)
  6. `fbs`: Fasting blood sugar > 120 mg/dL (1 = True, 0 = False)
  7. `restecg`: Resting electrocardiographic results (0: Normal, 1: ST-T wave abnormality, 2: Left ventricular hypertrophy)
  8. `thalach`: Maximum heart rate achieved during exercise (bpm)
  9. `exang`: Exercise-induced angina (1 = Yes, 0 = No)
  10. `oldpeak`: ST depression induced by exercise relative to rest (mm)
  11. `slope`: Slope of the peak exercise ST segment (0: Upsloping, 1: Flat, 2: Downsloping)
  12. `ca`: Number of major vessels colored by fluoroscopy (0–3)
  13. `thal`: Thalassemia defect (1: Normal, 2: Fixed Defect, 3: Reversible Defect)

### 5.2 Diabetes Mellitus Module (16 Clinical Signs)
- **Clinical Dataset**: Early Stage Diabetes Risk Dataset (Sylhet Diabetes Hospital).
- **Features**:
  `age`, `gender`, `polyuria`, `polydipsia`, `sudden_weight_loss`, `weakness`, `polyphagia`, `genital_thrush`, `visual_blurring`, `itching`, `irritability`, `delayed_healing`, `partial_paresis`, `muscle_stiffness`, `alopecia`, `obesity`.

### 5.3 Chronic Kidney Disease (CKD) Module (24 Features)
- **Clinical Dataset**: UCI Machine Learning CKD Repository.
- **Biomarkers**:
  `age`, `bp` (blood pressure), `sg` (specific gravity), `al` (albumin), `su` (sugar), `rbc` (red blood cells), `pc` (pus cell), `pcc` (pus cell clumps), `ba` (bacteria), `bgr` (blood glucose random), `bu` (blood urea), `sc` (serum creatinine), `sod` (sodium), `pot` (potassium), `hemo` (hemoglobin), `pcv` (packed cell volume), `wbcc` (white blood cell count), `rbcc` (red blood cell count), `htn` (hypertension), `dm` (diabetes mellitus), `cad` (coronary artery disease), `appet` (appetite), `pe` (pedal edema), `ane` (anemia).

### 5.4 Stroke Risk Module (10 Features + Severe Imbalance Calibration)
- **Clinical Dataset**: Kaggle Healthcare Stroke Dataset.
- **Features**: `gender`, `age`, `hypertension`, `heart_disease`, `ever_married`, `work_type`, `residence_type`, `avg_glucose_level`, `bmi`, `smoking_status`.
- **Handling Severe Class Imbalance**: In stroke datasets, positive instances represent $< 5\%$ of the cohort. Standard $0.5$ classification thresholds yield severe false negatives. This system deploys:
  1. Median Imputation (`SimpleImputer`) for missing BMI entries.
  2. StandardScaler normalization.
  3. Optimized Decision Threshold $\tau = 0.85$ on positive class log-odds to optimize sensitivity/specificity tradeoff.

---

## 6. Novelty Feature 1: Multi-XAI Triangulation & The ERI Consensus Index

### 6.1 The Disagreement Problem in Medical XAI
When machine learning models generate high-risk predictions, clinical practitioners cannot rely on a single explanation method:
- **SHAP (SHapley Additive exPlanations)** computes exact or approximate game-theoretic Shapley contributions across all feature coalitions. It has global efficiency and consistency properties, but can dilute local interaction effects.
- **LIME (Local Interpretable Model-agnostic Explanations)** fits an interpretable sparse linear surrogate locally around the perturbed patient vector. It excels at local fidelity, but suffers from perturbation variance and sampling instability.

In critical clinical cases, SHAP and LIME frequently highlight **different features** or assign conflicting impact directions to the same biomarker. This **Explanation Disagreement Dilemma** breeds clinician distrust.

### 6.2 The Explanation Reliability & Consistency Index (ERI)
To solve this dilemma, our system introduces the **Explanation Reliability & Consistency Index (ERI)**, an objective quantitative concordance metric computed in real time.

Let $\mathcal{F}_{\text{SHAP}}^{(K)}$ and $\mathcal{F}_{\text{LIME}}^{(K)}$ denote the top-$K$ most impactful biomarkers identified by SHAP and LIME, respectively (with $K=5$):

#### Component 1: Feature Overlap Concordance ($\mathcal{C}_{\text{overlap}}$)
Quantifies the percentage of top-$K$ biomarkers ($K=5$) identified in common by both explainers:
$$\mathcal{C}_{\text{overlap}} = \frac{|\mathcal{F}_{\text{SHAP}}^{(K)} \cap \mathcal{F}_{\text{LIME}}^{(K)}|}{K} \times 100\%$$

#### Component 2: Directional Sign Agreement ($\mathcal{S}_{\text{direction}}$)
Quantifies whether shared biomarkers push the clinical risk in the identical direction (e.g., both agree high glucose increases stroke risk):
$$\mathcal{S}_{\text{direction}} = \frac{1}{|\mathcal{F}_{\text{shared}}|} \sum_{f \in \mathcal{F}_{\text{shared}}} \mathbb{I}\left(\operatorname{sgn}(\phi_{\text{SHAP}}(f)) == \operatorname{sgn}(\beta_{\text{LIME}}(f))\right) \times 100\%$$

#### Component 3: Ranking Order Concordance ($\mathcal{R}_{\text{ranking}}$)
Measures rank stability among shared features using normalized rank displacement:
$$\mathcal{R}_{\text{ranking}} = \max\left(0.0, 1.0 - \frac{\sum_{f \in \mathcal{F}_{\text{shared}}} |\operatorname{rank}_{\text{SHAP}}(f) - \operatorname{rank}_{\text{LIME}}(f)|}{\operatorname{max\_displacement}}\right) \times 100\%$$

#### Composite ERI Mathematical Formulation
$$ERI = \left(0.40 \times \mathcal{C}_{\text{overlap}}\right) + \left(0.30 \times \mathcal{S}_{\text{direction}}\right) + \left(0.30 \times \mathcal{R}_{\text{ranking}}\right)$$

### 6.3 Clinical Interpretation Thresholds (Advisory Indicator)

Rather than acting as an automated gate or blocking clinical workflow, the ERI provides a real-time quantitative reliability indicator alongside the model prediction and explanations to assist the clinician's diagnostic review:

```
+-----------------------------------------------------------------------------------+
| ERI SCORE RANGE    RELIABILITY LEVEL     CLINICAL ADVISORY PROTOCOL               |
+-----------------------------------------------------------------------------------+
| 80.0% - 100.0%     HIGH RELIABILITY      High consensus: Both explainers agree    |
|                                          closely on biomarker importance & signs. |
| 50.0% - 79.9%      MODERATE RELIABILITY  Partial consensus: Key markers align but |
|                                          ranking/sub-features diverge.            |
| 0.0% - 49.9%       LOW RELIABILITY       Divergent explanations: Explainer noise  |
|                                          warrants closer clinician verification.  |
+-----------------------------------------------------------------------------------+
```

---

## 7. Novelty Feature 2: Dual-Tier Constrained Counterfactual Analysis Engine

> [!IMPORTANT]
> **Clinical Decision Support & Simulation Disclaimer:**
> Counterfactual explanations generated by this CDSS are hypothetical algorithmic simulations derived from classifier decision boundaries to explore risk sensitivity. They are intended strictly for clinical decision support, sensitivity analysis, and exploratory review—**NOT** as direct medical prescriptions, therapeutic directives, or guaranteed treatment outcomes. All patient treatment plans and clinical interventions must be formulated and approved by qualified healthcare providers.

### 7.1 What is Counterfactual Explanation in Medicine?
A counterfactual explanation answers the clinician's core question:
> *"What minimal, clinically feasible changes would transform this high-risk patient into a low-risk prediction state according to the model?"*

Mathematically, given a patient feature vector $x \in \mathbb{R}^d$ where the model predicts high risk $f(x) = 1$, find a perturbation vector $\delta \in \mathbb{R}^d$ such that:
$$f(x + \delta) = 0 \quad \text{subject to } \min \|\delta\|_p \text{ and } (x + \delta) \in \mathcal{C}$$
where $\mathcal{C}$ represents the clinically feasible manifold.

### 7.2 The Failure of Standard Counterfactuals (e.g., DiCE, Genetic Solvers)
Unconstrained optimization algorithms frequently produce medically absurd solutions:
- Recommending a 68-year-old patient *"reduce their age to 42"*
- Recommending a patient change biological sex or genetic traits
- Recommending non-physiological biomarker values (e.g., Blood Pressure $= 40\text{ mmHg}$)
- Recommending simultaneous changes across 10 parameters (zero patient compliance)

### 7.3 Our Dual-Tier Actionable Architecture with Biological Guardrails

Our engine enforces three mandatory constraints:

#### 1. Immutability Guardrail $\mathcal{I}$
Certain features are designated as strictly immutable and are frozen during optimization:
- Heart: `age`, `sex`
- Diabetes: `age`, `gender`
- CKD: `age`
- Stroke: `age`, `gender`, `ever_married`, `work_type`, `residence_type`

$$\forall i \in \mathcal{I}, \quad \delta_i = 0$$

#### 2. Directional Medical Plausibility & Reference Boundaries
Biomarkers can only be perturbed toward certified medical reference intervals (e.g., blood pressure only decreases toward $115\text{--}120\text{ mmHg}$, heart rate only increases toward healthy aerobic conditioning):
$$(x_i + \delta_i) \in [\text{Ref}_{\text{min}}, \text{Ref}_{\text{max}}]$$

#### 3. Dual-Tier Partitioning ($L_0$ Sparsity Constraint)
The engine separates candidate solutions into two distinct actionable categories:

```
+-----------------------------------------------------------------------------------+
| TIER 1: SINGLE-BIOMARKER RECOURSE TRAJECTORIES (L0 = 1)                           |
| - Exactly ONE biomarker is perturbed.                                            |
| - Maximum focus and compliance feasibility.                                      |
| - Represents a targeted single-biomarker recourse trajectory (e.g., Chol -> 175).|
+-----------------------------------------------------------------------------------+
| TIER 2: MULTI-BIOMARKER REGIMENS (L0 >= 2, e.g., L0 = 2 demonstrated)             |
| - Combination of 2 or more mutually supporting physiological markers.             |
| - Applied when single-biomarker shifts are insufficient or to explore synergy.    |
| - Represents multi-factorial physiological risk reduction (e.g., BP + Chol).      |
+-----------------------------------------------------------------------------------+
```

Each counterfactual generated by the engine includes:
- **Biomarker Name & Clinical Metric Label**
- **Baseline Value $\to$ Target Reference Level**
- **Exact Numeric Adjustment Delta ($\Delta$) and Metric Unit**
- **Directional Indicator ($\rightarrow$ or $\downarrow / \uparrow$)**
- **Physiological Rationale** (e.g., *"Lower vascular resistance and cardiac afterload"* based on established medical reference bounds).

---

## 8. File-by-File Directory Blueprint

### 8.1 Backend Architecture (`/backend`)

```
backend/
├── app.py                      # Flask REST API entrypoint & route coordinator
├── auth.py                     # Authentication blueprint (/auth/*) & RBAC decorator
├── auth_database.py            # SQLite user database management & default credential seeding
├── database.py                 # SQLite clinical history database (predictions.db)
├── model_loader.py             # Serialized Joblib model loader (RF, DT, LR, Scalers)
├── prediction.py               # Core inference engine across 4 disease domains
├── explainability.py           # SHAP attribution computation (Tree & Linear explainers)
├── lime_explain.py             # LIME tabular surrogate computation
├── shap_lime_agreement.py      # ERI Concordance Index calculation engine
├── counterfactual_engine.py    # Clinically-constrained Dual-Tier Counterfactual engine
├── counterfactual_heart.py     # Heart-specific counterfactual permutation solver
├── recommendation.py           # Clinical rule-based guidance generator
├── report_generator.py         # ReportLab PDF clinical report compiler
└── requirements.txt            # Python dependencies (Flask, scikit-learn, shap, lime, etc.)
```

#### Detailed File Descriptions:
- **`app.py`**: Configures Flask, JWTManager, CORS, and registers all endpoints (`/predict`, `/report`, `/stats`, `/history`). Orchestrates the complete pipeline: Feature Validation $\to$ Prediction $\to$ SHAP $\to$ LIME $\to$ ERI $\to$ Dual-Tier CF $\to$ History Logging.
- **`auth.py`**: Handles user login, signup, `/auth/me`, `/auth/users`, and `/auth/users/<id>/role`. Defines `@role_required(*roles)`.
- **`auth_database.py`**: Initializes `users.db`. Automatically creates default credentials for Admin, Doctor, and Staff on every startup via `seed_default_users()`.
- **`database.py`**: Manages `predictions.db` and writes cases to `prediction_history`.
- **`model_loader.py`**: Safely loads `.pkl` files from `../models/` for Heart, Diabetes, CKD, and Stroke.
- **`prediction.py`**: Formats raw input into feature matrices, scales inputs, calls `.predict()` and `.predict_proba()`, and applies disease thresholds.
- **`explainability.py`**: Computes SHAP values using `TreeExplainer` or `LinearExplainer`, extracting top contributing features.
- **`lime_explain.py`**: Instantiates `LimeTabularExplainer` around training distributions, returning local perturbations.
- **`shap_lime_agreement.py`**: Implements the ERI equation: extracts shared top features, compares sign directions, calculates ranking displacement, and computes overall agreement percentage.
- **`counterfactual_engine.py`**: Filters immutable variables, evaluates medically plausible values within physiological reference boundaries, checks model probability drops, and sorts candidate counterfactuals into Tier 1 ($L_0=1$) and Tier 2 ($L_0 \ge 2$, e.g., $L_0=2$).
- **`report_generator.py`**: Uses ReportLab to generate official clinical PDFs formatted with hospital headers, biomarker tables, and doctor signatures.

---

### 8.2 Frontend Architecture (`/frontend`)

```
frontend/
├── package.json                # React 19, Vite 8, Axios, React Router dependencies
├── vite.config.js              # Vite build configuration & server port settings
├── index.html                  # HTML5 entrypoint with Google Fonts import
└── src/
    ├── App.jsx                 # Application router, role guards, and navigation shell
    ├── main.jsx                # React root renderer wrapped in AuthProvider & BrowserRouter
    ├── auth/
    │   ├── authcontext.jsx     # Global authentication context, JWT token storage, login/logout
    │   ├── login.jsx           # Clean login view supporting role-based post-login redirects
    │   ├── signup.jsx          # User registration view with Doctor/Staff role selection
    │   └── protectedroute.jsx  # Route wrapper checking user authentication & role permissions
    ├── components/
    │   ├── Navbar.jsx          # Institutional header with system status pill & user badge
    │   ├── Hero.jsx            # Clinical overview banner
    │   ├── Dashboard.jsx       # Real-time institutional statistics counter
    │   ├── PatientForm.jsx     # Main multi-disease diagnostic form with styled clinical tabs
    │   ├── PredictionCard.jsx  # Primary outcome gauge, probability meter, and risk badge
    │   ├── PatientSummary.jsx  # Input biomarker summary matrix
    │   ├── FeatureImportance.jsx # SHAP/LIME charts, ERI meter, & Dual-Tier Counterfactual cards
    │   ├── History.jsx         # Case history table (Doctor-only access)
    │   ├── Footer.jsx          # Institutional footer
    │   └── icons.jsx           # Lightweight SVG clinical icon set
    ├── pages/
    │   ├── AdminDashboard.jsx  # Admin user management & role promotion portal
    │   ├── DoctorDashboard.jsx # Doctor landing workspace
    │   ├── StaffDashboard.jsx  # Staff intake portal
    │   └── Unauthorized.jsx    # 403 Forbidden access denial screen
    ├── services/
    │   └── api.js              # Axios instance with dynamic base URL & JWT bearer interceptor
    └── styles/
        └── theme.css           # Primary clinical stylesheet (White / Sky Blue / Navy Blue)
```

#### Detailed File Descriptions:
- **`api.js`**: Automatically detects `localhost`/`127.0.0.1` and points API traffic to `http://localhost:5000`. Attaches `Authorization: Bearer <token>` to all requests.
- **`PatientForm.jsx`**: Dynamically switches input forms for Heart, Diabetes, CKD, and Stroke using clinical tabs (`.tabs.disease-tabs`). Executes `/predict` and loads explanation widgets.
- **`FeatureImportance.jsx`**: The core explainability UI. Displays:
  1. **ERI Concordance Card**: Overall consistency score, feature overlap (40%), direction agreement (30%), ranking agreement (30%), and reliability badge.
  2. **SHAP & LIME Comparison Bars**: Visual impact graphs for top biomarkers.
  3. **Dual-Tier Counterfactual Panels**: Interactive cards showing Tier 1 ($L_0=1$) single-biomarker interventions and Tier 2 ($L_0 \ge 2$) multi-biomarker regimens.
- **`AdminDashboard.jsx`**: Displays registered users, statistics, and role switching dropdowns (`doctor` $\leftrightarrow$ `staff`).
- **`History.jsx`**: Rendered only when `user.role === 'doctor'`. Fetches SQLite prediction history and renders searchable case records.

---

## 9. API Reference & Endpoints

### Authentication Endpoints

#### `POST /auth/login`
- **Access**: Public
- **Body**: `{"email": "doctor@hospital.com", "password": "Doctor@123"}`
- **Response**: `{"success": true, "token": "<JWT>", "user": {"id": 2, "name": "...", "role": "doctor"}}`

#### `POST /auth/signup`
- **Access**: Public
- **Body**: `{"name": "Dr. Sarah", "email": "sarah@hospital.com", "password": "Password@123", "role": "doctor"}`
- **Response**: `{"success": true, "message": "User registered successfully."}`

#### `GET /auth/me`
- **Access**: Authenticated (JWT required)
- **Response**: `{"success": true, "user": {"email": "...", "name": "...", "role": "..."}}`

#### `GET /auth/users`
- **Access**: `admin` only
- **Response**: `{"success": true, "users": [{"id": 1, "name": "...", "role": "admin"}, ...]}`

#### `PUT /auth/users/<user_id>/role`
- **Access**: `admin` only
- **Body**: `{"role": "doctor"}` (or `"staff"`)
- **Response**: `{"success": true, "message": "User role updated successfully."}`

---

### Diagnostic & Explainability Endpoints

#### `POST /predict`
- **Access**: `doctor`, `staff`
- **Body**:
  ```json
  {
    "disease": "heart",
    "features": [62, 1, 0, 145, 282, 0, 2, 142, 1, 2.8, 1, 2, 2],
    "patient_id": "PT-9021",
    "patient_name": "John Doe",
    "doctor_name": "Dr. Dhanush",
    "hospital_name": "City General Hospital"
  }
  ```
- **Response**:
  ```json
  {
    "disease": "heart",
    "class": 1,
    "prediction_text": "Heart Disease Detected",
    "probability": 84.6,
    "risk_level": "High",
    "top_features": [{"feature": "cp", "impact": 0.28}, ...],
    "lime_features": [{"feature": "cp <= 0", "weight": 0.24}, ...],
    "agreement": {
      "overall_consistency_score": 83.5,
      "consistency_level": "High",
      "feature_agreement": 80.0,
      "direction_agreement": 100.0,
      "ranking_agreement": 75.0,
      "common_features": ["Chest Pain Type", "ST Depression", "Serum Cholesterol"]
    },
    "single_counterfactuals": [
      {
        "changes": {"Resting Blood Pressure": [145, 118]},
        "prediction_text": "Low Risk / Healthy",
        "probability": 38.2,
        "number_of_changes": 1,
        "feature_changes": [{"feature": "trestbps", "old_value": 145, "new_value": 118, "delta": -27, "unit": "mmHg"}]
      }
    ],
    "multi_counterfactuals": [
      {
        "changes": {"Serum Cholesterol": [282, 175], "ST Depression": [2.8, 0.2]},
        "prediction_text": "Low Risk / Healthy",
        "probability": 24.1,
        "number_of_changes": 2
      }
    ]
  }
  ```

#### `POST /report`
- **Access**: `doctor`, `staff`
- **Body**: Same as `/predict`
- **Response**: Binary streaming PDF file download (`heart_Clinical_Report.pdf`).

#### `GET /history`
- **Access**: `doctor` only (Staff receives `403 Forbidden`)
- **Response**: Array of historical clinical cases.

#### `GET /stats`
- **Access**: `doctor`, `staff`
- **Response**: `{"cases_processed": 42, "high_risk_flags": 18, "low_risk_cases": 24}`

---

## 10. Step-by-Step Instructions: Running the System Locally

### Step 1: Clone and Navigate to Directory
Open PowerShell or your preferred terminal in the project directory:
```powershell
cd "c:\Users\DHANUSH S J\Documents\Codex\2026-09-13\files-pasted-by-the-user-yes\outputs\Explainable-AI-CDSS-complete-clean"
```

### Step 2: Set Up and Run the Python Backend
1. Open a terminal and navigate to the `backend` folder:
   ```powershell
   cd backend
   ```
2. Activate your virtual environment (or create one):
   ```powershell
   # If venv exists:
   .\venv\Scripts\activate

   # If creating fresh:
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Launch the Flask API server:
   ```powershell
   python app.py
   ```
   *The backend will initialize `users.db`, seed the 3 default users (Admin, Doctor, Staff), create `predictions.db`, and run on `http://localhost:5000`.*

### Step 3: Set Up and Run the React Frontend
1. Open a **second terminal** and navigate to the `frontend` folder:
   ```powershell
   cd frontend
   ```
2. Install npm packages (if running for the first time):
   ```powershell
   npm install
   ```
3. Start the Vite development server:
   ```powershell
   npm run dev
   ```
4. Open your web browser and navigate to:
   ```
   http://localhost:5173
   ```

---

## 11. Verification & Testing Guide

### Test Case 1: Doctor Login & Full Diagnostic Flow
1. Navigate to `http://localhost:5173/login`.
2. Enter Doctor credentials:
   - **Email**: `doctor@hospital.com`
   - **Password**: `Doctor@123`
3. Click **Sign In**.
4. You will be directed to the main CDSS diagnostic interface.
5. In the disease tabs, select **Heart Disease**.
6. Enter patient details:
   - Patient ID: `PT-101`, Patient Name: `Robert Miller`, Clinician: `Dr. Dhanush`
7. In the clinical parameters, enter high-risk values:
   - Age: `65`, Resting BP: `160`, Cholesterol: `285`, Max Heart Rate: `108`, Oldpeak: `3.2`
8. Click **Run Heart Disease Assessment**.
9. **Verify Results**:
   - **Prediction Card**: Displays "Heart Disease Detected" with high probability ($> 80\%$) and Red Risk Badge.
   - **ERI Metric Card**: Displays the calculated concordance percentage between SHAP and LIME.
   - **Single Counterfactuals**: Displays $L_0=1$ intervention (e.g., reduce blood pressure).
   - **Multi Counterfactuals**: Displays $L_0 \ge 2$ multi-parameter regimens.
   - **Case Archive**: Scroll to the bottom to verify the new case appears in the SQLite History table.
   - **Export PDF**: Click **Export Clinical PDF** to confirm PDF dossier generation.

---

### Test Case 2: Staff Login & Role Restriction Verification
1. Click **Sign Out** in the top navigation bar.
2. Sign in with Staff credentials:
   - **Email**: `staff@hospital.com`
   - **Password**: `Staff@123`
3. Notice that:
   - You can run predictions, view SHAP/LIME/ERI, view Counterfactuals, and export PDFs.
   - **Patient History / Case Archive is completely hidden** from the view.
   - Attempting to access `http://localhost:5000/history` directly returns `403 Forbidden`.

---

### Test Case 3: Admin User Management & Role Promotion
1. Sign out and sign in with Admin credentials:
   - **Email**: `admin@hospital.com`
   - **Password**: `Admin@123`
2. You will be directed to the **Admin Dashboard** (`/admin`).
3. You will see the total registered users, doctors, and staff count.
4. Locate the user `Clinical Staff Member` (`staff@hospital.com`).
5. In the role dropdown, switch their role from **staff** to **doctor**.
6. The UI displays *"User role updated successfully"*.
7. Sign out and log back in as `staff@hospital.com` / `Staff@123`.
8. The staff member is now recognized as a Doctor and can view the Patient History table.

---

## 12. IEEE Conference Paper Publication Framework

This architecture provides the empirical and theoretical foundation for an IEEE conference paper (e.g., *IEEE BIBM*, *IEEE EMBC*, or *IEEE Transactions on Medical Informatics*).

### 12.1 Proposed Paper Title
> **"A Triangulated Explainable Clinical Decision Support System with Dual-Tier Actionable Counterfactual Interventions and Biological Guardrails"**

### 12.2 Abstract Template
> *Machine Learning (ML) classifiers have demonstrated remarkable efficacy in predicting cardiovascular and metabolic disease risks. However, their clinical integration remains obstructed by model opacity and the "explanation disagreement problem," where distinct eXplainable AI (XAI) frameworks produce divergent biomarker attributions for identical patients. Furthermore, conventional counterfactual generation often recommends non-actionable or biologically impossible modifications (e.g., reducing patient age). In this work, we present a novel, production-ready Clinical Decision Support System (CDSS) that overcomes these limitations across four disease domains: Heart Disease, Diabetes, Chronic Kidney Disease, and Stroke. Our contributions are two-fold: First, we formulate the Explanation Reliability and Consistency Index (ERI), a tripartite meta-metric evaluating top-$K$ feature overlap (40%), directional agreement (30%), and rank concordance (30%) between game-theoretic SHAP and perturbation-based LIME explanations. Second, we propose a Clinically-Constrained Dual-Tier Counterfactual Engine that enforces strict biological immutability guardrails while partitioning actionable recommendations into Tier 1 (Single-Biomarker, $L_0=1$) and Tier 2 (Multi-Biomarker, $L_0 \ge 2$) recourse trajectories. Experimental validation demonstrates that the proposed framework delivers quantified cross-attribution stability while offering clinicians realistic, compliance-optimized recourse simulations with physiological rationales.*

### 12.3 Comparison Against Existing Literature (50-Paper Survey)

| Evaluation Dimension | Standard ML Papers | Existing SHAP/LIME Papers | Our Proposed Framework |
| :--- | :---: | :---: | :---: |
| **Multi-Disease Coverage** | Single disease only | Usually 1 or 2 diseases | **4 Clinical Diseases** (Heart, Diabetes, CKD, Stroke) |
| **XAI Methodology** | Black-box / None | SHAP or LIME in isolation | **Dual-Engine (SHAP + LIME)** |
| **Attribution Concordance** | Absent | Subjective inspection | **Mathematical ERI Index** (Overlap + Direction + Rank) |
| **Counterfactual Engine** | None | Absent or unconstrained DiCE | **Clinically Constrained Dual-Tier ($L_0=1$ vs $L_0 \ge 2$)** |
| **Immutability Guardrails** | N/A | None (alters age/sex) | **Strict Biological & Demographic Freezing** |
| **Targeted Recourse & Units** | N/A | Raw numeric values | **Units, Exact $\Delta$, & Physiological Rationales** |
| **Institutional RBAC** | None | Mock interface | **Full Admin, Doctor, Staff RBAC with SQLite** |
| **Clinical Reporting** | None | Raw screenshots | **Automated Multi-Page PDF Dossier Generation** |

---

## 13. Summary of System Novelties

```
+-----------------------------------------------------------------------------------------+
|                                    PROJECT NOVELTIES                                    |
+-----------------------------------------------------------------------------------------+
| 1. EXPLANATION RELIABILITY INDEX (ERI): Resolves the XAI disagreement problem by        |
|    mathematically calculating consensus across overlap, sign direction, and rank.      |
|                                                                                         |
| 2. DUAL-TIER CONSTRAINED COUNTERFACTUAL ENGINE: Separates single-biomarker recourse     |
|    trajectories (Tier 1, L0=1) from multi-biomarker synergistic regimens (Tier 2, L0>=2)|
|    with physiological reference bounds.                                                 |
|                                                                                         |
| 3. BIOLOGICAL IMMUTABILITY GUARDRAILS: Prevents biologically implausible simulations    |
|    by freezing non-modifiable variables (Age, Gender, Marital Status, Medical History).|
|                                                                                         |
| 4. TRIANGULATED CLINICAL VALIDATION: Integrates Prediction Probabilities, SHAP, LIME,   |
|    ERI, Counterfactual Interventions, and Automated PDF Dossiers into a single system.  |
+-----------------------------------------------------------------------------------------+
```

*This file (`abcd.md`) serves as the complete technical manual and research documentation for the Explainable AI Clinical Decision Support System.*
