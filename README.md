## Aplicação simples feita com DJANGO, permite o usuário procurar ações NASDAQ e fazer, ler, atualizar e deletar comentários sobre as mesmas ##

# Checklist para rodar o desafio Stocktracker

- [ ]  Primeiro verifique se o Python está instalado, com o comando

```sql
python3 --version
```

![Untitled](Checklist%20para%20rodar%20o%20desafio%20Stocktracker%206135b06ff64343dabf9a0907871cb99f/Untitled.png)

- [ ]  Com o python instalado vamos clonar o repositório, com o comando:

```sql
git clone https://github.com/nicholasloureiro/desafio_agromercantil.git
```

- [ ]  A pasta desafio_agromercantil será criada, então vamos entrar nela e criar um ambiente virtual com os comandos:

```sql
cd desafio_agromercantil

python3 -m venv venv

- No windows -> venv\Scripts\activate.ps1
- No linux -> source venv/bin/activate

você deverá ver o escrito (venv) na esquerda do seu terminal
```

![Untitled](Checklist%20para%20rodar%20o%20desafio%20Stocktracker%206135b06ff64343dabf9a0907871cb99f/Untitled%201.png)

- [ ]  Hora de instalar os requirements com o comando:

```sql
pip install -r requirements.txt
```

- [ ]  Por fim,  faça as migrações do banco e rode o programa, com os comandos:

Eu subi essa parte em 2 computadores, o primeiro funcionou com esse conjunto:

```sql
python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```

O segundo funcionou adicionando um 3 ao final de python, o erro encontrado é de importação do django. Caso se deparar com um erro de importação nesse passo, tente das duas formas.

```sql
python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver
```
