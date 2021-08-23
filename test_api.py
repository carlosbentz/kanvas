from django.test import TestCase
from rest_framework.test import APIClient


class TestAccountView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.student1_data = {
            "username": "student1",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False,
        }

        self.student1_login_data = {
            "username": "student1",
            "password": "1234",
        }

        self.facilitator_data = {
            "username": "facilitator",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True,
        }

        self.facilitator_login_data = {
            "username": "facilitator",
            "password": "1234",
        }

        self.instructor_data = {
            "username": "instructor",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True,
        }

        self.instructor_login_data = {
            "username": "instructor",
            "password": "1234",
        }

    def test_create_and_login_for_student_account(self):
        # criando um usuário do tipo student
        student_user = self.client.post(
            "/api/accounts/", self.student1_data, format="json"
        )

        # testa se o student user foi criado corretamente
        self.assertEqual(
            student_user.json(),
            {"id": 1, "username": "student1", "is_superuser": False, "is_staff": False},
        )
        self.assertEqual(student_user.status_code, 201)

        # testa se o login foi realizado corretamente e se o token é retornado
        response = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()

        self.assertIn("token", response.keys())

    def test_create_and_login_for_facilitator_account(self):
        # criando um usuário do tipo facilitator
        facilitator_user = self.client.post(
            "/api/accounts/", self.facilitator_data, format="json"
        )

        # testa se o facilitator user foi criado corretamente
        self.assertEqual(
            facilitator_user.json(),
            {
                "id": 1,
                "username": "facilitator",
                "is_superuser": False,
                "is_staff": True,
            },
        )
        self.assertEqual(facilitator_user.status_code, 201)

        # testa se o login foi realizado corretamente e se o token é retornado
        response = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()

        self.assertIn("token", response.keys())

    def test_create_and_login_for_instructor_account(self):
        # criando um usuário do tipo instructor user
        instructor_user = self.client.post(
            "/api/accounts/", self.instructor_data, format="json"
        )

        # testa se o instructor user foi criado corretamente
        self.assertEqual(
            instructor_user.json(),
            {"id": 1, "username": "instructor", "is_superuser": True, "is_staff": True},
        )
        self.assertEqual(instructor_user.status_code, 201)

        # testa se o login foi realizado corretamente e se o token é retornado
        response = self.client.post(
            "/api/login/", self.instructor_login_data, format="json"
        ).json()

        self.assertIn("token", response.keys())

    def test_wrong_credentials_do_not_login(self):
        # criando um usuário do tipo instructor
        response = self.client.post(
            "/api/accounts/", self.instructor_data, format="json"
        )

        # faz o login com os dados do facilitador, sendo que esse não foi criado
        # testa se o sistema não faz o login e retorna 401
        response = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_create_two_equals_users(self):
        # cria um usuário do tipo instructor
        response = self.client.post(
            "/api/accounts/", self.instructor_data, format="json"
        )
        
        # tenta criar novamente o usuário instructor, testa se o sistema retorna 409
        response_2 = self.client.post(
            "/api/accounts/", self.instructor_data, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_2.status_code, 409)


class TestCourseView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.student1_data = {
            "username": "student1",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False,
        }

        self.student1_login_data = {
            "username": "student1",
            "password": "1234",
        }

        self.student2_data = {
            "username": "student2",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False,
        }

        self.facilitator_data = {
            "username": "facilitator",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True,
        }

        self.facilitator_login_data = {
            "username": "facilitator",
            "password": "1234",
        }

        self.instructor1_data = {
            "username": "instructor",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True,
        }

        self.instructor1_login_data = {
            "username": "instructor",
            "password": "1234",
        }

        self.course_data = {"name": "course1"}
    
    def test_create_course_with_invalid_token(self):
        # criação de um instructor user
        self.client.post("/api/accounts/", self.instructor1_data, format="json")
        
        # Usando um token inválido
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "invalidtoken")
        
        # Tentativa de criação de um curso
        response = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )
        
        # Testa se retorna 401 e no body "invalid token"
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid token."})

    def test_instructor_can_create_course(self):
        # Criação de um instructor user
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Token de instrutor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Criação de um curso
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )

        # Testa se o retorno está correto e o status_code também
        self.assertDictEqual(course.json(), {"id": 1, "name": "course1", "users": []})
        self.assertEqual(course.status_code, 201)
    
    def test_create_two_courses_with_the_same_name_generate_the_same_ids(self):
        # Criação de um instructor user
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Token de instrutor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Criação do curso1
        course_1 = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )
        
        # Criação do curso1 novamente
        course_1_again = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )
        
        # Testa se os ids são iguais na criação do mesmo curso duas vezes 
        self.assertDictEqual(course_1.json(), {"id": 1, "name": "course1", "users": []})
        self.assertDictEqual(course_1_again.json(), {"id": 1, "name": "course1", "users": []})

    def test_facilitator_or_student_cannot_create_course(self):
        # Criação de um student user
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Estudante não pode criar cursos
        status_code = self.client.post(
            "/api/courses/", self.course_data, format="json"
        ).status_code
        self.assertEqual(status_code, 403)

        # Criação de um facilitator user
        self.client.post("/api/accounts/", self.facilitator_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Facilitador não pode criar cursos
        response = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You do not have permission to perform this action."})

    def test_anonymous_can_list_courses(self):
        # Criação de um instructor user
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação de um curso
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        ).json()

        # reset client -> no login
        client = APIClient()

        # Usuários anônimos podem listar os cursos e os alunos matriculados
        course_list = client.get("/api/courses/")

        self.assertEqual(
            course_list.json(), [{"id": 1, "name": "course1", "users": []}]
        )
        self.assertEqual(course_list.status_code, 200)
    
    def test_anonymous_can_filter_courses(self):
        # Criação de um instructor user
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação de um curso
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        ).json()

        # reset client -> no login
        client = APIClient()

        # Usuários anônimos podem listar os cursos e os alunos matriculados
        course_list = client.get("/api/courses/1/")

        self.assertEqual(
            course_list.json(), {"id": 1, "name": "course1", "users": []}
        )
        self.assertEqual(course_list.status_code, 200)
    
    def test_anonymous_cannot_filter_invalid_course(self):
        # Criação de um instructor user
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação de um curso
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        ).json()

        # reset client -> no login
        client = APIClient()

        # Usuários anônimos não podem filtrar curso, caso seja passado um course_id inválido.
        # Nesse caso ele está tentando filtrar o curso 2, porém só existe o curso 1 cadastrado
        course_list = client.get("/api/courses/2/", format='json')

        self.assertEqual(course_list.json(), {'errors': 'invalid course_id'})
        self.assertEqual(course_list.status_code, 404)
    
    def test_whether_a_list_is_entered_to_enroll_students_in_the_course(self):
        # create student 1
        self.client.post("/api/accounts/", self.student1_data, format="json")
        
        # create student 2
        self.client.post("/api/accounts/", self.student2_data, format="json")
        
        # create instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")
        
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # create course
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )
        
        # Matriculando os estudantes 1, porém ao invés de uma lista, é passado um inteiro
        response = self.client.put(
            "/api/courses/1/registrations/",
            {"user_ids": 1},
            format="json",
        )
        
        # Testa se retorna um status 400
        self.assertEqual(response.status_code, 400)

    def test_instructor_can_register_students_on_course(self):
        # Criação do student 1
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Criação student 2
        self.client.post("/api/accounts/", self.student2_data, format="json")

        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação do course
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        ).json()

        self.assertEqual(course, {"id": 1, "name": "course1", "users": []})

        # Matriculando os students 1 e 2 no course
        response = self.client.put(
            "/api/courses/1/registrations/",
            {"user_ids": [1, 2]},
            format="json",
        )

        self.assertEqual(len(response.json()["users"]), 2)
        self.assertEqual(response.status_code, 200)

        # Mudando os estudantes no curso, agora temos apenas o student 1
        response = self.client.put(
            "/api/courses/1/registrations/",
            {"user_ids": [1]},
            format="json",
        )
        self.assertEqual(len(response.json()["users"]), 1)
        self.assertEqual(response.json()["users"][0]["id"], 1)
        self.assertEqual(response.status_code, 200)

        # Mudando os estudantes no curso, agora temos apenas o student 2
        response = self.client.put(
            "/api/courses/1/registrations/",
            {"user_ids": [2]},
            format="json",
        )
        self.assertEqual(len(response.json()["users"]), 1)
        self.assertEqual(response.json()["users"][0]["id"], 2)
        self.assertEqual(response.status_code, 200)

        # Mudando os estudantes no curso, não temos nenhum estudante
        response = self.client.put(
            "/api/courses/1/registrations/",
            {"user_ids": []},
            format="json",
        )
        self.assertEqual(len(response.json()["users"]), 0)
        self.assertEqual(response.status_code, 200)
    
    def test_only_students_can_be_enrolled_in_the_course(self):        
        # Criação do facilitator user
        self.client.post("/api/accounts/", self.facilitator_data, format="json")

        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação do course
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )
        
        # Matriculando um facilitator user
        response = self.client.put(
            "/api/courses/1/registrations/",
            {"user_ids": [1]},
            format="json",
        )
        
        self.assertDictEqual(response.json(), {"errors": "Only students can be enrolled in the course."})
        self.assertEqual(response.status_code, 400)
        
        # Matriculando um instructor user
        response = self.client.put(
            "/api/courses/1/registrations/",
            {"user_ids": [2]},
            format="json",
        )
        
        self.assertDictEqual(response.json(), {"errors": "Only students can be enrolled in the course."})
        self.assertEqual(response.status_code, 400)
        
        # Matriculando um facilitator e instructor
        response = self.client.put(
            "/api/courses/1/registrations/",
            {"user_ids": [1, 2]},
            format="json",
        )
        
        self.assertDictEqual(response.json(), {"errors": "Only students can be enrolled in the course."})
        self.assertEqual(response.status_code, 400)
    
    def test_enrolls_students_with_invalid_course_id(self):
        # Criação do student 1
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Criação student 2
        self.client.post("/api/accounts/", self.student2_data, format="json")

        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação do course
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )

        # Matriculando os students 1 e 2 no course com id 2, 
        # porém não existe, pois só foi criado somente 1 curso até o momento
        response = self.client.put(
            "/api/courses/2/registrations/",
            {"user_ids": [1, 2]},
            format="json",
        )
        
        self.assertDictEqual(response.json(), {"errors": "invalid course_id"})
        self.assertEqual(response.status_code, 404)

    def test_enroll_students_with_invalid_id(self):
        # Criação do student 1
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Criação student 2
        self.client.post("/api/accounts/", self.student2_data, format="json")

        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação do course
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )

        # Matriculando os students 3 e 4 no course com id 1, 
        # porém esses alunos não existem, pois só foram criados os alunos com ids 1 e 2
        response = self.client.put(
            "/api/courses/1/registrations/",
            {"user_ids": [3, 4]},
            format="json",
        )
        
        self.assertDictEqual(response.json(), {"errors": "invalid user_id list"})
        self.assertEqual(response.status_code, 404)
        
    def test_instructor_can_delete_courses(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação do course
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )
        
        # Instrutor deleta curso
        delete_course = self.client.delete("/api/courses/1/", format="json")
        
        self.assertEqual(delete_course.status_code, 204)
        
        # Instrutor tenta deletar curso novamente (obs: ele não existe mais)
        delete_course = self.client.delete("/api/courses/1/", format="json")
        
        self.assertEqual(delete_course.status_code, 404)
    
    def test_student_or_facilitator_cannot_delete_courses(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")
        
        # Criação do facilitator
        self.client.post("/api/accounts/", self.facilitator_data, format="json")
        
        # Criação do student
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação do course pelo instructor
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        )
        
        # login do facilitator
        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Facilitator tenta deletar curso
        delete_course = self.client.delete("/api/courses/1/", format="json")
        
        self.assertEqual(delete_course.status_code, 403)
        
        # login do estudante
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Estudante tenta deletar curso
        delete_course = self.client.delete("/api/courses/1/", format="json")
        self.assertEqual(delete_course.status_code, 403)

class TestActivityView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.student1_data = {
            "username": "student1",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False,
        }

        self.student1_login_data = {
            "username": "student1",
            "password": "1234",
        }

        self.student2_data = {
            "username": "student2",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False,
        }

        self.student2_login_data = {
            "username": "student2",
            "password": "1234",
        }

        self.facilitator_data = {
            "username": "facilitator",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True,
        }

        self.facilitator_login_data = {
            "username": "facilitator",
            "password": "1234",
        }

        self.instructor1_data = {
            "username": "instructor",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True,
        }

        self.instructor1_login_data = {
            "username": "instructor",
            "password": "1234",
        }

        self.activity_data_1 = {"title": "activity1", "points": 10}
        self.activity_data_2 = {"title": "activity2", "points": 10}
        self.activity_data_3 = {"title": "activity3", "points": 10}
        self.submission_data_1 = {"grade": 10, "repo": "http://gitlab.com/submission1"}
        self.submission_data_2 = {"grade": 10, "repo": "http://gitlab.com/submission2"}
        self.submission_data_3 = {"grade": 10, "repo": "http://gitlab.com/submission3"}

    def test_facilitator_or_instructor_can_create_an_activity(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação da activity 1 pelo instructor
        activity = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        )
        
        self.assertDictEqual(activity.json(), {"id": 1, "title": "activity1", "points": 10, "submissions": []})
        self.assertEqual(activity.status_code, 201)
        
        # Criação do facilitator
        self.client.post("/api/accounts/", self.facilitator_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Criação da activity 2 pelo facilitator
        activity = self.client.post(
            "/api/activities/", self.activity_data_2, format="json"
        )
        
        self.assertDictEqual(activity.json(), {"id": 2, "title": "activity2", "points": 10, "submissions": []})
        self.assertEqual(activity.status_code, 201)
    
    def test_students_cannot_create_activities(self):
        # Criação do student
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Autenticação do student
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação da activity 1 pelo student
        activity = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        )
        
        self.assertEqual(activity.status_code, 403)
    
    def test_if_it_is_not_possible_to_create_activities_with_the_same_title(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação da activity 1 pelo instructor
        activity1 = self.client.post(
            "/api/activities/", {"title": "activity1", "points": 10}, format="json"
        )
        
        self.assertDictEqual(activity1.json(), {"id": 1, "title": "activity1", "points": 10, "submissions": []})
        self.assertEqual(activity1.status_code, 201)
        
        # Criação da mesma activity 1 pelo instructor, porém com points diferentes (ambas devem ter o mesmo id)
        activity2 = self.client.post(
            "/api/activities/", {"title": "activity1", "points": 8}, format="json"
        )
        
        self.assertDictEqual(activity2.json(), {"id": 1, "title": "activity1", "points": 8, "submissions": []})
        self.assertEqual(activity1.status_code, 201)        
    
    def test_facilitator_or_instructor_can_list_activities(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação da activity 1 pelo instructor
        activity1 = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        )
        
        # Listando as atividades
        activities = self.client.get("/api/activities/", format='json')
        
        self.assertEqual(activities.status_code, 200)
        self.assertListEqual(activities.json(), [{"id": 1, "title": "activity1", "points": 10, "submissions": []}])
        
        # Criação do facilitator
        self.client.post("/api/accounts/", self.facilitator_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação da activity 2 pelo facilitator
        activity2 = self.client.post(
            "/api/activities/", self.activity_data_2, format="json"
        )
        
        # Listando as duas atividades, nesse caso deve retornar uma lista com as duas atividades
        activities = self.client.get("/api/activities/", format='json')
        
        self.assertEqual(activities.status_code, 200)
        self.assertListEqual(activities.json(), [{"id": 1, "title": "activity1", "points": 10, "submissions": []},
                                                 {"id": 2, "title": "activity2", "points": 10, "submissions": []}])
        
    def test_student_cannot_list_activities(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação da activity 1 pelo instructor
        activity1 = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        )
        
        # Criação do student
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Autenticação do student
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Tentando listar as atividades, porém não é possível
        activities = self.client.get("/api/activities/", format='json')
        
        self.assertEqual(activities.status_code, 403)
    
    def test_student_can_submit_an_activity(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação da activity 1 pelo instructor
        activity = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        )        
        
        # Criação do student
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Autenticação do student
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Estudante faz uma submissão de uma atividade com o campo grade
        submission = self.client.post("/api/activities/1/submissions/", self.submission_data_1, format="json")
        
        self.assertEqual(submission.status_code, 201)
        self.assertDictEqual(submission.json(), {"id": 1, "grade": None, "repo": "http://gitlab.com/submission1", "user_id": 2, "activity_id": 1})
        
        # Estudante faz uma nova submissão de uma atividade sem o campo grade
        submission = self.client.post("/api/activities/1/submissions/", {"repo": "http://gitlab.com/submission1"}, format="json")
        
        self.assertEqual(submission.status_code, 201)
        self.assertDictEqual(submission.json(), {"id": 2, "grade": None, "repo": "http://gitlab.com/submission1", "user_id": 2, "activity_id": 1})
        
        # Estudante faz uma submissão da primeira atividade novamente, com os mesmos dados
        # (deve ser possível e será gerado uma nova atividade com outro id)
        submission = self.client.post("/api/activities/1/submissions/", self.submission_data_1, format="json")
        
        self.assertEqual(submission.status_code, 201)
        self.assertDictEqual(submission.json(), {"id": 3, "grade": None, "repo": "http://gitlab.com/submission1", "user_id": 2, "activity_id": 1})
        
    def test_facilitator_or_instructor_cannot_submity_an_activity(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação da activity 1 pelo instructor
        activity = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        )
        
        # Tentativa de submissão pelo instrutor
        submission = self.client.post("/api/activities/1/submissions/", {"repo": "http://gitlab.com/submission1"}, format="json")
        self.assertEqual(submission.status_code, 403)
        
         # Criação do facilitator
        self.client.post("/api/accounts/", self.facilitator_data, format="json")

        # Autenticação do facilitator
        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Tentativa de submissão pelo facilitator
        submission = self.client.post("/api/activities/1/submissions/", {"repo": "http://gitlab.com/submission1"}, format="json")
        self.assertEqual(submission.status_code, 403)
    
    def test_facilitator_or_instructor_can_edit_a_submission_grade(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação da activity 1 pelo instructor
        activity = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        )        
        
        # Criação do student
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Autenticação do student
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Estudante faz uma submissão de atividade com o campo grade
        submission1 = self.client.post("/api/activities/1/submissions/", self.submission_data_1, format="json")
        
        # Autenticação do instructor novamente
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Instrutor edita a nota de uma atividade
        grading_submission = self.client.put("/api/submissions/1/", {"grade": 7}, format="json")
        
        self.assertEqual(grading_submission.status_code, 200)
        self.assertDictEqual(grading_submission.json(), {"id": 1, "grade": 7, "repo": "http://gitlab.com/submission1", "user_id": 2, "activity_id": 1})
        
        # Instrutor edita a nota de uma atividade
        grading_submission = self.client.put("/api/submissions/1/", {"grade": 7}, format="json")
        
        self.assertEqual(grading_submission.status_code, 200)
        self.assertDictEqual(grading_submission.json(), {"id": 1, "grade": 7, "repo": "http://gitlab.com/submission1", "user_id": 2, "activity_id": 1})
        
        # Criação do facilitator
        self.client.post("/api/accounts/", self.facilitator_data, format="json")
        
        # Autenticação do facilitator
        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Facilitador edita a nota de uma atividade
        grading_submission = self.client.put("/api/submissions/1/", {"grade": 1}, format="json")
        
        self.assertEqual(grading_submission.status_code, 200)
        self.assertDictEqual(grading_submission.json(), {"id": 1, "grade": 1, "repo": "http://gitlab.com/submission1", "user_id": 2, "activity_id": 1})
    
    def test_student_cannot_edit_a_submission_grade(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação da activity 1 pelo instructor
        activity = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        )        
        
        # Criação do student
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Autenticação do student
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Estudante faz uma submissão de atividade com o campo grade
        submission1 = self.client.post("/api/activities/1/submissions/", self.submission_data_1, format="json")
        
        # Estudente tenta editar a nota de uma atividade
        grading_submission = self.client.put("/api/submissions/1/", {"grade": 10}, format="json")
        
        self.assertEqual(grading_submission.status_code, 403)
    
    def test_student_can_view_only_your_submissions(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação de três atividades pelo instructor
        activity1 = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        )
        activity2 = self.client.post(
            "/api/activities/", self.activity_data_2, format="json"
        ) 
        activity3 = self.client.post(
            "/api/activities/", self.activity_data_3, format="json"
        )     
        
        # Criação do student 1
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Autenticação do student 1
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Student 1 faz submissões para duas atividades
        submission1 = self.client.post("/api/activities/1/submissions/", self.submission_data_1, format="json")
        submission2 = self.client.post("/api/activities/2/submissions/", self.submission_data_2, format="json")
        
        # Criação do student 2
        self.client.post("/api/accounts/", self.student2_data, format="json")
        
        # Autenticação do student 2
        token = self.client.post(
            "/api/login/", self.student2_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Student 2 faz submissões para três atividades
        submission1 = self.client.post("/api/activities/1/submissions/", self.submission_data_1, format="json")
        submission2 = self.client.post("/api/activities/2/submissions/", self.submission_data_2, format="json")
        submission3 = self.client.post("/api/activities/3/submissions/", self.submission_data_3, format="json")
        
        # Autenticação do student 1
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Student 1 consegue visualizar apenas as suas submissões (ou seja, 2)
        submissions = self.client.get("/api/submissions/", format="json")
        
        self.assertListEqual(submissions.json(), [{"id": 1, "grade": None, "repo": "http://gitlab.com/submission1", "user_id": 2, "activity_id": 1},
                                                  {"id": 2, "grade": None, "repo": "http://gitlab.com/submission2", "user_id": 2, "activity_id": 2}])
        self.assertEqual(submissions.status_code, 200)
        
        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
    def test_facilitator_or_instructor_can_view_all_submissions(self):
        # Criação do instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Criação de três atividades pelo instructor
        activity1 = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        )
        activity2 = self.client.post(
            "/api/activities/", self.activity_data_2, format="json"
        ) 
        activity3 = self.client.post(
            "/api/activities/", self.activity_data_3, format="json"
        )     
        
        # Criação do student 1
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # Autenticação do student 1
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Student 1 faz submissões para duas atividades
        submission1 = self.client.post("/api/activities/1/submissions/", self.submission_data_1, format="json")
        submission2 = self.client.post("/api/activities/2/submissions/", self.submission_data_2, format="json")
        
        # Criação do student 2
        self.client.post("/api/accounts/", self.student2_data, format="json")
        
        # Autenticação do student 2
        token = self.client.post(
            "/api/login/", self.student2_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        
        # Student 2 faz submissões para três atividades
        submission1 = self.client.post("/api/activities/1/submissions/", self.submission_data_1, format="json")
        submission2 = self.client.post("/api/activities/2/submissions/", self.submission_data_2, format="json")
        submission3 = self.client.post("/api/activities/3/submissions/", self.submission_data_3, format="json")
        
        # Autenticação do instructor
        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Instructor consegue ver todas as submissões
        submissions = self.client.get("/api/submissions/", format="json")
        self.assertListEqual(submissions.json(), [{"id": 1, "grade": None, "repo": "http://gitlab.com/submission1", "user_id": 2, "activity_id": 1},
                                                  {"id": 2, "grade": None, "repo": "http://gitlab.com/submission2", "user_id": 2, "activity_id": 2},
                                                  {"id": 3, "grade": None, "repo": "http://gitlab.com/submission1", "user_id": 3, "activity_id": 1},
                                                  {"id": 4, "grade": None, "repo": "http://gitlab.com/submission2", "user_id": 3, "activity_id": 2},
                                                  {"id": 5, "grade": None, "repo": "http://gitlab.com/submission3", "user_id": 3, "activity_id": 3}
                                                  ])
        self.assertEqual(submissions.status_code, 200)
        
        # Criação do facilitador
        self.client.post("/api/accounts/", self.facilitator_data, format="json")
        
        # Autenticação do facilitador
        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Facilitator consegue ver todas as submissões
        submissions = self.client.get("/api/submissions/", format="json")
        self.assertListEqual(submissions.json(), [{"id": 1, "grade": None, "repo": "http://gitlab.com/submission1", "user_id": 2, "activity_id": 1},
                                                  {"id": 2, "grade": None, "repo": "http://gitlab.com/submission2", "user_id": 2, "activity_id": 2},
                                                  {"id": 3, "grade": None, "repo": "http://gitlab.com/submission1", "user_id": 3, "activity_id": 1},
                                                  {"id": 4, "grade": None, "repo": "http://gitlab.com/submission2", "user_id": 3, "activity_id": 2},
                                                  {"id": 5, "grade": None, "repo": "http://gitlab.com/submission3", "user_id": 3, "activity_id": 3}
                                                  ])
        self.assertEqual(submissions.status_code, 200)
