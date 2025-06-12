# 📊 API para Sistema de Enquetes

Um backend simples e robusto, construído com Django e Django REST Framework, para gerenciar enquetes de múltipla escolha.

Esta API permite listar enquetes ativas, visualizar suas opções e registrar votos de forma segura — prevenindo votos duplicados por participante.

## 🛠 Tecnologias Utilizadas

- Python
- Django
- Django REST Framework (DRF)
- PostgreSQL

## ⚙️ Configuração do Projeto

Para configurar e executar o projeto em um ambiente de desenvolvimento local, siga os passos abaixo:

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2️⃣ Criar e Ativar o Ambiente Virtual

É uma boa prática isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar no Windows
.venv\Scripts\activate

# Ativar no macOS/Linux
source .venv/bin/activate
```

### 3️⃣ Instalar as Dependências

Instale as dependências listadas em `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4️⃣ Aplicar as Migrações do Banco de Dados

Este comando cria as tabelas no banco de dados com base nos modelos definidos em `models.py`:

```bash
python manage.py migrate
```

### 5️⃣ Criar um Superusuário

Você precisará de um usuário administrador para acessar o painel administrativo do Django e cadastrar as primeiras enquetes e opções para teste.

```bash
python manage.py createsuperuser
```

Siga as instruções no terminal para definir nome, e-mail e senha.

---

## ▶️ Executando a Aplicação

Com o ambiente configurado, inicie o servidor de desenvolvimento do Django:

```bash
python manage.py runserver
```

A API estará disponível em: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


---


## 🗄️ Modelo de Dados

A API é sustentada por três modelos principais, que garantem a integridade e a lógica do sistema de enquetes.

### 📝 Enquete

Armazena as informações principais de cada enquete.

- `id`: Chave Primária (PK).
- `titulo`: Título da enquete (ex: `"Qual sua linguagem favorita?"`).
- `data_criacao`: Data e hora em que a enquete foi criada.
- `status`: Estado atual da enquete (`"Aberta"`, `"Fechada"`).

### 🗳️ Opcao

Representa as alternativas de resposta para uma enquete.

- `id`: Chave Primária (PK).
- `enquete`: Chave Estrangeira (FK) que conecta a opção à sua enquete mãe.
- `texto_opcao`: Texto da alternativa (ex: `"Python"`, `"JavaScript"`).
- `votos`: Contador numérico dos votos recebidos por esta opção.

### 🧾 Voto

Registra cada voto individual, funcionando como uma tabela de junção para controle e auditoria.

- `id`: Chave Primária (PK).
- `id_participante`: Identificador único do participante (ex: um ID de sessão do navegador).
- `enquete`: Chave Estrangeira (FK) para a enquete em que o voto foi registrado.
- `opcao_escolhida`: Chave Estrangeira (FK) para a opção que foi votada.
- `data_voto`: Data e hora em que o voto foi computado.

### 🔗 Relacionamentos

- **Um-para-Muitos:**  
  Uma enquete pode ter várias opções. Este relacionamento é definido pela chave estrangeira no modelo `Opcao`.

- **Controle de Voto Único:**  
  A combinação dos campos `enquete` e `id_participante` no modelo `Voto` é única.  
  Isso garante a regra de negócio de que um mesmo participante não pode votar mais de uma vez na mesma enquete.

---

## 📄 Contrato da API (Endpoints para o Frontend)

A seguir estão os endpoints que devem ser consumidos pela aplicação cliente (ex: Angular).

---

### 1️⃣ Listar Todas as Enquetes Ativas

- **Endpoint:** `GET /api/enquetes/`  
- **Descrição:** Retorna uma lista com todas as enquetes que estão com o status "Aberta".  
- **Resposta de Sucesso (200 OK):**

```json
[
    {
        "id": 1,
        "titulo": "Qual sua linguagem de programação favorita?",
        "data_criacao": "2025-06-12T03:04:47.641235Z",
        "status": "Aberta",
        "opcoes": [
            {"id": 1, "texto_opcao": "Python", "votos": 15},
            {"id": 2, "texto_opcao": "JavaScript", "votos": 22}
        ]
    }
]
```

---

### 2️⃣ Obter Detalhes de uma Enquete Específica

- **Endpoint:** `GET /api/enquetes/<id>/`  
- **Descrição:** Retorna os dados completos de uma única enquete, incluindo suas opções e a contagem de votos atual.  
- **Resposta de Sucesso (200 OK):**

```json
{
    "id": 1,
    "titulo": "Qual sua linguagem de programação favorita?",
    "data_criacao": "2025-06-12T03:04:47.641235Z",
    "status": "Aberta",
    "opcoes": [
        {"id": 1, "texto_opcao": "Python", "votos": 15},
        {"id": 2, "texto_opcao": "JavaScript", "votos": 22},
        {"id": 3, "texto_opcao": "Rust", "votos": 8}
    ]
}
```

---

### 3️⃣ Registrar um Voto em uma Enquete

- **Endpoint:** `POST /api/enquetes/<id>/votar/`  
- **Descrição:** Registra um voto para uma opção específica de uma enquete. A API previne que um mesmo `id_participante` vote mais de uma vez na mesma enquete.  

- **Corpo da Requisição (Payload):**

```json
{
    "id_opcao": 2,
    "id_participante": "identificador-unico-do-navegador-do-usuario"
}
```

- **Resposta de Sucesso (200 OK):** Retorna o objeto da enquete com a contagem de votos atualizada.

```json
{
    "id": 1,
    "titulo": "Qual sua linguagem de programação favorita?",
    "opcoes": [
        {"id": 2, "texto_opcao": "JavaScript", "votos": 23}
    ]
}
```

- **Resposta de Erro (409 Conflict):** Voto Duplicado

```json
{
  "error": "Este participante já votou nesta enquete."
}
```

- **Resposta de Erro (400 Bad Request):** Opção Inválida

```json
{
  "error": "Opção inválida para esta enquete."
}
```

---

## 📜 Licença

Este projeto está licenciado sob a Licença MIT.

---

## 🤝 Contribuindo

Contribuições são bem-vindas!  
Se você quiser sugerir melhorias, relatar bugs ou propor novas funcionalidades, sinta-se à vontade para abrir uma *issue* ou *pull request*.

---
