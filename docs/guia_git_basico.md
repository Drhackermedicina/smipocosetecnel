# Guia básico de Git: commit e push

Este guia explica, passo a passo, como salvar suas alterações no Git e enviá-las para um repositório remoto (por exemplo, GitHub).
Se você ainda não tem os arquivos na sua máquina, veja primeiro como obtê-los em [`docs/como_clonar_projeto.md`](como_clonar_projeto.md).

## Pré-requisitos

- Git instalado no computador. No Windows, você pode instalar via [Git for Windows](https://git-scm.com/download/win).
- Acesso ao repositório remoto (permissão para enviar alterações).

## 1. Configurar o Git (apenas na primeira vez)

Abra o terminal (Prompt de Comando no Windows ou Terminal no macOS/Linux) e execute:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

Essas informações serão usadas para identificar seus commits.

## 2. Verificar o status do repositório

Dentro da pasta do projeto, veja quais arquivos foram modificados:

```bash
git status
```

Arquivos em vermelho ainda não foram adicionados ao commit.

## 3. Adicionar arquivos ao commit

Escolha os arquivos que deseja salvar. Para adicionar todos os arquivos modificados de uma vez:

```bash
git add .
```

Se preferir adicionar arquivos específicos, substitua o ponto pelo nome do arquivo, por exemplo:

```bash
git add README.md docs/guia_git_basico.md
```

## 4. Criar o commit

Com os arquivos adicionados, crie um commit com uma mensagem objetiva:

```bash
git commit -m "Descreva rapidamente a alteração"
```

Exemplo de mensagem: `git commit -m "Atualiza README com guia de commit"`.

## 5. Enviar para o repositório remoto (push)

Antes de enviar, garanta que você está na branch correta (ex.: `main`, `work`):

```bash
git branch
```

Para enviar o commit para o servidor remoto:

```bash
git push origin nome-da-branch
```

Substitua `nome-da-branch` pela branch desejada. Se você estiver na branch `work`, o comando será:

```bash
git push origin work
```

Se o repositório estiver protegido por autenticação, informe suas credenciais ou token quando solicitado.

## 6. Resolver conflitos (quando necessário)

Se o push falhar por causa de alterações remotas, atualize sua branch:

```bash
git pull --rebase origin nome-da-branch
```

Resolva os conflitos conforme indicado pelo Git, repita o commit (se for o caso) e tente o `git push` novamente.

## 7. Confirmar no repositório remoto

Depois do push, acesse o repositório (GitHub, GitLab etc.) e verifique se o commit aparece no histórico. Aproveite para abrir uma Pull Request, se necessário.

---

> **Dica:** use commits pequenos e frequentes, com mensagens claras. Isso facilita revisar, entender e desfazer alterações quando preciso.
