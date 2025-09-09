import os
import heapq
from collections import defaultdict, deque
import time

class TaskScheduler:
    def __init__(self):
        self.processors = 0
        self.task_time = {}
        self.children = defaultdict(list)
        self.parent_count = defaultdict(int)
    
    def parse_input(self, input_text):
        """Parseia o texto de entrada"""
        lines = input_text.strip().split('\n')
        
        # Primeira linha: número de processadores
        if lines and lines[0].startswith('# Proc'):
            self.processors = int(lines[0].split()[2])
            lines = lines[1:]
        
        # Limpar estruturas
        self.task_time = {}
        self.children = defaultdict(list)
        self.parent_count = defaultdict(int)
        
        # Processar dependências
        for line in lines:
            line = line.strip()
            if not line or '->' not in line:
                continue
            
            parent, child = map(str.strip, line.split('->'))
            
            # Extrair tempos das tarefas
            for task in [parent, child]:
                if '_' in task and task not in self.task_time:
                    try:
                        _, time_str = task.rsplit('_', 1)
                        self.task_time[task] = int(time_str)
                    except ValueError:
                        self.task_time[task] = 0
            
            # Registrar dependências
            self.children[parent].append(child)
            self.parent_count[child] += 1
        
        # Garantir que todas as tarefas têm tempo definido
        all_tasks = set(self.task_time.keys())
        all_tasks.update(self.children.keys())
        all_tasks.update(self.parent_count.keys())
        
        for task in all_tasks:
            if task not in self.task_time:
                self.task_time[task] = 0
    
    def schedule(self, policy):
        """Executa o escalonamento com a política especificada"""
        if self.processors == 0 or not self.task_time:
            return 0
        
        # Cópia das dependências para não modificar o original
        parent_count = self.parent_count.copy()
        
        # Tarefas disponíveis para execução (sem dependências)
        available = deque()
        for task in self.task_time:
            if parent_count.get(task, 0) == 0:
                available.append(task)
        
        # Processadores: tempo atual de cada um
        processors = [0] * self.processors
        completion_times = {}
        
        # Filas de prioridade baseadas na política
        if policy == "MIN":
            task_heap = []
            push_func = lambda h, t: heapq.heappush(h, (self.task_time[t], t))
            pop_func = heapq.heappop
        else:  # MAX
            task_heap = []
            push_func = lambda h, t: heapq.heappush(h, (-self.task_time[t], t))
            pop_func = lambda h: heapq.heappop(h)
        
        while available or task_heap:
            # Adicionar tarefas disponíveis à fila de prioridade
            while available:
                task = available.popleft()
                push_func(task_heap, task)
            
            if not task_heap:
                break
            
            # Encontrar o próximo processador livre
            current_time = min(processors)
            
            # Alocar tarefas para processadores livres
            for i in range(self.processors):
                if processors[i] <= current_time and task_heap:
                    if policy == "MIN":
                        task_time, task = pop_func(task_heap)
                    else:  # MAX
                        neg_time, task = pop_func(task_heap)
                        task_time = -neg_time
                    
                    # Calcular tempo de término
                    end_time = current_time + task_time
                    completion_times[task] = end_time
                    processors[i] = end_time
                    
                    # Liberar tarefas dependentes
                    for child in self.children.get(task, []):
                        parent_count[child] -= 1
                        if parent_count[child] == 0:
                            available.append(child)
        
        return max(completion_times.values()) if completion_times else 0

def process_file(input_path, output_path=None):
    """Processa um arquivo de teste e retorna os resultados"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        scheduler = TaskScheduler()
        scheduler.parse_input(content)
        
        min_time = scheduler.schedule("MIN")
        max_time = scheduler.schedule("MAX")
        
        result = {
            'file': os.path.basename(input_path),
            'processors': scheduler.processors,
            'tasks': len(scheduler.task_time),
            'min_time': min_time,
            'max_time': max_time
        }
        
        if output_path:
            with open(output_path, 'a', encoding='utf-8') as f:
                f.write(f"Arquivo: {result['file']}\n")
                f.write(f"Processadores: {result['processors']}\n")
                f.write(f"Tarefas: {result['tasks']}\n")
                f.write(f"Tempo MIN: {result['min_time']}\n")
                f.write(f"Tempo MAX: {result['max_time']}\n")
                f.write("-" * 40 + "\n")
        
        return result
        
    except Exception as e:
        print(f"Erro ao processar {input_path}: {e}")
        return None

def process_directory(test_cases_dir, results_dir):
    """Processa todos os arquivos em um diretório"""
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    output_file = os.path.join(results_dir, "resultados.txt")
    
    # Limpar arquivo de resultados
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("RESULTADOS DOS TESTES\n")
        f.write("=" * 40 + "\n\n")
    
    results = []
    total_start = time.time()
    
    # Processar todos os arquivos .txt no diretório de testes
    for filename in os.listdir(test_cases_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(test_cases_dir, filename)
            print(f"Processando: {filename}")
            
            start_time = time.time()
            result = process_file(file_path, output_file)
            end_time = time.time()
            
            if result:
                result['processing_time'] = end_time - start_time
                results.append(result)
                print(f"  ✓ MIN: {result['min_time']}, MAX: {result['max_time']}")
    
    total_end = time.time()
    
    # Gerar relatório final
    generate_summary(results, output_file, total_end - total_start)
    
    return results

def generate_summary(results, output_path, total_time):
    """Gera um resumo dos resultados"""
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write("\n" + "=" * 40 + "\n")
        f.write("RESUMO FINAL\n")
        f.write("=" * 40 + "\n\n")
        
        f.write(f"Total de casos testados: {len(results)}\n")
        f.write(f"Tempo total de processamento: {total_time:.3f} segundos\n\n")
        
        f.write("Detalhes por caso:\n")
        for result in results:
            f.write(f"{result['file']}: ")
            f.write(f"P={result['processors']}, ")
            f.write(f"T={result['tasks']}, ")
            f.write(f"MIN={result['min_time']}, ")
            f.write(f"MAX={result['max_time']}, ")
            f.write(f"Tempo={result['processing_time']:.3f}s\n")

def main():
    """Função principal"""
    # Configurar paths
    test_cases_dir = "test_cases"
    results_dir = "results"
    
    print("Iniciando processamento dos casos de teste...")
    print(f"Diretório de testes: {test_cases_dir}")
    print(f"Diretório de resultados: {results_dir}")
    print("-" * 50)
    
    # Processar todos os casos de teste
    results = process_directory(test_cases_dir, results_dir)
    
    print("\n" + "=" * 50)
    print("Processamento concluído!")
    print(f"Total de casos processados: {len(results)}")
    print(f"Resultados salvos em: {os.path.join(results_dir, 'resultados.txt')}")

if __name__ == "__main__":
    main()