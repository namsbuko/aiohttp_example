# aiohttp_example

заполнить backend/.env

docker-compose up


# Описание API

content-type - json/application, 
авторизация через заголовок Authorization -  Bearer <token>, например

Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lX2RhdGEiOiJzb21lX2RhdGEifQ.37mVV0tV-AwWlT77mUMBSg3xCXkPBGkGKiU5IVTuOx8

Content-Type: application/json

роуты:

/login - получение токена, сделал get запрос, исключительно для теста

/<client_id>/<tariff_id> - получение инфо о клиенте и тарифе

# Вкратце расскажите об использованных технологиях
Использовал aiohttp, aioredis, jwt. Для развертывания docker-compose. Все стандартно. Единственное, проверку jwt токена делает nginx, что бывает удобно при использовании микросервисов

Если используется JWT - пожалуйста, пару API ключей для разных клиентов
Для всех клиентов ключи одинаковые, поскольку сущности самого клиента не вводил, получить ключ можно через api - /login

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lX2RhdGEiOiJzb21lX2RhdGEifQ.37mVV0tV-AwWlT77mUMBSg3xCXkPBGkGKiU5IVTuOx8

