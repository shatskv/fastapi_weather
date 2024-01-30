# API на FASTAPI для получения погоды с [openweathermap.org](https://openweathermap.org/)

API умеет: 
- Получать погоду с [openweathermap.org](https://openweathermap.org/) и отдавать ее пользователю

## Как установить

- Python3 должен быть установлен
- Затем используйте `pip` (или `pip3`, еслить есть конфликт с Python2) для установки зависимостей: 
    ```
    pip install -r requirements.txt
    ```

- Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.


## Как пользоваться
API можно запустить через терминал и через докер
В корне проекта нужно создать файл **.env** указав токен с [openweathermap.org](https://openweathermap.org/):
```
APP_ID=1233233dffds33fsdsd
```
### Запуск через терминал:
```
make run
```
### Запуск тестов
```
make tests
```
Обратиться к API по *localhost:8000* через HTTP-клиент
##№ Запуск через docker:
- Образ собирается при пуше в Github, для этого нужно создать токен и указать его в **secrets**, дав имя "DOCKER_TOKEN"
- Запустить контейнер, указав файл **.env**:
    ```
    docker run -p 8001:8000 --env-file=.env ghcr.io/{{ github.repository_owner }}/fast-api-weather:latest
    ```
   *-p 8001:8000*: 8001 - внешний порт, к которому нужно обращаться (можно поменять), 8000 - внутренний порт API в контейнере
- Обратиться к API по *localhost:8001* через HTTP-клиент
- Город нужно передевать в параметре *city*:
![screenshot](https://i.ibb.co/j4QqNVM/api-weather.png)
- Ответ будет получен в *body* в формате *json*


## Цель проекта

Код написан в образовательный целях на онлайн-курсе для python-разработчиков [learn.python.ru/advanced/](https://learn.python.ru/advanced/)
