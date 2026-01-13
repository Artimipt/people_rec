#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = test_task
PYTHON_VERSION = 3.9
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements:
	uv pip install -r requirements.txt
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format
	
	
# Download video data
.PHONY: download-video
download-video:
	mkdir -p data/raw
	wget --header 'Host: cloclo58.datacloudmail.ru' --user-agent 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0' --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' --header 'Accept-Language: en-US,en;q=0.5' --referer 'https://cloud.mail.ru/' --header 'Upgrade-Insecure-Requests: 1' --header 'Sec-Fetch-Dest: iframe' --header 'Sec-Fetch-Mode: navigate' --header 'Sec-Fetch-Site: cross-site' 'https://cloclo58.datacloudmail.ru/public/get/4HwgZAv1dgB7D3niA47UtPZ3Edh5c3YMzeicDz4EFb9cA8R1wnN5zWZpszjPLqHPPnkXCK3evVQycP8T5LdFwBUr67xbYd7EChB6NjsBCeiwfj8NYUGfdyJYc9fefHJ6ZBcTg3Q5JnJGDgniwhodypuReSPf4FYQEcNAqEuzvoj9FbkowgcQQ6ancsnFSSWabAD79rrkViRoyRArP1U91g9Z4AkUn393NdMvUwiK8NttuxJQJicJHGbdy2Ci8ZmveRqxnVaJCMRUqe2akUYFH9ZtuLPrwoivR5hoFKPLMPrC3JnYhLJxqgYPjwtNqe9RqTojaUTQmqFovNLbz86zZd8DsHRYhJdNQvWhsG8sNZAwUDd3m5gk1r22DKdpnbELi3u1getk2mE7Ry7bsz/no/crowd.mp4' --output-document 'data/crowd.mp4'



## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"
	



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
