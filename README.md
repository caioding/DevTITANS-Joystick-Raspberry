# Backup do projeto DevTITANS Equipe 3: Joystick no Raspberry

Cópia independente de
[ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry](https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry),
feita em 15/11/2026, para o projeto não se perder se o original for apagado.

## O que está guardado e onde

| Parte | Onde está nesta cópia | Como foi copiado |
|---|---|---|
| Código: branches `main`, `driver`, `firmware`, `FirmwareBraco`, `integracao-braco`, 55 commits com os autores originais | as próprias branches deste repositório | `git clone --mirror` + `git push --mirror` |
| Wiki: 13 páginas, 49 commits | a Wiki deste repositório | `git clone --mirror` da `.wiki.git` + `git push --mirror` |
| Issues: 18, com labels e responsáveis (não ficam no git) | esta branch, pasta `issues/`: `ISSUES.md` (legível) e os `.json` (dados completos da API) | `exportar_issues.py` (API REST pública do GitHub) |
| Imagem anexada à wiki (hospedada pelo GitHub, fora do git) | esta branch, `anexos/598c6eae-37a2-409a-8827-f4bcb5dd5d07` (PNG) | `curl` do endereço `github.com/user-attachments/assets/...` |
| Board "Equipe 3: Hands On Final" (GitHub Projects, 18 itens, 5 visões) | esta branch, pasta `board/`: `BOARD.md` (legível), `board.csv` (abre no Excel) e os `memex-*.json` (dados completos: campos, opções, iterações, visões) | `exportar_board.py`: lê os dados que a página pública do board embute, sem login |

Os links nas issues e na wiki continuam apontando para o repositório original. O conteúdo está todo aqui.

## Board e issues recriados no GitHub (15/11/2026)

- **Board:** [github.com/users/caioding/projects/4](https://github.com/users/caioding/projects/4). Feito com
  "Make a copy" do board original (campos, 5 visões, automações) e com as 18 issues adicionadas por
  "Add item from repository". Os status batem item por item com o `Backlog.tsv` original (7 Todo, 4 In progress,
  7 Done). O board está ligado ao repositório.
- **Issues:** criadas pelo formulário do GitHub, com título e texto originais e uma linha "Copiada da issue nº N do
  repositório original". As 7 concluídas foram fechadas como *completed*. Os responsáveis originais (Thiago,
  Raphael) não são colaboradores aqui, então ficaram registrados no texto, escritos sem @ para não notificar ninguém.
- **Números:** o #1 já era um pull request e a "Entrega" foi criada antes da hora, então ficou assim:

| Original | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aqui | 2 | 4 | 5 | 6 | 3 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |

## Comandos usados

```bash
git clone --mirror https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry.git codigo.git
git --git-dir=codigo.git push --mirror https://github.com/caioding/DevTITANS-Joystick-Raspberry.git

git clone --mirror https://github.com/ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry.wiki.git wiki.git
git --git-dir=wiki.git push --mirror https://github.com/caioding/DevTITANS-Joystick-Raspberry.wiki.git

python exportar_issues.py ThiagoChaves517/DevTITANS_Equipe-3_-Joystick-no-Raspberry issues
python exportar_board.py https://github.com/users/ThiagoChaves517/projects/13 board
curl -L -o anexos/598c6eae-37a2-409a-8827-f4bcb5dd5d07 https://github.com/user-attachments/assets/598c6eae-37a2-409a-8827-f4bcb5dd5d07
```

No Windows, com a pasta num caminho longo, use também `git config core.longpaths true` dentro do `codigo.git`
e do `wiki.git`.

## Atualizar a cópia depois

Quando o time fizer novos commits no original, rode dentro das pastas dos espelhos:

```bash
git --git-dir=codigo.git fetch -p origin
git --git-dir=codigo.git push --all https://github.com/caioding/DevTITANS-Joystick-Raspberry.git
```

```bash
git --git-dir=wiki.git fetch -p origin
git --git-dir=wiki.git push --mirror https://github.com/caioding/DevTITANS-Joystick-Raspberry.wiki.git
```

No código, use **`--all`**, e não `--mirror`. O `--mirror` apagaria esta branch `backup-github`, que não existe
no original. As issues: rode o `exportar_issues.py` de novo e faça commit nesta branch.
