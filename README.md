# Os Guardiões

## Descrição Geral do Projeto

Os Guardiões é um jogo 2D focado em exploração e sobrevivência ambientado no rico universo do folclore brasileiro. A história se passa em uma floresta protegida há muitos anos por três lendas: Iara, Curupira e Mula-sem-Cabeça, responsáveis por manter o equilíbrio da natureza e afastar aqueles que buscam destruir a mata. No entanto, um caçador ambicioso surge com o objetivo de invadir o local para derrubar as árvores e explorar suas riquezas. 

Para impedir a destruição completa, um jovem protetor da floresta assume a missão de adentrar um perigoso labirinto composto por diversas salas. O grande objetivo do jogador é explorar o mapa e coletar três chaves mágicas necessárias para selar e salvar a floresta antes que o tempo de 3 minutos se esgote. Ao longo da jornada, o personagem precisará superar os obstáculos e os desafios criados pelos próprios guardiões — a Iara tentará hipnotizá-lo para reduzir seu tempo; o Curupira aplicará um efeito de atordoamento que reduz sua velocidade; e a Mula-sem-Cabeça perseguirá o jogador, lançando projéteis de fogo. Superar essas salas concede ao herói itens colecionáveis essenciais, como vidas extras e bônus de tempo.

Este projeto foi desenvolvido como o requisito final para a conclusão da disciplina de Introdução à Programação (2026.1). O software foi integralmente construído utilizando a linguagem Python associada à biblioteca Pygame, pondo em prática conceitos de estruturação lógica e programação modular.

---

## Integrantes da Equipe

* Davi Melo e Luna \<dml\>
* Giovanna Reis da Silva \<grs4\>
* Heitor Condé Freire \<hcf3\>
* Maria Cecília Ribeiro Pereira de Melo \<mcrpm\>
* Maysa Barros Campelo \<mbc6\>

---

## Divisão de Trabalho

| Membro | Responsabilidades |
| :--- | :--- |
| **Davi Melo e Luna** | Desenvolvimento inicial e atualizações do personagem principal, mecânica de projéteis teleguiados e melhorias estruturais no sistema de inventário. |
| **Giovanna Reis da Silva** | Criação das classes dos guardiões Mula-sem-Cabeça (com sistema de perseguição no corredor e tiros de fogo) e Curupira (com mecânica de atordoamento); produção, adaptação e padronização das artes visuais (*sprites*) dos personagens (Curupira, Iara, Caçador e Mula-sem-Cabeça); elaboração do rascunho do mapa, correções no encerramento por vida; implementação lógica das telas de *Game Over* e *Win* com botões alinhados; e organização geral do repositório do projeto. |
| **Heitor Condé Freire** | Desenvolvimento e atualização da mecânica base do personagem e produção dos slides da apresentação. |
| **Maria Cecília R. P. de Melo** | Programação lógica da guardiã Iara (classe de poder, alcance e ajuste de velocidade) e mecânica de alteração de tempo atrelada ao seu ataque; criação e programação lógica do caçador na última sala, incluindo o sistema de tempo de espera (2 segundos) para ativação e perseguição; desenvolvimento do layout estrutural do labirinto e montagem/padronização das salas; além da criação e implementação de sprites e artes visuais para o projeto. |
| **Maysa Barros Campelo** | Implementação lógica e arte dos itens coletáveis (vida extra, tempo e sistema de portas trancadas com 3 chaves mínimas); tratamento dinâmico de caminhos de arquivos via biblioteca `os`; desenvolvimento, agrupamento e atualização do HUD (inventário e contadores); gerenciamento do sistema de tela cheia (F11/Esc) e ajuste no tempo limite do jogo para 3 minutos; criação das artes visuais e design das telas de início (Menu), instruções (Como Jogar), vitória e de todas as telas de derrota; inserção das *sprites* de árvores para a composição visual das paredes do labirinto. |

---

## Arquitetura do Projeto
```
JOGO-IP/
├── .vscode/                      		# Configurações locais do ambiente de desenvolvimento
│   └── settings.json
├── assetes/                      		# Recursos de mídia utilizados no jogo
│   ├── fontes/                   		# Tipografias do sistema
│   │   └── PixelifySans-Regular.ttf
│   └── sprites/                  		# Imagens de personagens, cenários e interfaces
│       ├── caçador.png
│       ├── como_jogar_bg.png
│       ├── coracao.png
│       ├── curupira.png
│       ├── hp_bar.piskel
│       ├── lara.png
│       ├── menu_bg.png
│       ├── mula-sem-cabeca.png
│       ├── relogio.png
│       ├── tela_derrota_caçador.png
│       ├── tela_derrota_tempo.png
│       ├── tela_derrota_vida.png
│       ├── tela_vitória.png
│       ├── tileset_chave.png
│       └── treepacknewwest.png
├── classes/                      		# Módulos contendo a lógica orientada a objetos
│   ├── coletaveis.py             		# Lógica de sensores e itens (vida extra e tempo)
│   ├── config.py                 		# Definições de configurações gerais e cores do jogo
│   ├── guardioes.py              		# Classes de IA e ataques das lendas (Iara, Curupira, Mula)
│   ├── hud.py                    		# Sistema de interface de usuário (inventário e medidores)
│   ├── jogador.py                		# Mecânicas, movimentos e estados do personagem principal
│   └── labirinto.py              		# Geração das salas e gerenciamento do mapa
├── .gitignore                    		# Instruções de exclusão de arquivos para o Git (pycache)
├── jogo.py                       		# Arquivo principal que executa o loop do jogo
└── README.md                     		# Documentação geral do repositório
```
---

## Capturas de Tela

### Tela Inicial e Menu
![Menu Principal](https://lh3.googleusercontent.com/d/1tRKJD3Rk2bUjlJZcbg-hBiCFHklCoKmA)

### Como Jogar
![Instruções de Como Jogar](https://lh3.googleusercontent.com/d/1_py2QMWJAd20ZtnkxCQrmf9dC66N1_YF)

### Labirinto e Gameplay
![Demonstração do Labirinto](https://lh3.googleusercontent.com/d/13j5LsIbsDau-pUA5WN417CLQCCUoV5Lm)

![Demonstração do Labirinto](https://lh3.googleusercontent.com/d/1Az5uJoDgwmyew6Dge124rX1G5vIpMgY9)

![Demonstração do Labirinto](https://lh3.googleusercontent.com/d/1GDYZ6os_QRrJdlw7XxzRXLVaR3LFz45F)

![Demonstração do Labirinto](https://lh3.googleusercontent.com/d/1LPM40IaXGn9h08UWCe27zDbnvD43wB-4)

![Demonstração do Labirinto](https://lh3.googleusercontent.com/d/1iZP2aN0PeMovvsodfv7Xtt4Sobndwtyd)

### Telas de Vitória
![Tela de Vitória](https://lh3.googleusercontent.com/d/1dN30PFas29jZiPHqTQEscyyPQ40s77VJ)

### Telas de Derrota
Aqui o jogador pode encontrar três destinos diferentes dependendo de como perdeu:

* **Derrota por Vida:**
  ![Derrota por Vida](https://lh3.googleusercontent.com/d/19EaIFf89ahbrRHeYTUtAvoDNATdlvWJW)
* **Derrota por Tempo:**
  ![Derrota por Tempo](https://lh3.googleusercontent.com/d/1AAWJeTDDIso4-7eby440X6GpSYD4lQcN)
* **Derrota pelo Caçador:**
  ![Derrota pelo Caçador](https://lh3.googleusercontent.com/d/1tx0qUTpEuQLpN2HHPWljNVjI-lifMT8P)

---

## Ferramentas e Justificativas

* **Python:** Linguagem de programação base escolhida devido ao escopo pedagógico da disciplina e facilidade de legibilidade.
* **Pygame:** Biblioteca voltada para o desenvolvimento de jogos 2D, crucial para a renderização gráfica de superfícies, manipulação de janelas e captura de eventos de teclado em tempo real.
* **Visual Studio Code (VS Code):** Ambiente de desenvolvimento integrado (IDE) principal, utilizado para agilizar a escrita, testes locais e refatoração do código do grupo.
* **GitHub & Git:** Ferramentas indispensáveis utilizadas para o controle de versão, divisão do ecossistema de desenvolvimento em ramos (*branches*) e armazenamento remoto seguro do código.
* **Canva:** Utilizado para a confecção e estilização visual dos *slides* de apresentação do projeto para a avaliação.
* **WhatsApp:** Canal de comunicação instantânea interno da equipe, garantindo respostas rápidas, alinhamento de horários e tomadas de decisões ágeis.
* **Discord:** Plataforma de comunicação ativa usada especificamente para reuniões de alinhamento com os monitores da disciplina.

---

## Conceitos Utilizados da Disciplina

* **Comandos Condicionais (if/elif/else):** Fundamentais para gerenciar o fluxo lógico e as tomadas de decisão em tempo real. Foram aplicados no controle de colisão entre projéteis, inimigos e o jogador, na validação de permissões para transição de salas (ex: bloquear a porta final caso o jogador não possua as 3 chaves), e na mudança de estados para renderização das três telas distintas de derrota e da tela de vitória.
* **Estruturas de Repetição (for/while):** O laço principal (`while`) garante a execução contínua do jogo e a captura de eventos a cada frame. Já os laços `for` foram utilizados para iterar sobre listas e grupos de sprites do Pygame (como o grupo de coletáveis e inimigos), para fazer a varredura das matrizes de tiles que constroem o cenário e para desenhar elementos repetidos na interface do HUD, como os corações de vida.
* **Programação Orientada a Objetos (POO):** O projeto foi modularizado utilizando os pilares de POO para manter o código limpo e organizado. Foram criadas classes específicas para representar cada entidade (como `ColetavelChave`, `Player` e as lendas). Aplicou-se o conceito de **Herança**, em que as classes herdam de `pygame.sprite.Sprite` para reaproveitar propriedades de desenho e mascaramento de colisão, além do encapsulamento de atributos como contadores de inventário, posições em coordenadas (`x`, `y`) e retângulos de colisão (`rect`).
* **Estruturas de Dados Integradas (Listas, Dicionários e Tuplas):** Essenciais para mapear e conectar o labirinto do jogo. Utilizou-se estruturas de dicionários e tuplas de coordenadas para gerenciar o sistema de vizinhos e portas de cada sala (ex: `salas[(2, -2)]`), permitindo transições fluidas de tela dependendo da direção calculada ('N', 'S', 'E', 'O').
* **Leitura de Arquivos Externos (JSON):** Empregada para desvincular a estrutura do mapa do código-fonte principal. O sistema realiza a leitura analítica de um arquivo de configuração no formato `.json` para carregar dinamicamente o layout de cada sala, facilitando a manutenção e a expansão do labirinto.
* **Manipulação de Módulos e Bibliotecas Nativas:** Uso prático e integração de bibliotecas nativas da linguagem, como o módulo `os` para realizar caminhos relativos e manipulação de diretórios do sistema de arquivos de forma multiplataforma (evitando quebras no carregamento de assets entre computadores diferentes), além de coletores matemáticos como o `Counter` para agrupamento lógico de itens. 

---

## Desafios, Erros e Lições Aprendidas

**Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?**
O maior erro cometido pelo grupo ocorreu nas etapas iniciais do desenvolvimento, em que a definição da ideia geral do jogo ficou muito vaga. Esse desalinhamento fez com que os integrantes seguissem caminhos diferentes, desenvolvendo códigos de forma isolada. Para contornar a situação, o grupo realizou uma reunião de alinhamento emergencial, reestruturou o escopo do jogo focando na temática do folclore brasileiro, dividiu as tarefas de forma clara e estabeleceu prazos rígidos no repositório Git, o que permitiu que o projeto progredisse com fluidez.

**Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?**
O principal obstáculo técnico foi compreender a engenharia interna de desenvolvimento de um jogo do zero — como estruturar um loop principal eficiente, coordenar o carregamento de mapas baseados em caracteres e sincronizar os sensores de colisão com taxas de atualização adequadas. O grupo superou essa barreira por meio de pesquisas profundas, consultas a documentações técnicas e estudo prático sobre a biblioteca Pygame.

**Quais as lições aprendidas durante o projeto?**
Ao longo do desenvolvimento de *Os Guardiões*, o grupo adquiriu lições valiosas que vão além da programação básica:
* **Importância do Planejamento Prévio:** Aprendemos que gastar tempo alinhando a ideia e a mecânica logo no início evita retrabalho e códigos conflitantes.
* **Domínio do Controle de Versão (Git/GitHub):** Compreendemos na prática a importância de trabalhar com ramificações (*branches*), realizar revisões de código e resolver conflitos para garantir a integridade do projeto em equipe.
* **Desenvolvimento Tranquilo:** A necessidade de usar caminhos relativos (através da biblioteca `os`) para carregar *assets* nos ensinou a criar softwares preparados para rodar em qualquer máquina sem quebras de diretórios.
* **Modularização e Código Limpo:** A transição do desenvolvimento isolado para a Programação Orientada a Objetos nos mostrou como estruturar um projeto de grande porte dividindo-o em classes reutilizáveis e fáceis de manter.

---

## Instruções de Execução

1. Clone o repositório do projeto:
 ```bash
git clone https://github.com/mcecirpm/Jogo-IP.git
```
2. Instale as dependências:
 ```bash
pip install pygame
```
3. Execute o jogo:
 ```bash
python jogo.py
```

---

## Controles

| Ação | Comando no Teclado |
| :--- | :--- |
| **Mover para Cima** | W |
| **Mover para Baixo** | S |
| **Mover para a Esquerda** | A |
| **Mover para a Direita** | D |
| **Atirar / Atacar** | Setas direcionais (⭡, ⭣, ⭠, ⭢) |
| **Alternar Tela Cheia** | F11 |
| **Sair do Jogo** | Esc |
