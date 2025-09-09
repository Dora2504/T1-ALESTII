import matplotlib.pyplot as plt
import numpy as np

# Dados fornecidos
files = ['caso010.txt', 'caso020.txt', 'caso040.txt', 'caso060.txt', 'caso080.txt', 
         'caso100.txt', 'caso150.txt', 'caso200.txt', 'caso300.txt', 'caso400.txt', 'caso500.txt']
processors = [5, 6, 8, 9, 10, 12, 14, 16, 19, 22, 24]
tasks = [10, 20, 40, 60, 79, 100, 146, 198, 298, 392, 486]
min_time = [689, 1099, 1323, 2361, 2245, 2344, 2875, 3552, 4129, 4942, 5424]
max_time = [599, 999, 1155, 2294, 2197, 2293, 2826, 3529, 4091, 4996, 5433]
diff = [-90, -100, -168, -67, -48, -51, -49, -23, -38, 54, 9]

# Configuração do estilo
plt.style.use('default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Gráfico 1: Bar Chart MIN vs MAX por caso
x = np.arange(len(files))
width = 0.35

bars1 = ax1.bar(x - width/2, min_time, width, label='MIN Time', color='#1f77b4', alpha=0.8)
bars2 = ax1.bar(x + width/2, max_time, width, label='MAX Time', color='#ff7f0e', alpha=0.8)

ax1.set_xlabel('Casos')
ax1.set_ylabel('Tempo')
ax1.set_title('MIN vs MAX Time por Caso')
ax1.set_xticks(x)
ax1.set_xticklabels([f.split('.')[0] for f in files], rotation=45)
ax1.legend()

# Adicionar valores de diferença acima das barras
for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    height1 = bar1.get_height()
    height2 = bar2.get_height()
    diff_val = diff[i]
    color = 'red' if diff_val > 0 else 'green'
    ax1.text(bar2.get_x() + bar2.get_width()/2, max(height1, height2) + 50, 
             f'{diff_val}', ha='center', va='bottom', color=color, fontweight='bold')

# Gráfico 2: Line Chart Makespan vs Número de Tarefas
ax2.plot(tasks, min_time, 'o-', label='MIN Time', color='#1f77b4', linewidth=2, markersize=6)
ax2.plot(tasks, max_time, 's-', label='MAX Time', color='#ff7f0e', linewidth=2, markersize=6)

ax2.set_xlabel('Número de Tarefas')
ax2.set_ylabel('Makespan')
ax2.set_title('Makespan vs Número de Tarefas')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.7)

# Ajustar layout
plt.tight_layout()
plt.show()