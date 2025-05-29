Сайт, который анализирует указанные страницы на SEO-пригодность по аналогии с PageSpeed Insights. 

Установка:

1. Склонируйте репозиторий с проектом на ваше локальное устройство:
git clone https://github.com/0pilione/python-project-83.git
2. Перейдите в директорию проекта:
cd python-project-83
3. Установите необходимые зависимости с помощью Poetry:
make install
4. Создайте файл .env, который будет содержать ваши конфиденциальные настройки:
touch .env
5. Откройте файл .env и задайте значения для ключей SECRET_KEY и DATABASE_URL.
Затем запустите команды из database.sql в SQL-консоли вашей базы данных, чтобы создать необходимые таблицы.

Использование:

Для запуска сервера Flask с помощью Gunicorn выполните команду:
make start

По умолчанию сервер будет доступен по адресу http://0.0.0.0:8000.

Также можно запустить сервер локально в режиме разработки с активным отладчиком:
make dev

Сервер для разработки будет доступен по адресу http://127.0.0.1:8000.

Чтобы добавить новый сайт, введите его адрес в форму на главной странице. Введенный адрес будет проверен и добавлен в базу данных.

После добавления сайта можно начать его проверку. На странице каждого конкретного сайта появится кнопка, и нажав на нее, вы создадите запись в таблице проверки.

Все добавленные URL можно увидеть на странице /urls.

Способы использования:

Проект можно использовать локально и онлайн (например с помощью стороннего сервиса render.com).

### Hexlet tests and linter status:
[![Actions Status](https://github.com/0pilione/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/0pilione/python-project-83/actions)
[![GitHub Actions Demo](https://github.com/0pilione/python-project-83/actions/workflows/github-actions-demo.yml/badge.svg)](https://github.com/0pilione/python-project-83/actions/workflows/github-actions-demo.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=0pilione_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=0pilione_python-project-83)
