prefix = $(HOME)
bindir = $(prefix)/bin
# completiondir = /etc/bash_completion.d
completiondir = $(prefix)/.bash_completion.d

all: install

install:
	ln -sf $(PWD)/pw $(bindir)/
	mkdir -p $(completiondir)
	ln -sf $(PWD)/completion/pw.bash $(completiondir)/
	@echo "***"
	@echo "*** add the following line to your bashrc for autocompletion:"
	@echo "*** source $(completiondir)/pw.bash"
	@echo "***"

uninstall:
	unlink $(bindir)/pw
	unlink $(completiondir)/pw.bash
	rm --dir $(completiondir)

perf:
	$(MAKE) -C perf/ all

.PHONY: perf install all
