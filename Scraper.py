#!/usr/bin/env python3

# pip install --user requests
# pip install --user beautifulsoup4

import requests, bs4, csv, datetime, os

list_of_titles = []

if os.path.exists('jobs_dump.csv'):
    with open('jobs_dump.csv', newline='', encoding='utf-8') as csvfile:
        myreader = csv.reader(csvfile, dialect='excel')
        for row in myreader:
            list_of_titles.append(row[0])
        print(f'File exists. There are {len(list_of_titles)-1} jobs currently in the sheet.')
else:
    print('File does not exist. File will be created shortly.')

print()

downloaded_file = requests.get("https://www.jobs.ac.uk/search/?sortOrder=1&pageSize=10000")
print('Downloaded data from website.')

parsed_file = bs4.BeautifulSoup(downloaded_file.text, 'html.parser')

titles = parsed_file.select('.j-search-result__text > a')
departments = parsed_file.select('.j-search-result__department')
employers = parsed_file.select('.j-search-result__employer')
salaries = parsed_file.select('.j-search-result__info')
close_date = parsed_file.select('.j-search-result__date--blue')

print('Parsed data from website.')
print()

if len(titles) == len(departments) == len(employers) == len(salaries) == len(close_date):
    print(f'The website currently has {len(titles)} jobs listed.')
else:
    print(f'There is a problem with the retrieval. There were an inconsistent number of titles, departments, employers, salaries and closing dates.')

print()

n = 0
records_added = 0
timenow = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")

with open('jobs_dump.csv', 'a', newline='\n', encoding='utf-8') as csvfile:
    
    csvwriter = csv.writer(csvfile, dialect='excel')
    
    if len(list_of_titles) < 1:
        csvwriter.writerow(['Title', 'Department', 'Employer', 'Salary', 'Closing Date','URL'])

    for title in titles:

        if titles[n].getText().strip() not in list_of_titles:

            url = r'=HYPERLINK("https://www.jobs.ac.uk' + titles[n].get('href') + r'","link")'
            csvwriter.writerow([(titles[n].getText().strip()), (departments[n].getText().strip()), (employers[n].getText().strip()), (" ".join(salaries[n].getText().strip().replace("\n","").split())).replace('Salary:',''), (close_date[n].getText().strip()), url ])
            records_added +=1

            if records_added %1000 == 0:
                print(f'Added {records_added} records.')
        n +=1
    
    if records_added > 1000:
        print()

if records_added > 0:
    print(f'Updated - added {str(records_added)} records.')
else:
    print('Updated - no new records added.')