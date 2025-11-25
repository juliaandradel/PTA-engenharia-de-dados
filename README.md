<!-- PROJECT LOGO -->
<br />
<p align="center">
 <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados">
   <img src="https://ci3.googleusercontent.com/mail-sig/AIorK4zWbC3U-G_vTTZE6rUQqJjzL8u7WNZjzhEaYi9z7slJn8vNhgnFVootxjm377GVCdPGY_F64WolHmGJ" alt="Logo" width="180px">
 </a>
 <h3 align="center">PTA Engenharia de Dados</h3>
 <p align="center">
 Projeto criado em 2025.2 para a frente de engenharia de dados no Processo de Treinamento de Área (PTA) do CITi. Seguimos práticas modernas e visamos capacitação técnica alinhada às demandas reais da empresa.<br>
 <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados"><strong>Explore the docs »</strong></a><br><br>
   · <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados/issues">Report Bug</a>
   · <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados/issues">Request Feature</a>
 </p>
</p>


<!-- TABLE OF CONTENTS -->
## Tabela de Conteúdo


- [Sobre o Projeto](#sobre-o-projeto)
- [Como Instalar](#como-instalar)
- [Como Rodar](#como-rodar)
- [Endpoints da API](#endpoints-da-api)
- [Carga Inicial e Estrutura da Base](#carga-inicial-e-estrutura-da-base)
- [Exemplos de Tratamento](#exemplos-de-tratamento)
- [Garantia de Integridade Referencial](#garantia-de-integridade-referencial)
- [Integração n8n](#integracao-n8n)
- [Documentação Técnica da Arquitetura](#documentacao-tecnica-da-arquitetura)
- [Contato](#contato)


## Sobre o Projeto


Este projeto foi desenvolvido para o PTA do CITi, com foco em engenharia de dados. Possui uma API modular criada com FastAPI, permitindo fácil manutenção e escalabilidade. O principal objetivo é construir uma pipeline completa, acessível via API, que trata, garante integridade e integra dados de grandes planilhas (10.000+ linhas por aba), automatizando cargas e atualizações constantes.


## Como Instalar


1. Garanta instalação do **Python** e **Docker Desktop** na sua máquina.


2. Clone o repositório:
git clone https://github.com/CITi-UFPE/PTA-engenharia-de-dados.git


3. Acesse o diretório do projeto:
cd PTA-engenharia-de-dados


## Como Rodar


### Usando Docker


1. Inicie o Docker Desktop.


2. Suba os serviços com Docker Compose:


3. Acesse em seu navegador:
http://localhost:8000


4. Para a documentação interativa da API (Swagger UI), acesse:
http://localhost:8000/docs


### Localmente


1. Assegure-se de estar na raiz do projeto.


2. Instale as dependências:
pip install -r ./requirements.txt


3. Execute a aplicação:
uvicorn app.main:app


4. Acesse:
http://localhost:8000


5. Para a documentação interativa (Swagger UI):
http://localhost:8000/docs




## Endpoints da API


A API conta com os seguintes endpoints principais:
- `POST /reset-memory`: Reseta os dados temporários/memória usada para validação das referências.
- `POST /produtos-tratados`: Recebe lista de produtos e devolve versão tratada.
- `POST /vendedores-tratados`: Recebe lista de vendedores e devolve versão tratada.
- `POST /pedidos-tratados`: Recebe lista de pedidos e devolve versão tratada (com análise de status, prazos e datas).
- `POST /clean/items`: Recebe lista de itens dos pedidos, filtra órfãos e devolve versão pronta para uso.


## Carga Inicial e Estrutura da Base


A carga inicial trata os arquivos originais de produtos, vendedores, pedidos e itens com scripts Python, utilizando pandas e funções customizadas. Para cada tabela, são gerados arquivos estáticos `_tratados.csv`, prontos para carga e uso na API. O processo trata datas, status, valores, garante integridade referencial e substituição de ausências por medianas.


## Exemplos de Tratamento


Cada função de tratamento segue regras específicas:
- Pedidos: Normalização de datas, status, cálculo de entrega prevista e realizada, verificação de entrega no prazo e persistência dos IDs válidos.
- Itens dos pedidos: Filtragem por referências válidas (removendo órfãos), conversão e tratamento de preços, preenchimento de valores faltantes com a mediana de cada coluna.


## Garantia de Integridade Referencial


As operações de tratamento garantem que:
- Não existam order_items apontando para orders, products ou sellers inexistentes.
- Apenas linhas com referências válidas são mantidas na estrutura tratada e enviada para a API.
- As validações utilizam conjuntos armazenados temporariamente durante o processamento e carga.




## Integração n8n


O n8n é usado para orquestrar a atualização contínua da base. Ele envia dados das planilhas originais para os endpoints POST da API, automatizando a integração entre o Google Drive, scripts de tratamento e a base final em tempo real. Novos dados adicionados ao Google Sheets são processados e incorporados à base sem intervenção manual.






## Documentação Técnica da Arquitetura


O projeto utiliza o n8n para orquestrar a automação do pipeline de dados entre planilhas Google Sheets, a API FastAPI e o sistema de armazenamento dos dados tratados. A arquitetura é composta por três camadas principais: origem dos dados, processamento automatizado e persistência dos resultados.


### Comunicação Entre Componentes


- **Google Sheets Trigger:** O fluxo inicia automaticamente sempre que um novo item é adicionado à planilha original, chamada [Júlia] Data Lake.
- **Node Limit:** Isola o último registro inserido, garantindo o processamento incremental de novos dados.


- **Node JavaScript:** Transforma o item em um objeto JSON com propriedade `lista_pronta`, preparando para envio em lote ao endpoint.
const item = $input.item.json;
return {
json: {
lista_pronta: [item]
}
};


text
- **Node HTTP Request:** Realiza uma requisição POST para os endpoints da API (por exemplo, `/pedidos-tratados`) utilizando o JSON do nó anterior: `{{ $json.lista_pronta }}`. Isso garante que cada atualização seja validada pela API antes de entrar na base tratada.
- **Node If:** Avalia se o dado possui o campo `order_id` válido. Se verdadeiro, o registro é atualizado na planilha de destino e recebe status de integridade referencial. Se falso, é gerado aviso de rejeição.
- **Node Send Message:** Dependendo do resultado do IF, uma mensagem é enviada automaticamente por e-mail:
 - Sucesso: “O sistema detectou um novo item na planilha bruta. Resumo: Preço ajustado, data formatada, status salvo na aba "pedidos_tratados". Integridade verificada com sucesso.”
 - Falha: “O item com pedido {{ $json.order_id }} foi rejeitado pela API porque o ID não existe no banco de dados.”


### Garantia de Integridade e Atualização


A API executa regras estritas para garantir que itens, pedidos, produtos e vendedores estejam sempre referenciando entidades válidas. Linhas órfãs são rejeitadas, protegendo a consistência da base. O banco de dados, nesse fluxo, pode ser local (arquivo CSV) ou um banco relacional, e deve ser atualizado apenas com registros validados pela API.


### Como Rodar Todo o Pipeline


1. Configure e rode o Docker para iniciar a API FastAPI.
2. Prepare o workflow n8n com os nodes descritos, apontando os endpoints corretos e configurando triggers das suas planilhas de origem.
3. Certifique-se que as credenciais do Google Sheets e do tunnel (ngrok) estão válidas.
4. A cada novo registro na planilha, o n8n enviará de forma automatizada os dados para a API, que processará e devolverá o item tratado, pronto para ser salvo na base.
5. Monitore as mensagens de sucesso/rejeição para acompanhar o status dos dados.


Essa abordagem permite escalabilidade, auditoria automática e integração contínua entre o frontend da empresa (planilhas Google) e o backend analítico via API, utilizando o n8n como motor de automação e mensageria.




## Contato


- [CITi UFPE](https://github.com/CITi-UFPE) - [contato@citi.org.br](mailto:contato@citi.org.br)
- [João Pedro Bezerra](https://github.com/jpbezera), Líder de Dados em 2025.2 - [jpbmtl@cin.ufpe.br](mailto:jpbmtl@cin.ufpe.br)


