import math
from collections import Counter


def id3(data, target_attribute, attributes):
    # Cria o nó raiz
    root = {}

    # Verifica se todos os exemplos dão vitória, empate ou derrota
    if all(example[target_attribute] == 'win' for example in data):
        root['label'] = 'win'
        return root
    elif all(example[target_attribute] == 'draw' for example in data):
        root['label'] = 'draw'
        return root
    elif all(example[target_attribute] == 'loss' for example in data):
        root['label'] = 'loss'
        return root
    
    # Verifica se não há atributos de previsão restantes
    elif not attributes:
        # Retorna a raiz da árvore com a label = valor mais comum da target
        target_values = [example[target_attribute] for example in data]
        most_common_target_value = Counter(target_values).most_common(1)[0][0] # retorna o valor mais comum
        root['label'] = most_common_target_value
        return root

    else:
        # Seleciona o melhor atributo para classificar os exemplos
        A = select_attribute(data, target_attribute, attributes)
        root['attribute'] = A

        # Para cada valor possível do atributo, cria um novo ramo e chama recursivamente o ID3
        for value in get_attribute_values(data, A):
            # Cria um novo ramo
            root[value] = {}
            data_vi = [example for example in data if example[A] == value]

            # Verifica se o subconjunto de exemplos está vazio
            if not data_vi:
                # Adiciona um nó folha com o valor mais comum da target
                target_values = [example[target_attribute] for example in data]
                most_common_target_value = Counter(target_values).most_common(1)[0][0]
                root[value]['label'] = most_common_target_value

            else:
                # Chama recursivamente o ID3 com o subconjunto de exemplos
                new_attributes = attributes - {A}
                root[value] = id3(data_vi, target_attribute, new_attributes)

        return root


def select_attribute(data, target_attribute, attributes):
    # Calcula a entropia do conjunto de exemplos
    entropy_S = entropy([example[target_attribute] for example in data])

    # Calcula o ganho de informação para cada atributo
    information_gain = {}
    for attribute in attributes:
        information_gain[attribute] = entropy_S - remainder(data, attribute, target_attribute)

    # Retorna o atributo com maior ganho de informação
    return max(information_gain, key=information_gain.get)


def entropy(target_values):
    
    # Conta o número de ocorrências de cada valor da target
    value_counts = Counter(target_values)

    # Calcula a entropia
    entropy = 0
    for count in value_counts.values():
        probability = count / len(target_values)
        entropy -= probability * math.log2(probability)

    return entropy


def remainder(data, attribute, target_attribute):
    # Calcula o remainder
    remainder = 0
    for value in get_attribute_values(data, attribute):
        data_vi = [example for example in data if example[attribute] == value]
        entropy_vi = entropy([example[target_attribute] for example in data])
        probability_vi = len(data_vi) / len(data)
        remainder += probability_vi * entropy_vi

    return remainder


def get_attribute_values(data, attribute):
    # Retorna os valores possíveis do atributo
    return set(example[attribute] for example in data)


def read_csv(file_path):
    # Lê o ficheiro CSV e retorna uma lista de dicionários
    with open(file_path, 'r') as f:
        lines = f.readlines()
        headers = lines[0].strip().split(',')
        rows = []
        for line in lines[1:]:
            values = line.strip().split(',')
            row = {}
            for i in range(len(headers)):
                row[headers[i]] = values[i]
            rows.append(row)
        return rows


            
def predict_example(example, tree):
    # Devolve a label prevista para o exemplo
    if 'label' in tree: # Verifica se o nó é uma folha
        return tree['label']
    else:
        attribute = tree['attribute'] # Atributo que divide o nó
        attribute_value = example.get(attribute)  # Retorna None se o atributo não estiver presente no exemplo

        if attribute_value is None or attribute_value not in tree:
            # Retorna a label mais comum do subconjunto de exemplos se o valor do atributo não estiver presente no nó
            labels_in_subtree = [subtree['label'] for subtree in tree.values() if 'label' in subtree]
            
            if len(labels_in_subtree) == 0:
                return 'draw' # Retorna a label default (draw) quando não há labels no subconjunto de exemplos
            
            return max(labels_in_subtree, key=labels_in_subtree.count) # Retorna a label mais comum do subconjunto de exemplos

        subtree = tree[attribute_value] # Seleciona o ramo correspondente ao valor do atributo
        return predict_example(example, subtree) # Chama recursivamente a função com o ramo selecionado


