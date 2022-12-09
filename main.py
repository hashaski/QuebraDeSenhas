import hashlib, base64

def codificar_senha(senha):
    """
    Codifica a string 'senha' e retorna o resultado.
    """
    
    senha_encoded = senha.encode('utf-8')
    digest = hashlib.sha512(senha_encoded).digest()
    digest_b64_encoded = base64.b64encode(digest)
    digest_b64_encoded_utf8_decoded = digest_b64_encoded.decode('utf-8')
    return digest_b64_encoded_utf8_decoded


def ordenar(lista):
    """
    Recebe uma lista, a ordena e retorna o resultado
    """
    if not lista:
        return []
    return (ordenar([x for x in lista[1:] if x <  lista[0]])
            + [lista[0]] +
            ordenar([x for x in lista[1:] if x >= lista[0]]))


def processar_combinacoes(lista, tamanho_max, tamanho = 1, comb_counter = 0):
    """
    Gera todas as combinações possíveis de tamanho 'tamanho' da lista 'lista' através da função 'gerar_combinacao'.

    Passa todas as combinações pela função 'verificar', e executa a função recursivamente até que 'tamanho' == 'tamanho_max' - 1,
    de modo que a última execução processe as combinações de tamanho 'tamanho_max'.
    
    Mantém um contador para fins de exibição de progresso de execução.
    """
    

    tamanhos = [i for i in range(1, tamanho_max + 1)]
    numero_combinacoes = sum(len(lista) ** expoente for expoente in tamanhos)
    
    def gerar_combinacao(lista, dimensao = 1):
        """
        Gera o produto cartesiano da lista 'lista' com ela mesma 'dimensao' vezes.
        """
        
        if dimensao == 1:
            return ((a,) for a in lista)
        elif dimensao == 2:
            return ((a, b) for a in lista for b in lista)
        elif dimensao == 3:
            return ((a, b, c) for a in lista for b in lista for c in lista)
        elif dimensao == 4:
            return ((a, b, c, d) for a in lista for b in lista for c in lista for d in lista)
        elif dimensao == 5:
            return ((a, b, c, d, e) for a in lista for b in lista for c in lista for d in lista for e in lista)
    
    
    def verificar_combinacao(combinacao):
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
    

    for combinacao in gerar_combinacao(lista, dimensao = tamanho):
        # Implementamos o contador abaixo, mas o removemos na entraga por conta da perda de desempenho:
        #comb_counter += 1
        #print(f"Verificando combinação {comb_counter} de {numero_combinacoes} ({(comb_counter/numero_combinacoes) * 100 :.2f}%)", end = "\r")
        verificar_combinacao(" ".join(combinacao))

    if tamanho < tamanho_max:
        processar_combinacoes(lista, tamanho_max, tamanho + 1, comb_counter)
        return
    
    print(f"""{numero_combinacoes} combinações foram verificadas com sucesso.    
As senhas quebradas foram adicionadas ao arquivo senhas_quebradas.txt.\n""")
        
    for credencial in credenciais_codificadas:
        senhas_nao_quebradas_file.write(f"{credencial[0]}:{credencial[1]}\n")
    
    print(f"{len(credenciais_codificadas)} senhas não foram quebradas.") if len(credenciais_codificadas) > 0 else print("Não restaram senhas não quebradas.")

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

print("\nVerificando combinações...\n")
processar_combinacoes(ordenar(palavras), 5)

palavras_file.close()
credenciais_codificadas_file.close()
senhas_quebradas_file.close()
senhas_nao_quebradas_file.close()