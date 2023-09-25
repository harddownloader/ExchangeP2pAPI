from datetime import datetime
from dateutil import parser


def main():
    date_str = '2023-05-22T12:30:01+03:00'
    date_format = '%Y-%m-%d %H:%M:%S'
    date_obj = parser.parse(date_str, ignoretz=True)
    date_format_str = date_obj.strftime(date_format)
    print('date_format_str type = ', type(date_format_str), '  value', date_format_str)


if __name__ == "__main__":
    main()
