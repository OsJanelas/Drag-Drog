import json
import os
import math
import time
import sys
from difflib import get_close_matches

# --- 1. CONFIGURAÇÕES E MEMÓRIA (COM PROTEÇÃO) ---
SENHA_MESTRE = "030213" 

def carregar_memoria():
    try:
        if os.path.exists("memoria_drag.json"):
            with open("memoria_drag.json", "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                if not conteudo:
                    return {"perguntas": []}
                return json.loads(conteudo)
    except Exception as e:
        print(f"\n⚠️ AVISO: Erro ao ler a memória ({e}).")
        print("Vou iniciar com uma memória vazia para não travar.\n")
    return {"perguntas": []}

def salvar_memoria(dados):
    try:
        with open("memoria_drag.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")

# --- 2. O EFEITO DE ESCRITA ---
def drag_fala(texto):
    sys.stdout.write("Drag Drog: ")
    for letra in str(texto):
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(0.03) 
    sys.stdout.write("\n")

# --- 3. CÉREBRO MATEMÁTICO ---
def calcular(entrada):
    # Limpeza básica para aceitar termos em português
    conta = entrada.replace('quanto é', '').replace('vezes', '*').replace('x', '*')
    conta = conta.replace('dividido por', '/').replace('mais', '+').replace('menos', '-')
    conta = conta.replace(',', '.').strip()
    
    try:
        # Só tenta calcular se houver números ou símbolos matemáticos
        if any(c.isdigit() for c in conta):
            res = eval(conta, {"__builtins__": None}, {"math": math})
            return f"O resultado é {res}"
    except:
        return None
    return None

def buscar_na_memoria(pergunta, memoria):
    lista = [p["pergunta"] for p in memoria["perguntas"]]
    match = get_close_matches(pergunta, lista, n=1, cutoff=0.6)
    if match:
        for p in memoria["perguntas"]:
            if p["pergunta"] == match[0]: 
                return p["resposta"]
    return None

# --- 4. INÍCIO DO PROGRAMA ---
memoria = carregar_memoria()

print("="*30)
print("      DRAG DROG ONLINE      ")
print("="*30)

login = input("Senha de Professor (ou Enter para Usuário): ")
modo_treino = (login == SENHA_MESTRE)

if modo_treino:
    drag_fala("Modo PROFESSOR ativado. Estou pronta para aprender!")
else:
    drag_fala("Modo USUÁRIO ativado. Olá!")

while True:
    try:
        user = input("\nVocê: ").strip().lower()
    except EOFError:
        break

    if user in ["sair", "tchau", "exit"]:
        drag_fala("Até logo, mestre!")
        break

    if not user:
        continue

    # 1º - Tenta matemática
    math_res = calcular(user)
    if math_res:
        drag_fala(math_res)
        continue

    # 2º - Tenta buscar na memória (Geografia, etc)
    resp = buscar_na_memoria(user, memoria)
    if resp:
        drag_fala(resp)
    elif modo_treino:
        drag_fala("Isso eu não sei. O que devo responder?")
        nova = input("Sua resposta: ")
        if nova:
            memoria["perguntas"].append({"pergunta": user, "resposta": nova})
            salvar_memoria(memoria)
            drag_fala("Aprendido! Pode testar agora.")
    else:
        drag_fala("Ainda não aprendi sobre isso. Peça ao meu mestre para me ensinar.")