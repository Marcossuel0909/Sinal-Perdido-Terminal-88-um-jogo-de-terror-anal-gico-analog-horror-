# narrativa.py
from estado import dados, log_mensagens
from audio import tocar_bip_morse

EVENTOS_DIAS = {
    1: {
        "mensagem_inicio": "=== DIA 1: INÍCIO DO TURNO ===",
        "novos_arquivos": {
            "SINAL_DELTA.ENC": {"freq": 94.5, "conteudo": "REGISTRO_ESTACAO_DELTA.TXT"}
        },
        "textos": {
            "REGISTRO_ESTACAO_DELTA.TXT": "12/11/1988 - [ESTAÇÃO DELTA] Perfuração atingiu 1200m. Captamos um zumbido estranho..."
        }
    },
    2: {
        "mensagem_inicio": "=== DIA 2: INTERFERÊNCIA NA REDE ===",
        "novos_arquivos": {
            "AMPLITUDE_88.ENC": {"freq": 101.2, "conteudo": "RELATORIO_TECNICO.TXT"}
        },
        "textos": {
            "RELATORIO_TECNICO.TXT": "13/11/1988 - Os transmissores estão ligados sem operador. Algo fala de dentro da mina."
        }
    },
    3: {
        "mensagem_inicio": "=== DIA 3: ESTRANHAMENTO SONORO ===",
        "novos_arquivos": {
            "ANOMALIA_VOZ.ENC": {"freq": 105.8, "conteudo": "AUDIO_REGISTRO.TXT"}
        },
        "textos": {
            "AUDIO_REGISTRO.TXT": "14/11/1988 - A frequência responde ao microfone. Não sintonize em 108.0 MHz."
        }
    },
    4: {
        "mensagem_inicio": "=== DIA 4: INVASÃO DO SISTEMA ===",
        "novos_arquivos": {
            "SINAL_PROIBIDO.ENC": {"freq": 108.0, "conteudo": "ENTIDADE.TXT"}
        },
        "textos": {
            "ENTIDADE.TXT": "EU POSSO TE OUVIR. O TERMINAL É MEU TRANSPORTE. TRANSMITA O SINAL."
        }
    },
    5: {
        "mensagem_inicio": "=== DIA 5: DECISÃO CRÍTICA ===",
        "novos_arquivos": {},
        "textos": {}
    }
}

def checar_avanco_dia():
    """Avança o dia conforme ações são realizadas e carrega a história."""
    if dados.get("acoes_no_dia", 0) >= 6:
        dados["acoes_no_dia"] = 0
        if dados["dia"] < 5:
            dados["dia"] += 1
            tocar_bip_morse()
            
            dia_atual = dados["dia"]
            evento = EVENTOS_DIAS.get(dia_atual, {})
            
            log_mensagens.append("")
            log_mensagens.append(evento.get("mensagem_inicio", f"=== DIA {dia_atual} ==="))
            
            for arq, info in evento.get("novos_arquivos", {}).items():
                dados["arquivos_encriptados"][arq] = info
                
            for arq_nome, conteudo in evento.get("textos", {}).items():
                dados["conteudo_arquivos"][arq_nome] = conteudo
                
            if dia_atual == 5:
                log_mensagens.append("[SISTEMA] SINAL MESTRE LIBERADO!")
                log_mensagens.append("Escolha o destino da estação:")
                log_mensagens.append(" -> Digite 'TRANSMITIR' para propagar o sinal.")
                log_mensagens.append(" -> Digite 'ISOLAR' para purgar o sistema e conter a anomalia.")