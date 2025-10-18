# Guia passo a passo para iniciar o sistema no Windows

Este guia foi escrito para quem está começando e precisa rodar o sistema em um computador com Windows 10 ou 11.

## 1. Instalar o Python
1. Acesse <https://www.python.org/downloads/>.
2. Clique em **Download Python 3.xx**.
3. Abra o arquivo baixado e marque a opção **Add Python to PATH** antes de clicar em **Install Now**.
4. Ao final da instalação, clique em **Close**.

## 2. Baixar o projeto
1. Clique no botão verde **Code** na página do GitHub e escolha **Download ZIP**.
2. Extraia o arquivo ZIP em uma pasta fácil de lembrar, por exemplo `C:\SMI`.

## 3. Abrir o Prompt de Comando na pasta do projeto
1. Pressione `Win + R`, digite `cmd` e pressione **Enter**.
2. No Prompt, navegue até a pasta onde extraiu o projeto. Exemplo:
   ```cmd
   cd C:\SMI
   ```
   Dica: copie o caminho completo da pasta no explorador de arquivos e cole no terminal com `Ctrl + V`.

## 4. Criar e ativar o ambiente virtual
1. Execute o comando para criar o ambiente virtual:
   ```cmd
   python -m venv .venv
   ```
2. Ative o ambiente:
   ```cmd
   .venv\Scripts\activate
   ```
   Quando o ambiente estiver ativo, o terminal exibirá algo parecido com `(.venv) C:\SMI>` no início da linha.

## 5. Instalar dependências
Com o ambiente virtual ativo, rode:
```cmd
pip install -r requirements.txt
```
Esse comando baixa e instala todas as bibliotecas que o sistema utiliza.

## 6. Iniciar o servidor manualmente (opcional)
Para rodar o servidor diretamente pelo terminal, execute:
```cmd
uvicorn app.main:app --reload
```
O servidor ficará disponível em <http://localhost:8000> até você fechar a janela do Prompt ou pressionar `Ctrl + C`.

## 7. Usar o inicializador automático
Se preferir uma opção mais simples:
1. Ainda na pasta `C:\SMI`, dê um duplo clique em `start_app.bat`.
2. Na primeira execução, o script criará o ambiente virtual, instalará as dependências e iniciará o servidor automaticamente.
3. Nas próximas vezes, ele apenas ativará o ambiente, conferirá atualizações e abrirá o servidor.

## 8. Acessar a interface de testes
Abra o navegador e visite <http://localhost:8000/docs>. Ali você poderá testar todos os endpoints do sistema.

## 9. Encerrar o servidor
- Se estiver usando o terminal manualmente, pressione `Ctrl + C`.
- Se estiver usando o script, feche a janela do terminal quando terminar.

Pronto! Com esses passos você consegue instalar e iniciar o sistema mesmo sem experiência prévia com desenvolvimento.
