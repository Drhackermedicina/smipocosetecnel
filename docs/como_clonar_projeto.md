# Como obter o projeto no seu computador

Este guia explica, passo a passo, duas maneiras de colocar os arquivos do sistema no seu computador: fazendo o **download em formato ZIP** ou **clonando com Git**. Escolha o método que for mais confortável para você.

## 1. Fazer download como ZIP (sem usar Git)

1. Abra o repositório no GitHub (ou na plataforma onde os arquivos estiverem hospedados).
2. Clique no botão verde **Code** e, em seguida, em **Download ZIP**.
3. Depois que o arquivo `.zip` for baixado, localize-o na pasta **Downloads**.
4. Clique com o botão direito e escolha **Extrair tudo...** (Windows) ou use o utilitário padrão de extração no macOS/Linux.
5. Escolha uma pasta destino fácil de lembrar, por exemplo `C:\SMI` (Windows) ou `~/SMI` (macOS/Linux).
6. Após extrair, abra essa pasta no terminal/Prompt de Comando para seguir os passos de execução descritos no README.

> **Dica:** sempre que receber uma atualização do projeto, repita o download do ZIP para obter a versão mais recente.

## 2. Clonar com Git (mantendo o vínculo com o repositório)

Se você já criou um repositório no GitHub (ou recebeu acesso a um existente), é possível trazer os arquivos para o computador com o comando `git clone`.

1. Copie a URL do repositório remoto. No GitHub, ela aparece ao clicar no botão **Code** — escolha a opção **HTTPS** e copie o endereço (algo como `https://github.com/seu-usuario/seu-repo.git`).
2. Abra o terminal (Prompt de Comando no Windows) e navegue até a pasta onde deseja salvar o projeto:

   ```cmd
   cd C:\
   mkdir SMI
   cd SMI
   ```

   No macOS/Linux, os comandos são:

   ```bash
   cd ~
   mkdir SMI
   cd SMI
   ```

3. Execute o comando de clonagem substituindo a URL pelo endereço do seu repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   ```

4. Após a clonagem, entre na pasta criada (normalmente o nome do repositório):

   ```bash
   cd seu-repo
   ```

5. Agora você terá todos os arquivos na máquina e poderá seguir o guia de execução (`README.md`) e o guia de Git (`docs/guia_git_basico.md`) para fazer commits e enviar alterações.

### E se os arquivos ainda não estiverem no GitHub?

Se você recebeu o projeto por outro meio (por exemplo, um arquivo ZIP ou uma pasta copiada) e quer colocá-lo no seu GitHub:

1. Crie um repositório vazio no GitHub (sem README inicial).
2. No computador, abra a pasta do projeto e inicialize o Git (caso ainda não exista a pasta `.git`):

   ```bash
   git init
   ```

3. Adicione o repositório remoto recém-criado:

   ```bash
   git remote add origin https://github.com/seu-usuario/seu-repo.git
   ```

4. Siga o guia de commits em [`docs/guia_git_basico.md`](guia_git_basico.md) para criar um commit e, por fim, faça o push:

   ```bash
   git push -u origin main
   ```

   > Substitua `main` pelo nome da branch padrão do seu repositório, se for diferente.

Depois disso, os arquivos passarão a aparecer no seu GitHub e você poderá cloná-los a qualquer momento em outros computadores.
