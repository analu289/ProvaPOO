"""ALUNO: GUSTAVO BRAVO 
    ALUNO: ANA LÚCIA DA SILVA
    Agenda de Contatos com Etiquetas
    Cadastra contat.nome, telefone e etiquetas (ex: família, trabalho), permitindo buscar e edit	ar.
"""
class Contato:
    def __init__(self, nome, telefone, etiquetas=None):
        
        self.__nome = nome
        self.__telefone = telefone
        self.__etiquetas = etiquetas if etiquetas is not None else []

    def get_nome(self):
        return self.__nome

    def get_telefone(self):
        return self.__telefone

    def get_etiquetas(self):
        return self.__etiquetas

    def set_nome(self, novo_nome):
        if novo_nome.strip():
            self.__nome = novo_nome
        else:
            raise ValueError("Nome não pode ser vazio.")

    def set_telefone(self, novo_telefone):
        if novo_telefone.strip():
            self.__telefone = novo_telefone
        else:
            raise ValueError("Telefone não pode ser vazio.")

    def set_etiquetas(self, novas_etiquetas):
        # Valida que é uma lista e não é vazia
        if isinstance(novas_etiquetas, list) and novas_etiquetas:
            self.__etiquetas = novas_etiquetas
        else:
            raise ValueError("Deve fornecer uma lista de etiquetas não vazia.")

    # Métodos para gerenciar etiquetas individualmente
    def adicionar_etiqueta(self, etiqueta):
        if etiqueta not in self.__etiquetas:
            self.__etiquetas.append(etiqueta)

    def remover_etiqueta(self, etiqueta):
        if etiqueta in self.__etiquetas:
            self.__etiquetas.remove(etiqueta)

    # Método para demonstrar polimorfismo
    def exibir_informacoes(self):
        """Exibe as informações básicas do contato."""
        info = f"Nome: {self.get_nome()}\n"
        info += f"Telefone: {self.get_telefone()}\n"
        info += f"Etiquetas: {', '.join(self.get_etiquetas()) if self.get_etiquetas() else 'Nenhuma'}"
        return info

    def __str__(self):
        """Representação em string do objeto para impressão amigável."""
        return self.exibir_informacoes()

# --- Classes Filhas (Herança) ---
class ContatoPessoal(Contato):
    def __init__(self, nome, telefone, aniversario=None, etiquetas=None):
        # Chama o construtor da classe pai
        super().__init__(nome, telefone, etiquetas)
        self.__aniversario = aniversario

    def get_aniversario(self):
        return self.__aniversario

    def set_aniversario(self, novo_aniversario):
        self.__aniversario = novo_aniversario

    # Sobrescreve o método exibir_informacoes da classe pai (Polimorfismo)
    def exibir_informacoes(self):
        info = super().exibir_informacoes() # Reutiliza a implementação do pai
        if self.get_aniversario():
            info += f"\nAniversário: {self.get_aniversario()}"
        return info

class ContatoComercial(Contato):
    def __init__(self, nome, telefone, empresa, cargo=None, etiquetas=None):
        super().__init__(nome, telefone, etiquetas)
        self.__empresa = empresa
        self.__cargo = cargo

    def get_empresa(self):
        return self.__empresa

    def set_empresa(self, nova_empresa):
        if nova_empresa.strip():
            self.__empresa = nova_empresa
        else:
            raise ValueError("Empresa não pode ser vazia.")

    def get_cargo(self):
        return self.__cargo

    def set_cargo(self, novo_cargo):
        self.__cargo = novo_cargo

    # Sobrescreve o método exibir_informacoes da classe pai (Polimorfismo)
    def exibir_informacoes(self):
        info = super().exibir_informacoes() # Reutiliza a implementação do pai
        info += f"\nEmpresa: {self.get_empresa()}"
        if self.get_cargo():
            info += f"\nCargo: {self.get_cargo()}"
        return info

# --- Classe Agenda ---
class Agenda:
    def __init__(self):
        self.contatos = {}

    def adicionar_contato(self, contato_obj):
        """
        Adiciona um objeto Contato (ou subclasse) à agenda.
        Utiliza o polimorfismo para aceitar diferentes tipos de Contato.
        """
        if not isinstance(contato_obj, Contato):
            raise TypeError("O objeto fornecido não é uma instância de Contato ou subclasse.")

        nome = contato_obj.get_nome()
        try:
            if nome in self.contatos:
                raise ValueError(f"Contato '{nome}' já existe na agenda.")
            self.contatos[nome] = contato_obj
            print(f"Contato '{nome}' adicionado com sucesso!")
        except ValueError as e:
            print(f"Erro ao adicionar contato: {e}")

    def listar_contatos(self):
        """Lista todos os contatos, utilizando o polimorfismo do exibir_informacoes."""
        if not self.contatos:
            print("Nenhum contato cadastrado.")
        else:
            print("\n--- Lista de Contatos ---")
            for nome, contato in self.contatos.items():
                print("-" * 20)
                # O polimorfismo age aqui: cada tipo de contato exibirá suas informações
                # de forma diferente através do mesmo método 'exibir_informacoes()'
                print(contato.exibir_informacoes())
            print("-------------------------")

    def buscar_por_etiqueta(self, etiqueta):
        print(f"\n--- Contatos com a etiqueta '{etiqueta}': ---")
        encontrados = False
        for contato in self.contatos.values():
            if etiqueta in contato.get_etiquetas():
                # Aproveita o exibir_informacoes polimórfico
                print("-" * 10)
                print(contato.exibir_informacoes())
                encontrados = True
        if not encontrados:
            print("Nenhum contato encontrado com essa etiqueta.")
        print("---------------------------------------------")


    def editar_contato(self, nome, novo_telefone=None, novas_etiquetas=None, **kwargs):
        """
        Edita um contato existente.
        Permite editar atributos específicos de subclasses via kwargs.
        """
        try:
            if nome not in self.contatos:
                raise ValueError("Contato não encontrado para edição.")
            
            contato = self.contatos[nome]

            if novo_telefone:
                contato.set_telefone(novo_telefone)
            if novas_etiquetas:
                contato.set_etiquetas(novas_etiquetas)
            
            # Edição de atributos específicos de subclasses (Polimorfismo)
            if isinstance(contato, ContatoPessoal) and 'aniversario' in kwargs:
                contato.set_aniversario(kwargs['aniversario'])
            elif isinstance(contato, ContatoComercial):
                if 'empresa' in kwargs:
                    contato.set_empresa(kwargs['empresa'])
                if 'cargo' in kwargs:
                    contato.set_cargo(kwargs['cargo'])

            print(f"Contato '{nome}' atualizado com sucesso!")
        except ValueError as e:
            print(f"Erro ao editar contato: {e}")
        except AttributeError:
            print(f"Erro: Atributo específico não aplicável a este tipo de contato.")


    def remover_contato(self, nome):
        try:
            if nome in self.contatos:
                del self.contatos[nome]
                print(f"Contato '{nome}' removido com sucesso!")
            else:
                raise ValueError("Contato não encontrado para remoção.")
        except ValueError as e:
            print(f"Erro ao remover contato: {e}")

# --- Demonstração do Uso ---
if __name__ == "__main__":
    agenda = Agenda()

    # Adicionando diferentes tipos de contatos
    agenda.adicionar_contato(Contato("Ana Silva", "1111-2222", ["familia"]))
    agenda.adicionar_contato(ContatoPessoal("João Pereira", "2222-3333", "15/03/1990", ["amigo", "pessoal"]))
    agenda.adicionar_contato(ContatoComercial("Carlos Nogueira", "3333-4444", "Soluções SA", "Desenvolvedor", ["trabalho", "projetos"]))
    agenda.adicionar_contato(Contato("Beatriz Costa", "4444-5555", ["amigos"]))
    agenda.adicionar_contato(ContatoPessoal("Mariana Gomes", "5555-6666", "01/01/2000")) # Sem etiquetas iniciais

    # Tentar adicionar um contato com nome repetido
    agenda.adicionar_contato(Contato("Ana Silva", "9999-0000"))

    # Listar todos os contatos (demonstra polimorfismo no exibir_informacoes)
    agenda.listar_contatos()

    # Buscar por etiqueta
    agenda.buscar_por_etiqueta("trabalho")
    agenda.buscar_por_etiqueta("pessoal")
    agenda.buscar_por_etiqueta("esporte") # Não deve encontrar

    # Editar contatos
    print("\n--- Editando Contatos ---")
    agenda.editar_contato("Ana Silva", novo_telefone="119876-5432")
    agenda.editar_contato("João Pereira", novas_etiquetas=["amigo", "faculdade"], aniversario="20/03/1990") # Editando atributo específico de ContatoPessoal
    agenda.editar_contato("Carlos Nogueira", cargo="Arquiteto de Software", novas_etiquetas=["trabalho", "liderança"]) # Editando atributo específico de ContatoComercial
    agenda.editar_contato("Beatriz Costa", novo_telefone="4444-9999", novas_etiquetas=["amigos", "viagem"])
    agenda.editar_contato("Contato Inexistente", novo_telefone="123") # Deve dar erro

    # Listar após edições
    agenda.listar_contatos()

    # Remover contatos
    print("\n--- Removendo Contatos ---")
    agenda.remover_contato("Mariana Gomes")
    agenda.remover_contato("Carlos Nogueira")
    agenda.remover_contato("Contato Inexistente") # Deve dar erro

    # Lista final
    agenda.listar_contatos()