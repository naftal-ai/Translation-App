Scraping the site https://www.morfix.co.il
and Saving the results in a local sqlite database

for lunch this application run:
    #install requirements
    'python -m pip install -r ./requirements.txt'

then:
    #create the SQLite data base inside data folder
    'cd data'
    'python create_db.py'
    'cd ../'

then:
    #lunch the application
    'python ./main.py'


TODOs:
    - Design the UI more friendly
    - Design the db to match inflections search
    - Add Feature:
        Make test of all the words user translated
        rate the words according to times search each word
        integrate with AI chatbot to create short stories contain specific words  
