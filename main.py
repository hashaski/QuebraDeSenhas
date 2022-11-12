import hashlib, base64, itertools

"""
- tirar o itertools e arranjar uma forma para gerar combinacoes manual
- tentar tirar o append, extend e join
- tentar quebrar as senhas restantes com palavras novas
- ver se em "senhas_nao_quebradas" é preciso ordem alfabética de usuário ou senha
"""

def codificar_senha(senha):
    """
    Codifica e retorna a string 'senha'.
    """
    senha_encoded = senha.encode('utf-8')
    digest = hashlib.sha512(senha_encoded).digest()
    digest_b64_encoded = base64.b64encode(digest)
    digest_b64_encoded_utf8_decoded = digest_b64_encoded.decode('utf-8')
    return digest_b64_encoded_utf8_decoded


def gerar_combinacoes(lista, tamanho_max, tamanho = 1):
    """
    Gera todas as combinações possíveis dos elementos da lista 'lista',
    de tamanhos 1 até 'tamanho_max', e as insere na lista global 'combinacoes'.
    """

    def comb(lista, tamanho):
        pool = tuple(lista)
        n = len(pool)
        if not n and tamanho:
            return
        indices = [0] * tamanho
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(tamanho)):
                if indices[i] != n - 1:
                    break
            else:
                return
            indices[i:] = [indices[i] + 1] * (tamanho - i)
            yield tuple(pool[i] for i in indices)

    global combinacoes
    combinacoes.extend(comb(lista, tamanho))
    if tamanho < tamanho_max:
        gerar_combinacoes(lista, tamanho_max, tamanho + 1)
    #else:
    #    return


def verificar(combinacao):
    """
    Codifica a entrada 'combinacao' através da função 'codificar_senha'
    e verifica se o resultado está contido no arquivo usuarios_senhascodificadas.txt.

    Caso positivo, adiciona a combinação 'usuário:senha decodificada'
    ao arquivo senhas_quebradas.txt.

    Caso negativo, adiciona #WIP ao arquivo senhas_nao_quebradas.txt.
    """
    senha_codificada = codificar_senha(combinacao)
    for credencial in credenciais_codificadas:
        if senha_codificada == credencial[1]:
            senhas_quebradas_file.write(f"{credencial[0]}:{combinacao}\n")
            credenciais_codificadas.remove(credencial)
    #        return
    #return

#frase = input('# Digite as palavras da sua senha: ')
#codificada = codificar_senha(frase)
#print('#Senha Codificada:', codificada)

palavras_file = open("palavras.txt", "r")
credenciais_codificadas_file = open("usuarios_senhascodificadas.txt", "r")
senhas_quebradas_file = open("senhas_quebradas.txt", "w")
senhas_nao_quebradas_file = open("senhas_nao_quebradas.txt", "w")

palavras = []
for linha in palavras_file:
    palavras.append(linha.rstrip())

credenciais_codificadas = []
for linha in credenciais_codificadas_file:
    credenciais_codificadas.append(linha.rstrip().rsplit(":"))

combinacoes = []

gerar_combinacoes(palavras, 5)

for combinacao in combinacoes:
    verificar(" ".join(combinacao))

for credencial in credenciais_codificadas:
    senhas_nao_quebradas_file.write(f"{credencial[0]}:{credencial[1]}\n")