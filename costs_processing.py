# coding: utf-8

from config import COSTS_FILE, COSTS_DB


def main():
    """Обработка данных из базы расходов. Подробности в readme.md"""
    with open('data/{}'.format(COSTS_FILE), 'w') as f2write:
        with open('data/{}'.format(COSTS_DB)) as f:
            for line in f:
                if line.strip().split(',')[1] == 'SUCCESS':
                    f2write.write(line)


if __name__ == '__main__':
    main()
