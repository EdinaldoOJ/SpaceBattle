<div align="center">
<img src="https://cdn.discordapp.com/attachments/1125892268138713201/1126556476668923995/space_battle.png" width="700px" />
</div>

# Space Battle🚀

Este repositório contém o código-fonte e a documentação para um jogo distribuído desenvolvido no modelo cliente-servidor. O jogo permite que dois clientes se conectem a um servidor central e participem de uma experiência de jogo multiplayer em tempo real.

<div align="center">
<img src="https://cdn.discordapp.com/attachments/1125892268138713201/1126615440177762335/Scifi_Buildings_Create_a_nostalgic_logo_for_the_title_Space_Ba_3.jpg" width="700px" />
</div>


## História 🐱‍🚀

No coração dos vastos cosmos, duas naves estão destinadas a se enfrentar em uma rivalidade intergaláctica. Com influências nostálgicas dos jogos de 16 bits dos anos 90, prepare-se para mergulhar em uma história intensa e emocionante.

Escolha seu lado: a poderosa nave estelar "Justice Wing", defensora da paz e justiça, ou a temida nave pirata "Shadow Fang", símbolo de ambição e caos. A bordo de suas naves futuristas, encare combates frenéticos no espaço sideral, desviando-se de tiros laser e lançando projéteis precisos.

Prepare-se para a batalha final, onde o destino de ambos os lados será decidido.

Em Space Battle: A Batalha das Naves, a emoção está em suas mãos. Desafie oponentes formidáveis, explore asteroides perigosos, nebulosas brilhantes e planetas exóticos. Prove sua coragem e habilidade como piloto espacial, mergulhando em uma experiência intensa de combate intergaláctico.

Escolha seu lado e torne-se uma lenda do espaço. O destino da galáxia está em jogo. Prepare-se para a aventura espacial mais emocionante dos anos 90! Quem sairá vitorioso nesse confronto lendário? A resposta está em você.


## Inspirações 🎭

O design e a implementação de Space Battle foram profundamente influenciados por várias fontes de inspiração, incluindo as lendárias sagas de Star Wars e outras histórias de ficção científica dos anos 90. 

Combinando elementos nostálgicos com a estética pixelada característica dos jogos da época, buscamos criar uma experiência imersiva e emocionante.
Star Wars, com suas batalhas espaciais épicas e o conflito entre o bem e o mal, serviu como uma das principais inspirações para a narrativa e o cenário do jogo. Queríamos capturar a atmosfera de aventura e ação que cativou gerações de fãs. As naves icônicas, como o Millennium Falcon e a Estrela da Morte, nos inspiraram a criar as nossas próprias naves marcantes e distintas, como a "Justice Wing" e a "Shadow Fang".

Além disso, os jogos de ação espacial dos anos 90, como Space Invaders, Gradius, Star Fox e Galaga também desempenharam um papel importante em nosso processo de escolha e criação. Esses jogos icônicos nos influenciaram na jogabilidade frenética para aprimorar a experiência do jogador. Queríamos capturar a mesma emoção e desafio que esses jogos proporcionavam.

 Ao combinar essas inspirações, criamos um universo único em Space Battle, onde a rivalidade entre as naves "Justice Wing" e "Shadow Fang" se desenrola em meio a um cenário estelar repleto de perigos e mistérios


## Linguagens e Tecnologias Utilizadas 🐱‍💻

### - Aseprite : 
Aseprite é uma robusta ferramenta de criação de sprites e animações. Foi escolhida para desenvolver os gráficos pixelados e a estética visual do jogo, por sua facilidade para realizar o projeto, através de sua organização em camadas, possibilidade de pré-visualizar como o desenvolvimento do desenho está sendo feito, e sua diversa paleta de cores, o que   permitiu a criação das naves

### - Visual Studio Code :

IDE Integrated Development Environment - Ambiente de Desenvolvimento Integrado, é uma ferramenta usada no desenvolvimento de aplicações, que combina diferentes funcionalidades em uma única interface gráfica do usuário.
	
Essa ferramenta permite ao desenvolvedor digitar todas as codificações e regras do software a ser criado a partir de uma linguagem específica. O desenvolvimento de sistemas pode ser realizado de diversas formas. Neste contexto, o IDE assegura uma maior produtividade e precisão do processo, uma vez que várias funcionalidades não precisarão ser personalizadas a cada demanda.
	
O Visual Studio Code (VS Code) é um editor de código de código aberto desenvolvido pela Microsoft, tem funcionalidades que facilitam o processo de desenvolvimento, facilitando o trabalho de desenvolvedores. Sendo uma ferramenta de fácil entendimento, possui uma loja de extensões imensa, e que continua crescendo.

Ou seja, com essa enorme coleção de extensões, podemos adicionar diversas funcionalidades ao VS Code de forma bem simples. Qualquer um pode criar uma extensão e publicar na loja. Desse modo, sempre há novas ferramentas que podem ser interessantes para alguém.

<div align="center"> 
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" width="30" height="35" />
</div>


### -Python :

Python foi a linguagem de programação escolhida para implementar a lógica e a mecânica do jogo. Python é uma linguagem versátil, de alto nível e de fácil compreensão, o que facilita o desenvolvimento de jogos. Sua sintaxe limpa e a vasta quantidade de bibliotecas disponíveis fazem dela uma opção popular para o desenvolvimento de jogos independentes.

<div align="center"> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="35" height="35" />
</div>

### -Pygame: 

Pygame é uma biblioteca de jogos em Python que fornece ferramentas e recursos para o desenvolvimento de jogos 2D. Ela foi utilizada em Space Battle para lidar com a criação da janela de exibição do jogo, gerenciamento de eventos, manipulação de sprites, detecção de colisões e reprodução de efeitos sonoros. Pygame simplifica muitos aspectos do desenvolvimento de jogos, permitindo que os desenvolvedores se concentrem na jogabilidade e na lógica do jogo.

A escolha dessas tecnologias foi baseada em sua facilidade de uso, documentação abrangente, comunidade ativa e capacidade de atender às necessidades específicas do projeto. Aseprite permitiu a criação dos visuais pixelados e estéticos, enquanto Python e Pygame ofereceram uma combinação poderosa para a implementação da lógica do jogo e sua interação com o jogador.

Juntas, essas tecnologias permitiram o desenvolvimento de Space 


## Desenvolvimento de Jogo Distribuído Modelo Cliente-Servidor 🐱‍👤

O jogo foi implementado seguindo o modelo cliente-servidor, em que um servidor central gerencia a lógica do jogo e os clientes se conectam a ele para participar da jogabilidade. A comunicação entre o cliente e o servidor é estabelecida por meio de um socket TCP.

### Protocolo da Camada de Aplicação 🧾

O protocolo da camada de aplicação define a forma como o cliente e o servidor se comunicam durante o jogo. Ele possui a seguinte estrutura:

- *Conexão do cliente*: Os clientes se conectam ao servidor por meio de um socket TCP.
- *Mensagens do cliente para o servidor*: Os clientes enviam mensagens para o servidor informando sobre suas ações, como pressionar teclas do teclado, solicitar informações sobre o status do jogo, solicitar dados iniciais do jogo, liberar teclas do teclado e desconectar do servidor.
- *Mensagens do servidor para o cliente*: O servidor envia mensagens para os clientes fornecendo informações sobre o estado do jogo, enviando dados iniciais do jogo, informando sobre o vencedor do jogo e impondo limites de conexão.
- *Estrutura das mensagens*: O protocolo utiliza uma estrutura de mensagens composta por um comando (command) e dados (data), separados por um caractere especial de terminação (chatlib.END_OF_MESSAGE). O comando indica o tipo de mensagem e os dados fornecem informações adicionais, se necessário.


### Escolha do Protocolo TCP 👾

O protocolo TCP (Transmission Control Protocol) foi escolhido para a comunicação entre o cliente e o servidor devido às suas características de confiabilidade e controle de fluxo. O TCP garante que os dados sejam entregues sem erros e em ordem, o que é fundamental para a sincronização correta do estado do jogo entre o servidor e os clientes. Além disso, o TCP lida com a fragmentação e retransmissão de pacotes automaticamente, garantindo que a comunicação seja robusta mesmo em redes instáveis.

### Funcionamento do Software 🔮

O software do jogo segue uma arquitetura cliente-servidor, em que o servidor é responsável por gerenciar a lógica do jogo e os clientes se conectam a ele para jogar. O servidor espera por conexões de clientes e gerencia as interações entre eles.

Quando um cliente se conecta, ele envia mensagens para o servidor informando suas ações, como pressionar teclas do teclado. O servidor atualiza o estado do jogo de acordo com as ações dos clientes, realiza cálculos e verifica condições de vitória. Em determinados momentos, o servidor envia mensagens de status do jogo para os clientes, informando sobre o estado atual do jogo e o vencedor, se houver.

O jogo utiliza a biblioteca Pygame para criar a interface gráfica, lidar com elementos multimídia e processar eventos de entrada. O código fornecido no repositório representa uma parte do jogo, incluindo classes e funções relacionadas a elementos específicos, como jatos, balas e a lógica do servidor.

### Propósito e Motivação 🤩

O propósito do jogo distribuído modelo cliente-servidor é proporcionar uma experiência de jogo interativa em que os jogadores possam competir entre si. A escolha do modelo cliente-servidor permite que vários jogadores se conectem a um servidor centralizado e participem de uma jogabilidade compartilhada. Isso cria um ambiente competitivo em que os jogadores podem se desafiar e buscar a vitória.

O jogo se destaca pela jogabilidade multiplayer em tempo real, onde os jogadores podem enfrentar uns aos outros. A comunicação entre os jogadores é facilitada pelo servidor, que sincroniza o estado do jogo e garante uma experiência consistente para todos os participantes.



### Requisitos Mínimos

- *Python*: É necessário ter o Python instalado na máquina para executar o jogo.
- *Pygame*: A biblioteca Pygame deve ser instalada. Você pode instalar usando o comando `pip install pygame` no terminal.
- *Pillow*: A biblioteca Pillow também deve ser instalada. Você pode instalar usando o comando `pip install pillow` no terminal.
- *Compatibilidade*: Certifique-se de ter uma versão do Pygame compatível com a versão do Python que você está utilizando.

Antes de executar o jogo, verifique os requisitos específicos, como configurações de rede e configurações do servidor, se houver, para garantir o funcionamento adequado do jogo em seu ambiente local.


## Contribuição

O projeto é open source, quem tiver interesse pode fazer as mudanças que acharem necessárias


## Contato

Informações de contato para que os interessados possam entrar em contato caso tenham alguma dúvida ou queiram colaborar com o projeto. Você pode me contatar através do e-mail [tnsilva.cic@uesc.br] ou [eoliveira.cic@uesc.br].

## Referências

(https://www.pygame.org/news)
(https://www.python.org/)
(https://www.aseprite.org/)
(https://pillow.readthedocs.io/en/stable/)
(https://www.starwars.com/)
(https://www.wienerphilharmoniker.at/en/konzerte/the-music-of-john-williams/10196/)
(https://www.nintendo.com/pt-br/)
## Agradecimentos

Agradecimentos especiais a equipe que contribuíram com o desenvolvimento do jogo. Ao professor Jorge Lima pela possibilidade de poder desenvolver esse projeto e as críticas e ideias dos nossos amigos: Samuel, Gustavo, Gabriel e Marcos, que puderam nos auxiliar nos ajustes finais do projeto.


---





<p> Create by Edinaldo and Tauan</p>


<div align="center">
<img src="https://cdn.discordapp.com/attachments/1125892268138713201/1126574420861923438/picasion.com_0ac37155c681abdc7a8b79f8f034ebf7.gif" width="150" height="150" border="0" />
</div>