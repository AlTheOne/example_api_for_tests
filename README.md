# Example app


DockerHub Image: https://hub.docker.com/r/altheone/example_app

## Local run

1. Install deps
```
pip install -r requirements.txt
```

2. Go in app dir
```
cd ./app
```

4. Run app
```
uvicorn main:app 
```

5. Open docs url [http://localhost:8000/docs](http://localhost:8000/docs)


## Run docker

1. Build image
```
docker build -t altheone/example_app .
```

2. Run container
```
docker run --name example_app -p 8000:80 altheone/example_app
```

3. Open docs url [http://localhost:8000/docs](http://localhost:8000/docs)


## Send to DockerHub

1. Зарегестрируйтесь на [DockerHub](https://hub.docker.com/)

2. Создайте репозиторий.

Пример: https://hub.docker.com/r/altheone/example_app

4. Создайте токен

5. Добавьте авторизационный токен

```shell
docker login -u <DOCKER_HUB_LOGIN>
```

* Команда запросит пароль. В качестве пароля введите полученный токен.

5. Создайте образ
```shell
docker build -t <DOCKER_HUB_LOGIN>/<REPO_NAME> .
```

- `<DOCKER_HUB_LOGIN>` - Логин на ресурсе DockerHub.
- `<REPO_NAME>` - Название репозитория на ресурсе DockerHub.

Например: `docker build -t altheone/example_app .`

6. Проверьте работоспособность приложения.
```shell
docker run -p 8000:80 <DOCKER_HUB_LOGIN>/<REPO_NAME>
```

Например: `docker run -p 8000:80 altheone/example_app`

Приложение должно быть доступно по адресу: `http://localhost:8000`

7. Отправьте образ в DockerHub
```shell
docker push <DOCKER_HUB_LOGIN>/<REPO_NAME>
```

Например: `docker push altheone/example_app`
