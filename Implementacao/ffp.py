import sys
import time


def ler_arquivo():
    with open("prof.txt") as arquivo:
        conteudo_do_arquivo = arquivo.readlines()

    numero_de_vertices = int(conteudo_do_arquivo[0])
    numero_de_arestas = int(conteudo_do_arquivo[1])
    numero_de_brigadistas = int(conteudo_do_arquivo[2])
    numero_de_focos_de_incendio = int(conteudo_do_arquivo[3])
    focos_de_incendio = []
    for foco in range(numero_de_focos_de_incendio):
        focos_de_incendio.append(int(conteudo_do_arquivo[4 + foco]))

    grafo = [[] for vertice in range(numero_de_vertices)]

    for aresta in range(numero_de_arestas):
        vertices = conteudo_do_arquivo[4 + numero_de_focos_de_incendio + aresta].split(" ")

        grafo[int(vertices[0])].append(int(vertices[1]))
        grafo[int(vertices[1])].append(int(vertices[0]))

    return grafo, numero_de_brigadistas, numero_de_focos_de_incendio, focos_de_incendio, numero_de_vertices


def relevancia(vertice_da_analise, focos_de_incendio, numero_de_brigadistas, grafo, estados):
    soma = 0  # inicializar soma com 0
    antecessores = 0
    sucessores = 0
    anteriores = 0

    #print(f'\n\nAnalise do vertice {vertice_da_analise}:')
    #print(f'Soma: {soma}')
    #print(f'Antecessores: {antecessores}')
    #print(f'Sucessores: {sucessores}')
    #print(f'Anteriores: {anteriores}')

    estados[vertice_da_analise] = 1  # marcar vertice da analise como defendido

    # queimar vertices adjacentes aos focos
    proximos_a_serem_queimados = []
    for foco in focos_de_incendio:  # esse for percorre todos os vértices com focos de incêndio
        for vertice in grafo[foco]:  # percorre as adjacências de um foco
            if estados[vertice] == 0:  # vertice intocado
                proximos_a_serem_queimados.append(vertice)

    proximos_a_serem_queimados = list(set(proximos_a_serem_queimados))  # remover possiveis repeticao

    quantidade_a_serem_queimadas = len(proximos_a_serem_queimados)
    soma += quantidade_a_serem_queimadas
    antecessores += quantidade_a_serem_queimadas
    anteriores += quantidade_a_serem_queimadas

    #print(f'\n\nAnalise do vertice {vertice_da_analise}:')
    #print(f'Soma: {soma}')
    #print(f'Antecessores: {antecessores}')
    #print(f'Sucessores: {sucessores}')
    #print(f'Anteriores: {anteriores}')

    focos_de_incendio = proximos_a_serem_queimados  # os proximos a serem queimados, agora sao queimados
    for foco in focos_de_incendio:
        estados[foco] = 2

    # A primeira iteracao deve executar independente se os antecessores eh menor
    # ou igual ao numero de defensores

    # queimar vertices adjacentes aos focos
    proximos_a_serem_queimados = []
    for foco in focos_de_incendio:  # esse for percorre todos os vértices com focos de incêndio
        for vertice in grafo[foco]:  # percorre as adjacências de um foco
            if estados[vertice] == 0:  # vertice intocado
                proximos_a_serem_queimados.append(vertice)

    if not proximos_a_serem_queimados:  # se nao tem proximos a serem queimados retorna a soma atual
        return soma

    proximos_a_serem_queimados = list(set(proximos_a_serem_queimados))  # remover possiveis repeticoes
    sucessores += len(proximos_a_serem_queimados)
    anteriores = (sucessores / antecessores) * anteriores - numero_de_brigadistas

    if anteriores <= 0:
        return soma

    soma += anteriores

    #print(f'\n\nAnalise do vertice {vertice_da_analise}:')
    #print(f'Soma: {soma}')
    #print(f'Antecessores: {antecessores}')
    #print(f'Sucessores: {sucessores}')
    #print(f'Anteriores: {anteriores}')

    focos_de_incendio = proximos_a_serem_queimados  # os proximos a serem queimados, agora sao queimados
    for foco in focos_de_incendio:
        estados[foco] = 2

    while focos_de_incendio:
        antecessores = sucessores

        # queimar vertices adjacentes aos focos
        proximos_a_serem_queimados = []
        for foco in focos_de_incendio:  # esse for percorre todos os vértices com focos de incêndio

            for vertice in grafo[foco]:  # percorre as adjacências de um foco
                if estados[vertice] == 0:  # vertice intocado
                    proximos_a_serem_queimados.append(vertice)

        proximos_a_serem_queimados = list(set(proximos_a_serem_queimados))  # remover possiveis repeticoes
        sucessores = (len(proximos_a_serem_queimados))

        #print(f'\n\nAnalise do vertice {vertice_da_analise}:')
        #print(f'Soma: {soma}')
        #print(f'Antecessores: {antecessores}')
        #print(f'Sucessores: {sucessores}')
        #print(f'Anteriores: {anteriores}')

        if antecessores <= numero_de_brigadistas:
            break

        if not proximos_a_serem_queimados:  # se nao tem proximos a serem queimados retorna a soma atual
            break

        anteriores = (sucessores / antecessores) * min(antecessores, anteriores) - numero_de_brigadistas

        #print(f'\n\nAnalise do vertice {vertice_da_analise}:')
        #print("Conta Complexa")
        #print(f'Soma: {soma}')
        #print(f'Antecessores: {antecessores}')
        #print(f'Sucessores: {sucessores}')
        #print(f'Anteriores: {anteriores}')

        if anteriores <= 0:
            break

        soma += anteriores

        #print(f'\n\nAnalise do vertice {vertice_da_analise}:')
        #print("Conta Complexa")
        #print(f'Soma: {soma}')
        #print(f'Antecessores: {antecessores}')
        #print(f'Sucessores: {sucessores}')
        #print(f'Anteriores: {anteriores}')

        # queimar os proximos a serem queimados
        focos_de_incendio = proximos_a_serem_queimados
        for foco in focos_de_incendio:
            estados[foco] = 2

    return soma


def algoritmo_ffp(grafo, numero_de_brigadistas, focos_de_incendio, numero_de_focos_de_incendio, numero_de_vertices):
    print("\n\nIniciando o Algoritmo !\n\n")

    numero_de_vertices_queimados = numero_de_focos_de_incendio
    rodada = 0
    vertices_defendidos = []

    estados = [0] * numero_de_vertices  # iniciamente todos os vertices estao intocados
    # marcar focos de incendio como queimados
    for foco in focos_de_incendio:
        estados[foco] = 2

    while focos_de_incendio:  # enquanto tiver focos de incendio
        rodada += 1

        #print("\n\nRodada", rodada)

        #marcar vertices proximos ao foco como proximos a serem queimados
        proximos_a_serem_queimados = []
        for foco in focos_de_incendio:  # esse for percorre todos os vértices com focos de incêndio
            for vertice in grafo[foco]:  # percorre as adjacências de um foco
                if estados[vertice] == 0:  # vertice intocado
                    proximos_a_serem_queimados.append(vertice)

        proximos_a_serem_queimados = list(set(proximos_a_serem_queimados))  # remover possiveis repeticoes

        if not proximos_a_serem_queimados:  # se nao tiver proximos a serem queimados termina a execucao
            break

        # defender vertices com menor relevancia
        for defensor in range(numero_de_brigadistas):
            # calcular o somatorio(relevancia) de cada vertice a ser queimado
            somas = []
            for proximo_a_ser_queimado in proximos_a_serem_queimados:
                somas.append((proximo_a_ser_queimado,
                              relevancia(proximo_a_ser_queimado, focos_de_incendio.copy(), numero_de_brigadistas, grafo,
                                         estados.copy())))
            #print(f'Defensor {defensor}. Medias:{somas}')
            if proximos_a_serem_queimados:  # enquanto tiver vertices para serem defendidos
                minimo = min(somas, key=lambda x: x[1])
                estados[minimo[0]] = 1  # defender o vertice com menor relevancia
                vertices_defendidos.append((minimo[0], rodada))  # adicionar na lista de vertices defendidos
                proximos_a_serem_queimados.remove(minimo[0])  # e remover dos proximos a serem queimados
                #print("Vertice Defendido", minimo[0])
                #print("Soma do Vertice Defendido", minimo[1])
            else:
                break

        focos_de_incendio = proximos_a_serem_queimados  # os focos de incendio recebem os proximos a serem queimados
        # e os vertices que nao foram defendidos sao queimados
        for foco in focos_de_incendio:
            estados[foco] = 2
            numero_de_vertices_queimados += 1

    #print(estados)
    return numero_de_vertices_queimados, vertices_defendidos


if __name__ == "__main__":
    grafo, numero_de_brigadistas, numero_de_focos_de_incendio, focos_de_incendio, numero_de_vertices = ler_arquivo()
    print(numero_de_brigadistas)
    print(numero_de_focos_de_incendio)
    print(focos_de_incendio)
    print(numero_de_vertices)

    tempo = time.time()
    numero_de_vertices_queimados, vertices_defendidos = algoritmo_ffp(grafo, numero_de_brigadistas,
                                                                      focos_de_incendio, numero_de_focos_de_incendio,
                                                                      numero_de_vertices)
    tempo = time.time() - tempo

    print("Fim do Algoritmo \n")
    for vertice_defendido in vertices_defendidos:
        print("Vértice defendido:", vertice_defendido[0], "\nNa rodada:", vertice_defendido[1])

    print("\nNúmero de vértices queimados:", numero_de_vertices_queimados)
    print("\nDuração", tempo, "s")
    