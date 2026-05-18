# Launcher de Jogos da Oficina de Programação de Jogos

Este é o repositório do Launcher de Jogos da Oficina de Programação de Jogos.

O launcher é uma interface simplificada que permite executar os jogos disponibilizados
para a oficina (desenvolvidos com Greenfoot ou Godot) e que também permite voltar o 
código de cada jogo para a sua versão original.

## Como adicionar jogos

1. Coloque cada jogo em uma subpasta dentro do diretório `jogos/`.
2. Para cada jogo, adicione uma imagem PNG em `imagens/` com o mesmo nome da pasta do 
   jogo (exemplo: para o jogo na pasta `jogos/PacMan`, use `imagens/PacMan.png`).
3. O sistema suporta até 7 jogos. Se houver mais de 7, apenas os 7 primeiros em ordem 
   alfabética serão exibidos e um aviso será mostrado no terminal.

**Observação**:

- Se o nome da pasta do jogo contiver "godot", o launcher executa esse jogo com a Godot.
  - O launcher usa automaticamente o primeiro arquivo encontrado na pasta `godot/`.
- Caso contrário, o launcher considera que o jogo é do Greenfoot.
  - Para esses jogos, o Greenfoot precisa estar previamente instalado na máquina.

## Configuração da Godot

O executável da Godot não deve ser versionado neste repositório.

Para configurar:

1. Baixe o executável da Godot para Linux (arquivo binário, sem extensão) no site oficial.
2. Coloque o arquivo baixado dentro da pasta `godot/` na raiz do projeto.
3. O script `iniciar.sh` aplica `chmod +x` automaticamente no primeiro arquivo encontrado em `godot/`.

Se não houver arquivo em `godot/`, jogos Godot não poderão ser iniciados.

## Como preparar os jogos para a oficina

Os jogos desenvolvidos na disciplina podem conter pastas `.git` com histórico de versão. Para o contexto da oficina, o histórico não é relevante, apenas a possibilidade de restaurar o código original de cada jogo.

Use o script `preparar_jogos.sh` para automatizar esse processo:

1. O script verifica cada subpasta em `jogos/`.
2. Remove a pasta `.git` (se existir) de cada jogo.
3. Inicializa um novo repositório git limpo em cada pasta de jogo, marcando o estado atual como a versão base.

### Como usar

```bash
chmod +x preparar_jogos.sh
./preparar_jogos.sh
```

Depois disso, cada pasta de jogo terá um repositório git limpo, permitindo que o botão "Restaurar Jogos" da interface volte o código para o estado original da oficina, independentemente de alterações feitas durante o evento.



## Como rodar a interface gráfica

O script `iniciar.sh` pode ser usado para automatizar o processo de inicialização do 
ambiente, incluindo a ativação de ambientes virtuais, instalação de dependências e 
execução da interface gráfica. Para usá-lo:

```bash
chmod +x iniciar.sh
./iniciar.sh
```

## Observações

- Certifique-se de que as imagens estejam no formato PNG e tenham o mesmo nome das pastas dos jogos.
- O script detecta automaticamente os jogos presentes em `jogos/` e suas imagens em `imagens/`.
- Para restaurar os jogos para a versão original (caso estejam sob controle do git), utilize o botão "Restaurar Jogos" na interface.
- Jogos Greenfoot dependem de instalação prévia do Greenfoot no sistema.
- O arquivo `imagens/evento.png` é exibido a interface para fornecer informações gerais sobre a oficina.





