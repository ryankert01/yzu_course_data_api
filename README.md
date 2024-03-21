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

[https://ryankert01.github.io/yzu_course_data_api/](https://ryankert01.github.io/yzu_course_data_api/)



一個課程資料包含：
```
[course Website, course ID, 系所, 課名, 英語上課？, 必修選修, 上課時間，地點, 老師]
```

Yearly data: 
```json
{
  "111,1  ": {},
  "111,2  ": {},
  "110,1  ": {},
  "110,2  ": {}
}
```

api response example: (300,301,302,...代表系所或開課單位

```json
{
  "111,1  ": {  # yearly-data
    "300": [],  # no class exist in this option
    "301": [],
    "302": [
      {
        "courseURL": "https://portalfun.yzu.edu.tw/cosSelect/Cos_Plan.aspx?y=111&s=1&id=ME108&c=A",
        "courseID": "ME108 A",
        "courseYear": "機械工程學系學士班 1年級",
        "courseName": "應用力學靜力",
        "isEnglish": false,
        "courseType": "系必修",
        "courseTime": ["207", "3208", "208", "3208", "209", "3208"],
        "courseTeacher": "何旭川(Shiuh-Chuan Her)"
      },
      {
        "courseURL": "https://portalfun.yzu.edu.tw/cosSelect/Cos_Plan.aspx?y=111&s=1&id=ME108&c=B",
        "courseID": "ME108 B",
        "courseYear": "機械工程學系學士班 1年級",
        "courseName": "應用力學靜力",
        "isEnglish": true,
        "courseType": "系必修",
        "courseTime": ["406", "3208", "407", "3208", "408", "3208"],
        "courseTeacher": "余念一(Niann-i Yu)"
      }
    ]
  }
}
```
