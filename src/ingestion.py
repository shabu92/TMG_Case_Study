import pandas as pd 

### first we will Read the hitlog CSV file in DF and Validate the file ###

required_columns = ["page_name", "page_url", "user_id", "timestamp"] 

# Function to read hitlog file
def read_hitlog(file_path):
    df = pd.read_csv(file_path)

## we will check if all required columns in hitlog file are available if no raise error ##

    missing_columns = [  ## --> checks columns in DF and compare with required_columns

        column for column in required_columns
            if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"missing required columns: {missing_columns}")

    print ("hitlog file loaded successfully...")

    return df[required_columns].copy()

## cleaning and validate stage of source hitlog file ####
def clean_hitlog(df):

    for column in ["page_name", "page_url", "user_id"]: # ----> remove leading & Trailing spaces in data if present
        df[column] = df[column].astype("string").str.strip()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce") # ---> convert timestamp into datetime format 

    df = df.dropna(subset = ["user_id", "page_url", "timestamp"]) # ---> remove records with missing values 

    df = df[ (df["user_id"] != "") & (df["page_url"] != "") ] # --> remove records if user id, page url is null
    
    ### using url as page name if page name is missing ###

    blank_names = df["page_name"].isna() | (df["page_name"] == "")
    df.loc[blank_names, "page_name"] = df.loc[blank_names, "page_url"]

    ### removing excat dubpilcate rows if user visists to same url many times  ###

    df = df.drop_duplicates()

    print("data cleaning completed...")

    return df.reset_index(drop=True)

