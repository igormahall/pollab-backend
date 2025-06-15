# 📊 API Django — Sistema de Enquetes

Backend **RESTful** para gerenciar enquetes de múltipla escolha.  
Construído com **Django 5** + **Django REST Framework** e banco **PostgreSQL**.

---

## ✨ Visão Geral

| Item | Detalhe |
|------|---------|
| **Stack** | Python 3.12 · Django 5 · DRF 3 · PostgreSQL |
| **Auth** | Token (DRF Simple JWT)¹ |
| **Objetivo** | CRUD completo de enquetes, prevenção de voto duplicado, auditoria de votos |
| **Deploy** | Docker Compose, Heroku / Render / Fly.io ou VPS |

> ¹ O exemplo padrão identifica o usuário por `id_participante`, mas a base está pronta para JWT ou qualquer outro esquema de autenticação.

---

## ⚙️ Configuração Rápida (Dev)

```bash
# 1. Clone o repositório e entre na pasta
git clone https://github.com/<seu-usuario>/enquete-api.git
cd enquete-api

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate       # Windows
#source .venv/bin/activate   # macOS / Linux

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
# Copie o arquivo de exemplo. No Windows, use 'copy' em vez de 'cp'.
cp .env.example .env

# AGORA, ABRA O ARQUIVO '.env' E EDITE-O com sua SECRET_KEY e a URL do seu banco de dados.
# Para gerar uma nova SECRET_KEY, você pode usar o comando que está comentado dentro do .env.example

# 5. Execute as migrações e crie um superusuário
python manage.py migrate
python manage.py createsuperuser

# 6. Execute o servidor de desenvolvimento
python manage.py runserver
```

A API sobe em **http://127.0.0.1:8000/**.

A documentação interativa da API estará em **/api/swagger/**.

---

## 🗄️ Modelo de Dados — Detalhado

A lógica do sistema é sustentada por três tabelas principais.  
Os modelos foram cuidadosamente normalizados para manter integridade, rastreabilidade e desempenho.

### 1. Enquete (`Poll`)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | `BigAutoField` (PK) | Identificador único |
| `titulo` | `CharField(max_length=120)` | Pergunta exibida ao usuário |
| `data_criacao` | `DateTimeField(auto_now_add=True)` | Timestamp de criação |
| `data_encerramento` | `DateTimeField(null=True, blank=True)` | Encerramento opcional |
| `status` | `CharField(choices=[('Aberta','Aberta'),('Fechada','Fechada')], default='Aberta')` | Estado atual |

**Métodos de domínio**

* `is_aberta()` → `bool` – retorna se a enquete ainda aceita votos  
* `total_votos` (property) → `int` – soma dos votos computados em todas as opções

---

### 2. Opção (`Choice`)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | `BigAutoField` (PK) | Identificador único |
| `enquete` | `ForeignKey('Poll', related_name='opcoes', on_delete=CASCADE)` | Enquete associada |
| `texto_opcao` | `CharField(max_length=100)` | Texto exibido no botão de voto |
| `votos` | `PositiveIntegerField(default=0)` | Contador denormalizado (cache) |

**Métodos auxiliares**

* `percentual` (property) – calcula **votos desta opção ÷ total da enquete × 100** com fallback 0 %

> O contador `votos` é atualizado via `F()` expressions para evitar condição de corrida e reduzir agregações caras em alta escala.

---

### 3. Voto (`Vote`)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | `BigAutoField` (PK) | Identificador |
| `id_participante` | `CharField(max_length=64)` | Identificador do usuário/visitante |
| `enquete` | `ForeignKey('Poll', on_delete=CASCADE)` | Enquete votada |
| `opcao_escolhida` | `ForeignKey('Choice', on_delete=CASCADE)` | Opção votada |
| `data_voto` | `DateTimeField(auto_now_add=True)` | Timestamp |

**Restrição de unicidade**

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=["enquete", "id_participante"],
            name="unique_vote_per_participant_per_poll",
        )
    ]
```
Garante **1 voto por participante** em cada enquete.

---

### 🔗 Relacionamentos & Fluxo

```
Poll 1 ──< Choice 1 ──< Vote
           ^                 |
           |-----------------|
```

1. **Uma** `Enquete` possui **várias** `Opções`.  
2. Ao votar, cria‑se um objeto `Voto` apontando para a opção escolhida.  
3. Caso a restrição de unicidade dispare, retorna 409 Conflict.  
4. Após salvar o voto, o campo `votos` da opção é incrementado de forma atômica.

---

## 🔌 Endpoints REST

| Verbo + Rota | Ação | Descrição |
|--------------|------|-----------|
| `GET /api/enquetes/` | Listar | Retorna apenas enquetes **Abertas** |
| `GET /api/enquetes/{id}/` | Detalhar | Inclui opções + contagem de votos |
| `POST /api/enquetes/` | Criar | Cria enquete com opções aninhadas |
| `POST /api/enquetes/{id}/votar/` | Votar | Registra voto único |

> Todas as respostas seguem o padrão `application/json` com camelCase no payload.

Exemplo — **POST /api/enquetes/4/votar/**
```json
{
  "id_opcao": 2,
  "id_participante": "9bbfae66-762c-4a90-9f4c-87db9e"
}
```

Possíveis respostas:

| Código | Significado |
|--------|-------------|
| **200** OK | Voto computado |
| **400** Bad Request | Opção não pertence à enquete |
| **409** Conflict | Participante já votou |

---

## 🚀 Deploy em Produção

```bash
docker compose up --build -d
```

* Container `web` (Django + Gunicorn)  
* Container `db` (PostgreSQL)  
* `collectstatic` executado automaticamente  

Edite variáveis no `.env` para **`DJANGO_SECRET_KEY`**, **`ALLOWED_HOSTS`** e **`DATABASE_URL`**.

---

## ✅ Testes

```bash
pytest -q
```
Cobertura mínima garantida **≥ 90 %**.

---

## 🤝 Contribuindo

1. **Fork** → **branch** (`git checkout -b feature/xyz`)  
2. `pre-commit run --all-files`  
3. Abra um **Pull Request** descrevendo a motivação e o escopo

---

## 📜 Licença

Distribuído sob a licença **MIT** — consulte `LICENSE` para detalhes.
