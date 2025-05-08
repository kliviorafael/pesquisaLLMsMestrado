import requests
import json
import time

# Configurações
TEST_CASES_FILE = "/home/side/projeto_klivio/test_cases.json"
TEST_MODE = False  # Modo de teste automático
MODEL = "llama3:latest"  # Nome do modelo LLaMA no Ollama

# Funções de métricas
def calcular_metricas(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'accuracy': accuracy
    }

# Funções principais
def get_schema_property(key, value):
    try:
        prompt = (
            f"Baseado no Schema.org, responda APENAS com o nome da propriedade mais adequada para:\n"
            f"Chave: {key}\nValor: {value} (tipo: {type(value).__name__})\n"
            f"Formato de resposta EXCLUSIVO: NomeDaPropriedade\n"
            f"Se não encontrar correspondência exata, responda 'N/A'"
        )

        # Payload da requisição
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }

        # Requisição ao modelo local
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        response.raise_for_status()
        resultado = response.json()
        resposta = resultado["message"]["content"].strip()

        return resposta.split('\n')[0].strip().lower()
    except Exception as e:
        return f"erro: {str(e)}"

def avaliar_modelo():
    try:
        with open(TEST_CASES_FILE) as f:
            test_cases = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar casos de teste: {str(e)}")
        return

    resultados = []
    tp = fp = fn = 0

    print(f"\n🔍 Executando {min(len(test_cases), 20)} testes automáticos...")  # Limita a 20 casos

    for i, caso in enumerate(test_cases[:20]):  # Limita a 20 casos
        try:
            predicao = get_schema_property(
                caso["key"], 
                caso["value"]
            )
            esperado = caso["expected"].lower()

            # Contabiliza resultados
            if predicao == esperado:
                tp += 1
                status = "✅"
            elif predicao == "n/a":
                fn += 1
                status = "➖"
            else:
                fp += 1
                status = "❌"

            resultados.append({
                "key": caso["key"],
                "predicao": predicao,
                "esperado": esperado,
                "status": status
            })

            time.sleep(1)  # Intervalo de 1 segundo entre as requisições

        except Exception as e:
            fn += 1
            resultados.append({
                "key": caso["key"],
                "error": str(e),
                "status": "💥"
            })

    metricas = calcular_metricas(tp, fp, fn)

    # Relatório de resultados
    print("\n📊 Resultados da Avaliação Automática")
    print("----------------------------------------")
    print(f"✅ Verdadeiros Positivos: {tp}")
    print(f"❌ Falsos Positivos: {fp}")
    print(f"➖ Falsos Negativos: {fn}")
    print(f"🎯 Precisão: {metricas['precision']:.2%}")
    print(f"📈 Recall: {metricas['recall']:.2%}")
    print(f"🔷 F1-Score: {metricas['f1']:.2%}")
    print(f"🎯 Acurácia: {metricas['accuracy']:.2%}")

    print("\n🧪 Detalhe dos Casos:")
    for i, resultado in enumerate(resultados[:20]):  # Exibe apenas os primeiros 20
        print(f"{resultado['status']} {i+1:03d} | Chave: {resultado['key']:15} | Esperado: {resultado.get('esperado', 'N/A'):15} | Predito: {resultado.get('predicao', 'ERRO'):15}")

    return metricas

def processar_json():
    choice = input("\n🔍 Como deseja fornecer o JSON? (1) Manual (2) URL: ").strip()

    try:
        if choice == "1":
            json_input = input("✏️ Insira o JSON: ").strip()
            data = json.loads(json_input)
            source = "Manual"
        elif choice == "2":
            api_url = input("🔗 Digite a URL da API: ").strip()
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            source = api_url
        else:
            print("⚠️ Opção inválida")
            return
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return

    print("\n📋 Estrutura do JSON:")
    explorar_json(data)
    
    final_data = {}
    items = data.items() if isinstance(data, dict) else data[0].items()

    for key, value in items:
        schema_property = get_schema_property(key, value)

        if not TEST_MODE:
            print(f"\n🔑 Chave: {key}")
            print(f"📌 Valor: {value}")
            print(f"🤖 Sugestão: {schema_property}")
            
            while True:
                opcao = input("(1) Confirmar (2) Editar (3) Pular): ").strip()
                if opcao == '1':
                    final_property = schema_property
                    break
                elif opcao == '2':
                    final_property = input("✏️ Nova propriedade: ").strip()
                    break
                elif opcao == '3':
                    final_property = None
                    break
                else:
                    print("⚠️ Opção inválida")
        else:
            final_property = schema_property

        if final_property:
            final_data[key] = {
                "anotacao": final_property,
                "valor": value,
                "tipo": type(value).__name__
            }

    print("\n🎯 Resultado Final:")
    print(json.dumps({
        "@context": "https://schema.org",
        "@type": "Dataset",
        "fonte": source,
        "data": final_data
    }, indent=2, ensure_ascii=False))

def main():
    global TEST_MODE

    while True:
        print("\n🏠 Menu Principal:")
        print("1. Processar JSON")
        print("2. Executar Testes Automáticos")
        print("3. Sair")
        opcao = input("▶️ Escolha: ").strip()

        if opcao == "1":
            TEST_MODE = False
            processar_json()
        elif opcao == "2":
            TEST_MODE = True
            print("\n🔬 Iniciando modo de teste automático...")
            avaliar_modelo()
        elif opcao == "3":
            print("\n👋 Encerrando...")
            break
        else:
            print("⚠️ Opção inválida")

if __name__ == "__main__":
    main()

