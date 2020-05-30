# coding: utf-8

from metrika_lib import attendance, traffic_sources, content


def main():
    print(attendance(44147844, '2020-05-18', '2020-05-24'))
    print(traffic_sources(44147844, '2020-05-18', '2020-05-24'))


if __name__ == '__main__':
    main()
