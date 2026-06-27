# Talk to your DB
- This is a sql agent made using Langchain 
- you can use this tool to connect with your db and perform the sql operations with natural language(English) and agent calls the tools and performs the sql query and talks to your database.
- secured this agent so it doesnt delete or drop tables or info on its own.
- added Guadrails like Human in the loop to ask human permission before updating or inserting into db 
- delete can be done only manually (for more security reasons)
- Modular architecture
- Multi-model support (add how many ever model and can change ,(model agnostic agent))

## API Keys
- get your open ai api key
- and beready with postgress url for .env 

## Install reuirements 
- from requiremwnts.tx 
- pip install psycopg2-binary is for postgres