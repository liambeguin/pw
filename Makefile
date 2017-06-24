all:
	@echo noop

install:
	@echo noop

perf:
	$(MAKE) -C perf/ all

.PHONY: perf install all
