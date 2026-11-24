import pandas as pd
import pytest
from src.transformation import calculate_article_counts, get_top_three
from src.ingestion import read_hitlog


### check if CSV exsit ###

def test_file_exist(tmp_path): ## --> check if CSV file exist or not

    file_path = tmp_path / "hitlog.csv" ## --> temp directory for hitlog.csv

    data = {
            "page_name": ["Article 1"],
            "page_url": ["/articles/a1"],
            "user_id": ["user1"],
            "timestamp":[
                "2026-11-01 10:00:00"
        ]
    }

    pd.DataFrame(data).to_csv(file_path, index=False) ## --> we are converting dict into dataframe and save to CSV in temp path

    assert file_path.exists() ## --> condition to check if file exist  

### check if CSV loaded correct or not ###

def test_file_loaded(tmp_path):

    file_path = tmp_path / "hitlog.csv"

    data = {
            "page_name": ["Article 1"],
            "page_url": ["/articles/a1"],
            "user_id": ["user1"],
            "timestamp":[
                "2026-11-01 10:00:00"
        ]
    }
    pd.DataFrame(data).to_csv(file_path, index=False)

    result = read_hitlog(file_path)

    assert not result.empty ## --> check if csv is not empty 
    assert len(result) == 1 ## ---> checks for how many rows loaded 
    assert list(result.columns) == [ ## ---> compare coulmns with actual df if coulmns are same then passed 

        "page_name", "page_url", "user_id", "timestamp"
    ]

## checking if articles count is correct - one article visit get counted as 1? ###

def test_article_count():
    data = {
        "page_name": ["Article 1", "registration"],
        "page_url": ["/articles/a1", "/register"],
        "user_id": ["user1", "user1"],
        "timestamp": pd.to_datetime([
            "2026-11-01 10:00:00",
            "2026-11-01 10:05:00"
        ])
    }

    df = pd.DataFrame(data)

    result = calculate_article_counts(df)

    expected = {
        ("Article 1", "/articles/a1"): 1
    }

    assert result == expected

### TEST CASE 2 ignore articles visited after registration ###

def test_article_after_register():
    data = {
        "page_name": ["registration", "Article 1"],
        "page_url": ["/register", "/articles/a1"],
        "user_id": ["user1", "user1"],
        "timestamp": pd.to_datetime([
            "2026-11-01 10:00:00",
            "2026-11-01 10:05:00"
        ])
    }

    df = pd.DataFrame(data)

    result = calculate_article_counts(df)

    assert result == {}

### TEST CASE 3 ---> count article only once per user - Same user visits article twice, count only once ###

def test_duplicate_article_visit():
    data = {
            "page_name": ["Article 1", "Article 1", "registration"],
            "page_url": ["/articles/a1", "/articles/a1", "/register"],
            "user_id": ["user1", "user1", "user1"],
            "timestamp": pd.to_datetime([
                "2026-11-01 10:00:00",
                "2026-11-01 10:02:00",
                "2026-11-01 10:05:00"
        ])
    }

    df = pd.DataFrame(data)

    result = calculate_article_counts(df)

    expected = {
            ("Article 1", "/articles/a1"): 1
        }

    assert result == expected


### TEST CASE 4 ---> ignore users who dont register ###

def test_user_without_registration():
    data = {
            "page_name": ["Article 1"],
            "page_url": ["/articles/a1"],
            "user_id": ["user1"],
            "timestamp": pd.to_datetime([
                "2026-11-01 10:00:00",
        ])
    }

    df = pd.DataFrame(data)
    
    result = calculate_article_counts(df)

    assert result == {}


    ### TEST CASE 5 ---> checking for top 3 articles are getting or not ###

def test_get_top_three_influenced():

    data = {
        ("Article 1", "/articles/a1"): 3,
        ("Article 2", "/articles/a2"): 2,
        ("Article 3", "/articles/a3"): 1,
        ("Article 4", "/articles/a4"): 4,
    }

    result = get_top_three(data)

    assert len(result) == 3
    assert result[0]["page_name"] == "Article 4"
    assert result[0]["total"] == 4
    assert result[1]["page_name"] == "Article 1"
    assert result[2]["page_name"] == "Article 2"
        








