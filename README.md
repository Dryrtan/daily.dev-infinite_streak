# Daily.dev Infinite Streak

Este projeto automatiza o processo de manutenção do streak de leitura no Daily.dev. O script faz login na plataforma, verifica se um post foi lido hoje e, se necessário, lê um post para manter o streak ativo. Ele roda em um loop contínuo com intervalo configurável.

## Funcionalidades

- **Automação de Login**: Faz login automaticamente no Daily.dev usando credenciais fornecidas.
- **Verificação de Streak**: Verifica se o streak de leitura já foi contado para o dia atual.
- **Leitura de Posts**: Se o streak não estiver atualizado, lê até 5 posts para garantir a contagem.
- **Execução em Loop**: Roda indefinidamente com intervalo configurável (padrão: 24 horas).
- **Logs Detalhados**: Exibe logs em tempo real com timestamps para facilitar o monitoramento.
- **Containerização**: Utiliza Docker para isolamento e facilidade de execução.

## Pré-requisitos

- Docker instalado no sistema.

## Instalação

1. Clone este repositório:
   ```
   git clone https://github.com/Dryrtan/daily.dev-infinite_streak.git
   cd daily.dev-infinite_streak
   ```

2. Construa a imagem Docker:
   ```
   docker build -t daily-dev-streak .
   ```

## Uso

Execute o container com as variáveis de ambiente necessárias:

```
docker run -e EMAIL=seu_email@example.com -e PASSWORD=sua_senha -e INTERVAL_HOURS=24 --name daily-dev-streak daily-dev-streak
```

Ou execute desta forma para rodar em background:

```
docker run -d -e EMAIL=seu_email@example.com -e PASSWORD=sua_senha -e INTERVAL_HOURS=24 --name daily-dev-streak daily-dev-streak
```

O script iniciará imediatamente e executará em loop, verificando e atualizando o streak conforme o intervalo de tempo (por padrão 24 horas).

## Variáveis de Ambiente

- `EMAIL`: Email usado para login no Daily.dev (obrigatório).
- `PASSWORD`: Senha correspondente ao email (obrigatório).
- `INTERVAL_HOURS`: Intervalo em horas entre execuções (opcional, padrão: 24).

## Logs

Os logs são exibidos em tempo real no terminal, incluindo:
- Início de cada execução.
- Etapas do processo de login e verificação.
- Status do streak.
- Próxima execução prevista.

Exemplo de log:
```
[18-11-2025 10:00:00] 🚀 Iniciando script com intervalo de 24 horas.
[18-11-2025 10:00:00] 🔄 Iniciando execução #1...
[18-11-2025 10:00:05] 🔐 Iniciando processo de login no Daily.dev...
...
[18-11-2025 10:01:00] ⏳ Aguardando 24 horas para a próxima execução, prevista para 19-11-2025 10:01:00...
```

## Estrutura do Projeto

- `main.py`: Script principal em Python.
- `Dockerfile`: Arquivo para construção da imagem Docker.
- `requirements.txt`: Dependências Python.

## Notas

- O script roda em modo headless (sem interface gráfica) para execução em servidores.
- Certifique-se de que as credenciais estejam corretas para evitar falhas de login.
- O intervalo padrão de 24 horas garante verificação diária, mas pode ser ajustado conforme necessário.

## Licença

Este é um projeto pessoal. Fique à vontade para alterar e usar da forma que você quiser, não irei dar manutenção a este projeto, ele é apenas uma prova de conceito. Encorajo você a não usar ele, dedique uma parte do seu dia para ler os posts do daily.dev, existe bastante material interessante por lá. Não me responsabilizo pelo que você vai fazer com este projeto, assuma seus B.O. Verifique os termos de serviço do Daily.dev antes de usar.
