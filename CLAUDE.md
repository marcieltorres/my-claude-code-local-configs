# CLAUDE.md

Instruções para agentes de IA trabalhando neste repositório.

## O que este repo é

Um lugar para compartilhar e documentar configurações locais do Claude Code (`settings.json`,
hooks de `PreToolUse`, e o racional por trás de cada decisão). Não há aplicação, servidor ou
biblioteca aqui — o conteúdo é configuração e documentação.

## Onde as coisas ficam

- `settings.example.json` — versão sanitizada do `settings.json` real, pra copiar/adaptar
- `.claude/hooks/` — scripts de hook versionados (quando existirem)
- `.claude/plans/ideia.md` — ideia em avaliação para uma engine de regras de hook mais robusta
  (repo separado, Python stdlib). **Não implementar a partir dela sem confirmação explícita** —
  é uma ideia futura, não uma tarefa aprovada.

## Regra de sanitização (a mais importante)

Nunca commitar neste repo:
- Tokens, chaves de API, credenciais
- Caminhos absolutos específicos de uma máquina (`/Users/<nome>/...`)
- URLs de repositórios privados ou nomes internos de empresa/organização
- Qualquer coisa vinda de `.claude/settings.local.json` (é local por definição)

Antes de propor uma mudança em qualquer arquivo de config de exemplo, revisar se algo
pessoal/específico de máquina não vazou.

## Fluxo de contribuição

1. Abrir uma issue antes de qualquer PR (ver `CONTRIBUTING.md`)
2. Seguir o `.github/PULL_REQUEST_TEMPLATE`
3. CI (`.github/workflows/pull_request.yml`) precisa passar — hoje só valida que os `.json`
   do repo são JSON válido
4. Commits em Conventional Commits, sem atribuição de IA

## Estilo

- Markdown e JSON com indentação de 2 espaços (ver `.editorconfig`)
- Nada de comentário `//` em `.json` — não é JSON válido
