import hashlib, base64

"""
- tentar tirar o append e join
- tentar quebrar as senhas restantes com palavras novas
- ver se em "senhas_nao_quebradas" é preciso ordem alfabética de usuário ou senha
"""

def codificar_senha(senha):
    """
    Codifica a string 'senha' e retorna o resultado.
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

    def gerar_combinacao(*args, dimensao = 1):
        print(f"Gerando combinações de tamanho {dimensao}...")
        bases = [tuple(base) for base in args] * dimensao
        resultado = [[]]
        saida = []
        for base in bases:
            resultado = [x+[y] for x in resultado for y in base]
        for combinacao in resultado:
            saida.append(tuple(combinacao))
        return saida

    global combinacoes
    combinacoes += gerar_combinacao(lista, dimensao = tamanho)
    if tamanho < tamanho_max:
        gerar_combinacoes(lista, tamanho_max, tamanho + 1)
        

def verificar(combinacao):
    """
    Codifica a entrada 'combinacao' através da função 'codificar_senha'
    e verifica se o resultado está contido no arquivo usuarios_senhascodificadas.txt.

    Caso positivo, adiciona a combinação 'usuário:senha decodificada'
    ao arquivo senhas_quebradas.txt e remove a credencial da lista 'credenciais_codificadas'.
    """
    senha_codificada = codificar_senha(combinacao)
    for credencial in credenciais_codificadas:
        if senha_codificada == credencial[1]:
            senhas_quebradas_file.write(f"{credencial[0]}:{combinacao}\n")
            credenciais_codificadas.remove(credencial)

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

comb_counter = 0
print("\nVerificando combinações...\n")
for combinacao in combinacoes:
    comb_counter += 1
    print(f"Verificando combinação {comb_counter} de {len(palavras)**5} ({comb_counter/len(palavras)**5 :.2f}%)", end = "\r")
    verificar(" ".join(combinacao))
print(f"""{comb_counter} combinações verificadas com sucesso.

As senhas quebradas foram adicionadas ao arquivo senhas_quebradas.txt.\n""")

print(f"{len(credenciais_codificadas)} senhas não foram quebradas.") if len(credenciais_codificadas) > 0 else print("Todas as senhas foram quebradas.")

for credencial in credenciais_codificadas:
    senhas_nao_quebradas_file.write(f"{credencial[0]}:{credencial[1]}\n")

palavras_file.close()
credenciais_codificadas_file.close()
senhas_quebradas_file.close()
senhas_nao_quebradas_file.close()