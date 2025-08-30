
# Instalação e execução

1. **Crie e ative um ambiente virtual Python:**
	```bash
	python3 -m venv venv
	source venv/bin/activate
	```
2. **Instale as dependências:**
	```bash
	pip install -r requirements.txt
	```

3. **Abra dois terminais:**
	- **Terminal 1:** Para rodar o MongoDB
	  ```bash
	  mongod --dbpath ~/data/db
	  ```
	  (Crie a pasta com `mkdir -p ~/data/db` se necessário)
	- **Terminal 2:** Para rodar a API FastAPI
	  ```bash
	  TESTING=False uvicorn main:app --reload
	  ```

Assim, a API funcionará perfeitamente, pois o banco de dados e a aplicação estarão rodando simultaneamente.

# Para desenvolvimento com MongoDB real, use:
TESTING=False uvicorn main:app --reload