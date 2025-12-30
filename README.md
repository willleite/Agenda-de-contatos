#  Agenda de Contatos — Sistema Full Stack

Sistema de *Agenda de Contatos* desenvolvido em arquitetura *Full Stack, utilizando **React no Frontend* e *FastAPI no Backend*, com persistência de dados em banco relacional.  
O projeto foi estruturado seguindo boas práticas de organização, separação de responsabilidades e integração via API REST.

---

##  Visão Geral

O sistema permite o gerenciamento completo de contatos telefônicos, oferecendo operações de *criação, leitura, atualização e exclusão (CRUD)*, além de comunicação segura entre frontend e backend.

---

##  Tecnologias Utilizadas

### Frontend
- React
- Vite
- JavaScript (ES6+)
- HTML5
- CSS3

### Backend
- Python 3
- FastAPI
- SQLAlchemy
- Uvicorn
- SQLite

---

##  Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- *Python 3.10 ou superior*
- *Node.js 18 ou superior*
- *npm*
- *Git* (opcional)

---

##  Execução do Projeto

###  Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/agenda_contatos.git
cd agenda_contatos

##Executar Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

##Backend disponivel em:
http://127.0.0.1:8000

##Executar Fentend
cd frontend
npm install
npm run dev

##Frontend disponivel em:
http://localhosr:5173

##Executar Frontend e Backend simultaneamente(Windows)
```bash 
start-all.bat