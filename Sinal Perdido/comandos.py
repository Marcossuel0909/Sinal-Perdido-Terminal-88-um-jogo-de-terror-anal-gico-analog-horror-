from estado import dados, log_mensagens
from audio import tocar_estatica_radio, tocar_bip_morse
from narrativa import checar_avanco_dia

def registrar_acao():
    """Conta cada ação executada pelo jogador para avançar o dia."""
    dados["acoes_no_dia"] = dados.get("acoes_no_dia", 0) + 1
    checar_avanco_dia()

def consumir_energia(qtd=5):
    dados["energia"] -= qtd
    if dados["energia"] <= 0:
        dados["energia"] = 0
        dados["final_jogo"] = "DERROTA_ENERGIA"

def adicionar_log_multilinha(texto, limite_caracteres=55):
    palavras = texto.split(" ")
    linha_atual = ""
    for palavra in palavras:
        if len(linha_atual) + len(palavra) + 1 <= limite_caracteres:
            linha_atual += (palavra + " ")
        else:
            log_mensagens.append(linha_atual.strip())
            linha_atual = palavra + " "
    if linha_atual:
        log_mensagens.append(linha_atual.strip())

def processar_comando(comando_str):
    partes = comando_str.strip().split(maxsplit=1)
    if not partes:
        return

    cmd = partes[0].upper()
    arg = partes[1] if len(partes) > 1 else ""

    if dados.get("final_jogo"):
        return

    # --- GERADOR ---
    if cmd == "GERADOR":
        if dados["gerador_passo"] == 0:
            dados["gerador_passo"] = 1
            log_mensagens.append("=== INICIANDO SEQUÊNCIA DE REPARTIDA DO GERADOR ===")
            log_mensagens.append("PASSO 1: Digite 'GERADOR PARTIDA' para injetar combustível.")
        elif dados["gerador_passo"] == 1 and arg.upper() == "PARTIDA":
            dados["gerador_passo"] = 2
            log_mensagens.append("PASSO 1 CONCLUÍDO. Pressão subindo...")
            log_mensagens.append("PASSO 2: Digite 'GERADOR PRESSAO' para estabilizar turbinas.")
        elif dados["gerador_passo"] == 2 and arg.upper() == "PRESSAO":
            dados["gerador_passo"] = 0
            dados["energia"] = min(100, dados["energia"] + 50)
            log_mensagens.append("[SUCESSO] GERADOR REINICIADO COM ÊXITO!")
            log_mensagens.append(f"[ENERGIA RECARREGADA] Nível atual: {dados['energia']}%")
            registrar_acao()
        else:
            log_mensagens.append("[FALHA NO GERADOR] Sequência incorreta! O gerador travou.")
            dados["gerador_passo"] = 0
            consumir_energia(5)

    # --- SINTONIZAR ---
    elif cmd == "SINTONIZAR":
        try:
            freq = float(arg)
            dados["frequencia_atual"] = freq
            consumir_energia(3)
            tocar_estatica_radio()
            log_mensagens.append(f"[RÁDIO] Sintonizado em {freq:.1f} MHz.")
            
            achou = False
            for arq, info in dados["arquivos_encriptados"].items():
                if abs(freq - info["freq"]) < 0.2:
                    log_mensagens.append(f"[SINAL DETECTADO] Arquivo '{arq}' capturado!")
                    tocar_bip_morse()
                    if arq not in dados["arquivos_desbloqueados"]:
                        dados["arquivos_desbloqueados"].append(arq)
                    achou = True
            if not achou:
                log_mensagens.append("[RÁDIO] * Estática e ruído de fundo *")
            registrar_acao()
        except ValueError:
            log_mensagens.append("[ERRO] Digite uma frequência válida. Ex: SINTONIZAR 94.5")

    # --- ARQUIVOS ---
    elif cmd == "ARQUIVOS":
        consumir_energia(1)
        log_mensagens.append("--- ARQUIVOS NO DISCO ---")
        for arq in dados["arquivos_desbloqueados"]:
            status = "[ENC]" if arq.endswith(".ENC") else "[TXT]"
            log_mensagens.append(f"- {arq} {status}")
        registrar_acao()

    # --- LER ---
    elif cmd == "LER":
        consumir_energia(2)
        arg = arg.upper()
        if arg in dados["arquivos_desbloqueados"]:
            if arg.endswith(".ENC"):
                log_mensagens.append(f"[ERRO] Arquivo '{arg}' está encriptado. Use DECODE.")
            else:
                log_mensagens.append(f"=== {arg} ===")
                conteudo = dados["conteudo_arquivos"].get(arg, "Arquivo vazio.")
                adicionar_log_multilinha(conteudo)
                registrar_acao()
        else:
            log_mensagens.append(f"[ERRO] Arquivo '{arg}' não encontrado.")

    # --- DECODE ---
    elif cmd == "DECODE":
        consumir_energia(8)
        arg = arg.upper()
        if arg in dados["arquivos_desbloqueados"] and arg.endswith(".ENC"):
            info = dados["arquivos_encriptados"][arg]
            arq_descript = info["conteudo"]
            tocar_bip_morse()
            log_mensagens.append(f"[SUCESSO] {arg} descriptografado como '{arq_descript}'!")
            dados["arquivos_desbloqueados"].remove(arg)
            dados["arquivos_desbloqueados"].append(arq_descript)
            registrar_acao()
        else:
            log_mensagens.append(f"[ERRO] Não foi possível descriptografar '{arg}'.")

    # --- FINAIS DO JOGO (DIA 5) ---
    elif cmd == "TRANSMITIR":
        if dados["dia"] == 5:
            dados["final_jogo"] = "VITORIA_TRANSMITIR"
        else:
            log_mensagens.append("[ERRO] Canal mestre de transmissão bloqueado até o Dia 5.")

    elif cmd == "ISOLAR":
        if dados["dia"] == 5:
            dados["final_jogo"] = "VITORIA_ISOLAR"
        else:
            log_mensagens.append("[ERRO] Protocolo de purga indisponível.")

    # --- AJUDA & LIMPAR ---
    elif cmd == "AJUDA":
        log_mensagens.append("=== LISTA DE COMANDOS DO TERMINAL ===")
        log_mensagens.append(" SINTONIZAR [freq] - Sintoniza em uma frequência (Ex: 94.5)")
        log_mensagens.append(" ARQUIVOS         - Lista os arquivos salvos no disco")
        log_mensagens.append(" LER [arquivo]    - Lê o conteúdo de um arquivo TXT")
        log_mensagens.append(" DECODE [arquivo] - Descriptografa arquivos .ENC")
        log_mensagens.append(" GERADOR          - Inicia sequência de recarga de energia")
        log_mensagens.append(" LIMPAR           - Limpa as mensagens da tela")
        if dados["dia"] == 5:
            log_mensagens.append(" TRANSMITIR       - Retransmite a anomalia para a rede")
            log_mensagens.append(" ISOLAR           - Queima os circuitos do terminal")

    elif cmd == "LIMPAR":
        log_mensagens.clear()

    else:
        log_mensagens.append(f"[ERRO] Comando '{cmd}' inválido. Digite AJUDA.")