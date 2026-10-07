class Endereco:
    def __init__(self, rua, numero, bairro, cidade, estado, cep):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep

    def atualizar(self, **campos):
        for campo, valor in campos.items():
            if hasattr(self, campo):
                setattr(self, campo, valor)

    def formatado(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado} - CEP {self.cep}"

    def __str__(self):
        return self.formatado()


class Aluno:
    def __init__(self, nome, matricula, data_nascimento, dados_endereco):
        self.nome = nome
        self.matricula = matricula
        self.data_nascimento = data_nascimento
        self._endereco = Endereco(**dados_endereco)

    @property
    def endereco(self):
        return self._endereco

    def atualizar_endereco(self, **campos):
        if self._endereco is not None:
            self._endereco.atualizar(**campos)

    def liberar_endereco(self):
        endereco = self._endereco
        self._endereco = None
        return endereco

    def exibir_dados(self):
        local = self._endereco.formatado() if self._endereco else "Sem endereço"
        return f"Aluno: {self.nome} | Matrícula: {self.matricula} | Nascimento: {self.data_nascimento} | {local}"

    def __str__(self):
        return self.exibir_dados()


class SalaDeAula:
    def __init__(self, numero, capacidade):
        self.numero = numero
        self.capacidade = capacidade
        self.ocupada = False

    def reservar(self):
        if self.ocupada:
            return False
        self.ocupada = True
        return True

    def liberar(self):
        self.ocupada = False

    def __str__(self):
        situacao = "ocupada" if self.ocupada else "livre"
        return f"Sala {self.numero} (capacidade {self.capacidade}, {situacao})"


class Professor:
    def __init__(self, nome, disciplina, registro):
        self.nome = nome
        self.disciplina = disciplina
        self.registro = registro
        self.escolas = []

    def lecionar_em(self, escola):
        if escola not in self.escolas:
            self.escolas.append(escola)
        if self not in escola.professores:
            escola.professores.append(self)

    def deixar_escola(self, escola):
        if escola in self.escolas:
            self.escolas.remove(escola)
        if self in escola.professores:
            escola.professores.remove(self)

    def listar_escolas(self):
        return [escola.nome for escola in self.escolas]

    def __str__(self):
        return f"Professor: {self.nome} | Disciplina: {self.disciplina} | Escolas: {', '.join(self.listar_escolas()) or 'nenhuma'}"


class Escola:
    def __init__(self, nome, cnpj):
        self.nome = nome
        self.cnpj = cnpj
        self._salas = []
        self.professores = []
        self.alunos = []
        self.enderecos_arquivados = []
        self.aberta = True

    @property
    def salas(self):
        return list(self._salas)

    def criar_sala(self, numero, capacidade):
        sala = SalaDeAula(numero, capacidade)
        self._salas.append(sala)
        return sala

    def remover_sala(self, numero):
        for sala in self._salas:
            if sala.numero == numero:
                self._salas.remove(sala)
                return True
        return False

    def contratar_professor(self, professor):
        professor.lecionar_em(self)

    def dispensar_professor(self, professor):
        professor.deixar_escola(self)

    def matricular_aluno(self, aluno):
        if aluno not in self.alunos:
            self.alunos.append(aluno)

    def remover_aluno(self, aluno):
        if aluno in self.alunos:
            self.alunos.remove(aluno)
            endereco = aluno.liberar_endereco()
            if endereco is not None:
                self.enderecos_arquivados.append(endereco)
            return endereco
        return None

    def fechar(self):
        for professor in list(self.professores):
            professor.deixar_escola(self)
        self._salas.clear()
        self.aberta = False

    def __str__(self):
        return (
            f"Escola: {self.nome} | CNPJ: {self.cnpj} | Salas: {len(self._salas)} | "
            f"Professores: {len(self.professores)} | Alunos: {len(self.alunos)}"
        )


def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Valor não pode ser vazio.")


def ler_inteiro(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor.lstrip("-").isdigit():
            return int(valor)
        print("Digite um número inteiro válido.")


def escolher(itens, titulo, formatar=str):
    if not itens:
        print("Nenhum item disponível.")
        return None
    print(titulo)
    for i, item in enumerate(itens, start=1):
        print(f"  {i}. {formatar(item)}")
    print("  0. Cancelar")
    while True:
        opcao = ler_inteiro("Escolha: ")
        if opcao == 0:
            return None
        if 1 <= opcao <= len(itens):
            return itens[opcao - 1]
        print("Opção inválida.")


class Sistema:
    def __init__(self):
        self.escolas = []
        self.professores = []

    def escolas_abertas(self):
        return [e for e in self.escolas if e.aberta]

    def escolher_escola(self, titulo="Selecione a escola:"):
        escola = escolher(self.escolas_abertas(), titulo, lambda e: e.nome)
        return escola

    def cadastrar_escola(self):
        nome = ler_texto("Nome da escola: ")
        cnpj = ler_texto("CNPJ: ")
        self.escolas.append(Escola(nome, cnpj))
        print("Escola cadastrada com sucesso.")

    def listar_escolas(self):
        if not self.escolas:
            print("Nenhuma escola cadastrada.")
            return
        for escola in self.escolas:
            situacao = "aberta" if escola.aberta else "fechada"
            print(f"{escola} | {situacao}")

    def cadastrar_professor(self):
        nome = ler_texto("Nome do professor: ")
        disciplina = ler_texto("Disciplina: ")
        registro = ler_texto("Registro: ")
        self.professores.append(Professor(nome, disciplina, registro))
        print("Professor cadastrado com sucesso.")

    def listar_professores(self):
        if not self.professores:
            print("Nenhum professor cadastrado.")
            return
        for professor in self.professores:
            print(professor)

    def vincular_professor(self):
        professor = escolher(self.professores, "Selecione o professor:", lambda p: p.nome)
        if professor is None:
            return
        escola = self.escolher_escola()
        if escola is None:
            return
        if escola in professor.escolas:
            print("Professor já leciona nessa escola.")
            return
        escola.contratar_professor(professor)
        print(f"{professor.nome} agora leciona em {escola.nome}.")

    def desvincular_professor(self):
        professor = escolher(self.professores, "Selecione o professor:", lambda p: p.nome)
        if professor is None:
            return
        escola = escolher(professor.escolas, "Desvincular de qual escola?", lambda e: e.nome)
        if escola is None:
            return
        escola.dispensar_professor(professor)
        print(f"{professor.nome} deixou {escola.nome}. O professor continua cadastrado.")

    def cadastrar_sala(self):
        escola = self.escolher_escola()
        if escola is None:
            return
        numero = ler_inteiro("Número da sala: ")
        if any(s.numero == numero for s in escola.salas):
            print("Já existe uma sala com esse número nessa escola.")
            return
        capacidade = ler_inteiro("Capacidade: ")
        escola.criar_sala(numero, capacidade)
        print("Sala criada com sucesso.")

    def listar_salas(self):
        escola = self.escolher_escola()
        if escola is None:
            return
        if not escola.salas:
            print("Essa escola não possui salas.")
            return
        for sala in escola.salas:
            print(sala)

    def alternar_sala(self):
        escola = self.escolher_escola()
        if escola is None:
            return
        sala = escolher(escola.salas, "Selecione a sala:", str)
        if sala is None:
            return
        if sala.ocupada:
            sala.liberar()
            print("Sala liberada.")
        else:
            sala.reservar()
            print("Sala reservada.")

    def matricular_aluno(self):
        escola = self.escolher_escola()
        if escola is None:
            return
        nome = ler_texto("Nome do aluno: ")
        matricula = ler_texto("Matrícula: ")
        nascimento = ler_texto("Data de nascimento: ")
        print("Endereço do aluno:")
        dados = {
            "rua": ler_texto("  Rua: "),
            "numero": ler_texto("  Número: "),
            "bairro": ler_texto("  Bairro: "),
            "cidade": ler_texto("  Cidade: "),
            "estado": ler_texto("  Estado: "),
            "cep": ler_texto("  CEP: "),
        }
        escola.matricular_aluno(Aluno(nome, matricula, nascimento, dados))
        print("Aluno matriculado com sucesso.")

    def listar_alunos(self):
        escola = self.escolher_escola()
        if escola is None:
            return
        if not escola.alunos:
            print("Essa escola não possui alunos.")
            return
        for aluno in escola.alunos:
            print(aluno)

    def atualizar_endereco(self):
        escola = self.escolher_escola()
        if escola is None:
            return
        aluno = escolher(escola.alunos, "Selecione o aluno:", lambda a: a.nome)
        if aluno is None:
            return
        campos = ["rua", "numero", "bairro", "cidade", "estado", "cep"]
        novos = {}
        print("Deixe em branco para manter o valor atual.")
        for campo in campos:
            atual = getattr(aluno.endereco, campo)
            valor = input(f"  {campo.capitalize()} [{atual}]: ").strip()
            if valor:
                novos[campo] = valor
        aluno.atualizar_endereco(**novos)
        print("Endereço atualizado.")

    def remover_aluno(self):
        escola = self.escolher_escola()
        if escola is None:
            return
        aluno = escolher(escola.alunos, "Selecione o aluno a remover:", lambda a: a.nome)
        if aluno is None:
            return
        endereco = escola.remover_aluno(aluno)
        print(f"Aluno {aluno.nome} removido.")
        if endereco is not None:
            print(f"Endereço preservado para relatórios: {endereco}")

    def listar_enderecos_arquivados(self):
        escola = self.escolher_escola()
        if escola is None:
            return
        if not escola.enderecos_arquivados:
            print("Nenhum endereço arquivado nessa escola.")
            return
        for endereco in escola.enderecos_arquivados:
            print(endereco)

    def fechar_escola(self):
        escola = self.escolher_escola("Selecione a escola a fechar:")
        if escola is None:
            return
        confirmacao = input(f"Confirma o fechamento de {escola.nome}? (s/n): ").strip().lower()
        if confirmacao != "s":
            print("Operação cancelada.")
            return
        escola.fechar()
        print("Escola fechada. As salas foram destruídas e os professores desvinculados.")


def exibir_menu():
    print()
    print("=" * 44)
    print("        SISTEMA DE GERENCIAMENTO ESCOLAR")
    print("=" * 44)
    print(" 1. Cadastrar escola")
    print(" 2. Listar escolas")
    print(" 3. Cadastrar professor")
    print(" 4. Listar professores")
    print(" 5. Vincular professor a uma escola")
    print(" 6. Desvincular professor de uma escola")
    print(" 7. Criar sala de aula")
    print(" 8. Listar salas de uma escola")
    print(" 9. Reservar/liberar sala")
    print("10. Matricular aluno")
    print("11. Listar alunos de uma escola")
    print("12. Atualizar endereço de aluno")
    print("13. Remover aluno")
    print("14. Listar endereços arquivados")
    print("15. Fechar escola")
    print(" 0. Sair")


def main():
    sistema = Sistema()
    acoes = {
        1: sistema.cadastrar_escola,
        2: sistema.listar_escolas,
        3: sistema.cadastrar_professor,
        4: sistema.listar_professores,
        5: sistema.vincular_professor,
        6: sistema.desvincular_professor,
        7: sistema.cadastrar_sala,
        8: sistema.listar_salas,
        9: sistema.alternar_sala,
        10: sistema.matricular_aluno,
        11: sistema.listar_alunos,
        12: sistema.atualizar_endereco,
        13: sistema.remover_aluno,
        14: sistema.listar_enderecos_arquivados,
        15: sistema.fechar_escola,
    }
    while True:
        exibir_menu()
        opcao = ler_inteiro("Opção: ")
        if opcao == 0:
            print("Encerrando o sistema.")
            break
        acao = acoes.get(opcao)
        if acao is None:
            print("Opção inválida.")
            continue
        print()
        acao()


if __name__ == "__main__":
    main()