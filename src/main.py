import sys
import os


# учёт корректной строки в словаре со статистикой
def add_entry(my_dict: dict, handler: str, level: str) -> None:
    if level not in "DEBUG INFO WARNING ERROR CRITICAL".split():
        return
    if handler not in my_dict:
        my_dict[handler] = {x: 0 for x in "DEBUG INFO WARNING ERROR CRITICAL".split()}
    my_dict[handler][level] += 1


def generate_report(files: [set, list]) -> dict:
    # в словарь собираем статистику по "ручкам"
    statistics = dict()

    files = [file for file in files if os.path.isfile(file)]
    for log_file in files:
        with open(log_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.split()
                # интересует только строки в формате [дата] [время] [уровень] [имя логгера] [сообщение]
                if len(line) > 0 and '-' in line[0]:
                    date, time, level, logger, *message = line
                    # интересуют только записи django.request
                    if 'django.request' in logger and len(message) >= 2 and len(level) > 2:
                        handler = message[1]
                        add_entry(statistics, handler, level[1:-1])
                    # print(level, logger, message)
    return statistics


# проверка корректности отчёта
def is_correct(report):
    check_1 = len(report.keys()) > 0
    check_2 = all(type(key) is str for key in report)
    check_3 = all(set(report[key].keys()) == set("DEBUG INFO WARNING ERROR CRITICAL".split()) for key in report)
    check_4 = all(all(type(value) is int for value in report[key].values()) for key in report)
    return check_1 and check_2 and check_3 and check_4


def print_report(report: dict, file=None) -> None:
    # если словарь некорректен, то ничего не делаем
    if not is_correct(report):
        return

    # если параметр file непуст, открываем запись в файл
    if file is not None:
        file = open(file, 'w')

    # считаем общую сумму по каждой колонке
    total = {entry: sum([report[key][entry] for key in report])
             for entry in "DEBUG INFO WARNING ERROR CRITICAL".split()}
    # подбираем хорошую ширину каждой колонки
    columns = {'HANDLER': max(len(x) for x in report.keys()) + 1}
    for entry in "DEBUG INFO WARNING ERROR CRITICAL".split():
        columns[entry] = max(len(entry), len(str(total[entry]))) + 1

    # шапка таблицы
    print(' '.join(key.ljust(value) for key, value in columns.items()),
          file=file)
    # таблица
    for key in sorted(report.keys()):
        value = report[key]
        print(key.ljust(columns['HANDLER']),
              *[str(y).ljust(columns[x]) for x, y in value.items()],
              file=file)
    # строка с суммой по каждому столбцу
    print(' ' * columns['HANDLER'],
          ' '.join([str(value).ljust(columns[key]) for key, value in total.items()]),
          file=file)

    if file is not None:
        file.close()


# изменяет некорректное имя файла на корректное
def correct_filename(filename: str)-> str:
    # Заменяем запрещённые символы на подчёркивания
    for x in '[<>:"|?*\x00-\x1f]':
        filename = filename.replace(x, '_')
    return filename[:255]  # Обрезаем до максимальной длины


# основная функция
def main() -> None:
    # обработка параметров
    handlers_file = None
    log_files = set()
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '--report' and i < len(sys.argv) - 1:
            handlers_file = correct_filename(sys.argv[i + 1])
        else:
            log_files.add(correct_filename(sys.argv[i]))
    log_files -= {handlers_file}
    # print(log_files)

    # Генерируем и выводим отчет
    report = generate_report(log_files)
    print_report(report, file=handlers_file)


if __name__ == "__main__":
    main()

