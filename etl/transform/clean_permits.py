import pandas as pd

def clean_permits(df):
    # Normalize BIN field
    if 'bin__' in df.columns:
        df['bin'] = df['bin__'].astype(str).str.zfill(7)
    elif 'bin' in df.columns:
        df['bin'] = df['bin'].astype(str).str.zfill(7)

    # Parse date columns safely
    for date_col in ['filing_date', 'issuance_date', 'expiration_date']:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # Define potential renames based on known schema
    rename_map = {
        'job_type': 'job_type',
        'permit_type': 'permit_type',
        'permit_status': 'status',
        'bin': 'bin',
        'borough': 'borough',
        'house_street': 'address',  # optional
        'block': 'block',
        'lot': 'lot',
        'community_board': 'community_board',
        'work_type': 'work_type',
        'filing_date': 'filing_date',
        'issuance_date': 'issuance_date',
        'expiration_date': 'expiration_date'
    }

    # Only include columns that exist
    existing_map = {k: v for k, v in rename_map.items() if k in df.columns}
    cleaned = df.rename(columns=existing_map)
    cleaned = cleaned[list(existing_map.values())].drop_duplicates()

    return cleaned