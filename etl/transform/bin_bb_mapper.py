def extract_bin_bbl(df):
    bin_col = next((c for c in df.columns if "bin" in c.lower()), None)
    bbl_col = next((c for c in df.columns if "bbl" in c.lower()), None)

    if not bin_col or not bbl_col:
        raise ValueError("BIN or BBL column not found.")
    
    return df[[bin_col, bbl_col]].rename(columns={bin_col: "bin", bbl_col: "bbl"}).drop_duplicates()