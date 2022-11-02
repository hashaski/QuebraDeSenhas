import hashlib, base64, itertools

"""
- tirar o itertools e arranjar uma forma para gerar combinacoes manual
- tentar tirar o append, extend e join
- ordenar saída senhas_quebradas e senha_nao_quebradas
- tentar quebrar as senhas restantes com palavras novas
"""

def codificar_senha(senha):
    """
    
    """
    senha_encoded = senha.encode('utf-8')
    digest = hashlib.sha512(senha_encoded).digest()
    digest_b64_encoded = base64.b64encode(digest)
    digest_b64_encoded_utf8_decoded = digest_b64_encoded.decode('utf-8')
    return digest_b64_encoded_utf8_decoded


def gerar_combinacoes(lista, tamanho_max):
    """

    """
    global combinacoes
    combinacoes.extend(itertools.combinations_with_replacement(lista, tamanho_max))
    if tamanho_max > 1:
        gerar_combinacoes(lista, tamanho_max - 1)
    else:
        return

def verificar(combinacao):
    """
    
    """
    senha_codificada = codificar_senha(combinacao)
    for credencial in credenciais_codificadas:
        if senha_codificada == credencial[1]:
            senhas_quebradas_file.write(f"{credencial[0]}:{combinacao}\n")
            return
    #BURRO: senhas_nao_quebradas_file.write(senha_codificada)
    return

#frase = input('# Digite as palavras da sua senha: ')
#codificada = codificar_senha(frase)
#print('#Senha Codificada:', codificada)

palavras_file = open("palavras.txt", "r")
credenciais_codificadas_file = open("usuarios_senhascodificadas.txt", "r")
senhas_quebradas_file = open("senhas_quebradas.txt", "a")
senhas_nao_quebradas_file = open("senhas_nao_quebradas.txt", "a")

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

# teste