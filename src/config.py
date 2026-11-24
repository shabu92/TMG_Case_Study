# import os

# # get env
# ENV = os.getenv("ENV", "dev").lower()

# # env configuration
# CONFIG ={

#     "dev":
#     {
#         "input": "envdata/dev/hitlog.csv",
#         "output": "envdata/dev/hitlog.csv"
#     },
#     "staging":
#     {
#         "input": "envdata/staging/hitlog.csv",
#         "output": "envdata/staging/hitlog.csv"
#     },
#     "prod":
#     {
#         "input": "envdata/prod/hitlog.csv",
#         "output": "envdata/prod/hitlog.csv"
#     }
# }

# # validate env
# if ENV not in CONFIG:
#     raise ValueError(f"Invalid env: {ENV}")

# settings = CONFIG[ENV]

# print(f"Running ENV: {ENV}")