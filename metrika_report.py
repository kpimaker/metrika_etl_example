# coding: utf-8

from metrika_lib import traffic_sources
from config import METRIKA_FILE, LOAD_DATE


def main():
    """Выгрузка отчета из Яндекс.Метрики. Подробности в readme.md"""
    with open('data/{}'.format(METRIKA_FILE), 'w') as f:
        for rec in traffic_sources(44147844, LOAD_DATE, LOAD_DATE):
            f.write('{},{},{}\n'.format(LOAD_DATE, rec[0], rec[1]))


if __name__ == '__main__':
    main()
