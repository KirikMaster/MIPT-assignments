import psutil
print("CPU:", psutil.cpu_count())
print("RAM:", int(psutil.virtual_memory().total/1024), "kb")