import pandas as pd
import os
from datetime import datetime

def run_multi_violation_audit(file_path: str, target_year: int = 2021):
    """
    Executes a GDPR Article 5 compliance audit tracking accounts created 
    no earlier than 2021, listing every associated violation per email address.
    """
    print("=" * 80)
    print(f"[+] LAUNCHING MULTI-VIOLATION DETAILED AUDIT REGISTER")
    print(f"[+] CURRENT TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # 1. Access Check
    if not os.path.exists(file_path):
        print(f" Critical IO Error: Cannot locate file at:\n    '{file_path}'")
        return

    # 2. Schema Map Formulation
    column_names = [
        'first_name', 'last_name', 'email', 'masked_token_1', 
        'masked_token_2', 'account_created_at', 'consent_given', 
        'is_active', 'risk_score'
    ]

    try:
        # Load Local Schema
        df = pd.read_csv(file_path, sep=';', names=column_names, header=None)
        print(f"[✔] File Ingestion Successful. Total Records Scanned: {len(df):,}")
        
        # Enforce temporal alignment
        df['account_created_at'] = pd.to_datetime(df['account_created_at'], errors='coerce')
        df['consent_given'] = df['consent_given'].fillna(0).astype(int)
        df['is_active'] = df['is_active'].fillna(0).astype(int)

        # 3. Apply Strict Operational Constraints
        # "No earlier than 2021" means equal to or greater than Jan 1, 2021
        cutoff_date = pd.Timestamp(f"{target_year}-01-01")
        target_df = df[df['account_created_at'] >= cutoff_date].copy()
        print(f"[+] Filter Applied: Evaluated {len(target_df):,} accounts created on/after {target_year}-01-01.")

        current_time = pd.Timestamp.now()

        # =====================================================================
        # AUDIT VECTOR A: Data Retention Policy Overlap (Example Criteria)
        # For post-2021 accounts, high risk score (>=7) triggers an operational review flag
        # =====================================================================
        vector_a_mask = (target_df['risk_score'] >= 7)
        violation_a_df = target_df[vector_a_mask].copy()
        violation_a_df['violation_type'] = 'Excessive Risk Score Allocation'
        violation_a_df['days_since_creation'] = (current_time - violation_a_df['account_created_at']).dt.days

        # =====================================================================
        # AUDIT VECTOR B: Unlawful Interaction Base (No Consent + Active Account)
        # Post-2021 accounts collecting data without opt-in history are immediate breaches
        # =====================================================================
        vector_b_mask = (target_df['consent_given'] == 0) & (target_df['is_active'] == 1)
        violation_b_df = target_df[vector_b_mask].copy()
        violation_b_df['violation_type'] = 'Active Processing Without Consent Base'
        violation_b_df['days_since_creation'] = (current_time - violation_b_df['account_created_at']).dt.days

        # =====================================================================
        # REPORT SYNTHESIS (NO DEDUPLICATION)
        # =====================================================================
        # By concatenating rows directly, an email with multiple violations will appear multiple times
        combined_violations = pd.concat([violation_a_df, violation_b_df], ignore_index=True)
        
        print(f" Total Violation 'Excessive Risk Score' Rows: {len(violation_a_df):,}")
        print(f" Total Violation 'No Consent Active' Rows: {len(violation_b_df):,}")
        print(f"Global Flat Violation Rows (All Exceptions Preserved): {len(combined_violations):,}")

        # 4. Export Detailed Exception Log to CSV
        output_dir = os.path.dirname(file_path)
        output_file = os.path.join(output_dir, "detailed_multi_violations_report#2.csv")
        
        if not combined_violations.empty:
            reporting_fields = [
                'email', 'first_name', 'account_created_at', 'consent_given', 
                'is_active', 'risk_score', 'violation_type', 'days_since_creation'
            ]
            
            # Sort explicitly by email address so multiple violations sit next to each other
            final_registry = combined_violations[reporting_fields].sort_values(by=['email', 'violation_type'])
            
            # Exporting directly to your local CSV file here
            final_registry.to_csv(output_file, index=False)
            print(f"Comprehensive Audit Report successfully exported to CSV:\n    '{output_file}'")
            
            print("\n" + "=" * 65)
            print("[+] COMPLIANCE AUDIT LOG PREVIEW (MULTIPLE VIOLATIONS INCLUDED)")
            print("=" * 65)
            print(final_registry[['email', 'violation_type', 'risk_score']].head(6).to_string(index=False))
            print("=" * 65)
        else:
            print("[✔] Complete Compliance Achieved: Zero post-2021 risks recorded in system metrics.")

    except Exception as e:
        print(f" Critical Audit Interruption: {str(e)}")

# ==========================================
# TRIGGER ENGINE RUN
# ==========================================
if __name__ == "__main__":
    run_multi_violation_audit(target_database, target_year=2021 )
