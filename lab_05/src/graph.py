import matplotlib.pyplot as plt
import numpy as np

# данные извлекаются из файла
def get_measurements(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            # начало нового устройства/очереди
            if line.startswith("Устройство") or line.startswith("Очередь"):
                current_device = line
                data[current_device] = {}
            # сами строки с временами
            elif line.startswith("t"):
                parts = line.split(", ")
                for part in parts:
                    metric, value = part.split(" = ")
                    value = float(value.replace(" мс", "").strip())
                    data[current_device][metric] = value
    return data

# данные извлекаются из файла
data = get_measurements('measure.txt')

# распределяем времена для каждой метрики
metrics = ['tмин', 'tмакс', 'tсред', 'tмед']
device_names = list(data.keys())
metric_values = {metric: [] for metric in metrics}
for device in device_names:
    for metric in metrics:
        metric_values[metric].append(data[device].get(metric, 0))

# настройки и сохранение графика
x = np.arange(len(device_names))
width = 0.2
fig, ax = plt.subplots(figsize=(10, 6))
bars = []
for i, metric in enumerate(metrics):
    bars.append(ax.bar(x + i * width, metric_values[metric], width, label=metric))
ax.set_xlabel('Устройства/Очереди')
ax.set_ylabel('Время (мс)')
ax.set_title('Измерения времени для устройств и очередей')
ax.set_xticks(x + width * (len(metrics) - 1) / 2)
ax.set_xticklabels(device_names, rotation=45)
ax.legend()
plt.tight_layout()
plt.savefig('measure.png')