# imports
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Equipamento
from .forms import EquipamentoForm
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User


# funções de apoio
def login_sauron(usuario,senha):
    from mechanize import Browser
    from bs4 import BeautifulSoup as bs
    from getpass import getpass
    from http.cookiejar import CookieJar

    usuario = str(usuario)
    senha = str(senha)

    #___---¨¨¨ Variáveis do login ¨¨¨---___
    link_de_acesso = "https://meuacesso.sistemas.ro.gov.br/"

    #___---¨¨¨ Sub-Funções do login ¨¨¨---___
    def valida_acesso_sauron(usuario,senha):
        # Faz acesso no sauron

        # Prepara o navegador
        cookies = CookieJar()  # Cria um repositório de cookies
        browser = Browser()    # Inicia um browser
        browser.set_cookiejar(cookies)   # Aponta para o repositório de cookies

        # Acessa o link que redireciona para a página inicial
        browser.open(link_de_acesso)

        # Faz login
        browser.select_form(nr=0)      # o formulário de login é o primeiro(nr=0)
        browser.form['Username'] = usuario  # O texto em form['texto'] é o nome do elemento web onde a informação será inserida
        browser.form['Password'] = senha
        browser.submit()  # envia os dados através do formulário de login

        
        # Tenta obter informações do acesso
        try:
            # Carrega os dados da página atual ("página clique para continuar") e confirma
            browser.select_form(nr=0) # O botão de confirmar é do tipo formulário, então uma opção foi dar submit vazio no primeiro form
            browser.submit()

            # A página carregada deve ser o login efetuado
            pagina_de_acesso = browser.response().read()

            # Passa os dados da página para o BeautifulSoup
            soup = bs(pagina_de_acesso, 'html.parser')

            #print(soup.decode())

            # Salva o resultado em texto, pesquisando classes como tag
            nome = str(soup.find(class_="user-block-name").get_text())
            cpf = str(soup.find(class_="user-block-role").get_text())

            return(nome,cpf)

            #print(f"Login realizado com sucesso!\nNome: {nome.title()}\nCPF: {cpf}\n\n")
            
            

        except Exception as ex:
            #print("Erro", f"Erro ao realizar o login: {ex}")
            #print("senha incorreta\n")
            return("","")


    #___---¨¨¨ Início da execução ¨¨¨---___
    return(valida_acesso_sauron(usuario, senha))
# views de agendamento
def index(request):
    error_message = None
    instruction_message = None
    
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #print(f"\n\nUsuário: {username}\nSenha: {password}\n\n")

        nome,cpf = login_sauron(username,password)

        #print(f"Login realizado com sucesso!\nNome: {nome}\nCPF: {cpf}\n\n")

        # Verifique se o usuário e a senha são "teste"
        if nome != "" and cpf != "" and nome is not None and cpf is not None:
            request.session['username'] = nome  # Salve o nome do usuário na sessão
            return render(request, 'agendamentos/home.html')
        else:
            messages.error(request, 'Credenciais inválidas')  # Use o sistema de mensagens do Django para exibir a mensagem de erro
            return render(request, 'agendamentos/login.html')

    return render(request, 'agendamentos/login.html')
    
def home(request):   
    return render(request, 'agendamentos\home.html')    
def cliente(request):
    return render(request, 'agendamentos\cliente.html')
    
def agendar_equipamento(request):
    return render(request, 'agendamentos\agendar_equipamento.html')
    
def historico(request):
    return render(request, 'agendamentos\historico.html')
    
def administrador(request):
    return render(request, 'agendamentos/administrador.html')
    
#def cadastrar_equipamentos(request):
    if request.method == 'POST':
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_equipamento')  # Redireciona de volta para a página de cadastro
    else:
        form = EquipamentoForm()

    return render(request, 'cadastrar_equipamento.html', {'form': form})
    
def editar_equipamento(request, equipamento_id):
    equipamento = get_object_or_404(Equipamento, pk=equipamento_id)

    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            return redirect('editar_equipamento')

    form = EquipamentoForm(instance=equipamento)
    return render(request, 'editar_equipamento.html', {'form': form, 'equipamento': equipamento})
    
#def excluir_equipamento(request, equipamento_id):
    equipamento = get_object_or_404(Equipamento, pk=equipamento_id)
    equipamento.delete()
    return redirect('excluir_equipamento')  # Redireciona de volta para a página de exclusão
    
    
######################################------------MODIFICAÇÕES---------------###################################################

def listar_equipamentos(request):
    equipamentos = Equipamento.objects.all()
    return render(request, 'agendamentos/equipamentos_list.html', {'equipamentos': equipamentos})

def cadastrar_equipamento(request):
  if request.method == "POST":
    nome = request.POST["nome"]
    descricao = request.POST["descricao"]
    equipamento = Equipamento(nome=nome, descricao=descricao)
    equipamento.save()

    # Verifica se o usuário tem permissão para cadastrar um equipamento
    if request.user.has_perm("equipamentos.add_equipamento"):
      return HttpResponse("Equipamento cadastrado com sucesso!")
    else:
      return HttpResponseForbidden()
  else:
    return render(request, "agendamentos/cadastrar_equipamento.html")
    

def gerenciar_equipamentos(request):
    equipamentos = Equipamento.objects.all()
    return render(request, 'agendamentos/gerenciar_equipamentos.html', {'equipamentos': equipamentos})

def excluir_equipamento(request, equipamento_id):
    equipamento = get_object_or_404(Equipamento, pk=equipamento_id)
    equipamento.delete()
    return redirect('gerenciar_equipamentos')

def alterar_equipamento(request, equipamento_id):
    equipamento = get_object_or_404(Equipamento, pk=equipamento_id)
    if request.method == 'POST':
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_equipamentos')
    else:
        form = EquipamentoForm(instance=equipamento)
    return render(request, 'agendamentos/alterar_equipamento.html', {'form': form, 'equipamento': equipamento})