# coding: utf-8

import pandas as pd
from config import METRIKA_FILE, COSTS_FILE


def main():
    """Объединение результатов Я.Метрики и расходов и подсчет столбца cost_per_visit. Подробности в readme.md"""
    metrika = pd.read_csv('data/{}'.format(METRIKA_FILE), names=['date', 'source', 'visits'])
    costs = pd.read_csv('data/{}'.format(COSTS_FILE), names=['date', 'status', 'source', 'costs'])

    joined = metrika.merge(costs, on=['date', 'source'])
    joined['cost_per_visit'] = joined['costs'] / joined['visits']

    joined.to_csv('data/{}'.format('joined.csv'), index=False)


if __name__ == '__main__':
    main()
