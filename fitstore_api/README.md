# FitStore API

Este projeto demonstra, na prática, como implementar TDD (Test Driven Development) em uma aplicação FastAPI com Pytest, utilizando MongoDB como banco de dados. Aqui você encontrará exemplos de testes unitários, testes de integração e boas práticas de documentação para APIs.

## Estrutura da pasta `fitstore_api`
- `main.py`: Arquivo principal da aplicação FastAPI.
- `models/`: Modelos de dados utilizados pela API.
- `schemas/`: Schemas Pydantic para validação e serialização.
- `routers/`: Rotas/endpoints da API.
- `database/`: Configuração de conexão com o MongoDB.
- `tests/`: Testes unitários e de integração com Pytest.
- Outros arquivos de configuração e documentação.

## Como executar a API

### 1. Crie e ative um ambiente virtual (recomendado)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instale as dependências
```bash
pip install -r fitstore_api/requirements.txt
```

### 3. Execute o MongoDB e a API em terminais separados

Para o funcionamento correto da API, é necessário abrir **dois terminais**:

- **Terminal 1:** Inicie o MongoDB localmente:
	```bash
	mongod --dbpath ~/data/db
	```
	(Se necessário, crie a pasta com `mkdir -p ~/data/db`)

- **Terminal 2:** Ative o ambiente virtual e execute a API:
	```bash
	source venv/bin/activate
	cd fitstore_api
	TESTING=False uvicorn main:app --reload
	```

Assim, o banco de dados e a aplicação FastAPI estarão rodando simultaneamente, garantindo o funcionamento perfeito da API.

A aplicação estará disponível em: http://127.0.0.1:8000

### 5. Acesse a documentação interativa
Abra no navegador:
```
http://127.0.0.1:8000/docs
```

## Como rodar os testes

Com o ambiente virtual ativado e as dependências instaladas, execute:
```bash
pytest
```

---

Para mais detalhes sobre endpoints, exemplos de uso e boas práticas, consulte os arquivos de código e a documentação gerada automaticamente pelo FastAPI.
