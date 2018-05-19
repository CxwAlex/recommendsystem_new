import re
from recommendsystem.ETL import ReadFile
from pandas import DataFrame

def SummaryLog(read_filepath):
    read_log = ReadFile(read_filepath)
    log = []
    for i in read_log:
        if not re.match('第', i):
            continue
        log.append(eval(i.split('：', 1)[1]))
    columns = ['recall','precision','coverage','popularity','novelty','diversity']
    index = range(len(log))
    summary = DataFrame(0.0, columns=columns, index=index)
    for i in index:
        for j in columns:
            summary[j][i] = log[i][j]
    result = {}
    for i in columns:
        if i == 'recall' or i == 'precision':
            result[i] = format(summary[i].mean(), '.2%')
        elif i == 'coverage' or i == 'popularity':
            result[i] = eval(format(summary[i].mean(), '.3'))
        else:
            result[i] = eval(format(summary[i].mean(), '.2'))

    return result




