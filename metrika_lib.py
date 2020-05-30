# coding: utf-8

import requests

API_URL = 'https://api-metrika.yandex.ru/stat/v1/data'


def attendance(counter, start_date, end_date):
    """
    Возвращает отчет по посещаемости счетчика counter за период от start_date до end_date. Пример:
    print(attendance(44147844, '2020-05-18', '2020-05-24'))

    Результат
    [
        ['2020-05-20', 856.0], ['2020-05-21', 837.0], ['2020-05-18', 802.0], ['2020-05-19', 770.0],
        ['2020-05-22', 704.0], ['2020-05-23', 394.0], ['2020-05-24', 387.0]
    ]

    :param counter: int номер счетчика Яндекс.Метрики
    :param start_date: str начальная дата отчета (аналог параметра date1 в API Метрики)
    :param end_date: str начальная дата отчета (аналог параметра date2 в API Метрики)
    :return: list
    """
    return content(counter, start_date, end_date, 'ym:s:visits', 'ym:s:date')


def traffic_sources(counter, start_date, end_date):
    """
    Возвращает отчет по источникам трафика счетчика counter за период от start_date до end_date. Пример:
    print(traffic_sources(44147844, '2020-05-18', '2020-05-24'))

    Результат
    [
        ['Переходы по ссылкам на сайтах', 1994.0], ['Переходы из поисковых систем', 1629.0], ['Прямые заходы', 762.0],
        ['Переходы по рекламе', 254.0], ['Внутренние переходы', 69.0], ['Переходы из социальных сетей', 32.0]
    ]

    :param counter: int номер счетчика Яндекс.Метрики
    :param start_date: str начальная дата отчета (аналог параметра date1 в API Метрики)
    :param end_date: str начальная дата отчета (аналог параметра date2 в API Метрики)
    :return: list
    """
    return content(counter, start_date, end_date, 'ym:s:visits', 'ym:s:lastsignTrafficSource')


def content(counter, start_date, end_date, metrics, dimensions, limit=100, headers=''):
    """
    Возвращает содержимое многостраничного отчета.
    Документация https://yandex.ru/dev/metrika/doc/api2/api_v1/data-docpage/

    Пример:
    print(content(44147844, '2020-05-18', '2020-05-24', 'ym:s:visits', 'ym:s:date'))

    Результат
    [
        ['2020-05-20', 856.0], ['2020-05-21', 837.0], ['2020-05-18', 802.0], ['2020-05-19', 770.0],
        ['2020-05-22', 704.0], ['2020-05-23', 394.0], ['2020-05-24', 387.0]
    ]

    :param counter: int номер счетчика Яндекс.Метрики
    :param start_date: str начальная дата отчета (аналог параметра date1 в API Метрики)
    :param end_date: str начальная дата отчета (аналог параметра date2 в API Метрики)
    :param metrics: str строка с перечислением метрик отчета
    :param dimensions: str строка с перечислением измерений отчета
    :param limit: int число выгружаемых за 1 обращение строк
    :param headers: заголовок запроса к API (в демо-версии пустая строка, в реальном отчете словарь)
    :return: list
    """
    offset = 1
    report = []

    while True:
        print('Starting offset {}'.format(offset))
        params = make_request_params(counter, start_date, end_date, limit, offset, metrics, dimensions)

        data = request_report(params, headers)
        report += reformat_api_report(data)

        offset += limit
        if not data or len(data) < limit:
            break

    return report


def request_report(params, headers):
    """
    Возвращает ключ 'data' ответа API Яндекс.Метрики.

    :param params: словарь параметров запроса (результат функции make_request_params)
    :param headers: заголовок запроса к API (в демо-версии пустая строка, в реальном отчете словарь)
    :return: list
    """
    r = requests.get(API_URL, params=params, headers=headers)
    return r.json()['data']


def reformat_api_report(api_report):
    """
    Возвращает список столбцов отчета Яндекс.Метрики api_report в принятом формате.
    Пример формата можно посмотреть в примере функции content

    :param api_report: list
    :return: list
    """
    reformatted_report = []

    for line in api_report:
        dimensions = [x['name'] for x in line['dimensions']]
        reformatted_report.append(dimensions + line['metrics'])

    return reformatted_report


def make_request_params(counter, start_date, end_date, limit, offset, metrics, dimensions):
    """
    Формирует параметры запрос к API Яндекс.Метрики.

    :param counter: int номер счетчика Яндекс.Метрики
    :param start_date: str начальная дата отчета (аналог параметра date1 в API Метрики)
    :param end_date: str начальная дата отчета (аналог параметра date2 в API Метрики)
    :param limit: int число выгружаемых за 1 обращение строк
    :param offset: int индекс первой строки выборки, начиная с 1
    :param metrics: str строка с перечислением метрик отчета
    :param dimensions: str строка с перечислением измерений отчета
    :return: dict
    """
    return {
        'id': counter,
        'date1': start_date,
        'date2': end_date,
        'metrics': metrics,
        'dimensions': dimensions,
        'limit': limit,
        'offset': offset,
        'accuracy': 1,
    }
