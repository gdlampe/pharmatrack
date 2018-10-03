# Pharma Tracking
## How to use
### Run env
`source venv/bin/activate`

### Crawling data
Crawl drug from sources: `roche`, `gilead` and `pfizer`

`python manage.py runscript scrape --script-args roche pfizer`

#### Settings

Update maximum load page to crawl for pfizer:

[setting page](scripts/pfizer_header.py#L25)

`MAX_LOOP_PAGE = 2`

### Update study from CT

`python manage.py runscript study`

### Start server
`python manage.py runserver`