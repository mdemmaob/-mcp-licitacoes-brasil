# FAQ - Perguntas Frequentes

**1. Preciso de autenticação para usar as APIs?**
- Para consultas básicas, não. Algumas integrações podem exigir token para dados avançados.

**2. Como adiciono uma nova fonte de dados?**
- Crie um novo módulo em `src/api/` e uma tool correspondente em `src/tools/`.

**3. Como faço backup do projeto?**
- Use o script `deployment/backup.sh`.

**4. Como monitorar o servidor?**
- Métricas Prometheus em `/metrics` e erros via Sentry.

**5. Como contribuo com o projeto?**
- Veja o arquivo [CONTRIBUTING.md](../CONTRIBUTING.md). 