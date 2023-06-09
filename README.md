# Конвертация аудиофайла из wav в mp3
***
* стэк (python 3.10.4, Flask, SQLAlchemy, Postgres)
***
Реализован веб-сервис со следующими REST методами:
- Создание пользователя, POST:
  - Принимает на вход запросы с именем пользователя;
  - Создаёт в базе данных пользователя С заданным именем, 
  генерирует уникальный идентификатор пользователя и UUID
  токен доступа (в виде строки) для данного пользователя;
  - Возвращает сгенерированные идентификатор пользователя и
  токен.
- Добавление аудиозаписи, POST:
  - Принимает на вход запросы, содержащие уникальный
    идентификатор пользователя, токен доступа и аудиозапись в
    формате wav;
  - Преобразует аудиозапись в формат mp3, генерирует для неё
    уникальный UUID идентификатор и сохраняет их в базе данных;
  - Возвращает URL для скачивания записи вида
    http://host:port/record?id=id_записи&user=id_пользователя.
- Доступ к аудиозаписи, GET:
  - Предоставляет возможность скачать аудиозапись по ссылке, 
    полученной в результате предыдущего POST запроса.
  
### Старт проекта:
##### Установите зависимости проекта с помощью команды:
```
pip install -r requirements.txt
```
##### Создайте файл .env со следующими переменными и присвойте им свои значения:
```
DB_PASSWORD=...
DB_USER=...
DB_NAME=...
DB_HOST=localhost
```
##### Убедитесь, что у вас установлен Docker. 
Для запуска БД и приложения выполните команду:
```
docker-compose up -d
```
##### Установите Postman или утилиту curl.
Для создания и сохранения пользователя в базе данных, отправьте
POST запрос на адрес http://127.0.0.1:5000/user. В запросе укажите имя пользователя.
##### 
Примеры:
```
curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"Mike\"}" http://127.0.0.1:5000/user
```

```
Postman:
- Выберите запрос POST
- В адресной строке укажите http://127.0.0.1:5000/user
- На вкладке Body выберите raw JSON
- В теле запроса укажите {"name": "Mike"}
- Отправьте запрос, нажав на кнопку Send. 
```

В ответ на запрос вернется id и токен пользователя.
######
Для добавления аудиозаписи необходимо отправить POST запрос на адрес
http://127.0.0.1:5000/record. В форме запроса необходимо указать id пользователя,
токен доступа и аудиозапись в формате wav.

Примеры:
```
curl -X POST -F 'file=@/path/to/your/file' -F 'user_id=<id пользователя>' -F 'access_token=токен доступа' http://127.0.0.1:5000/record
```

```
Postman:
- Выберите запрос POST
- В адресной строке укажите http://127.0.0.1:5000/record
- На вкладке Body выберите form-data
- В теле запроса укажите следующие ключи и значения:
          - file: выберите аудиозапись в формате wav;
          - user_id: id пользователя;
          - access_token: токен доступа
- Отправьте запрос, нажав на кнопку Send. 
```
В результате запроса вернется ссылка, по которой можно будет скачать аудиозапись 
в формате mp3.

***
Так как аудиозапись перед сохранением конвертируется в формат,
Установите аудио кодек FFmpeg или Libav:

- Для Windows: Скачайте FFmpeg отсюда https://www.gyan.dev/ffmpeg/builds/ , распакуйте его и добавьте путь к исполняемому файлу в переменную PATH.
- Для macOS: Установите FFmpeg с помощью Homebrew командой `brew install ffmpeg` .
- Для Debian/Ubuntu Linux: Установите Libav с помощью команды `sudo apt-get install libav-tools`
***