# SMI - Sistema de Gestão para Materiais Elétricos e Hidráulicos

Este repositório contém um protótipo de backend para controle de estoque, cadastro de parceiros, emissão de notas fiscais (simulada) e gestão de alertas.

## Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/) para a API REST.
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/) com SQLite para persistência.
- Simulação de integração fiscal para autorização de NF-e/NFC-e.

## Como obter o projeto

Antes de seguir para a execução, garanta que os arquivos estejam no seu computador. Você pode:

- fazer o download em formato ZIP diretamente do GitHub;
- ou clonar o repositório com `git clone` para manter o vínculo com o remoto.

O passo a passo completo está em [`docs/como_clonar_projeto.md`](docs/como_clonar_projeto.md).

## Como executar

1. Garanta que o [Python 3.10+](https://www.python.org/downloads/) esteja instalado. No Windows, abra o menu Iniciar, digite **Prompt de Comando** e pressione **Enter** para abrir o terminal. No macOS/Linux, abra o **Terminal**.

2. Dentro do terminal, navegue até a pasta do projeto. Por exemplo, se você salvou em `C:\SMI` no Windows:

   ```cmd
   cd C:\SMI
   ```

   No macOS/Linux:

   ```bash
   cd ~/SMI
   ```

3. Crie um ambiente virtual e instale as dependências.

   - **Windows (Prompt de Comando):**

     ```cmd
     python -m venv .venv
     .venv\Scripts\activate
     pip install -r requirements.txt
     ```

   - **macOS/Linux:**

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     pip install -r requirements.txt
     ```

   Após a execução, o terminal exibirá o prefixo `(.venv)` indicando que o ambiente está ativo. Para sair, use `deactivate`.

4. Inicie a API:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Acesse a documentação interativa em `http://localhost:8000/docs`.

Se preferir um passo a passo detalhado com imagens para o Windows, consulte o guia em [`docs/guia_iniciante_windows.md`](docs/guia_iniciante_windows.md).

### Execução facilitada no Windows

Para quem prefere iniciar o sistema com um duplo clique no Windows, o repositório inclui o arquivo `start_app.bat`.

1. Faça o download ou clone do projeto em uma pasta sem espaços no caminho (por exemplo, `C:\SMI`).
2. Clique duas vezes em `start_app.bat`. O script irá:
   - verificar a instalação do Python;
   - criar o ambiente virtual `.venv` (caso ainda não exista);
   - instalar as dependências;
   - iniciar o servidor na porta 8000.
3. Aguarde a mensagem `Uvicorn running` e abra `http://localhost:8000/docs` no navegador.

#### Criar um atalho com ícone personalizado

1. Clique com o botão direito em `start_app.bat` → **Enviar para** → **Área de trabalho (criar atalho)**.
2. No atalho criado na área de trabalho, clique com o botão direito → **Propriedades** → **Alterar ícone...** e escolha um arquivo `.ico` de sua preferência (por exemplo, um ícone de caixa ou estoque).
3. Opcional: renomeie o atalho para algo como `Iniciar Sistema SMI`.

Sempre que desejar iniciar o sistema, basta clicar nesse atalho.

### Como salvar e enviar suas alterações com Git

Se você estiver personalizando o sistema e deseja guardar suas modificações na nuvem, siga o guia básico de Git em [`docs/guia_git_basico.md`](docs/guia_git_basico.md). Ele explica como:

- configurar seu nome e e-mail no Git;
- verificar o status dos arquivos modificados;
- criar commits com mensagens claras;
- enviar (`git push`) as alterações para o repositório remoto.

Esse passo a passo complementa o processo de desenvolvimento para que você consiga compartilhar seu trabalho com outras pessoas ou manter um histórico seguro das suas alterações.

## Endpoints principais

- `POST /partners/suppliers` – cadastro de fornecedores.
- `GET /partners/suppliers/{id}` – consulta de fornecedor.
- `PUT /partners/suppliers/{id}` – atualização de cadastro.
- `DELETE /partners/suppliers/{id}` – exclusão (com validações de vínculo).
- `POST /partners/customers` – cadastro de clientes.
- `GET /partners/customers/{id}` – consulta de cliente.
- `PUT /partners/customers/{id}` – atualização de cadastro.
- `DELETE /partners/customers/{id}` – exclusão (impede remoção com notas vinculadas).
- `POST /products` – cadastro de produtos com validação de fornecedor e SKU.
- `GET /products/{id}` – consulta detalhada do produto com saldo atual de estoque.
- `PUT /products/{id}` – atualização de dados comerciais e fiscais.
- `DELETE /products/{id}` – remoção segura de produtos sem movimentações.
- `GET /products/{id}/inventory` – histórico de movimentações de estoque.
- `POST /products/{id}/inventory` – movimentação de estoque.
- `POST /invoices` – criação de notas com itens e baixa automática de estoque.
- `POST /invoices/{id}/authorize` – simulação de autorização fiscal.
- `GET /alerts` – listagem de alertas ativos.

## Próximos passos sugeridos

- Implementar autenticação e controle de acesso.
- Integrar com webservices oficiais da SEFAZ para autorização real de NF-e/NFC-e.
- Criar módulo financeiro (contas a pagar/receber) e dashboards analíticos.
- Adicionar testes automatizados e pipelines CI/CD.
