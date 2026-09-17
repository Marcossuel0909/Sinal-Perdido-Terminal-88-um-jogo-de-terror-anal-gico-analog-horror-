# estado.py
dados = {
    "dia": 1,
    "frequencia_atual": 88.0,
    "energia": 40,
    "gerador_passo": 0,
    "arquivos_desbloqueados": ["REGISTRO_01.TXT"],
    "arquivos_encriptados": {
        "SINAL_DELTA.ENC": {"freq": 94.5, "conteudo": "REGISTRO_ESTACAO_DELTA.TXT"}
    },
    "conteudo_arquivos": {
        "REGISTRO_01.TXT": "10/11/1988 - Chegada a Estacao Norte. O frio e intenso, mas o terminal funciona.",
        "REGISTRO_ESTACAO_DELTA.TXT": "12/11/1988 - [ESTACAO DELTA] Perfuracao atingiu 1200m. Captamos um zumbido estranho..."
    }
}

log_mensagens = [
    "SISTEMA TERMINAL 88 INICIALIZADO...",
    "ALERTA: Nivel de energia instavel. Use GERADOR para manutencao.",
    "DIGITE 'AJUDA' PARA VER OS COMANDOS DISPONIVEIS."
]