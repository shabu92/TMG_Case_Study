import pandas as pd

article_prefix = "/articles/"
registration_url = "/register"

### main logic - here we will calculate how many unique users were influenced by each articles before registering  ###
def calculate_article_counts(df):
    
    article_counts = {}  # dict key value pair

    df["timestamp"] = pd.to_datetime(df["timestamp"]) ## --> convert timestamap in to date time

    for user_id, user_data in df.groupby("user_id"):     ##---> group records by individual user

        registrations = user_data[user_data["page_url"] == registration_url ] ##--> for each user, identify reg record wth time 

        if registrations.empty:  ## --> if not registrered then ignores
            continue

        registration_time = registrations["timestamp"].min()  ## ---> consider the first reg event

        ## ---> finds articles visited before registering -- page url starts with articles & article vist bfr reg 
        article_visits = user_data[(user_data["page_url"].str.startswith(article_prefix)) &
                (user_data["timestamp"] < registration_time)
        ]

        ## ---> remove duplicate article visits for same user(if same user visits same articles mul times)
        unique_articles = article_visits.drop_duplicates(subset=["page_url"])

        ## ---> loping unique articles and increase count for each eligible article
        for _, article in unique_articles.iterrows():

            page_name = article["page_name"]
            page_url = article["page_url"]

            key = (page_name, page_url) # python tuple -- to identfy article using both name and url

            article_counts[key] = article_counts.get(key, 0) + 1

    print("final article counts:", article_counts)

    return article_counts

### Here we will sort articles by total count and return top 3  ###

def get_top_three(article_counts): 

    results = []

    for (page_name, page_url), total in article_counts.items():  ##---> get both keys and values from dict

        results.append({"page_name": page_name, # --> covert dic info to list of dict
                        "page_url": page_url,
                        "total": total
        })

        results.sort(key=lambda x: (  ###----> sort by desc and use url fo rsecondary sort for crt results
            -x["total"],
            x["page_url"],
            x["page_name"]
        ))

    return results[:3] ## --> return only top 3 records 

