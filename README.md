# opencode-lmstudio-middleware

Middleware que permite a comunicação entre as aplicações **OpenCode** e **LMStudio**, facilitando o processamento de mensagens entre o LLM e o agente.

## Pré-requisitos

- Python 3.x instalado
- Aplicações OpenCode e LMStudio configuradas

## Instalação

Clone este repositório e instale as dependências necessárias:

```bash
git clone https://github.com/seu-usuario/opencode-lmstudio-middleware.git
cd opencode-lmstudio-middleware
pip install -r requirements.txt
```

## Instalação de Dependências

Instale as dependências necessárias com o comando:

```bash
pip install -r requirements.txt
```

## Configuração

1. **Defina a variável de ambiente** que indica o endereço e a porta do middleware:

    ```bash
    export LOCAL_ENDPOINT=http://localhost:8090/v1
    ```

2. **Copie o arquivo de configuração** `.opencode.json` para a raiz do seu diretório de usuário:

    ```bash
    cp .opencode.json ~/
    ```

## Configuração da Variável de Ambiente

Crie um arquivo `.env` na raiz do projeto ou defina a variável de ambiente `LM_STUDIO_BASE_URL` para apontar para o endereço do LMStudio. Por exemplo:

```bash
export LM_STUDIO_BASE_URL=http://192.168.1.6:1234
```

Se não for definida, o padrão será `http://localhost:1234`.

## Uso

Inicie o middleware antes de executar o OpenCode:

```bash
python main.py
```

Depois, execute o OpenCode normalmente.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Consulte o arquivo [LICENSE](LICENSE) para mais informações.