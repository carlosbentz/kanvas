# Kanvas
Api para um sistema de cursos, com alunos, atividades, notas e submissões.


# Este passo é para baixar o projeto
`git clone https://gitlab.com/carlosbentz/kanvas`

## Entrar na pasta
`cd kanvas`

## Criar um ambiente virtual
`python3 -m venv venv`

## Entrar no ambiente virtual
`source venv/bin/activate`

## Instalar as dependências
`pip install -r requirements.txt`

## Criar o banco de dados
`./manage.py migrate`

## Rodar localmente
`./manage.py runserver`

Por padrão, irá rodar em `http://127.0.0.1:8000/`

# Testes

## Rodar os testes
Para rodar os testes, apenas utilizar o comando no terminal:

` python manage.py test -v 2 &> report.txt`

## Sobre Usuários:

Esta plataforma terá 3 tipos de usuário:

-   Estudante
-   Facilitador
-   Instrutor

Você deverá utilizar os campos que vêm no User padrão do Django, ou seja:

Para diferenciar entre os tipos de acesso, você deverá trabalhar com os campos `is_staff` e `is_superuser`, sendo que:

-   Estudante - terá ambos os campos `is_staff` e `is_superuser` com o valor `False`
-   Facilitador - terá os campos `is_staff` == `True` e `is_superuser` == `False`
-   Instrutor - terá ambos os campos `is_staff` e `is_superuser` com o valor `True`


# Rotas

## Sobre Criação de Usuários:


### `POST /api/accounts/` 

```json

      // REQUEST
      {
        "username": "student",
        "password": "1234",
        "is_superuser": false,
        "is_staff": false
      }
      
```

```json

      // RESPONSE STATUS -> HTTP 201
      {
        "id": 1,
        "username": "student",
        "is_superuser": false,
        "is_staff": false
      }
      
```

Caso haja a tentativa de criação de um usuário que já está cadastrado o sistema irá responder com `HTTP 409 - Conflict`.

## Sobre Autenticação:

A API funcionará com autenticação baseada em token.

### `POST /api/login/` 

```json

      // REQUEST
      {
        "username": "student",
        "password": "1234"
      }
      
```

```json

      // RESPONSE STATUS -> HTTP 200
      {
        "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
      } 
      
```

Esse token servirá para identificar o usuário em cada request. Na grande maioria dos endpoints seguintes, será necessário colocar essa informação nos `Headers`. O header específico para autenticação tem o formato `Authorization: Token <colocar o token aqui>`.


Caso haja a tentativa de login de uma conta que ainda não tenha sido criada, o sistema irá retornar HTTP 401 - Unauthorized.


## Sobre Cursos:

`Course` é um model que representa um curso dentro da plataforma Kanvas. Apenas um `User` com acesso de instrutor (ou seja `is_superuser == True`) pode criar novos cursos, matricular usuários nos cursos e excluir cursos.

### `POST /api/courses/` 

```json

      // REQUEST
      // Header -> Authorization: Token <token-do-instrutor>
      {
        "name": "Node"
      }
      
```

```json

      // RESPONSE STATUS -> HTTP 201
      {
        "id": 1,
        "name": "Node",
        "users": []
      }
      
```

Não deve ser possível criar dois cursos com o mesmo nome, caso haja a tentativa de criação de um curso já existente, o sistema não irá criar um novo curso, apenas retornar o curso já existente.

### `PUT /api/courses/<int:course_id>/registrations/`

Para esse endpoint deve ser informada uma lista de id's de estudantes para serem matriculados no curso, caso não seja informada uma lista, o sistema irá responder com `HTTP 400 - Bad request`.

```json

      // REQUEST
      // Header -> Authorization: Token <token-do-instrutor>
      {
        "user_ids": [3, 4, 5]
      }
      
```

```json

      // RESPONSE STATUS -> HTTP 200
      {
        "id": 1,
        "name": "Node",
        "users": [
          {
            "id": 3,
            "username": "student1"
          },
          {
            "id": 4,
            "username": "student2"
          },
          {
            "id": 5,
            "username": "student3"
          }
        ]
      }
      
```

Desta forma é possível matricular vários alunos simultaneamente. Da mesma maneira, é possível remover vários estudantes ao mesmo tempo ao registrar novamente a lista de alunos.

```json

      // REQUEST
      // Header -> Authorization: Token <token-do-instrutor>
      {
        "user_ids": [3]
      }
      
```

```json

      // RESPONSE STATUS -> HTTP 200
      {
        "id": 1,
        "name": "Node",
        "users": [
          {
            "id": 3,
            "username": "student1"
          }
        ]
      }
      
```

Toda requisição feita para esse endpoint irá atualizar a lista de alunos matriculados no curso. No primeiro exemplo os alunos 3, 4 e 5 foram vinculados ao curso 1. Já na segunda requisição a lista de alunos foi atualizada, matriculando somente o aluno 3 e removendo os alunos 4 e 5 que não estavam na nova listagem.

Somente usuários do tipo estudante (ou seja, `is_staff == False` e `is_superuser == False`) podem ser matriculados no curso, caso essa regra não seja atendida, a aplicação irá responder da seguinte maneira:

```json

      // RESPONSE STATUS -> HTTP 400
      {
        "errors": "Only students can be enrolled in the course."
      }
      
```

Caso seja informado um `course_id` inválido, o sistema irá responder com `HTTP 404 - Not found.`

```json

      // RESPONSE STATUS -> HTTP 404
      {
        "errors": "invalid course_id"
      }
      
```

Caso sejam informados algum `user_id inválido`, a resposta será:

```json

      // RESPONSE STATUS -> HTTP 404
      {
        "errors": "invalid user_id list"
      }
      
```

### `GET /api/courses/`

Este endpoint pode ser acessado por qualquer client (mesmo sem autenticação). A resposta do servidor deve trazer uma lista de cursos, mostrando cada aluno inscrito, no seguinte formato:

```json

      // RESPONSE STATUS -> HTTP 200
      [
        {
          "id": 1,
          "name": "Node",
          "users": [
            {
              "id": 3,
              "username": "student1"
            }
          ]
        },
        {
          "id": 2,
          "name": "Django",
          "users": []
        },
        {
          "id": 3,
          "name": "React",
          "users": []
        }
      ]
      
```

### `GET /api/courses/<int:course_id>/`
Este endpoint pode ser acessado por qualquer client (mesmo sem autenticação). A resposta do servidor irá trazer o elemento filtrado pelo `course_id` informado na url, e deverá ter o seguinte formato.

```json

      // RESPONSE STATUS -> HTTP 200
      {
        "id": 1,
        "name": "Node",
        "users": [
          {
            "id": 3,
            "username": "student1"
          }
        ]
      }
      
```

Caso seja informado um `course_id` inválido, o sistema irá responder com `HTTP 404 - Not found.`

```json

      // RESPONSE STATUS -> HTTP 404
      {
        "errors": "invalid course_id"
      }
      
```

### `DELETE /api/courses/<int:course_id>/`

Este endpoint somente poderá ser acessado por um instrutor e ele realizará a exclusão do curso no sistema.

```json

      // REQUEST
      // Header -> Authorization: Token <token-do-instrutor>
      
```

```json

      // RESPONSE STATUS -> HTTP 204 NO CONTENT
      
```

Caso seja informado um `course_id` inválido, o sistema irá responder em `HTTP 404 - Not found`.

## Sobre Atividades e Submissões:

`Activity` representa uma atividade cadastrada no sistema pelos facilitadores ou instrutores para que os alunos possam fazer suas submissões.

`Submission` representa uma submissão de uma atividade feita por um aluno.


### `POST /api/activities/`

```json

// REQUEST
// Header -> Authorization: Token <token-do-facilitador ou token-do-instrutor>
{
  "title": "Kenzie Pet",
  "points": 10
}
      
```

```json

      // RESPONSE STATUS -> HTTP 201
      {
        "id": 1,
        "title": "Kenzie Pet",
        "points": 10,
        "submissions": []
      }
      
```

Não é possível criar duas atividades com o mesmo título, caso haja a tentativa de criação de uma atividade com o mesmo título, o sistema não irá criar uma nova atividade, mas sim, retornar a atividade já existente.

### `GET /api/activities/`

```json

// REQUEST
// Header -> Authorization: Token <token-do-instrutor ou token-do-facilitador>
      
```

```json

      // RESPONSE STATUS -> HTTP 200
      [
        {
          "id": 1,
          "title": "Kenzie Pet",
          "points": 10,
          "submissions": [
            {
              "id": 1,
              "grade": 10,
              "repo": "http://gitlab.com/kenzie_pet",
              "user_id": 3,
              "activity_id": 1
            }
          ]
        },
        {
          "id": 2,
          "title": "Kanvas",
          "points": 10,
          "submissions": [
            {
              "id": 2,
              "grade": 8,
              "repo": "http://gitlab.com/kanvas",
              "user_id": 4,
              "activity_id": 2
            }
          ]
        },
        {
          "id": 3,
          "title": "KMDb",
          "points": 9,
          "submissions": [
            {
              "id": 3,
              "grade": 4,
              "repo": "http://gitlab.com/kmdb",
              "user_id": 5,
              "activity_id": 3
            }
          ]
        }
      ]
      
```

### `POST /api/activities/<int:activity_id>/submissions/`
```json

      // REQUEST
      // Header -> Authorization: Token <token-do-estudante>
      {
        "grade": 10, // Esse campo é opcional
        "repo": "http://gitlab.com/kenzie_pet"
      }
      
```

```json

      // RESPONSE STATUS -> HTTP 201
      {
        "id": 7,
        "grade": null,
        "repo": "http://gitlab.com/kenzie_pet",
        "user_id": 3,
        "activity_id": 1
      }
      
```

Podemos observar que nesse request o campo `grade` foi informado, e a resposta do sistema foi um `grade: null`, pois alunos não podem dar nota a si mesmos.


### `PUT /api/submissions/<int:submission_id>/`

Esta rota tem o propósito de avaliar a submissão do aluno, apenas instrutores ou facilitadores poderão utilizá-la.

```json

// REQUEST
// Header -> Authorization: Token <token-do-facilitador ou token-do-instrutor>
{
  "grade": 10
}
      
```

```json

      // RESPONSE STATUS -> HTTP 200
      {
        "id": 3,
        "grade": 10,
        "repo": "http://gitlab.com/kenzie_pet",
        "user_id": 3,
        "activity_id": 1
      }
      
```

### `GET /api/submissions/` 

```json

      //REQUEST
      //Header -> Authorization: Token <token-do-estudante>
      
```

```json

      // RESPONSE STATUS -> HTTP 200
      [
        {
          "id": 2,
          "grade": 8,
          "repo": "http://gitlab.com/kanvas",
          "user_id": 4,
          "activity_id": 2
        },
        {
          "id": 5,
          "grade": null,
          "repo": "http://gitlab.com/kmdb2",
          "user_id": 4,
          "activity_id": 1
        }
      ]
      
```

Observem que nesse caso o campo `user_id` é o mesmo para todas as submissões.

Caso seja informado um token de estudante o sistema deverá retornar apenas as submissões daquele estudante, caso seja informado um token de facilitador ou token de instrutor, a aplicação responderá com todas as submissões de todos os estudantes.

```json

//REQUEST
//Header -> Authorization: Token <token-do-facilitador ou token-do-instrutor>
      
```

```json

      // RESPONSE STATUS -> HTTP 200
      [
        {
          "id": 1,
          "grade": 10,
          "repo": "http://gitlab.com/kenzie_pet",
          "user_id": 3,
          "activity_id": 1
        },
        {
          "id": 2,
          "grade": 8,
          "repo": "http://gitlab.com/kanvas",
          "user_id": 4,
          "activity_id": 2
        },
        {
          "id": 3,
          "grade": 4,
          "repo": "http://gitlab.com/kmdb",
          "user_id": 5,
          "activity_id": 3
        },
        {
          "id": 4,
          "grade": null,
          "repo": "http://gitlab.com/kmdb2",
          "user_id": 5,
          "activity_id": 3
        }
      ]
      
```

Observe que o campo `user_id` tem valores diferentes.


## Tecnologias utilizadas 📱
-   Django
-   Django Rest Framework
-   SQLite

