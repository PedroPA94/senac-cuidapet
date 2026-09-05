# CuidaPet – Prova de Conceito

O **CuidaPet** é um sistema proposto para conectar tutores de pets a cuidadores disponíveis para prestação de serviços.

Esta implementação corresponde à Prova de Conceito (POC) do projeto e contempla as jornadas de tutores e cuidadores.

A prova de conceito tem como objetivo validar o fluxo principal do sistema, permitindo a tutores:

* Se cadastrar na plataforma
* Cadastrar um pet durante o registro
* Realizar agendamentos
* Deixar avaliações

E aos cuidadores:

* Consultar solicitações recebidas
* Analisar os dados do atendimento, tutor e pet
* Aceitar ou recusar agendamentos pendentes
* Desistir ou finalizar atendimentos aceitos
* Acompanhar o histórico de atendimentos

## Sumário

* [Sobre o Projeto](#sobre-o-projeto)
* [Jornadas](#jornadas)
  * [Tutor](#tutor)
  * [Cuidador](#cuidador)
* [Vídeo demonstrativo](#vídeo-demonstrativo)
* [Estrutura do Projeto](#estrutura-do-projeto)
* [Modelo de dados](#modelo-de-dados)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Configuração do Ambiente](#configuração-do-ambiente)
* [Executando o Projeto](#executando-o-projeto)

## Sobre o Projeto

O presente trabalho é parte da disciplina **"Projeto Integrador: Análise de Soluções Integradas para Organizações"**, do curso de **Análise e Desenvolvimento de Sistemas do SENAC**.

### Integrantes do Grupo

* Cesar Alencar Delfino
* Guilherme Oliveira Silva
* Letycia Iwme Mangolin
* Pedro Papini de Araujo
* Samuel Siqueira Borges

### Metodologia

Durante o desenvolvimento, foi utilizada **programação em pares** em diversos momentos, promovendo colaboração e troca de conhecimento.

## Jornadas

### Tutor

#### 1. Cadastro do tutor e do pet

O usuário escolhe o perfil **Tutor** na tela de cadastro e informa nome,
telefone, e-mail e senha. Nesse mesmo fluxo, pode cadastrar um pet com
nome, espécie, raça e data de nascimento. O cadastro do pet é opcional nessa
etapa, mas é necessário ter um pet cadastrado para realizar um agendamento.

#### 2. Login e busca por cuidadores

Na tela de login, o tutor seleciona a opção **Tutor**. O sistema confere se a
opção corresponde ao tipo da conta e, após a autenticação, direciona o usuário
para a página inicial. Nela, é possível filtrar cuidadores por estado e cidade e
consultar nome, localização, descrição e valor da diária de cada profissional.

#### 3. Escolha do cuidador

Ao selecionar **Agendar**, o tutor acessa o perfil do cuidador, com sua
apresentação, os serviços oferecidos, o valor da diária e as avaliações deixadas
por outros clientes. Essa tela também concentra o formulário para solicitar o
atendimento.

#### 4. Solicitação do agendamento

O tutor escolhe seu pet, informa as datas de início e término e seleciona
a forma de pagamento entre **Pix**, **Cartão** e **Dinheiro**. A interface apresenta a
quantidade de dias e a estimativa do valor, enquanto o servidor calcula o total
definitivo multiplicando o número de diárias, incluindo as datas inicial e final,
pelo valor cobrado pelo cuidador.

Quando a solicitação é criada, ela recebe o status `PENDENTE` e fica disponível
para análise do cuidador.

#### 5. Acompanhamento dos agendamentos

Em **Meus agendamentos**, o tutor visualiza somente as próprias solicitações,
ordenadas da mais recente para a mais antiga. Cada cartão exibe cuidador, pet,
período, forma de pagamento, valor total, localização e o status atualizado do
serviço: `PENDENTE`, `ACEITO`, `RECUSADO`, `CONCLUIDO` ou `CANCELADO`.

#### 6. Avaliação do serviço

Depois que o cuidador finaliza o atendimento e o status passa para `CONCLUIDO`,
o tutor pode atribuir uma nota de 1 a 5 estrelas e escrever um comentário. Cada
agendamento aceita uma única avaliação; depois do envio, a nota fica registrada
na lista do tutor e passa a aparecer no perfil do cuidador, na tela de
agendamento.

#### 7. Permissões e segurança

O agendamento, sua listagem e o envio da avaliação exigem autenticação. No
formulário de agendamento, o tutor só pode selecionar pets vinculados à própria
conta; na listagem, as consultas também são filtradas pelo usuário autenticado. A
aplicação ainda verifica a propriedade do agendamento antes de registrar a
avaliação.

### Cuidador

#### 1. Login e direcionamento

Na tela de login, o usuário seleciona se deseja entrar como **Tutor** ou
**Cuidador**. O sistema valida se a opção corresponde ao tipo cadastrado na
conta e impede o acesso por uma jornada incompatível. Após autenticar, um perfil do tipo
`CUIDADOR` é direcionado automaticamente para o painel de solicitações. Tutores
continuam sendo direcionados para a página inicial.

#### 2. Consulta das solicitações

O painel mostra exclusivamente os agendamentos vinculados ao cuidador logado e
organiza os registros em três grupos:

* **Pendentes:** agendamentos com status `PENDENTE`.
* **A atender:** agendamentos já `ACEITO` pelo cuidador.
* **Histórico:** agendamentos `RECUSADO`, `CONCLUIDO` ou `CANCELADO`.

Cada cartão apresenta pet, tutor, período, valor e status atual.

O topo do dashboard apresenta quatro indicadores calculados com os dados do
cuidador autenticado: solicitações pendentes, agendamentos aceitos, serviços
concluídos e ganhos acumulados. Os ganhos consideram exclusivamente o valor dos
atendimentos com status `CONCLUIDO`.

#### 3. Análise dos detalhes

Ao selecionar **Ver detalhes**, o cuidador consulta período e valor do
atendimento, forma de pagamento, dados do pet e contato do tutor. A aplicação
valida que o agendamento pertence ao cuidador autenticado; solicitações de
outros profissionais retornam página não encontrada.

#### 4. Decisão e conclusão do atendimento

Uma solicitação `PENDENTE` oferece as ações **Aceitar solicitação** e
**Recusar**. Quando aceita, ela passa para o status `ACEITO` e oferece as ações
**Desistir** e **Finalizar atendimento**, que alteram o status para `CANCELADO` e
`CONCLUIDO`, respectivamente.

Todas as alterações usam requisições POST protegidas por CSRF e são executadas
dentro de uma transação, com bloqueio do registro. Uma solicitação só pode ser
aceita ou recusada enquanto estiver pendente; da mesma forma, apenas um
atendimento aceito pode ser finalizado ou cancelado.

#### 5. Acompanhamento do histórico

Após a decisão, o registro muda automaticamente de grupo no painel. Solicitações
aceitas ficam em **A atender**; recusadas, concluídas e canceladas ficam
em **Histórico**. O tutor também visualiza o status atualizado em sua lista de
agendamentos e só pode avaliar atendimentos concluídos.

#### 6. Permissões e segurança

Todas as páginas da jornada exigem autenticação e perfil `CUIDADOR`. As consultas
sempre filtram pelo cuidador logado, tanto na listagem quanto no detalhe e nas
ações de mudança de status. Assim, um cuidador não consegue consultar ou alterar
solicitações pertencentes a outro profissional.


## Vídeo demonstrativo


https://github.com/user-attachments/assets/8701eb9b-de78-4b44-942c-f138ababf2f5



## Estrutura do Projeto

```
senac-cuidapet/
├── paginas/                  # Aplicação principal
│   ├── migrations/           # Estrutura e dados iniciais do banco
│   ├── static/               # Estilos e imagens
│   ├── templates/            # Telas de tutores e cuidadores
│   ├── models.py             # Modelos de dados
│   ├── forms.py              # Formulários e validações
│   ├── views.py              # Regras e fluxos da aplicação
│   ├── urls.py               # Rotas da aplicação
│   └── tests.py              # Testes automatizados
├── setup/                    # Configurações gerais do Django
├── manage.py                 # Comandos de gerenciamento
└── requirements.txt          # Dependências Python
```

## Modelo de dados

<img width="1402" height="1122" alt="modelo" src="https://github.com/user-attachments/assets/6ae1be9b-db66-49ac-bf99-66fd70d50578" />


## Tecnologias Utilizadas

* Python 3.12.12
* Django 6.0.2


## Configuração do Ambiente

> Recomenda-se a utilização do **pyenv** para gerenciamento de versões do Python.  
Repositório oficial com instruções de instalação e uso:
[https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)


### Criar e Ativar o Ambiente Virtual (venv)

Dentro da pasta do projeto:

#### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```


### Instalar Dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém todas as dependências do projeto, incluindo Django 6.0.2.


## Executando o Projeto

### Aplicar Migrações

```bash
python manage.py migrate
```

As migrações também criam os serviços e os dados usados na demonstração.

### Dados para demonstração

Depois de aplicar as migrações, use uma das contas abaixo para percorrer as duas
jornadas:

| Perfil | E-mail | Senha |
| --- | --- | --- |
| Tutor | `augusto@email.com` | `123456` |
| Cuidador | `joao@email.com` | `123456` |

Essas credenciais são destinadas exclusivamente à demonstração local da POC.

### Iniciar o Servidor

```bash
python manage.py runserver
```

O sistema estará disponível em:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Executar os Testes

```bash
python manage.py test
```

<br>
