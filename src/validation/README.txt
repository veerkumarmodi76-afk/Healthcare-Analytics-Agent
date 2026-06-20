VALIDATION TOOLKIT — README
============================
Member 6: Validation (Model Testing, Benchmarking, Business Insights)

WHAT YOU HAVE
--------------
1. generate_sample_data.py   -> creates FAKE data so you can test everything
                                 right now, before teammates deliver real files.
2. validation_toolkit.py     -> the real validation script you'll present.
3. sample_data/ (folder)     -> created automatically when you run script 1.


STEP-BY-STEP: HOW TO RUN (today, with no real data yet)
----------------------------------------------------------
1. Open a terminal / command prompt.
2. Go to the folder where these files are saved:
       cd path/to/validation_project
3. Install the 3 libraries needed (only once):
       pip install pandas numpy scikit-learn
4. Generate the fake sample data:
       python generate_sample_data.py
   You should see a message confirming 3 CSV files were created.
5. Run the validation script:
       python validation_toolkit.py
   You'll see 4 sections printed:
       1. Underwriting Risk Model Validation
       2. Claim Cost Prediction Model Validation
       3. Lapse Prediction Model Validation
       4. Business Insights Summary (ready to paste into your report)


WHAT EACH NUMBER MEANS (so you can explain it confidently)
-------------------------------------------------------------
AUC Score (0 to 1)
   Measures how well the model tells apart "risky" vs "not risky" people.
   0.5 = no better than a coin flip. 0.7+ is considered good in practice.

Accuracy (%)
   Of all predictions, what % were correct.

Baseline Accuracy / Baseline MAE
   What you'd get WITHOUT any AI — just guessing the average or majority
   outcome for everyone. This is your "proof" that the AI model adds value.
   If your real model isn't clearly better than this baseline, that's an
   important (and valid) finding too — flag it honestly in your report.

MAE (Mean Absolute Error)
   On average, how many rupees off was the claim cost prediction.
   Lower = better.

RMSE (Root Mean Squared Error)
   Similar to MAE, but punishes big mistakes more. Lower = better.

R² Score (0 to 1)
   How much of the variation in claim costs the model explains.
   1.0 = perfect. 0 = the model is no better than just guessing the average.


WHEN TEAMMATES SEND YOU REAL FILES
-------------------------------------
1. Save their CSV files into this folder (or any folder you like).
2. Open validation_toolkit.py in a text editor.
3. Near the top, find this section:

       RISK_FILE = "sample_data/applicant_risk_scores.csv"
       CLAIM_FILE = "sample_data/predicted_claim_cost.csv"
       LAPSE_FILE = "sample_data/lapse_risk_scores.csv"

4. Change the paths to point to the real files, e.g.:

       RISK_FILE = "real_data/applicant_risk_scores.csv"

5. IMPORTANT: Check their column names match what the script expects:
       Risk file needs columns:   predicted_risk_score, actual_risk_flag
       Claim file needs columns:  predicted_claim_cost, actual_claim_cost
       Lapse file needs columns:  predicted_lapse_score, actual_lapse_flag

   If their column names are different (e.g. "risk_pred" instead of
   "predicted_risk_score"), just rename in their CSV, OR tell me the
   actual column names and I'll update the script for you in 30 seconds.

6. Re-run:
       python validation_toolkit.py

That's it — nothing else changes. The script will now validate against
real model outputs instead of fake ones.


WHAT TO PRESENT / SUBMIT
---------------------------
- Screenshot or copy the terminal output of validation_toolkit.py
- Copy the "Business Insights Summary" section into executive_summary.txt
- If asked "how did you validate the models", say:
    "I benchmarked each model's predictions against actual outcomes using
     standard metrics (AUC, accuracy, MAE, RMSE, R²), and compared each
     model against a naive baseline (guessing the average/majority class)
     to quantify how much real value the AI models add over simple
     heuristics."

This one sentence shows you understand WHY validation matters, not just
that you ran a script.
