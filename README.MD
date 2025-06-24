# 🧪 Pollab — Backend

**About Pollab**

**Pollab** (short for Poll Laboratory) is a modern, open-source polling platform designed to 
simplify the way users gather opinions and make decisions. Built with a **Django REST API** 
and **PostgreSQL**, it can be consumed by a _frontend_ and _mobile_ solution. Pollab features:
- 🧠 A clean and responsive UI 
- ⚙️ Reactive Forms with validation
- 🕒 Real-time vote tracking and countdown timers
- 📢 Toast notifications for a smooth UX

Whether you're testing ideas, collecting feedback, or showcasing interactive demos — Pollab lets you create, vote, and visualize results in seconds.
> **Join. Experiment. Transform.**

[//]: # (## Interface)

[//]: # ()
[//]: # (<p align="center">)

[//]: # (  <img src="readme_assets/mobile_create.png" alt="Splashscreen" width="30%"/>)

[//]: # (  <img src="readme_assets/mobile_polllist.png" alt="Enquetes Abertas" width="30%"/>)

[//]: # (  <img src="readme_assets/mobile_polldetails.png" alt="Detalhe da Enquete" width="30%"/>)

[//]: # (</p>)

---

## ✨ Visão Geral

| Item              | Detalhe                                                                                 |
|-------------------|-----------------------------------------------------------------------------------------|
| **Stack**         | Python · Django · DRF · PostgreSQL                                                      |
| **Idenfiticação** | O usuário/participante é identificado por um `id_participante` na requisição de voto.   |
| **Objetivo**      | CRUD de enquetes, prevenção de voto duplicado e listagem de resultados.                 |
| **Documentação**  | Geração automática de documentação da API com `drf-spectacular` (Swagger/ReDoc).        |


---

## ⚙️ Setup

0. **Prerequisites**

Before getting started, make sure the following tools are installed on your system:

- [Python ≥ 3.9](https://www.python.org/downloads/) (added to `PATH`)
- [PostgreSQL](https://www.postgresql.org/download/) (default user: `postgres`, password: `postgres`)
- [Git](https://git-scm.com/)
- [PyCharm Community](https://www.jetbrains.com/pycharm/download)

1. **Clone the repository in PyCharm**
    - Open PyCharm
    - Go to `File > New > Project from Version Control`.
    - Use the repository URL: https://github.com/igormahall/pollab-backend.git
    - Choose a local folder and click **Clone**.

2. **Create the virtual environment**
    ```bash
    .venv\Scripts\activate       # Windows
    # source .venv/bin/activate  # macOS / Linux
    ```

3. **Install the dependencies**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Create the `.env` file**
    - Create a new file called .env in the project root with the following content:
    ```env
    DJANGO_SECRET_KEY=your-secret-key-here
    ```
    - To generate a secure secret key:
    ```bash
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

5. **Create the PostgreSQL database**
    ```bash
    psql -U postgres
    ```
    - When prompted, enter the password: `postgres`
    - Inside the PostgreSQL shell:
    ```sql
    CREATE DATABASE enquete;
    \q
    ```

6. **Run the migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```

7. **Create a superuser**
    ```bash
    python manage.py createsuperuser
    ```
    - Follow the prompts to define username, email, and password.


8. **Start the development server**
    ```bash
    python manage.py runserver
    ```
    - Access the admin panel at: **http://127.0.0.1:8000/**.
    - API interative documentation at: **/api/swagger/**.

### Important
- Never commit your real `.env` file to version control!
- Ensure `.env` is listed in `.gitignore`.

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
