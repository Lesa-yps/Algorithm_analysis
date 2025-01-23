uint64_t tsum = 0;
time_stat.tmin = UINT64_MAX;
time_stat.tmax = 0;
for (int i = 0; i < task_count; i++){
    uint64_t value = time_stat.arr[i];
    if (value < time_stat.tmin)
        time_stat.tmin = value;
    if (value > time_stat.tmax)
        time_stat.tmax = value;
    tsum += value;}
time_stat.tavg = tsum / task_count;
qsort(time_stat.arr, task_count, sizeof(uint64_t), (int (*)(const void *, const void *))comparator);
if (task_count % 2 == 0)
    time_stat.tmed = (time_stat.arr[task_count / 2 - 1] + time_stat.arr[task_count / 2]) / 2;
else time_stat.tmed = time_stat.arr[task_count / 2];