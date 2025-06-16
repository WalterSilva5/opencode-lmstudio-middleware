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

## Configuração

1. **Defina a variável de ambiente** que indica o endereço e a porta do middleware:

    ```bash
    export LOCAL_ENDPOINT=http://localhost:8090/v1
    ```

2. **Copie o arquivo de configuração** `.opencode.json` para a raiz do seu diretório de usuário:

    ```bash
    cp .opencode.json ~/
    ```

## Uso

Inicie o middleware antes de executar o OpenCode:

```bash
python middleware.py
```

Depois, execute o OpenCode normalmente.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Consulte o arquivo [LICENSE](LICENSE) para mais informações.