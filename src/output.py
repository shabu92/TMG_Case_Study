import pandas as pd 

def write_output(results, output_path):

    columns = [ "page_name", "page_url", "total"] ## ---> columns reuired in output

    output_df = pd.DataFrame(results, columns=columns)

    output_df.to_csv(output_path, index=False)  ## --> to write output file

    print("output file generated successfully...")