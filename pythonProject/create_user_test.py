import sender_stand_request
import data
from data import user_body
from sender_stand_request import response


def get_user_doby(first_mane):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_mane
    return current_body


def positive_assert(first_name, get_user_body=None):
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(first_name)
    # El resultado de la solicitud para crear un/a nuevo/a usuario/a se guarda en la variable user_response
    user_response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    # Comprueba que el campo authToken está en la respuesta y contiene un valor
    assert user_response.json()["authToken"] != ""

    # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"
    users_table_response = sender_stand_request.get_users_table()

    # String que debe estar en el cuerpo de respuesta
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1


# Función de prueba negativa para los casos en los que la solicitud devuelve un error relacionado con caracteres
def negative_assert_symbol(first_name):
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(first_name)

    # El resultado se guarda en la variable response
    response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 400
    assert response.status_code == 400

    # Comprueba que el atributo code en el cuerpo de respuesta es 400
    assert response.json()["code"] == 400
    # Comprueba el atributo message en el cuerpo de respuesta
    assert response.json()["message"] == "El nombre que ingresaste es incorrecto. " \
                                         "Los nombres solo pueden contener caracteres latinos,  "\
                                         "los nombres deben tener al menos 2 caracteres y no más de 15 caracteres"


# Función de prueba negativa cuando el error es "No se enviaron todos los parámetros requeridos"
def negative_assert_no_firstname(user_body):
    # El resultado se guarda en la variable response
    response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 400
    assert response.status_code == 400

    # Comprueba que el atributo code en el cuerpo de respuesta es 400
    assert response.json()["code"] == 400
    # Comprueba el atributo message en el cuerpo de respuesta
    assert response.json()["message"] == "No se enviaron todos los parámetros requeridos"


# Prueba 1. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    # La versión actualizada del cuerpo de solicitud que contiene el nombre "Aa" se guarda en la variable "user_body"
    user_body = get_user_body("Aa")
    # El resultado de la solicitud relevante se guarda en la variable "user_response"
    user_response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    # Comprueba que el campo authToken está en la respuesta y contiene un valor
    assert user_response.json()["authToken"] != ""

    # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"
    users_table_response = sender_stand_request.get_users_table()
    # El string que debe estar en el cuerpo de la respuesta para recibir datos de la tabla "users" se ve así
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1


def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")


def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

def  negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 40
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se enviaron todos los parámetros requeridos"


# La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    # De lo contrario, se podrían perder los datos del diccionario de origen
    user_body = data.user_body.copy()
    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)


# El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body("")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400






















