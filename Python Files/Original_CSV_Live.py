# pip install --user requests
# pip install --user beautifulsoup4

import requests, bs4, csv, datetime

downloaded_file = requests.get("https://www.jobs.ac.uk/search/?sortOrder=1&pageSize=10000")
parsed_file = bs4.BeautifulSoup(downloaded_file.text, 'html.parser')

titles = parsed_file.select('.j-search-result__text > a')

departments = parsed_file.select('.j-search-result__department')

employers = parsed_file.select('.j-search-result__employer')

salaries = parsed_file.select('.j-search-result__info')

close_date = parsed_file.select('.j-search-result__date--blue')

print()
print('There are ' + str(len(titles)) + ' Job Titles')
print('There are ' + str(len(departments)) + ' Departments')
print('There are ' + str(len(employers)) + ' Employers')
print('There are ' + str(len(salaries)) + ' Salaries')
print('There are ' + str(len(close_date)) + ' Closing Dates')

n = 0

filename = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")

with open('jobs_dump_' + str(filename) + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
    
    csvwriter = csv.writer(csvfile, dialect='excel')
    
    csvwriter.writerow(['Title', 'Department', 'Employer', 'Salary', 'Closing Date','URL'])

    while n < len(titles):

        url = r'=HYPERLINK("https://www.jobs.ac.uk' + titles[n].get('href') + r'","link")'

        csvwriter.writerow([(titles[n].getText().strip()), (departments[n].getText().strip()), (employers[n].getText().strip()), (" ".join(salaries[n].getText().strip().replace("\n","").split())).replace('Salary:',''), (close_date[n].getText().strip()), url ])
        n +=1