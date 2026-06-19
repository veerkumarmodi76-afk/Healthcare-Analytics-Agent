# Feature Dictionary

## Dataset Version

AI-AIP Health Insurance Dataset v1.0

---

## Primary Identifiers

| Feature    | Type | Description                      |
| ---------- | ---- | -------------------------------- |
| ID_policy  | int  | Policy identifier                |
| ID_insured | int  | Insured identifier within policy |
| period     | int  | Calendar year                    |

---

## Demographic Features

| Feature  | Type     | Description                     |
| -------- | -------- | ------------------------------- |
| age      | int      | Age of insured                  |
| gender   | category | M/F                             |
| age_band | category | 18-25, 26-35, 36-50, 51-65, 65+ |

---

## Policy Features

| Feature              | Type     | Description              |
| -------------------- | -------- | ------------------------ |
| type_policy          | category | Individual or Collective |
| type_policy_dg       | category | Detailed policy type     |
| type_product         | category | S, P, D, I               |
| reimbursement        | category | Yes/No                   |
| new_business         | binary   | New or renewal           |
| distribution_channel | category | A, D, I                  |

---

## Exposure Features

| Feature           | Type     | Description                  |
| ----------------- | -------- | ---------------------------- |
| exposure_time     | float    | Portion of year covered      |
| seniority_insured | int      | Years insured                |
| seniority_policy  | int      | Policy age                   |
| insured_duration  | int      | period - year_effect_insured |
| policy_duration   | int      | period - year_effect_policy  |
| seniority_band    | category | 0-2, 3-5, 6-10, 10+          |

---

## Claims Features

| Feature              | Type  | Description                   |
| -------------------- | ----- | ----------------------------- |
| premium              | float | Annual premium                |
| cost_claims_year     | float | Annual claim cost             |
| n_medical_services   | int   | Number of medical services    |
| claim_frequency      | float | Services / exposure           |
| claim_severity       | float | Claims cost per service       |
| loss_ratio           | float | Claims / premium              |
| premium_per_exposure | float | Premium adjusted for exposure |
| claims_per_exposure  | float | Claims adjusted for exposure  |

---

## Household Features

| Feature     | Type | Description                            |
| ----------- | ---- | -------------------------------------- |
| family_size | int  | Number of insured members under policy |

---

## Geographic Features

| Feature        | Type     | Description                            |
| -------------- | -------- | -------------------------------------- |
| n_insured_pc   | float    | Insured count in postal code           |
| n_insured_mun  | float    | Insured count in municipality          |
| n_insured_prov | float    | Insured count in province              |
| IICIMUN        | float    | Municipal concentration index          |
| IICIPROV       | float    | Provincial concentration index         |
| C_H            | category | Habitat category                       |
| C_GI           | float    | General income percentile              |
| C_II           | float    | Insured income percentile              |
| C_IE_P         | float    | Insured primary education percentile   |
| C_IE_S         | float    | Insured secondary education percentile |
| C_IE_T         | float    | Insured tertiary education percentile  |
| C_GE_P         | float    | General primary education percentile   |
| C_GE_S         | float    | General secondary education percentile |
| C_GE_T         | float    | General tertiary education percentile  |
| C_C            | category | Climate cluster                        |

---

## Lapse Features

| Feature             | Type   | Description             |
| ------------------- | ------ | ----------------------- |
| lapse               | int    | Original lapse code     |
| lapse_binary        | binary | 1=lapsed, 0=active      |
| insured_lapsed_flag | binary | Insured lapse indicator |
| policy_lapsed_flag  | binary | Policy lapse indicator  |

---

## Underwriting Features

| Feature            | Type     | Description                 |
| ------------------ | -------- | --------------------------- |
| risk_score         | float    | Composite risk score        |
| risk_class         | category | Low, Medium, High, VeryHigh |
| risk_class_encoded | int      | 0,1,2,3                     |
