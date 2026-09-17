import pygame
import sys
import random
from estado import dados, log_mensagens
from comandos import processar_comando
from audio import tocar_clique_tecla

# --- INICIALIZAÇÃO DO PYGAME ---
pygame.init()
pygame.font.init()

LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SINAL PERDIDO: TERMINAL 88")

SUPERFICIE_JOGO = pygame.Surface((LARGURA, ALTURA))

# --- CORES E FONTE ---
COR_FUNDO = (13, 17, 23)
COR_VERDE = (0, 255, 102)
COR_AMARELO = (255, 170, 0)
COR_VERMELHO = (255, 60, 60)
FONTE = pygame.font.SysFont("Courier New", 18, bold=True)
FONTE_GRANDE = pygame.font.SysFont("Courier New", 28, bold=True)

# Scanlines
SURFACE_SCANLINES = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
for y in range(0, ALTURA, 3):
    pygame.draw.line(SURFACE_SCANLINES, (0, 0, 0, 80), (0, y), (LARGURA, y), 1)

texto_input = ""
clock = pygame.time.Clock()
rodando = True

def aplicar_efeito_crt(superficie_origem):
    superficie_final = superficie_origem.copy()
    energia_critica = dados["energia"] < 20
    sinal_anomalia = abs(dados["frequencia_atual"] - 108.0) < 0.2

    if (energia_critica or sinal_anomalia) and random.random() < 0.25:
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-2, 2)
        superficie_final.blit(superficie_origem, (offset_x, offset_y))

    superficie_final.blit(SURFACE_SCANLINES, (0, 0))
    pygame.draw.rect(superficie_final, (5, 5, 5), (0, 0, LARGURA, ALTURA), 10)
    return superficie_final

def desenhar_tela_final(tipo_final):
    SUPERFICIE_JOGO.fill((5, 5, 5))
    if tipo_final == "DERROTA_ENERGIA":
        t1 = FONTE_GRANDE.render("SISTEMA DESLIGADO", True, COR_VERMELHO)
        t2 = FONTE.render("A energia acabou. Algo se aproxima no escuro...", True, COR_VERMELHO)
    elif tipo_final == "VITORIA_TRANSMITIR":
        t1 = FONTE_GRANDE.render("SINAL TRANSMITIDO", True, COR_AMARELO)
        t2 = FONTE.render("A anomalia se espalhou por toda a rede nacional.", True, COR_VERDE)
    elif tipo_final == "VITORIA_ISOLAR":
        t1 = FONTE_GRANDE.render("ESTAÇÃO PURGADA", True, COR_VERDE)
        t2 = FONTE.render("Você destruiu o terminal. A anomalia foi contida.", True, COR_VERDE)
    
    t3 = FONTE.render("Pressione ESC para fechar.", True, (150, 150, 150))

    SUPERFICIE_JOGO.blit(t1, (LARGURA // 2 - t1.get_width() // 2, 200))
    SUPERFICIE_JOGO.blit(t2, (LARGURA // 2 - t2.get_width() // 2, 280))
    SUPERFICIE_JOGO.blit(t3, (LARGURA // 2 - t3.get_width() // 2, 400))

# --- LOOP PRINCIPAL DO JOGO ---
while rodando:
    SUPERFICIE_JOGO.fill(COR_FUNDO)

    tipo_final = dados.get("final_jogo")

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
            if not tipo_final:
                if evento.key == pygame.K_RETURN:
                    if texto_input.strip():
                        log_mensagens.append(f"> {texto_input}")
                        processar_comando(texto_input)
                        texto_input = ""
                elif evento.key == pygame.K_BACKSPACE:
                    texto_input = texto_input[:-1]
                    tocar_clique_tecla()
                else:
                    if len(texto_input) < 40 and evento.unicode.isprintable():
                        texto_input += evento.unicode
                        tocar_clique_tecla()

    if tipo_final:
        desenhar_tela_final(tipo_final)
    else:
        # --- DESENHAR CABEÇALHO ---
        cor_status_energia = COR_VERDE
        if dados['energia'] < 20:
            cor_status_energia = COR_VERMELHO
        elif dados['energia'] < 50:
            cor_status_energia = COR_AMARELO

        topo_txt = f"DIA: {dados['dia']} | ENERGIA: {dados['energia']}% | FREQ: {dados['frequencia_atual']:.1f} MHz"
        surf_topo = FONTE.render(topo_txt, True, cor_status_energia)
        SUPERFICIE_JOGO.blit(surf_topo, (20, 20))
        pygame.draw.line(SUPERFICIE_JOGO, COR_VERDE, (20, 45), (780, 45), 2)

        # --- DESENHAR CONSOLE DE MENSAGENS ---
        y_pos = 60
        for msg in log_mensagens[-20:]:
            surf_msg = FONTE.render(msg, True, COR_VERDE)
            SUPERFICIE_JOGO.blit(surf_msg, (20, y_pos))
            y_pos += 22

        # --- DESENHAR LINHA DE COMANDO ---
        pygame.draw.line(SUPERFICIE_JOGO, COR_VERDE, (20, 540), (780, 540), 1)
        prompt_surf = FONTE.render(f"TERMINAL_88> {texto_input}_", True, COR_VERDE)
        SUPERFICIE_JOGO.blit(prompt_surf, (20, 555))

    # --- APLICAR FILTRO CRT E RENDERIZAR NA TELA ---
    tela_processada = aplicar_efeito_crt(SUPERFICIE_JOGO)
    TELA.blit(tela_processada, (0, 0))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()