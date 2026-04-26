.PHONY: install test test-fast streamlit clean help

help:
	@echo "Comandos disponibles:"
	@echo "  make install     Instala dependencias (pip)"
	@echo "  make test        Ejecuta todos los tests"
	@echo "  make test-fast   Tests rápidos (excluye simulaciones lentas)"
	@echo "  make streamlit   Lanza el visualizador interactivo"
	@echo "  make clean       Limpia __pycache__ y .pytest_cache"

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v --tb=short

test-fast:
	python -m pytest tests/ -v --tb=short -m "not slow"

streamlit:
	streamlit run visualizador/app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
