from src.ingestion import read_hitlog, clean_hitlog
from src.transformation import (calculate_article_counts, get_top_three)
from src.output import write_output

#from src.config import settings

def main():

    input_path = "data/hitlog.csv"
    output_path = "data/output.csv"

   # input_path = settings["input"]
   # output_path = settings["output"]

    print("Starting telegraph data pipeline...")

    df =  read_hitlog(input_path)

    df = clean_hitlog(df)

    article_counts = calculate_article_counts(df)

    top_articles = get_top_three(article_counts)

    write_output(top_articles, output_path)

    print("Data pipeine excuted successfully...")

    print("\nTop 3 most influenced articles:")

    for article in top_articles:

        print(f"{article["page_name"]} influenced "
              f"{article["total"]} users")

if __name__ == "__main__":
    main()