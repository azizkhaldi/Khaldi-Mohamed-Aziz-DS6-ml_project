# Variables
PYTHON = python3
PIP = pip3
TRAIN_PATH = "/mnt/c/Users/azizk/Downloads/ML_Project_Files (1)11/archive (2)/churn-bigml-80.csv"  # Remplacez par votre chemin
TEST_PATH = "/mnt/c/Users/azizk/Downloads/ML_Project_Files (1)11/archive (2)/churn-bigml-20.csv"   # Remplacez par votre chemin

# Default target
all: install prepare train evaluate

# Install dependencies
install:
	$(PIP) install -r requirements.txt

# Prepare data
prepare:
	$(PYTHON) main.py --prepare --train_path $(TRAIN_PATH) --test_path $(TEST_PATH)

# Train model
train:
	$(PYTHON) main.py --train --train_path $(TRAIN_PATH) --test_path $(TEST_PATH)

# Evaluate model
evaluate:
	$(PYTHON) main.py --evaluate --train_path $(TRAIN_PATH) --test_path $(TEST_PATH)

# Code quality checks
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	black --check .

# Format code
format:
	black .

# Security check
security:
	bandit -r .

# Run all CI steps
ci: lint format security

# Clean up
clean:
	rm -rf _pycache_
	rm -f model.pkl
	rm -rf $(DEPLOY_DIR)

# Deploy the model
deploy: train evaluate
	mkdir -p $(DEPLOY_DIR)
	cp model.pkl $(DEPLOY_DIR)/
	cp -r src/ $(DEPLOY_DIR)/
	cp requirements.txt $(DEPLOY_DIR)/
	@echo "Déploiement terminé. Les fichiers sont dans $(DEPLOY_DIR)"

# Phony targets
.PHONY: all install prepare train evaluate lint format security ci clean
# Démarrer le serveur Jupyter Notebook
.PHONY: notebook
notebook:
	@echo "Démarrage de Jupyter Notebook..."
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		bash -c "source $(ENV_NAME)/bin/activate && jupyter notebook"; \
	else \
		jupyter notebook; \
	fi
# Run tests
test:
	pytest tests/
