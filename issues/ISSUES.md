# Issues de ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry

Exportado da API do GitHub. 18 itens, 0 comentários.

## #1 1.1 - Baixar o Repositório do AOSP & Compilar uma Imagem para Raspberry Pi

- Issue, estado: **closed**, criada por @ThiagoChaves517 em 2026-09-07, fechada em 2026-09-09
- Labels: —
- Responsáveis: @ThiagoChaves517
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/1

# Baixar o Repositório do AOSP & Compilar uma Imagem para Raspberry Pi

## Introdução

Para integrar o joystick na Raspberry Pi, antes é necessário embarcar nela uma imagem AOSP.
Neste guia, vamos utilizar como ambiente de desenvolvimento a distribuição AOSP do Projeto Glodroid e gerar uma imagem.

> **⚠️ Aviso de Hardware e Espaço:** A compilação do AOSP é um processo pesado. Recomenda-se ter pelo menos **16 GB de RAM** e cerca de **150 a 200 GB de espaço livre em disco** (já otimizado). Compilar o Android sem espaço suficiente fará com que o processo falhe silenciosamente no final.

---

## Checklist de Requisitos

*Nota: É crucial usar pacotes de sistema em vez de instalar módulos Python via `pip`. O sistema de compilação do AOSP (Soong), no Glodroid, isola o ambiente e ignorará bibliotecas instaladas via `pip` pelo usuário, causando erros na geração dos gráficos e da câmera.*

Abra o terminal e execute os seguintes comandos:

- [x]  Instale as dependências e ferramentas do sistema

```bash
# Atualize a lista de pacotes disponíveis
sudo apt-get update

# Pacotes base do AOSP e ferramentas de build
sudo apt-get install -y git-core gnupg flex bison build-essential zip curl zlib1g-dev \
gcc-multilib g++-multilib libc6-dev-i386 lib32ncurses5-dev x11proto-core-dev libx11-dev \
lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig swig libssl-dev \
device-tree-compiler mtools gettext libncurses5 libgmp-dev libmpc-dev cpio rsync \
dosfstools kmod gdisk lz4 cmake libglib2.0-dev git-lfs libgnutls28-dev pkg-config \
ninja-build wget

# Módulos Python e Meson obrigatórios nativos (Substitui o PIP)
sudo apt-get install -y python-is-python3 python3-dev python3-mako python3-jinja2 \
python3-ply python3-yaml python3-pyelftools meson

# Ferramentas extras exigidas pelo Kernel moderno do Linux e U-Boot
sudo apt-get install -y libelf-dev dwarves zstd u-boot-tools
```

- [ ] Configure o git.

```bash
git config --global user.name [Seu Nome]
git config --global user.email [Seu E-Mail]
```


- [ ]  Instale o repo (para poder baixar o repositório do Glodroid)

```bash
mkdir bin; cd bin
wget https://storage.googleapis.com/git-repo-downloads/repo
chmod 755 repo
export PATH=$PATH:~/bin/
echo "export PATH=$PATH:~/bin/" >> ~/.bashrc
```

- [ ] Configure o ambiente para evitar falhas do Kernel

> **Correção crítica para Ubuntu/Debian/Mint**: O sistema operacional hospedeiro frequentemente tenta interceptar o comando de instalação do kernel e gravá-lo no /boot do seu PC, o que quebra o build do AOSP. Os comandos abaixo criam um script customizado exigido pelo GloDroid.

```bash
# Faz o backup do script original do sistema
sudo mv /sbin/installkernel /sbin/installkernel.bak

# Cria o script customizado para o AOSP
sudo tee /sbin/installkernel > /dev/null << 'EOF'
#!/bin/bash
VERSION=$1
IMAGE=$2
MAP=$3
DIR=$4

# Cria o diretório alvo solicitado pelo AOSP
mkdir -p "$DIR"

# Copia os arquivos usando a nomenclatura exata que o GloDroid espera
cp "$IMAGE" "$DIR/vmlinux-$VERSION"
cp "$MAP" "$DIR/System.map-$VERSION"
cp ".config" "$DIR/config-$VERSION" 2>/dev/null || true

exit 0
EOF

# Dá permissão de execução ao script
sudo chmod +x /sbin/installkernel
```

- [ ] Baixe o repositório do código-fonte do Glodroid.

```bash
cd ~
git clone https://github.com/GloDroidCommunity/raspberry-pi.git
mv raspberry-pi aosp-raspberry
cd aosp-raspberry
```

- [ ] Instale e compile o Glodroid.

```bash
# Edita o script unfold_aosp.sh para incluir o parâmetro --depth=1
sed -i 's/repo init -u/repo init --depth=1 -u/g' unfold_aosp.sh

./unfold_aosp.sh && ./build.sh
```

## Resultado Esperado

Se o processo for concluído com sucesso, você encontrará o arquivo da imagem final gerada na seguinte pasta:

```bash
~/aosp-raspberry/aosptree/out/target/product/gd_rpi4/sdcard.img
```

Este é o arquivo que deverá ser gravado (flasheado) no seu cartão MicroSD para rodar na Raspberry Pi.

## #2 Kickoff da equipe

- Issue, estado: **closed**, criada por @RaphaelvnMello em 2026-09-09, fechada em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/2

Divisão em sub-times, criação do repositório GitHub e definição inicial de papéis

## #3 Estudo joystick/SNES

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/3

Sistema de eventos de joystick no Linux e protocolo do SNES; discussão sobre uso do acelerômetro como input

## #4 Levantamento de componentes

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/4

Levantamento e compra de servos/motores, acelerômetro, microcontrolador, cabos e peças para o braço

## #5 Entrega do Planejamento Parcial

- Issue, estado: **closed**, criada por @RaphaelvnMello em 2026-09-09, fechada em 2026-09-16
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/5

Times, subtarefas no GitHub, cronograma e apresentação

## #6 Início do firmware

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/6

Leitura dos botões do joystick conforme protocolo SNES

## #7 Estrutura do driver

- Issue, estado: **closed**, criada por @RaphaelvnMello em 2026-09-09, fechada em 2026-09-23
- Labels: —
- Responsáveis: @RaphaelvnMello
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/7

Estrutura inicial do driver de comunicação Joystick ↔ Raspberry Pi

## #8 Protocolo Raspberry e braço

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/8

Estudo do protocolo de comunicação entre Raspberry Pi e o braço robótico

## #9 Pesquisa de peças do braço

- Issue, estado: **closed**, criada por @RaphaelvnMello em 2026-09-09, fechada em 2026-09-25
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/9

Design e ajustes do modelo escolhido para o braço robótico

## #10 Leitura do acelerômetro

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/10

Implementação no firmware e definição final da mecânica de input (inclinação/gesto)

## #11 Ambiente de rede

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/11

Configuração de rede e ambiente do Raspberry Pi para testes com o driver

## #12 Início da impressão 3D

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/12

Início da impressão 3D das peças do braço robótico

## #13 Driver como input Android

- Issue, estado: **closed**, criada por @RaphaelvnMello em 2026-09-09, fechada em 2026-09-23
- Labels: —
- Responsáveis: @RaphaelvnMello
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/13

Driver reconhecendo o joystick como dispositivo de input no Android (mapeamento de eventos)

## #14 Comunicação Raspberry e braço

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/14

Implementação da comunicação Raspberry Pi → braço robótico (protocolo de comandos)

## #15 Finalização da impressão 3D

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/15

Finalização da impressão 3D e montagem estrutural do braço

## #16 Confecção do joystick e braço

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/16

Confecção física do joystick e montagem/calibração dos servos do braço robótico

## #17 Integração driver + firmware

- Issue, estado: **open**, criada por @RaphaelvnMello em 2026-09-09
- Labels: —
- Responsáveis: @RaphaelvnMello
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/17

Testes de leitura de botões e acelerômetro via SNES

## #18 1.2 - Instalar a imagem na Raspberry Pi

- Issue, estado: **closed**, criada por @ThiagoChaves517 em 2026-09-09, fechada em 2026-09-09
- Labels: —
- Responsáveis: —
- Milestone: —
- Original: https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry/issues/18

Instalar a imagem na Raspberry Pi
## Introdução

Para integrar o joystick na Raspberry Pi, antes é necessário embarcar nela uma imagem AOSP.
Neste subtask, o objetivo é  instalar a imagem gerada na Raspberry.

---

## Checklist de Requisitos

- [ ]  Instale o Raspberry Pi Imager.
- [ ] Escreva a imagem gerada na subtask anterior no SD card da Raspberry com o Raspberry Pi Imager.
- [ ] Teste


## Resultado Esperado

A Raspberrry Pi já apresenta um sistema operacional Android.
