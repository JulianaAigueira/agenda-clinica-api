# 🏥 API Clínica - Gestão de Agendamentos

Uma API RESTful desenvolvida em Python e Django Rest Framework para gerenciar pacientes, especialistas, procedimentos e agendamentos de uma clínica.

## 🚀 Tecnologias Utilizadas
* Python 3
* Django
* Django Rest Framework
* SQLite (Banco de dados padrão)

## ⚙️ Funcionalidades e Regras de Negócio
Este projeto vai além de um CRUD básico, implementando regras de negócio reais de uma clínica:
* **Prevenção de Conflitos (Double Booking):** A API calcula automaticamente a duração dos procedimentos e bloqueia (Status 400 Bad Request) tentativas de agendamento no mesmo horário para o mesmo especialista.
* **Validação Temporal:** Impede a criação de agendamentos com datas no passado.
* **Autenticação:** O acesso aos agendamentos é bloqueado (Status 403 Forbidden) para visitantes não autenticados.
* **Autorização (Filtro Dinâmico):** Clientes comuns só conseguem visualizar seus próprios agendamentos, enquanto usuários com status de `staff` (Administradores/Médicos) têm visão geral da agenda.

## 💻 Como executar o projeto localmente

1. Clone este repositório:
`git clone https://github.com/JulianaAigueira/agenda-clinica-api.git`

2. Crie e ative um ambiente virtual:
`python -m venv .venv`
`.venv\Scripts\activate` (No Windows)

3. Instale as dependências:
`pip install -r requirements.txt`

4. Crie o banco de dados e as tabelas:
`python manage.py migrate`

5. Inicie o servidor:
`python manage.py runserver`