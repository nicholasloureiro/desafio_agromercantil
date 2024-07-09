# Importando as bibliotecas necessárias
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .models import Posts
from .forms import PostsForm
import yfinance as yf
from yahoo_fin.stock_info import tickers_nasdaq
import numpy as np
import pandas as pd

# Função para listar todas as postagens
def post_list(request):
    posts = Posts.objects.all() # Consulta todas as postagens
    return render(request, 'postlist.html', {'posts':posts}) # Renderiza o template com as postagens

# Função para criar uma nova postagem
def post_create(request):
    if request.method == 'POST': # Verifica se o método é POST
        form = PostsForm(request.POST, request.FILES) # Pega as informações do formulário
        if form.is_valid(): # Verifica se o formulário é válido
            form.save() # Salva o formulário
            messages.success(request, 'O post foi criado com sucesso') # Mensagem de sucesso
            return HttpResponseRedirect(reverse('postlist')) # Redireciona para a lista de postagens
    else:
        form = PostsForm() # Carrega o formulário
    return render(request, 'post-form.html', {"form": form}) # Renderiza o template com o formulário

# Função para visualizar os detalhes de uma postagem
def post_detail(request, id):
    post = Posts.objects.get(id=id) # Pega a postagem pelo ID
    return render(request, 'post-detail.html', {'post': post}) # Renderiza o template com a postagem

# Função para atualizar uma postagem
def post_update(request, id):
    post = get_object_or_404(Posts, id=id) # Pega a postagem pelo ID
    if request.method == 'POST': # Verifica se o método é POST
        form = PostsForm(request.POST or None, request.FILES or None, instance=post) # Pega as informações do formulário
        if form.is_valid(): # Verifica se o formulário é válido
            form.save() # Salva o formulário
            messages.warning(request, 'O post foi atualizado com sucesso') # Mensagem de sucesso
            return HttpResponseRedirect(reverse('post-detail', args=[post.id])) # Redireciona para os detalhes da postagem
    else:
        form = PostsForm(instance=post) # Carrega o formulário com a postagem
    return render(request, 'post-form.html', {"form": form}) # Renderiza o template com o formulário

# Função para deletar uma postagem
def post_delete(request, id): 
    post = Posts.objects.get(id=id) # Pega a postagem pelo ID
    if request.method == 'POST': # Verifica se o método é POST         
        post.delete() # Deleta a postagem
        messages.error(request, 'O post foi deletado com sucesso') # Mensagem de sucesso
        return HttpResponseRedirect(reverse('postlist')) # Redireciona para a lista de postagens
    return render(request, 'post-delete.html') # Renderiza o template de deleção

# Função para pegar os períodos
def get_periods():
    # Definindo períodos e seus parâmetros de visualização
    periods = {
        '5d': 'Últimos 5 dias',
        '1mo': 'Último mês',
        '3mo': 'Últimos 3 meses',
        '6mo': 'Últimos 6 meses',
        '1y': 'Último ano',
        '2y': 'Últimos 2 anos',
        '5y': 'Últimos 5 anos',
        '10y': 'Últimos 10 anos',
        'ytd': 'Desde o início do ano',
        'max': 'Máximo disponível'
    }
    return periods

# Função para pegar os tickers
def stockpicker(request):
    stock_picker = tickers_nasdaq() # Pega a lista de tickers
    periods = get_periods() # Pega os períodos
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker, 'periods': periods}) # Renderiza o template com os tickers e períodos

# Função para recuperar os dados
def retrieve_data(ticker, selected_period):
    ticker_obj = yf.Ticker(ticker) # Cria um objeto ticker
    ticker_info = ticker_obj.info # Pega as informações do ticker
    hist_df = ticker_obj.history(period=selected_period) # Pega os dados históricos
    hist_df = hist_df.reset_index() # Reseta o índice
    return hist_df, ticker_info

# Função para pegar os dados do gráfico
def get_graph_data(hist_df):
    try:
        hist_data = hist_df.to_json(orient="records") # Converte os dados históricos para JSON
        p1, p2 = hist_df["Close"].values[-1], hist_df["Close"].values[-2] # Pega os dois últimos valores de fechamento
        change, prcnt_change = (p2-p1), (p2-p1) / p1 # Calcula a mudança e a porcentagem de mudança
        return hist_data, p1, change, prcnt_change
    except IndexError:
        return 0, 0, 0, 0

# Função para rastrear ações
def stocktracker(request):
    stock_picker = tickers_nasdaq() # Pega a lista de tickers
    periods = get_periods() # Pega os períodos
    selected_stock = request.GET.get('stockpicker', None) # Pega a ação selecionada
    selected_period = request.GET.get('period', None) # Pega o período selecionado
    if not selected_stock or not selected_period: # Verifica se a ação e o período foram fornecidos
        return HttpResponseBadRequest("Nenhuma ação ou período selecionado.") # Retorna um erro se não foram fornecidos
    hist_df, info = retrieve_data(selected_stock, selected_period) # Recupera os dados
    hist_data, p1, change, prcnt_change = get_graph_data(hist_df) # Pega os dados do gráfico
    if request.method == 'POST': # Verifica se o método é POST
        form = PostsForm(request.POST, request.FILES) # Pega as informações do formulário
        if form.is_valid(): # Verifica se o formulário é válido
            form.save() # Salva o formulário
            messages.success(request, 'O post foi criado com sucesso') # Mensagem de sucesso
    else:
        form = PostsForm() # Carrega o formulário
    details = yf.Ticker(selected_stock) # Cria um objeto ticker
    details = details.history(selected_period) # Pega os dados históricos
    hist_df = details.reset_index() # Reseta o índice
    hist_df.columns = hist_df.columns.str.replace(' ', '_') # Substitui os espaços nos nomes das colunas por underscores
    hist_df['color_abertura'] = np.where(hist_df['Open'] < hist_df['Close'], 'red', 'green') # Define a cor de abertura
    hist_df['color_fechamento'] = np.where(hist_df['Close'] < hist_df['Open'], 'red', 'green') # Define a cor de fechamento
    data = hist_df.to_dict(orient='records') # Converte os dados para um dicionário
    
    # Handle KeyError by checking if the keys exist in the info dictionary
    name = info.get("longName", "N/A")
    industry = info.get("industry", "N/A")
    sector = info.get("sector", "N/A")
    summary = info.get("longBusinessSummary", "N/A")
    
    return render(request, 'mainapp/stocktracker.html', { # Renderiza o template com os dados
        "data": data,
        "graph_data": hist_data,
        "name": name,
        "industry": industry,
        "sector": sector,
        "summary": summary,
        "close": f"{p1: .2f} USD",
        'stockpicker': stock_picker,
        'periods': periods,
        "form": form,
        "change": f"{change:.2f}",
        "pct_change": f"{prcnt_change*100:.2f}%"
    })
