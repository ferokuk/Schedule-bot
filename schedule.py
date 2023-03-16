import pandas
from camelot import read_pdf


def check(val: str, col: int, table) -> int | None:
    """Search index if val in col of table
    :param val:  value to search
    :param col: index of column
    :param table: table to work with
    :return: int if found, else None
    """
    a = table.index[table[col].str.contains(val)]
    if a.empty:
        return None
    elif len(a) > 1:
        return a.tolist()
    else:
        return a.item()


def get_schedule(group_name: str) -> str:
    """
    Makes a string with schedule of group_name group
    :param group_name:
    :return: string with a schedule
    """
    url = "http://www.fa.ru/org/spo/kip/Documents/raspisanie/2022-2023/%D0%B0%D1%83%D0%B4%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B8.pdf"
    tables = read_pdf(url, pages='all')
    table: pandas.DataFrame = pandas.concat([pandas.DataFrame(t.df) for t in tables], ignore_index=True)
    res = []
    lesson_start = float('inf')
    # Parse PDF
    for row in range(1, 7):
        info = []
        j = check(group_name, row, table)
        if isinstance(j, list):
            lesson_start = min(lesson_start, row)
            for s in j:
                info.append(table[0][s])
                info.append(table[row][s+1])
                info.append(table[row][0])

        elif j is not None:
            lesson_start = min(lesson_start, row)
            info.append(table[0][j])
            info.append(table[row][j+1])
            info.append(table[row][0])
        if info:
            res.append(info)
    schedule = ""
    # Parse lessons
    for l in res:
        time = l[2].split()
        if len(l) > 3:
            schedule += f"{lesson_start}) {l[1]} {l[0].split()[0]}, {l[4]} {l[3].split()[0]} {time[2]}"
        else:
            if lesson_start == 6:
                schedule += f"{lesson_start}) {l[1]} {l[0].split()[0]} {time[-1]}"
            elif lesson_start == 3:
                schedule += f"{lesson_start}) {l[1]} {l[0].split()[0]} {time[2] if group_name[0] == '1' else time[-2]}"
            else:
                schedule += f"{lesson_start}) {l[1]} {l[0].split()[0]} {time[-1]}"
        schedule += '\n'
        lesson_start += 1

    return schedule if schedule else "Не удалось найти расписание :("


if __name__ == "__main__":
    print(get_schedule("3ПКС-420"))
