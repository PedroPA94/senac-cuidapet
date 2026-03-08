# CuidaPet – Prova de Conceito

O **CuidaPet** é um sistema proposto para conectar tutores de pets a cuidadores disponíveis para prestação de serviços.

Esta implementação corresponde à Prova de Conceito (POC) do projeto, contemplando exclusivamente a jornada de usuário de um tutor que busca um cuidador.

O presente trabalho é parte da disciplina **“Projeto Integrador: Desenvolvimento de Sistemas Orientado a Dispositivos Móveis e Baseados na Web”**, do curso de **Análise e Desenvolvimento de Sistemas do SENAC**.

A prova de conceito tem como objetivo validar o fluxo principal do sistema, permitindo que tutores:

* Se cadastrar na plataforma
* Cadastrem seus pets
* Realizem agendamentos
* Deixem avaliações

## Tecnologias Utilizadas

* Python 3.12.12
* Django 6.0.2

<br>

# Estrutura do Projeto

```
senac-cuidapet/
├── paginas/                          # App principal do Django
│   ├── models.py                     # Modelos de dados
│   ├── views.py                      # Views
│   ├── forms.py                      # Formulários
│   ├── urls.py                       # Rotas da aplicação
│   ├── static/
│   │   └── css/                      # Estilos CSS
│   └── templates/                    # Templates HTML
│       ├── login.html                # Página de login
│       ├── home.html                 # Home - lista de cuidadores com filtros
│       ├── tutor_form.html           # Cadastro de tutor + pet
│       ├── cuidador_form.html        # Cadastro de cuidador + serviços
│       ├── agendamento_form.html     # Formulário de agendamento
│       ├── agendamento_list.html     # Lista de agendamentos do usuário
│       └── avaliacao_form.html       # Formulário de avaliação
├── setup/                            # Configurações do Django
├── manage.py                         # CLI do Django
├── requirements.txt                  # Dependências do projeto
```

<br>

# Configuração do Ambiente

> Recomenda-se a utilização do **pyenv** para gerenciamento de versões do Python.  
Repositório oficial com instruções de instalação e uso:
[https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)


## Criar e Ativar o Ambiente Virtual (venv)

Dentro da pasta do projeto:

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```


## Instalar Dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém todas as dependências do projeto, incluindo Django 6.0.2.

<br>

# Executando o Projeto

### Aplicar Migrações

```bash
python manage.py migrate
```

### Iniciar o Servidor

```bash
python manage.py runserver
```

O sistema estará disponível em:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

<br>