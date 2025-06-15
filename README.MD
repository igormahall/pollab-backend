# 📊 API Django — Sistema de Enquetes

Backend **RESTful** para gerenciar enquetes de múltipla escolha.  
Construído com **Django 5** + **Django REST Framework** e banco **PostgreSQL** 
e e oferece uma documentação interativa via Swagger.

---

## ✨ Visão Geral

| Item              | Detalhe                                                                                 |
|-------------------|-----------------------------------------------------------------------------------------|
| **Stack**         | Python · Django · DRF · PostgreSQL                                                      |
| **Idenfiticação** | O usuário/participante é identificado por um `id_participante` na requisição de voto.   |
| **Objetivo**      | CRUD de enquetes, prevenção de voto duplicado e listagem de resultados.                 |
| **Documentação**  | Geração automática de documentação da API com `drf-spectacular` (Swagger/ReDoc).        |


---

## ⚙️ Configuração Rápida (Dev)

```bash
# 1. Clone o repositório e entre na pasta
git clone https://github.com/<seu-usuario>/enquete-api.git
cd enquete-api

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # macOS / Linux

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
# Copie o arquivo de exemplo. No Windows, use 'copy' em vez de 'cp'.
cp .env.example .env

# AGORA, ABRA O ARQUIVO '.env' E EDITE-O com sua SECRET_KEY e a URL do seu banco de dados.
# Um comando para gerar uma nova SECRET_KEY está comentado dentro do arquivo .env.example.

# 5. Execute as migrações e crie um superusuário
python manage.py migrate
python manage.py createsuperuser

# 6. Execute o servidor de desenvolvimento
python manage.py runserver
```

A API sobe em **http://127.0.0.1:8000/**.

A documentação interativa da API estará em **/api/swagger/**.

---

## 🗄️ Modelo de Dados

A lógica do sistema é sustentada por três modelos principais.

### 1. Enquete

| Campo          | Tipo                | Descrição                                                   |
|----------------|---------------------|-------------------------------------------------------------|
| `id`           | `BigAutoField` (PK) | Identificador único                                         |
| `titulo`       | `CharField`         | Pergunta exibida ao usuário                                 |
| `data_criacao` | `DateTimeField`     | Timestamp de criação                                        |
| `status`       | `CharField`         | Estado atual (`Aberta` ou `Fechada`), selecionável no Admin |


---

### 2. Opcao

| Campo         | Tipo                            | Descrição                      |
|---------------|---------------------------------|--------------------------------|
| `id`          | `BigAutoField` (PK)             | Identificador único            |
| `enquete`     | `ForeignKey('Enquete')`         | Enquete associada              |
| `texto_opcao` | `CharField`                     | Texto exibido no botão de voto |
| `votos`       | `IntegerField`                  | Contador de votos              |

---

### 3. Voto

| Campo             | Tipo                    | Descrição                           |
|-------------------|-------------------------|-------------------------------------|
| `id`              | `BigAutoField` (PK)     | Identificador                       |
| `id_participante` | `CharField`             | Identificador único do participante |
| `enquete`         | `ForeignKey('Enquete')` | Enquete votada                      |
| `opcao_escolhida` | `ForeignKey('Opcao')`   | Opção votada                        |
| `data_voto`       | `DateTimeField`         | Timestamp do voto                   |

**Restrição de unicidade**

```python
class Meta:
    unique_together = ("enquete", "id_participante")
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

| Verbo + Rota                     | Ação     | Descrição                                                          |
|----------------------------------|----------|--------------------------------------------------------------------|
| `GET /api/enquetes/`             | Listar   | Retorna *todas* as enquetes, abertas e fechadas.                   |
| `GET /api/enquetes/{id}/`        | Detalhar | Retorna os dados de uma enquete específica, incluindo suas opções. |
| `POST /api/enquetes/`            | Criar    | Cria uma nova enquete e suas opções aninhadas.                     |
| `POST /api/enquetes/{id}/votar/` | Votar    | Registra um voto para um participante em uma opção específica.     |

> Todas as respostas seguem o padrão `application/json` com camelCase no payload.

Exemplo — **POST /api/enquetes/1/votar/**
```json
{
  "id_opcao": 2,
  "id_participante": "carlinhos_teste_123"
}
```

Possíveis respostas:

| Código              | Significado                               |
|---------------------|-------------------------------------------|
| **200** OK          | Voto computado com sucesso.               |
| **400** Bad Request | A opção enviada não pertence à enquete.   |
| **409** Conflict    | Este participante já votou nesta enquete. |

---

## 🚀 Deploy

O projeto está configurado para deploy em plataformas modernas como Render ou Heroku. 
As configurações de produção (como `DEBUG`, `ALLOWED_HOSTS` e `DATABASE_URL`) são lidas
a partir de variáveis de ambiente para garantir a segurança.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Se você quiser sugerir melhorias, relatar bugs ou propor 
novas funcionalidades, sinta-se à vontade para abrir uma issue ou pull request.

---

## 📜 Licença

Distribuído sob a licença **MIT**.
