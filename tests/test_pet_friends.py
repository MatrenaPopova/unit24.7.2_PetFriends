from api import PetFriends
from settings import valid_email, valid_password, incorrect_email, incorrect_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что можем авторизоваться с кореектными данными электронной почты и пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что можем получить информацию обо всех питомцах, используя корректные данные для авторизации"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Шкипотося', animal_type='кот', age='13', pet_photo='images/donut.jpeg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мурзяшка", "кот", "12", "images/donut.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Пончик', animal_type='Котзилла', age=12):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


# Test-1
def test_create_new_pet_without_photo(name='Пышканчик', animal_type='кот', age='7'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


# Test-2
def test_add_photo_of_pet(pet_photo='images/donut.jpeg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception('Список питомцев пуст')


# Test-3
def test_get_api_key_for_incorrect_user(email=incorrect_email, password=incorrect_password):
    """Проверяем, что не можем авторизоваться с некорректными данными электронной почты и пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


# Test-4
def test_get_api_key_for_without_correct_user(email=valid_email, password=incorrect_password):
    """Проверяем, что не можем авторизоваться с некорректными данными пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


# Test-5
def test_add_new_pet_with_negative_age(name= 'Мурзяшка', animal_type= 'единорог', age= '-100', pet_photo= 'images/murzik.jpeg'):
    """Проверяем, что нельзя регистрировать питомца с отрицательным возрастом"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert result['name'] == name
    # Баг-1: приходит статус код 200, что означает, что на сайт можно добавлять животных с отрицательным возрастом.


# Test-6
def test_create_new_pet_without_photo_and_name(name=None, animal_type='Муравей', age='7'):
    """Проверяем, что невозможно добавить питомца без имени, ожидаем статус код 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400


# Test-7
def test_create_new_pet_without_photo_and_animal_type(name='George', animal_type=None, age='7'):
    """Проверяем, что невозможно добавить питомца без имени, ожидаем статус код 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400


# Test-8
def test_add_new_pet_with_nonexistent_animal_type(
        name='McDonald',
        animal_type='burger',
        age='13',
        pet_photo='images/burger.jpeg'):
    """Проверяем, возможность добавления питомца несуществующего типа"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200


# Test-9
def test_create_new_pet_without_age(name='George', animal_type='snake', age=None):
    """Проверяем, что невозможно добавить питомца без имени, ожидаем статус код 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400


#Test-10
def test_create_new_pet_with_age_seven(name='George', animal_type='kitty', age='seven'):
    """Проверяем, что невозможно добавить питомца без имени, ожидаем статус код 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    # Баг-2 (можно ли считать это багом?)
    # на самом сайте невозможно добавить питомца с прописным возрастом, но тут этот тест проходит
    # и тест добавляет питомца с возрастом "seven", кажется ошибка в самом API