NAME=http1
VERSION=$(shell changelog release version)
BUILD_DIR=build

YELLOW=\033[93m
RED=\033[1m\033[91m
CLEAR=\033[0m

.PHONY: env test

help:
	@echo "$(YELLOW)clean$(CLEAR)    Clean generated files"
	@echo "$(YELLOW)env$(CLEAR)      Activate virtual env"
	@echo "$(YELLOW)check$(CLEAR)    Check Python code"
	@echo "$(YELLOW)test$(CLEAR)     Run unit tests"
	@echo "$(YELLOW)package$(CLEAR)  Build package"
	@echo "$(YELLOW)release$(CLEAR)  Release project"

clean:
	@echo "$(YELLOW)Cleaning generated files$(CLEAR)"
	rm -rf $(BUILD_DIR)
	rm $(NAME)/*.pyc

env:
	@echo "$(YELLOW)Activating virtual env$(CLEAR)"
	. env/bin/activate

check: env
	@echo "$(YELLOW)Checking Python code$(CLEAR)"
	pylint --rcfile=etc/pylint.cfg $(NAME)

test: check
	@echo "$(YELLOW)Running unit tests$(CLEAR)"
	python $(NAME)/test_$(NAME).py

package: test clean
	@echo "$(YELLOW)Building package$(CLEAR)"
	mkdir -p $(BUILD_DIR)
	cp etc/setup.py $(BUILD_DIR)/
	sed -i -e "s/VERSION/$(VERSION)/" $(BUILD_DIR)/setup.py
	cp -r LICENSE README.rst etc/MANIFEST.in $(NAME) $(BUILD_DIR)/
	cd $(BUILD_DIR) && python setup.py sdist -d .

release: package
	@echo "$(YELLOW)Releasing project$(CLEAR)"
	cd $(BUILD_DIR) && python setup.py sdist -d . register upload
	release

