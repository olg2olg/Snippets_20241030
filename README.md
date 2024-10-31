# Snippets

## Инструкция по развертыванию проекта
1. `python3 -m venv django_venv`

2. `source django_venv/bin/activate`

3. `pip install -r requirements.txt`

4. `python manage.py migrate`

5. `python manage.py runserver`


## Запуск `ipython` в контексте `django` приложений
```
python manage.py shell_plus --ipython
```

## Выгрузка и загрузка данных при работе с БД
### Выгрузить данные из БД
```
python manage.py dumpdata MainApp --indent 4 > MainApp/fixtures/save_all.json
python manage.py dumpdata > fixtures/db_all.json

```
### Загрузить данные в БД
```
python manage.py loaddata MainApp/fixtures/save_all.json
```
----------------------------------------------------------------------------
0) Репозиторий был сделан дома с нуля и залит на github
1) Поэтому в Москве:
    git clone https://github.com/olg2olg/Snippets_20241030.git Snippets
    git remote -v 
2) когда захочу в Мосвк залить, то надо переподключить: 
    { git remote set-url origin [NEW_REMOTE_URL]
      git@github.com:olg2olg/Snippets_20241030.git }
    git add .
    commit -m "Module5:tesk11-12"
    git remote set-url origin git@github.com:olg2olg/Snippets_20241030.git
    git remote -v
        origin	git@github.com:olg2olg/Snippets_20241030.git (fetch)
        origin	git@github.com:olg2olg/Snippets_20241030.git (push)
    git push
        Enumerating objects: 19, done.
        Counting objects: 100% (19/19), done.
        Delta compression using up to 2 threads
        Compressing objects: 100% (10/10), done.
        Writing objects: 100% (10/10), 1.09 KiB | 1.09 MiB/s, done.
        Total 10 (delta 9), reused 0 (delta 0), pack-reused 0
        remote: Resolving deltas: 100% (9/9), completed with 9 local objects.
        To github.com:olg2olg/Snippets_20241030.git
        8299d78..5396155  master -> master
3) дома надо будет вначале обновить
    git pul


