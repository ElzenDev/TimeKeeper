import os
script_dir = os.path.dirname(__file__)
database_path = os.path.join(os.path.dirname(script_dir), "data" ,"processes.db") 
print(database_path)
