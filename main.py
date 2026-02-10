#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jogo de Caça-Palavras no Terminal
Interface visual aprimorada com arte ASCII e cores!
Sistema de 3 níveis progressivos com tema de Computação
ESQUEMA DE CORES: FOGO/ENERGIA (Vermelho/Laranja)
"""

import random
import os
import sys
import time

class CacaPalavras:
    def __init__(self, tamanho=12):
        self.tamanho = tamanho
        self.grid = [[' ' for _ in range(tamanho)] for _ in range(tamanho)]
        self.palavras = []
        self.palavras_encontradas = set()
        self.posicoes_palavras = {}
        self.marcacoes = set()
        self.nivel = 1
        
        # Palavras organizadas por nível de dificuldade (tema: Computação)
        self.palavras_por_nivel = {
            1: {  # Nível Iniciante - Palavras simples
                'tamanho': 10,
                'palavras': ['MOUSE', 'TELA', 'TECLADO', 'PASTA', 'ARQUIVO', 
                           'REDE', 'WIFI', 'DISCO', 'MEMORIA', 'SISTEMA']
            },
            2: {  # Nível Intermediário - Palavras médias
                'tamanho': 12,
                'palavras': ['INTERNET', 'PROGRAMA', 'WINDOWS', 'BACKUP', 'SERVIDOR',
                           'FIREWALL', 'ANTIVIRUS', 'NAVEGADOR', 'EMAIL', 'DOWNLOAD']
            },
            3: {  # Nível Avançado - Palavras mais complexas
                'tamanho': 14,
                'palavras': ['PROCESSADOR', 'APLICATIVO', 'SOFTWARE', 'HARDWARE', 'SEGURANCA',
                           'IMPRESSORA', 'COMPUTADOR', 'BLUETOOTH', 'PENDRIVE', 'NOTEBOOK']
            }
        }
        
        # Cores ANSI - ESQUEMA FOGO/ENERGIA (Vermelho/Laranja)
        self.RESET = '\033[0m'
        self.BOLD = '\033[1m'
        self.GREEN = '\033[38;5;208m'  # Laranja para sucesso
        self.YELLOW = '\033[38;5;220m'  # Amarelo-laranja
        self.RED = '\033[91m'  # Vermelho vibrante
        self.CYAN = '\033[38;5;202m'  # Laranja-avermelhado
        self.MAGENTA = '\033[38;5;196m'  # Vermelho intenso
        self.BLUE = '\033[38;5;166m'  # Laranja escuro
        self.WHITE = '\033[38;5;255m'  # Branco brilhante
        self.BG_BLUE = '\033[48;5;88m'  # Fundo vermelho escuro
        self.BG_GREEN = '\033[48;5;208m'  # Fundo laranja para palavras encontradas
        self.BG_YELLOW = '\033[48;5;166m'  # Fundo laranja escuro
        
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def reiniciar_jogo(self, nivel):
        """Reinicia o jogo com um novo nível"""
        self.nivel = nivel
        
        # Atualiza tamanho do grid baseado no nível
        config_nivel = self.palavras_por_nivel.get(nivel, self.palavras_por_nivel[3])
        self.tamanho = config_nivel['tamanho']
        
        # Reinicia o grid
        self.grid = [[' ' for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.palavras = []
        self.palavras_encontradas = set()
        self.posicoes_palavras = {}
        self.marcacoes = set()
        
        # Define novas palavras
        self.definir_palavras(config_nivel['palavras'])
    
    def get_nome_nivel(self):
        """Retorna o nome do nível atual"""
        nomes = {
            1: "INICIANTE",
            2: "INTERMEDIÁRIO",
            3: "AVANÇADO"
        }
        return nomes.get(self.nivel, "DESCONHECIDO")
    
    def banner_titulo(self):
        """Exibe um banner ASCII art bonito"""
        banner = f"""
{self.RED}{self.BOLD}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║  ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███╗ ║
    ║  ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║████║║
    ║  ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║██╔═╝║
    ║  ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██║  ║
    ║  ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███╗ ║
    ║   ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══╝ ║
    ║                                                               ║
    ║                    🔥  T O   T H E   G A M E  🔥             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
{self.RESET}"""
        print(banner)
        
        # Exibe nível atual
        nivel_cor = self.YELLOW if self.nivel == 1 else self.CYAN if self.nivel == 2 else self.MAGENTA
        print(f"\n    {nivel_cor}{self.BOLD}╔════════════════════════════════════════╗{self.RESET}")
        print(f"    {nivel_cor}{self.BOLD}║     NÍVEL {self.nivel}: {self.get_nome_nivel():<24} ║{self.RESET}")
        print(f"    {nivel_cor}{self.BOLD}║     Tema: COMPUTAÇÃO                   ║{self.RESET}")
        print(f"    {nivel_cor}{self.BOLD}╚════════════════════════════════════════╝{self.RESET}")
    
    def banner_vitoria(self):
        """Banner de vitória"""
        banner = f"""
{self.GREEN}{self.BOLD}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██╗   ██╗ ██████╗  ██████╗███████╗    ██╗   ██╗███████╗    ║
    ║   ██║   ██║██╔═══██╗██╔════╝██╔════╝    ██║   ██║██╔════╝    ║
    ║   ██║   ██║██║   ██║██║     █████╗      ██║   ██║█████╗      ║
    ║   ╚██╗ ██╔╝██║   ██║██║     ██╔══╝      ╚██╗ ██╔╝██╔══╝      ║
    ║    ╚████╔╝ ╚██████╔╝╚██████╗███████╗     ╚████╔╝ ███████╗    ║
    ║     ╚═══╝   ╚═════╝  ╚═════╝╚══════╝      ╚═══╝  ╚══════╝    ║
    ║                                                               ║
    ║                  🔥  V E N C E U !  🔥                       ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
{self.RESET}"""
        return banner
    
    def barra_progresso(self):
        """Cria uma barra de progresso visual"""
        total = len(self.palavras)
        encontradas = len(self.palavras_encontradas)
        percentual = (encontradas / total) * 100
        
        # Barra de 40 caracteres
        blocos_cheios = int((encontradas / total) * 40)
        blocos_vazios = 40 - blocos_cheios
        
        barra = f"{self.GREEN}█{self.RESET}" * blocos_cheios + f"{self.YELLOW}░{self.RESET}" * blocos_vazios
        
        return f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║  {self.BOLD}PROGRESSO{self.RESET}  [{barra}] {percentual:.0f}%        ║
    ║  {self.CYAN}Encontradas: {self.BOLD}{encontradas}{self.RESET}{self.CYAN}/{total}{self.RESET}                                          ║
    ╚═══════════════════════════════════════════════════════════════╝
"""
    
    def definir_palavras(self, palavras):
        """Define as palavras a serem escondidas"""
        self.palavras = [p.upper() for p in palavras]
        
    def pode_colocar_palavra(self, palavra, linha, coluna, direcao):
        """Verifica se pode colocar uma palavra na posição e direção especificadas"""
        direcoes = {
            'H': (0, 1),
            'V': (1, 0),
            'D': (1, 1),
            'A': (-1, 1),
        }
        
        if direcao not in direcoes:
            return False
        
        dx, dy = direcoes[direcao]
        tam = len(palavra)
        
        linha_final = linha + dx * (tam - 1)
        coluna_final = coluna + dy * (tam - 1)
        
        if linha_final < 0 or linha_final >= self.tamanho:
            return False
        if coluna_final < 0 or coluna_final >= self.tamanho:
            return False
        
        for i in range(tam):
            l = linha + dx * i
            c = coluna + dy * i
            if self.grid[l][c] != ' ' and self.grid[l][c] != palavra[i]:
                return False
        
        return True
    
    def colocar_palavra(self, palavra, linha, coluna, direcao):
        """Coloca uma palavra no grid"""
        direcoes = {
            'H': (0, 1),
            'V': (1, 0),
            'D': (1, 1),
            'A': (-1, 1),
        }
        
        dx, dy = direcoes[direcao]
        posicoes = []
        
        for i, letra in enumerate(palavra):
            l = linha + dx * i
            c = coluna + dy * i
            self.grid[l][c] = letra
            posicoes.append((l, c))
        
        self.posicoes_palavras[palavra] = posicoes
    
    def preencher_grid(self):
        """Preenche espaços vazios com letras aleatórias"""
        letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.grid[i][j] == ' ':
                    self.grid[i][j] = random.choice(letras)
    
    def gerar_caca_palavras(self):
        """Gera o caça-palavras colocando todas as palavras"""
        direcoes = ['H', 'V', 'D', 'A']
        palavras_nao_inseridas = []
        
        for palavra in self.palavras:
            colocada = False
            tentativas = 0
            max_tentativas = 100
            
            while not colocada and tentativas < max_tentativas:
                linha = random.randint(0, self.tamanho - 1)
                coluna = random.randint(0, self.tamanho - 1)
                direcao = random.choice(direcoes)
                
                if self.pode_colocar_palavra(palavra, linha, coluna, direcao):
                    self.colocar_palavra(palavra, linha, coluna, direcao)
                    colocada = True
                
                tentativas += 1
            
            # Se não conseguiu colocar a palavra, adiciona à lista de não inseridas
            if not colocada:
                palavras_nao_inseridas.append(palavra)
        
        # Remove palavras que não foram inseridas da lista de palavras do jogo
        for palavra in palavras_nao_inseridas:
            self.palavras.remove(palavra)
    
        self.preencher_grid()
    
    def exibir_grid(self):
        """Exibe o grid com design moderno"""
        print(f"\n{self.RED}{self.BOLD}    ╔═══════════════ TABULEIRO ═══════════════╗{self.RESET}\n")
        
        # Cabeçalho com números das colunas
        print(f"    {self.YELLOW}    ", end="")
        for i in range(self.tamanho):
            print(f" {i:2}", end="")
        print(f"{self.RESET}")
        
        print(f"    {self.RED}    ╔{'═══' * self.tamanho}═╗{self.RESET}")
        
        # Linhas do grid
        for i in range(self.tamanho):
            print(f"    {self.YELLOW} {i:2} {self.RED}║{self.RESET}", end="")
            for j in range(self.tamanho):
                letra = self.grid[i][j]
                
                # Destaca letras encontradas
                if (i, j) in self.marcacoes:
                    print(f"{self.BG_GREEN}{self.BOLD}{self.WHITE} {letra} {self.RESET}", end="")
                else:
                    print(f" {self.WHITE}{letra}{self.RESET} ", end="")
            print(f"{self.RED}║{self.RESET}")
        
        print(f"    {self.RED}    ╚{'═══' * self.tamanho}═╝{self.RESET}")
    
    def exibir_palavras(self):
        """Exibe a lista de palavras com design bonito"""
        print(f"\n{self.MAGENTA}{self.BOLD}    ╔═════════════ PALAVRAS PARA ENCONTRAR ═════════════╗{self.RESET}")
        
        # Calcula quantas colunas cabem
        colunas = 3
        palavras_por_linha = len(self.palavras) // colunas + (1 if len(self.palavras) % colunas else 0)
        
        for i in range(palavras_por_linha):
            linha = "    "
            for j in range(colunas):
                idx = i + j * palavras_por_linha
                if idx < len(self.palavras):
                    palavra = self.palavras[idx]
                    if palavra in self.palavras_encontradas:
                        linha += f"{self.GREEN}✓ {palavra:<12}{self.RESET} "
                    else:
                        linha += f"{self.WHITE}□ {palavra:<12}{self.RESET} "
            print(linha)
        
        print(f"{self.MAGENTA}{self.BOLD}    ╚════════════════════════════════════════════════════╝{self.RESET}")
    
    def obter_coordenada(self, mensagem, cor=None):
        """Obtém uma coordenada do usuário"""
        if cor is None:
            cor = self.CYAN
        while True:
            try:
                entrada = input(f"    {cor}{self.BOLD}➤ {mensagem}{self.RESET}").strip()
                
                if entrada.lower() == 'sair':
                    return None
                
                if ',' in entrada:
                    partes = entrada.split(',')
                else:
                    partes = entrada.split()
                
                if len(partes) != 2:
                    print(f"    {self.RED}✗ Formato inválido! Use: linha,coluna (ex: 3,5){self.RESET}")
                    continue
                
                linha = int(partes[0].strip())
                coluna = int(partes[1].strip())
                
                if 0 <= linha < self.tamanho and 0 <= coluna < self.tamanho:
                    return (linha, coluna)
                else:
                    print(f"    {self.RED}✗ Coordenadas fora do grid! Use valores de 0 a {self.tamanho-1}{self.RESET}")
            except ValueError:
                print(f"    {self.RED}✗ Digite números válidos!{self.RESET}")
            except KeyboardInterrupt:
                return None
    
    def extrair_palavra_entre_coordenadas(self, coord_inicial, coord_final):
        """Extrai a palavra entre duas coordenadas"""
        l1, c1 = coord_inicial
        l2, c2 = coord_final
        
        dl = l2 - l1
        dc = c2 - c1
        
        if dl == 0 and dc == 0:
            return None, []
        
        passos = max(abs(dl), abs(dc))
        
        if dl != 0 and dc != 0 and abs(dl) != abs(dc):
            return None, []
        
        step_l = 0 if dl == 0 else dl // abs(dl)
        step_c = 0 if dc == 0 else dc // abs(dc)
        
        palavra = ""
        posicoes = []
        l, c = l1, c1
        
        for _ in range(passos + 1):
            if 0 <= l < self.tamanho and 0 <= c < self.tamanho:
                palavra += self.grid[l][c]
                posicoes.append((l, c))
                l += step_l
                c += step_c
            else:
                return None, []
        
        return palavra, posicoes
    
    def verificar_selecao(self, coord_inicial, coord_final):
        """Verifica se a seleção corresponde a uma palavra"""
        palavra, posicoes = self.extrair_palavra_entre_coordenadas(coord_inicial, coord_final)
        
        if palavra is None:
            return "INVALIDA", None, []
        
        # Verifica apenas palavras na direção correta (sem reverso)
        if palavra in self.palavras:
            if palavra in self.palavras_encontradas:
                return "JÁ_ENCONTRADA", palavra, posicoes
            else:
                self.palavras_encontradas.add(palavra)
                self.marcacoes.update(posicoes)
                return "CORRETA", palavra, posicoes
        else:
            return "INCORRETA", palavra, posicoes
    
    def jogo_completo(self):
        """Verifica se todas as palavras foram encontradas"""
        return len(self.palavras_encontradas) == len(self.palavras)
    
    def animacao_carregamento(self):
        """Animação de carregamento"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        print(f"\n    {self.RED}Gerando caça-palavras ", end="", flush=True)
        for _ in range(20):
            for frame in frames:
                print(f"{frame}", end="", flush=True)
                time.sleep(0.05)
                print("\b", end="", flush=True)
        print(f"✓{self.RESET}\n")
    
    def caixa_mensagem(self, titulo, mensagem, cor):
        """Exibe uma mensagem em uma caixa bonita"""
        largura = 60
        print(f"\n    {cor}╔{'═' * largura}╗{self.RESET}")
        print(f"    {cor}║{self.BOLD}{titulo.center(largura)}{self.RESET}{cor}║{self.RESET}")
        print(f"    {cor}╠{'═' * largura}╣{self.RESET}")
        print(f"    {cor}║  {mensagem:<{largura-2}}║{self.RESET}")
        print(f"    {cor}╚{'═' * largura}╝{self.RESET}\n")
    
    def jogar(self):
        """Loop principal do jogo"""
        self.limpar_tela()
        self.banner_titulo()
        self.animacao_carregamento()
        self.gerar_caca_palavras()
        
        input(f"    {self.YELLOW}Pressione ENTER para começar...{self.RESET}")
        
        while not self.jogo_completo():
            self.limpar_tela()
            self.banner_titulo()
            print(self.barra_progresso())
            self.exibir_grid()
            self.exibir_palavras()
            
            print(f"\n{self.CYAN}{self.BOLD}    ╔════════════════ INSTRUÇÕES ════════════════╗{self.RESET}")
            print(f"    {self.CYAN}║{self.RESET}  📍 Digite coordenadas: {self.YELLOW}linha,coluna{self.RESET}    {self.CYAN}║{self.RESET}")
            print(f"    {self.CYAN}║{self.RESET}  💡 Exemplo: {self.YELLOW}3,5{self.RESET} ou {self.YELLOW}3 5{self.RESET}             {self.CYAN}║{self.RESET}")
            print(f"    {self.CYAN}║{self.RESET}  🚪 Digite {self.RED}'sair'{self.RESET} para desistir          {self.CYAN}║{self.RESET}")
            print(f"    {self.CYAN}╚════════════════════════════════════════════╝{self.RESET}\n")
            
            coord_inicial = self.obter_coordenada("Coordenada INICIAL: ")
            
            if coord_inicial is None:
                self.caixa_mensagem("GAME OVER", "Você desistiu do jogo!", self.RED)
                faltantes = set(self.palavras) - self.palavras_encontradas
                print(f"    {self.YELLOW}Palavras que faltavam:{self.RESET}")
                for palavra in faltantes:
                    print(f"      {self.RED}• {palavra}{self.RESET}")
                print()
                return False  # Retorna False quando desistiu
            
            coord_final = self.obter_coordenada("Coordenada FINAL: ")
            
            if coord_final is None:
                self.caixa_mensagem("GAME OVER", "Você desistiu do jogo!", self.RED)
                faltantes = set(self.palavras) - self.palavras_encontradas
                print(f"    {self.YELLOW}Palavras que faltavam:{self.RESET}")
                for palavra in faltantes:
                    print(f"      {self.RED}• {palavra}{self.RESET}")
                print()
                return False  # Retorna False quando desistiu
            
            resultado, palavra, posicoes = self.verificar_selecao(coord_inicial, coord_final)
            
            if resultado == "CORRETA":
                self.caixa_mensagem("✓ CORRETO!", f"Você encontrou: {palavra}", self.GREEN)
                input(f"    {self.WHITE}Pressione ENTER para continuar...{self.RESET}")
            elif resultado == "JÁ_ENCONTRADA":
                self.caixa_mensagem("⚠ ATENÇÃO", f"Você já encontrou: {palavra}", self.YELLOW)
                input(f"    {self.WHITE}Pressione ENTER para continuar...{self.RESET}")
            elif resultado == "INVALIDA":
                self.caixa_mensagem("✗ ERRO", "Seleção inválida! Use uma linha reta.", self.RED)
                input(f"    {self.WHITE}Pressione ENTER para continuar...{self.RESET}")
            else:
                self.caixa_mensagem("✗ INCORRETO", f"'{palavra}' não está na lista!", self.RED)
                input(f"    {self.WHITE}Pressione ENTER para continuar...{self.RESET}")
        
        if self.jogo_completo():
            self.limpar_tela()
            print(self.banner_vitoria())
            print(self.barra_progresso())
            self.exibir_grid()
            print(f"\n    {self.GREEN}{self.BOLD}🔥 Parabéns! Você completou o NÍVEL {self.nivel}! 🔥{self.RESET}\n")
            return True  # Retorna True quando completou o nível


def main():
    """Função principal"""
    jogo = CacaPalavras()
    nivel_atual = 1
    
    continuar = True
    
    while continuar and nivel_atual <= 3:
        # Reinicia o jogo com o nível atual
        jogo.reiniciar_jogo(nivel_atual)
        
        # Joga o nível
        completou = jogo.jogar()
        
        if not completou:
            # Jogador desistiu
            continuar = False
        else:
            # Completou o nível - pergunta se quer continuar
            if nivel_atual < 3:
                # Obtém o nome do próximo nível
                proximo_nivel = nivel_atual + 1
                nomes_niveis = {1: "INICIANTE", 2: "INTERMEDIÁRIO", 3: "AVANÇADO"}
                nome_proximo = nomes_niveis.get(proximo_nivel, "")
                
                print(f"\n{jogo.YELLOW}{jogo.BOLD}    ╔════════════════════════════════════════════╗{jogo.RESET}")
                print(f"    {jogo.YELLOW}{jogo.BOLD}║     Deseja ir para o próximo nível?        ║{jogo.RESET}")
                print(f"    {jogo.YELLOW}{jogo.BOLD}║     Nível {proximo_nivel}: {nome_proximo:<24} ║{jogo.RESET}")
                print(f"    {jogo.YELLOW}{jogo.BOLD}╚════════════════════════════════════════════╝{jogo.RESET}\n")
                
                resposta = input(f"    {jogo.CYAN}Digite 'sim' para continuar ou 'nao' para sair: {jogo.RESET}").strip().lower()
                
                if resposta in ['sim', 's', 'yes', 'y']:
                    nivel_atual += 1
                    print(f"\n    {jogo.GREEN}🔥 Avançando para o nível {nivel_atual}!{jogo.RESET}")
                    time.sleep(2)
                else:
                    continuar = False
                    print(f"\n    {jogo.RED}Você completou {nivel_atual} nível(is)! Parabéns! 🔥{jogo.RESET}\n")
            else:
                # Completou todos os níveis
                jogo.limpar_tela()
                print(f"""
{jogo.MAGENTA}{jogo.BOLD}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        ██████╗ ███╗   ███╗ █████╗ ███████╗████████╗███████╗ ║
    ║        ██╔══██╗████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝ ║
    ║        ██████╔╝██╔████╔██║███████║███████╗   ██║   █████╗   ║
    ║        ██╔══██╗██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝   ║
    ║        ██║  ██║██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗ ║
    ║        ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝ ║
    ║                                                               ║
    ║            🔥  VOCÊ É UM MESTRE EM COMPUTAÇÃO! 🔥            ║
    ║              Completou todos os 3 níveis!                     ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
{jogo.RESET}
                """)
                continuar = False
    
    print(f"    {jogo.RED}Obrigado por jogar! 🔥{jogo.RESET}\n")


if __name__ == "__main__":
    main()