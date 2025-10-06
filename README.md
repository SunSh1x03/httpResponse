# httpResponse

Utilitário de linha de comando que envia uma requisição HTTP simples via *sockets* para inspecionar rapidamente a resposta de um servidor.

## Visão Geral

O projeto surgiu como um exemplo minimalista de como podemos construir nossas próprias ferramentas quando bibliotecas mais completas não estão disponíveis. A nova versão foi atualizada para Python 3, ganhou uma interface de linha de comando e oferece feedback mais amigável em caso de falhas de conexão.

## Instalação

Não há dependências externas. Basta clonar este repositório e executar o script diretamente com Python 3.11 ou superior.

```bash
git clone https://github.com/<seu-usuario>/httpResponse.git
cd httpResponse
python3 httpcheck.py --help
```

## Uso

```bash
python3 httpcheck.py exemplo.com --path / --header "User-Agent: httpcheck/1.0"
```

Parâmetros principais:

- `host`: endereço do servidor que receberá a requisição;
- `--port`: porta TCP (padrão: 80);
- `--path`: caminho do recurso (padrão: `/`);
- `--method`: método HTTP (padrão: `GET`);
- `--header`: cabeçalhos adicionais (pode ser repetido);
- `--timeout`: tempo máximo de espera em segundos;
- `--version`: exibe a versão atual da ferramenta.

## Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
