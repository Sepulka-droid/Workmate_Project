import pytest
import os
import sys
from src.main import *


# проверяем корректность на имеющихся корректных файлах
def test_generate_report():
    short_report = {'/api/orders/': {'DEBUG': 4, 'INFO': 7, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 0},
              '/api/users/': {'DEBUG': 1, 'INFO': 3, 'WARNING': 0, 'ERROR': 4, 'CRITICAL': 1},
              '/api/auth/login/': {'DEBUG': 4, 'INFO': 2, 'WARNING': 0, 'ERROR': 4, 'CRITICAL': 1},
              '/api/products/': {'DEBUG': 2, 'INFO': 1, 'WARNING': 1, 'ERROR': 2, 'CRITICAL': 0},
              '/api/payments/': {'DEBUG': 3, 'INFO': 0, 'WARNING': 1, 'ERROR': 2, 'CRITICAL': 2}}

    big_report = {'/api/orders/': {'DEBUG': 6191, 'INFO': 6200, 'WARNING': 1271, 'ERROR': 4955, 'CRITICAL': 1258},
                  '/api/users/': {'DEBUG': 6141, 'INFO': 6382, 'WARNING': 1267, 'ERROR': 5021, 'CRITICAL': 1285},
                  '/api/payments/': {'DEBUG': 6287, 'INFO': 6207, 'WARNING': 1228, 'ERROR': 5059, 'CRITICAL': 1279},
                  '/api/auth/login/': {'DEBUG': 6301, 'INFO': 6252, 'WARNING': 1218, 'ERROR': 5004, 'CRITICAL': 1328},
                  '/api/products/': {'DEBUG': 6149, 'INFO': 6214, 'WARNING': 1220, 'ERROR': 5063, 'CRITICAL': 1220}}


    assert generate_report(["./src/short_django_api.log"]) == short_report
    assert generate_report(["./src/big_django_api.log"]) == big_report


# проверка корректности добавления записи в словарь
def test_add_entry():
    test_dict = {}

    # добавление корректной записи
    add_entry(test_dict, '/api/users/', 'WARNING')
    assert test_dict['/api/users/']['WARNING'] == 1

    # добавление некорректной записи
    add_entry(test_dict, '/api/users/', 'UNKNOWN')
    assert 'UNKNOWN' not in test_dict['/api/users/']


# проверка качества записанного handlers
def test_print_report():
    short_report = {'/api/orders/': {'DEBUG': 4, 'INFO': 7, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 0},
              '/api/users/': {'DEBUG': 1, 'INFO': 3, 'WARNING': 0, 'ERROR': 4, 'CRITICAL': 1},
              '/api/auth/login/': {'DEBUG': 4, 'INFO': 2, 'WARNING': 0, 'ERROR': 4, 'CRITICAL': 1},
              '/api/products/': {'DEBUG': 2, 'INFO': 1, 'WARNING': 1, 'ERROR': 2, 'CRITICAL': 0},
              '/api/payments/': {'DEBUG': 3, 'INFO': 0, 'WARNING': 1, 'ERROR': 2, 'CRITICAL': 2}}

    # запись корректного словаря
    if os.path.isfile('test.txt'):
        os.remove('test.txt')
    print_report(short_report, file='test.txt')
    assert os.path.isfile('test.txt')

    # запись некорректного словаря
    if os.path.isfile('test.txt'):
        os.remove('test.txt')
    print_report({}, file='test.txt')
    assert not os.path.isfile('test.txt')


# проверка функции оценки отчёта
def test_is_correct():
    short_report = {'/api/orders/': {'DEBUG': 4, 'INFO': 7, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 0},
              '/api/users/': {'DEBUG': 1, 'INFO': 3, 'WARNING': 0, 'ERROR': 4, 'CRITICAL': 1},
              '/api/auth/login/': {'DEBUG': 4, 'INFO': 2, 'WARNING': 0, 'ERROR': 4, 'CRITICAL': 1},
              '/api/products/': {'DEBUG': 2, 'INFO': 1, 'WARNING': 1, 'ERROR': 2, 'CRITICAL': 0},
              '/api/payments/': {'DEBUG': 3, 'INFO': 0, 'WARNING': 1, 'ERROR': 2, 'CRITICAL': 2}}
    assert is_correct(short_report)

    # некорректные отчёты
    failed_report_1 = {'/api/orders/': {'DEBUG': 4, 'INFO': 7, 'WARNING': 2, 'ERROR': 3}}
    assert not is_correct(failed_report_1)

    failed_report_2 = {'/api/orders/': {'DEBUG': 4, 'INFO': 7, 'WARNING': 2,
                                        'ERROR': 3, 'CRITICAL': 0, 'UNKNOWN': 2}}
    assert not is_correct(failed_report_2)

    failed_report_3 = {'/api/orders/': {'DEBUG': 4, 'INFO': 'cat', 'WARNING': 2,
                                        'ERROR': 3, 'CRITICAL': 0}}
    assert not is_correct(failed_report_3)

    failed_report_4 = {123: {'DEBUG': 4, 'INFO': 7, 'WARNING': 2, 'ERROR': 3}}
    assert not is_correct(failed_report_3)


# проверка функции исправления имени файла
def test_correct_filename():
    assert correct_filename('cat.txt') == 'cat.txt'
    assert correct_filename('./cat.txt') == './cat.txt'
    assert correct_filename('cat?dog.txt') == 'cat_dog.txt'
    assert correct_filename('cat' * 200) == ('cat' * 200)[:255]