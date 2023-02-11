from subprocess import PIPE, run
from datetime import datetime

result = run(["ps", "-aux"], stderr=PIPE, stdout=PIPE)

processes = result.stdout.decode('utf-8').split('\n')[:-1]
proc_title = processes.pop(0).split()
res = []

for proc in processes:
    proc_items = proc.split()
    if len(proc_items) > 11:
        for i in range(11, len(proc_items)):
            proc_items[10] += ' ' + proc_items[i]
    res.append({proc_titles[i]: proc_items[i] for i in range(11)})

users = list(set(proc['USER'] for proc in res))

processes_count = len(processes)

users_process = {user: len([proc for proc in res if proc['USER'] == user]) for user in users}

all_mem = '{:.2f}'.format(sum([float(proc['%MEM']) for proc in res]))

all_cpu = '{:.2f}'.format(sum([float(proc['%CPU']) for proc in res]))

max_mem = [proc['COMMAND'] for proc in res if float(proc['%MEM']) == max([float(pr['%MEM']) for pr in res])][0][:20]

max_proc_time = [proc['COMMAND'] for proc in res if float(proc['%CPU']) == max([float(pr['%CPU']) for pr in res])][0][:20]

out_info = {'Пользователи системы': users,
            'Процессов запущено': processes_count,
            'Пользовательских процессов': users_process,
            'Всего памяти используется': all_mem,
            'Всего CPU используется': all_cpu,
            'Больше всего памяти использует': max_mem,
            'Больше всего CPU использует': max_proc_time}

for param, value in out_info.items():
    print(f'{param}: {value}')

# Сохраняем результаты в файл
now = datetime.now().strftime('%d-%m-%Y-%H:%M')
f = open(f'{now}-scan.txt', 'w')
for param, value in out_info.items():
    f.write(f'{param}: {value} \n')
f.close()
