# Aplicação simples feita com DJANGO, permite o usuário procurar ações NASDAQ e fazer, ler, atualizar e deletar comentários sobre as mesmas #
## Fiz o deploy da aplicação na AWS, está disponível no endereço http://54.227.113.17:8000/ o endereço está testado, caso não abra, pode ser alguma proteção de rede, então podemos rodar localmente ##

# Checklist para rodar o desafio Stocktracker

- [ ]  Primeiro verifique se o Python está instalado, com o comando

```sql
python3 --version
```
![i1](https://github.com/nicholasloureiro/desafio_agromercantil/assets/105894972/eca95ef2-4101-49ad-bdbd-0e92eb3be42e)



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

![i2](https://github.com/nicholasloureiro/desafio_agromercantil/assets/105894972/b972d56c-b863-43aa-b4c6-61608c2299a6)


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
