Markdown
# 📻 Sinal Perdido: Terminal 88

> *"Estação Delta — Perfuração atingiu 1200m. Captamos um zumbido estranho..."*

**Sinal Perdido: Terminal 88** é um jogo de terror analógico (*analog horror*) e simulação de terminal retrô desenvolvido em **Python** com **Pygame**. 

O jogador assume o papel de um operador de monitoramento dos anos 80 encarregado de rastrear frequências de rádio e descriptografar arquivos da misteriosa Estação Delta, enquanto lida com o consumo crítico de energia do terminal e interferências anômalas no sinal.

---

## 📸 Capturas e Efeitos Visuais

- **Interface CRT Retrô:** Simulação de monitor de tubo com *scanlines* e bordas curvas.
- **Glitch & Jitter Dinâmico:** Distorção visual de tela quando a energia está crítica ou ao sintonizar na frequência da anomalia (`108.0 MHz`).
- **Síntese de Áudio Procedural:** Sons de teclas, estática de rádio e código Morse gerados via código em tempo real, sem dependência de arquivos `.wav` ou `.mp3` externos.

---

## 🕹️ Como Jogar

### Comandos do Terminal

| Comando | Descrição |
| :--- | :--- |
| `SINTONIZAR [freq]` | Sintoniza o rádio em uma frequência (Ex: `SINTONIZAR 94.5`) |
| `ARQUIVOS` | Lista os arquivos salvos e capturados no disco |
| `LER [arquivo]` | Exibe o conteúdo de relatórios e registros em texto |
| `DECODE [arquivo]` | Descriptografa arquivos `.ENC` capturados nas frequências |
| `GERADOR` | Inicia a rotina manual de recarga de energia do terminal |
| `AJUDA` | Exibe a lista de comandos no console |
| `LIMPAR` | Limpa o histórico de mensagens da tela |

### Mecânicas Principais

1. **Gerenciamento de Energia:** Cada comando executado consome uma porcentagem da energia da instalação. Se a energia chegar a **0%**, o terminal desliga e o jogo termina.
2. **Procedimento do Gerador:** Para recarregar a bateria do terminal, o jogador deve executar a sequência correta:
   - `GERADOR` → `GERADOR PARTIDA` → `GERADOR PRESSAO`
3. **Progressão por Dias:** Executar ações avança o tempo. Cada dia (do Dia 1 ao Dia 5) revela novos registros da história da Estação Delta.
4. **Decisão Final (Dia 5):** No quinto dia, decisões no terminal desbloqueiam diferentes finais para o jogo (`TRANSMITIR` ou `ISOLAR`).

---

## 🏗️ Arquitetura do Projeto

O projeto adota uma estrutura modularizada para separar o gerenciamento de estado, as regras de negócio, a síntese de áudio e a renderização gráfica:

```text
sinal_perdido/
│
├── estado.py       # Estado global (Energia, dia, frequência, logs)
├── narrativa.py    # Eventos narrativos e arquivos liberados por dia
├── audio.py        # Síntese procedural de áudio (Morse, Estática, Clientes)
├── comandos.py     # Parser de comandos e lógica de regras de jogo
└── main.py         # Loop principal do Pygame, entrada do usuário e filtro CRT
🚀 Como Executar
Pré-requisitos
Python 3.8+ instalado na máquina.

Biblioteca Pygame.

Passo a Passo
Clone o repositório:

Bash
git clone [https://github.com/seu-usuario/sinal-perdido-terminal88.git](https://github.com/seu-usuario/sinal-perdido-terminal88.git)
cd sinal-perdido-terminal88
Instale as dependências:

Bash
pip install pygame
Execute o jogo:

Bash
python main.py
🛠️ Tecnologias Utilizadas
Python — Linguagem principal.

Pygame — Renderização gráfica e manipulação da janela.

wave & struct — Módulos nativos do Python para geração sintética de áudio e áudio PCM de 16-bit.
