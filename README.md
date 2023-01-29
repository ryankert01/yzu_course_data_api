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


一個課程資料包含：
```
[course Website, course ID, 系所, 課名, 英語上課？, 必修選修, 上課時間，地點, 老師]
```

api response example: (300,301,302,...
```json
{
  "300": [[]], # no class exist in this option
  "301": [[]],
  "302": [
    [], # the first is always empty
    [
      "https://portalfun.yzu.edu.tw/cosSelect/Cos_Plan.aspx?y=111&s=1&id=ME108&c=A",  # course Website
      "ME108 A",  # course ID
      "機械工程學系學士班 1年級",  # 系所
      "應用力學靜力",     ＃ 課名
      false,     # 英語上課？
      "系必修",    ＃必修選修
      ["207", "3208", "208", "3208", "209", ",3208"],   ＃上課時間，地點
      "何旭川(Shiuh-Chuan Her)"。  ＃老師
    ],
    [
      "https://portalfun.yzu.edu.tw/cosSelect/Cos_Plan.aspx?y=111&s=1&id=ME108&c=B",
      "ME108 B",
      "機械工程學系學士班 1年級",
      "應用力學靜力",
      true,
      "系必修",
      ["406", "3208", "407", "3208", "408", ",3208"],
      "余念一(Niann-i Yu)"
    ],
    ...
```
