Enriquecimento Semântico de Dados via Modelos de Linguagem

Este repositório contém o código-fonte e os dados utilizados no projeto de pesquisa "Enriquecimento Semântico de Dados via Modelos de Linguagem: Uma Abordagem Interativa para APIs", desenvolvido no Programa de Pós-Graduação em Tecnologia da Informação do IFPB.

📌 Descrição do Projeto
O projeto propõe uma aplicação interativa que realiza a geração semi-automatizada de anotações semânticas em dados JSON de APIs, utilizando modelos de linguagem de grande escala (LLMs), como o LLaMA e o DeepSeek, em conjunto com o vocabulário Schema.org.

A ferramenta permite que o usuário forneça dados manualmente ou por meio da URL de uma API. Para cada par de chave-valor identificado no JSON, são sugeridas propriedades semânticas que o usuário pode validar, editar ou rejeitar. Ao final do processo, é gerado um arquivo JSON-LD com os dados enriquecidos semanticamente, prontos para integração com sistemas que utilizam metadados estruturados.

📁 Conteúdo do Repositório
base.py: script Python com a implementação principal da aplicação.

test_cases.json: arquivo contendo os exemplos de dados JSON utilizados nos testes. Cada exemplo possui pares do tipo { "key": ..., "value": ..., "expected": ... }, onde o campo expected representa a propriedade esperada segundo o Schema.org.

🚀 Tecnologias e Ferramentas
Python

Schema.org

Modelos de linguagem (LLaMA 3.3, DeepSeek R1) via API local do Ollama

JSON / JSON-LD

📊 Resultados Preliminares
Nos testes com 300 exemplos, a aplicação obteve 100% de revocação, demonstrando alta capacidade de gerar anotações para todos os pares de entrada, ainda que com 38% de precisão, evidenciando a importância da validação humana no processo.

👨‍💻 Autores
Klivio Rafael Nunes e Silva – klivio.silva@academico.ifpb.edu.br

Diego Ernesto Rosa Pessoa – diego.pessoa@ifpb.edu.br

