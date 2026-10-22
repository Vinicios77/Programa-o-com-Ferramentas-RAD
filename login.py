import wx
import json
import os

ARQUIVO_USUARIOS = 'usuarios.json'

def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            return json.load(f)

    usuarios_padrao = {"admin": "1234"}
    salvar_usuarios(usuarios_padrao)
    return usuarios_padrao

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f)


class TelaPrincipal(wx.Frame):
    def __init__(self, parent, usuario):
        super().__init__(parent, title="Sistema Principal", size=(400, 300))
        painel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Mensagem de boas-vindas
        texto_bem_vindo = wx.StaticText(painel, label=f"Acesso liberado!\nBem-vindo(a), {usuario}.")
        fonte = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        texto_bem_vindo.SetFont(fonte)

        btn_sair = wx.Button(painel, label="Sair do Sistema")
        btn_sair.Bind(wx.EVT_BUTTON, self.ao_sair)

        sizer.Add(texto_bem_vindo, 0, wx.ALL | wx.CENTER, 30)
        sizer.Add(btn_sair, 0, wx.ALL | wx.CENTER, 10)

        painel.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.ao_fechar)
        self.Centre()

    def ao_sair(self, evento):
        wx.Exit()

    def ao_fechar(self, evento):
        wx.Exit()


class TelaRecuperacao(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Recuperação de Senha", size=(350, 250))
        self.painel = wx.Panel(self)
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        self.txt_usuario = wx.TextCtrl(self.painel)
        self.txt_nova_senha = wx.TextCtrl(self.painel, style=wx.TE_PASSWORD)

        sizer_principal.Add(wx.StaticText(self.painel, label="Digite seu Usuário:"), 0, wx.ALL, 5)
        sizer_principal.Add(self.txt_usuario, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        sizer_principal.Add(wx.StaticText(self.painel, label="Digite a Nova Senha:"), 0, wx.ALL, 5)
        sizer_principal.Add(self.txt_nova_senha, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        btn_salvar = wx.Button(self.painel, label="Salvar Nova Senha")
        btn_salvar.Bind(wx.EVT_BUTTON, self.ao_salvar)
        sizer_principal.Add(btn_salvar, 0, wx.ALL | wx.CENTER, 15)

        self.painel.SetSizer(sizer_principal)
        self.Centre()

    def ao_salvar(self, evento):
        usuario = self.txt_usuario.GetValue().strip()
        nova_senha = self.txt_nova_senha.GetValue().strip()
        
        if not usuario or not nova_senha:
            wx.MessageBox("Preencha todos os campos!", "Aviso", wx.OK | wx.ICON_WARNING)
            return

        usuarios = carregar_usuarios()

        if usuario in usuarios:
            usuarios[usuario] = nova_senha # Atualiza a senha
            salvar_usuarios(usuarios) # Grava no arquivo
            wx.MessageBox("Senha alterada com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)
            self.Close()
        else:
            wx.MessageBox("Usuário não encontrado no sistema.", "Erro", wx.OK | wx.ICON_ERROR)


class TelaLogin(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(350, 300))
        self.painel = wx.Panel(self)
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(self.painel, label="Login do Sistema")
        titulo.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer_principal.Add(titulo, 0, wx.ALL | wx.CENTER, 15)

        self.txt_usuario = wx.TextCtrl(self.painel)
        self.txt_senha = wx.TextCtrl(self.painel, style=wx.TE_PASSWORD)

        sizer_principal.Add(wx.StaticText(self.painel, label="Usuário:"), 0, wx.LEFT, 10)
        sizer_principal.Add(self.txt_usuario, 0, wx.EXPAND | wx.ALL, 10)
        
        sizer_principal.Add(wx.StaticText(self.painel, label="Senha:"), 0, wx.LEFT, 10)
        sizer_principal.Add(self.txt_senha, 0, wx.EXPAND | wx.ALL, 10)

        sizer_botoes = wx.BoxSizer(wx.HORIZONTAL)
        btn_entrar = wx.Button(self.painel, label="Entrar")
        btn_recuperar = wx.Button(self.painel, label="Esqueci a Senha")

        btn_entrar.Bind(wx.EVT_BUTTON, self.ao_entrar)
        btn_recuperar.Bind(wx.EVT_BUTTON, self.ao_recuperar)

        sizer_botoes.Add(btn_entrar, 0, wx.ALL, 5)
        sizer_botoes.Add(btn_recuperar, 0, wx.ALL, 5)
        
        sizer_principal.Add(sizer_botoes, 0, wx.CENTER | wx.TOP, 10)

        self.painel.SetSizer(sizer_principal)
        self.Centre()
        self.Show()

    def ao_entrar(self, evento):
        usuario = self.txt_usuario.GetValue().strip()
        senha = self.txt_senha.GetValue().strip()
        usuarios = carregar_usuarios()

        if usuario in usuarios and usuarios[usuario] == senha:
            self.Hide() # Oculta a tela de login
            tela_principal = TelaPrincipal(None, usuario)
            tela_principal.Show()
        else:
            wx.MessageBox("Usuário ou senha incorretos!", "Erro de Login", wx.OK | wx.ICON_ERROR)

    def ao_recuperar(self, evento):
        tela_recuperacao = TelaRecuperacao(self)
        tela_recuperacao.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = TelaLogin(None, "Login")
    app.MainLoop()