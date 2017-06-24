import libperf as perf

perf.time_command("get outlet states", "pw get")
perf.time_command("set state of single outlet", "pw set 1 on")
