# YZU course Info scrapping

scrape all course value and generate json file in `course_data/index.json`.

## environment variable

if not in github action but want to execute it locally, use `gen.py`.
And, change the followings credentials.

```python
info[1] = 'portal_password'
info[0] = 'partal_accountNumber eg.s1113339'
```

## Run

```sh
pip install -r requirements.txt
python gen.py
```

## API

https://www.ryankert.cc/python-testing-ci-cd/
