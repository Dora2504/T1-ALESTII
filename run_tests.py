#!/usr/bin/env python3


import sys
import os
from scheduler import process_file, process_directory

def quick_test():

    input_text = """# Proc 5
pxwmp_185 -> uqy_85
pxwmp_185 -> qpl_279
olg_320 -> pxwmp_185
err_92 -> olg_320
gqh_91 -> miu_291
cotov_474 -> err_92
cotov_474 -> gqh_91
ahei_490 -> cotov_474
err_92 -> gtv_225"""

    from scheduler import TaskScheduler
    
    scheduler = TaskScheduler()
    scheduler.parse_input(input_text)
    
    print(f"Processadores: {scheduler.processors}")
    print(f"Tarefas: {len(scheduler.task_time)}")
    print(f"MIN: {scheduler.schedule('MIN')}")
    print(f"MAX: {scheduler.schedule('MAX')}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Processar arquivo específico
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            result = process_file(file_path)
            if result:
                print(f"Arquivo: {result['file']}")
                print(f"Processadores: {result['processors']}")
                print(f"Tarefas: {result['tasks']}")
                print(f"MIN: {result['min_time']}")
                print(f"MAX: {result['max_time']}")
        else:
            print(f"Arquivo não encontrado: {file_path}")
    else:
        # Teste rápido
        quick_test()