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
| **Davi Melo e Luna** | Desenvolvimento inicial do personagem, mecânica de projéteis teleguiados, criação das telas de fim de jogo (*game over/win*). |
| **Giovanna Reis da Silva** | Criação das classes dos inimigos Mula-sem-Cabeça (com sistema de perseguição e tiros de fogo) e Curupira (com mecânica de atordoamento), estruturação do rascunho do mapa e correções no encerramento de jogo. |
| **Heitor Condé Freire** | Montagem dos slides e produção das sprites |
| **Maria Cecília R. P. de Melo** | Programação lógica da inimiga Iara, criação da classe de poder, ajuste de velocidade, mecânica de alteração de tempo atrelada ao ataque da guardiã e montagem do labirinto nas salas. |
| **Maysa Barros Campelo** | Implementação lógica dos itens coletáveis (vida extra, tempo e chaves), tratamento dinâmico de caminhos de *sprites* via biblioteca `os`, desenvolvimento e atualização do HUD (inventário e contadores) e gerenciamento de tela cheia. |

---

## Arquitetura do Projeto

`[Completar após finalizar o código.]`

---

## Capturas de Tela

### Tela Inicial:
![Tela Inicial do Jogo](link da imagem)

### Labirintos:
![Labirinto e Inimigos](link da imagem)

### Interface do HUD e Inventário:
![HUD e Coletáveis](link da imagem)

### Tela de Game Over / Vitória:
![Fim de Jogo](link da imagem)

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

`[Completar após finalizar o código.]`
* **Comandos Condicionais (if/elif/else):** 
* **Estruturas de Repetição (for/while):** 
* **Programação Orientada a Objetos (POO):** 

---

## Desafios, Erros e Lições Aprendidas

**Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?**
O maior erro cometido pelo grupo ocorreu nas etapas iniciais do desenvolvimento, onde a definição da ideia geral do jogo ficou muito vaga. Esse desalinhamento inicial fez com que os integrantes seguissem caminhos diferentes no desenvolvimento de códigos isolados. Para contornar a situação, o grupo realizou uma reunião de alinhamento emergencial, reestruturou o escopo do jogo focando na temática do folclore brasileiro, dividiu as tarefas de forma clara e estabeleceu prazos rígidos no repositório Git, o que permitiu que o projeto progredisse com fluidez.

**Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?**
O principal obstáculo técnico foi compreender a engenharia interna de desenvolvimento de um jogo do zero — como estruturar um loop principal eficiente, coordenar o carregamento de mapas baseados em caracteres e sincronizar os sensores de colisão com taxas de atualização adequadas. O grupo superou essa barreira por meio de pesquisas e estudo sobre o Pygame.

**Quais as lições aprendidas durante o projeto?**
`[Completar depois com nossas lições finais que o grupo adquiriu ao terminar tudo!]`

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
python main.py
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
