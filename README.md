# CuidaPet – Prova de Conceito

O **CuidaPet** é um sistema proposto para conectar tutores de pets a cuidadores disponíveis para prestação de serviços.

Esta implementação corresponde à Prova de Conceito (POC) do projeto e contempla as jornadas de tutores e cuidadores.

A prova de conceito tem como objetivo validar o fluxo principal do sistema, permitindo que tutores:

* Se cadastrar na plataforma
* Cadastrem seus pets
* Realizem agendamentos
* Deixem avaliações

Os cuidadores podem:

* Consultar solicitações recebidas
* Analisar os dados do atendimento, tutor e pet
* Aceitar ou recusar agendamentos pendentes
* Acompanhar serviços aceitos e o histórico de atendimentos

## Como funciona a jornada do cuidador

### 1. Login e direcionamento

Na tela de login, o usuário seleciona se deseja entrar como **Tutor** ou
**Cuidador**. O sistema valida se a opção corresponde ao tipo cadastrado na
conta e impede o acesso por uma jornada incompatível. Após autenticar, um perfil do tipo
`CUIDADOR` é direcionado automaticamente para o painel de solicitações. Tutores
continuam sendo direcionados para a página inicial.

### 2. Consulta das solicitações

O painel mostra exclusivamente os agendamentos vinculados ao cuidador logado e
organiza os registros em três grupos:

* **Novas solicitações:** agendamentos com status `PENDENTE`.
* **Próximos serviços:** agendamentos já `ACEITO` pelo cuidador.
* **Histórico:** agendamentos `RECUSADO`, `CONCLUIDO` ou `CANCELADO`.

Cada cartão apresenta pet, tutor, período, valor e status atual.

O topo do dashboard apresenta quatro indicadores calculados com os dados do
cuidador autenticado: solicitações pendentes, agendamentos aceitos, serviços
concluídos e ganhos acumulados. Os ganhos consideram exclusivamente o valor dos
atendimentos com status `CONCLUIDO`.

### 3. Análise dos detalhes

Ao selecionar **Ver detalhes**, o cuidador consulta período e valor do
atendimento, forma de pagamento, dados do pet e contato do tutor. A aplicação
valida que o agendamento pertence ao cuidador autenticado; solicitações de
outros profissionais retornam página não encontrada.

### 4. Aceite ou recusa

Uma solicitação `PENDENTE` oferece as ações **Aceitar solicitação** e
**Recusar**. As duas ações usam requisições POST protegidas por CSRF. A alteração
é executada dentro de uma transação e com bloqueio do registro, evitando duas
decisões simultâneas sobre o mesmo agendamento.

Depois da primeira decisão, o status não pode ser alterado por essa tela. Isso
evita que um atendimento confirmado seja recusado acidentalmente, ou o inverso.

### 5. Acompanhamento do histórico

Após a decisão, o registro muda automaticamente de grupo no painel. Solicitações
aceitas ficam em **Próximos serviços**; recusadas, concluídas e canceladas ficam
em **Histórico**. O tutor também visualiza o status atualizado em sua lista de
agendamentos e só pode avaliar atendimentos concluídos.

### 6. Permissões e segurança

Todas as páginas da jornada exigem autenticação e perfil `CUIDADOR`. As consultas
sempre filtram pelo cuidador logado, tanto na listagem quanto no detalhe e nas
ações de mudança de status. Assim, um cuidador não consegue consultar ou alterar
solicitações pertencentes a outro profissional.

## Sobre o Projeto

O presente trabalho é parte da disciplina **"Projeto Integrador: Desenvolvimento de Sistemas Orientado a Dispositivos Móveis e Baseados na Web"**, do curso de **Análise e Desenvolvimento de Sistemas do SENAC**.

### Integrantes do Grupo

* Cesar Alencar Delfino
* Guilherme Oliveira Silva
* Letycia Iwme Mangolin
* Pedro Papini de Araujo
* Samuel Siqueira Borges

### Metodologia

Durante o desenvolvimento, foi utilizada **programação em pares** em diversos momentos, promovendo colaboração e troca de conhecimento.

## Tecnologias Utilizadas

* Python 3.12.12
* Django 6.0.2

<br>

# Vídeo demonstrativo


https://github.com/user-attachments/assets/8701eb9b-de78-4b44-942c-f138ababf2f5


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

# Modelo de dados

<img width="1402" height="1122" alt="modelo" src="https://github.com/user-attachments/assets/6ae1be9b-db66-49ac-bf99-66fd70d50578" />

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
