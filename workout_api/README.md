# Workout API - Competição de Crossfit

Este projeto é uma API assíncrona para gerenciamento de atletas em uma competição de crossfit, desenvolvida com FastAPI.

## Passo a passo para executar a API

### 1. Crie e ative um ambiente virtual (recomendado)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instale as dependências
```bash
pip install -r workout_api/requirements.txt
```

### 3. Execute a aplicação
```bash
cd workout_api
uvicorn main:app --reload
```

A aplicação estará disponível em: http://127.0.0.1:8000

### 4. Acesse a documentação interativa
Abra no navegador:
```
http://127.0.0.1:8000/docs
```
Você poderá testar todos os endpoints da API por essa interface.


## Funcionalidades avançadas

### Customização do response dos endpoints
O endpoint GET `/atletas` retorna uma lista de atletas com os seguintes campos customizados:
- `nome`: nome do atleta
- `centro_treinamento`: nome do centro de treinamento
- `categoria`: nome da categoria

Exemplo de resposta:
```json
[
	{
		"nome": "João Silva",
		"centro_treinamento": "CT Elite",
		"categoria": "RX"
	},
	...
]
```

### Tratamento de exceção de integridade (CPF duplicado)
Ao tentar cadastrar um atleta com um CPF já existente, a API retorna:
- Mensagem: `Já existe um atleta cadastrado com o cpf: <cpf>`
- Status code: `303 See Other`

Exemplo de resposta:
```json
{
	"detail": "Já existe um atleta cadastrado com o cpf: 12345678900"
}
```

### Paginação com fastapi-pagination
O endpoint `/atletas` suporta paginação usando os parâmetros `limit` e `offset`:
- `limit`: quantidade máxima de itens por página (padrão: 10)
- `offset`: número de itens a pular antes de começar a listar (padrão: 0)

Exemplo:
```
GET http://127.0.0.1:8000/atletas?limit=5&offset=10
```
Retorna 5 atletas a partir do 11º registro.

---

## Como fazer buscas (query parameters)

#### Buscar todos os atletas:
```
GET http://127.0.0.1:8000/atletas
```

#### Buscar atletas por nome:
```
GET http://127.0.0.1:8000/atletas?nome=Joao
```

#### Buscar atletas por CPF:
```
GET http://127.0.0.1:8000/atletas?cpf=12345678900
```

#### Buscar atletas por nome e CPF:
```
GET http://127.0.0.1:8000/atletas?nome=Joao&cpf=12345678900
```

Você pode fazer essas buscas diretamente no navegador, no Postman, via curl ou pela interface /docs do FastAPI.

---

Se tiver dúvidas ou problemas, consulte o arquivo `Como_executar.md` dentro da pasta workout_api ou peça ajuda!
