import wx
import mysql.connector

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '@Vinicios777', 
    'database': 'sistema_pet'
}

def conectar():
    return mysql.connector.connect(**DB_CONFIG)

def verificar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE nome = %s", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None and resultado[0] == senha

def salvar_pet(dono, nome, idade, raca, peso, cor):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO pets (dono, nome, idade, raca, peso, cor) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (dono, nome, idade, raca, peso, cor))
    conn.commit()
    conn.close()

def buscar_pets(dono):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, raca, idade, peso, cor FROM pets WHERE dono = %s", (dono,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

class TelaCadastroPet(wx.Frame):
    def __init__(self, parent, usuario_logado):
        super().__init__(parent, title=f"Meus PETs - Usuário: {usuario_logado}", size=(600, 600))
        self.usuario = usuario_logado
        painel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(painel, label="Cadastrar Novo PET")
        titulo.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(titulo, 0, wx.ALL | wx.CENTER, 10)

        self.txt_nome = self.criar_campo(painel, sizer, "Nome do PET:")
        self.txt_idade = self.criar_campo(painel, sizer, "Idade:")
        self.txt_raca = self.criar_campo(painel, sizer, "Raça:")
        self.txt_peso = self.criar_campo(painel, sizer, "Peso:")
        self.txt_cor = self.criar_campo(painel, sizer, "Cor:")

        btn_salvar = wx.Button(painel, label="Salvar PET")
        btn_salvar.Bind(wx.EVT_BUTTON, self.ao_salvar)
        sizer.Add(btn_salvar, 0, wx.ALL | wx.CENTER, 10)

        sizer.Add(wx.StaticLine(painel), 0, wx.EXPAND | wx.ALL, 10)
        
        titulo_lista = wx.StaticText(painel, label="PETs que eu já tive:")
        titulo_lista.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(titulo_lista, 0, wx.LEFT, 15)

        self.lista_pets = wx.ListBox(painel, style=wx.LB_SINGLE)
        sizer.Add(self.lista_pets, 1, wx.EXPAND | wx.ALL, 15)

        painel.SetSizer(sizer)
        
        self.atualizar_lista()

        self.Bind(wx.EVT_CLOSE, self.ao_fechar)
        self.Centre()

    def criar_campo(self, painel, sizer, label):
        sizer_linha = wx.BoxSizer(wx.HORIZONTAL)
        sizer_linha.Add(wx.StaticText(painel, label=label, size=(90, -1)), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 15)
        txt_ctrl = wx.TextCtrl(painel)
        sizer_linha.Add(txt_ctrl, 1, wx.EXPAND | wx.RIGHT, 15)
        sizer.Add(sizer_linha, 0, wx.EXPAND | wx.BOTTOM, 5)
        return txt_ctrl

    def atualizar_lista(self):
        self.lista_pets.Clear()
        pets = buscar_pets(self.usuario)
        for pet in pets:
            linha = f"Dono: {self.usuario} | Pet: {pet[0]} | Idade: {pet[2]} | Raça: {pet[1]} | Peso: {pet[3]} | Cor: {pet[4]}"
            self.lista_pets.Append(linha)

    def ao_salvar(self, evento):
        nome = self.txt_nome.GetValue().strip()
        idade = self.txt_idade.GetValue().strip()
        raca = self.txt_raca.GetValue().strip()
        peso = self.txt_peso.GetValue().strip()
        cor = self.txt_cor.GetValue().strip()

        if not all([nome, idade, raca, peso, cor]):
            wx.MessageBox("Preencha todos os campos!", "Aviso", wx.OK | wx.ICON_WARNING)
            return

        salvar_pet(self.usuario, nome, idade, raca, peso, cor)
        wx.MessageBox("PET salvo com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)
        
        self.txt_nome.SetValue("")
        self.txt_idade.SetValue("")
        self.txt_raca.SetValue("")
        self.txt_peso.SetValue("")
        self.txt_cor.SetValue("")

        self.atualizar_lista()

    def ao_fechar(self, evento):
        wx.Exit()

class TelaLogin(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Login - Sistema PET", size=(350, 250))
        painel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(painel, label="Login do Sistema")
        titulo.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(titulo, 0, wx.ALL | wx.CENTER, 15)

        self.txt_usuario = wx.TextCtrl(painel)
        self.txt_senha = wx.TextCtrl(painel, style=wx.TE_PASSWORD)

        sizer.Add(wx.StaticText(painel, label="Usuário:"), 0, wx.LEFT, 10)
        sizer.Add(self.txt_usuario, 0, wx.EXPAND | wx.ALL, 10)
        
        sizer.Add(wx.StaticText(painel, label="Senha:"), 0, wx.LEFT, 10)
        sizer.Add(self.txt_senha, 0, wx.EXPAND | wx.ALL, 10)

        btn_entrar = wx.Button(painel, label="Entrar")
        btn_entrar.Bind(wx.EVT_BUTTON, self.ao_entrar)
        sizer.Add(btn_entrar, 0, wx.ALL | wx.CENTER, 10)

        painel.SetSizer(sizer)
        self.Centre()
        self.Show()

    def ao_entrar(self, evento):
        usuario = self.txt_usuario.GetValue().strip()
        senha = self.txt_senha.GetValue().strip()

        if verificar_login(usuario, senha):
            self.Hide()
            tela_pet = TelaCadastroPet(None, usuario)
            tela_pet.Show()
        else:
            wx.MessageBox("Usuário ou senha incorretos!", "Erro", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    frame = TelaLogin(None)
    app.MainLoop()