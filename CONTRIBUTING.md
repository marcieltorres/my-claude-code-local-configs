# Contributing [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

Obrigado por considerar contribuir. Leia com calma antes de abrir uma issue ou PR.

## O que este repo é

Um lugar para compartilhar e documentar configurações locais do [Claude Code](https://code.claude.com) — `settings.json`, hooks de `PreToolUse`, e as decisões por trás delas. Não é uma biblioteca nem um serviço; é configuração e documentação.

## O que é aceito como contribuição

- Correções ou melhorias nas configs de exemplo (`settings.example.json`)
- Novas regras de hook, ou melhorias nas existentes
- Correções e melhorias na documentação
- Relato de problema ao usar as configs deste repo em outra máquina/setup

## Antes de abrir um PR

Abra uma issue primeiro. Qualquer mudança precisa ser discutida antes — isso evita retrabalho.

## Regra de sanitização

**Nunca commite dado real de máquina ou de empresa.** Isso inclui:

- Tokens, chaves de API, credenciais
- Caminhos absolutos específicos de uma máquina (`/Users/<nome>/...`)
- URLs de repositórios privados, nomes internos de organização/empresa
- Qualquer coisa de `.claude/settings.local.json` (esse arquivo é local por definição — nunca deveria estar versionado)

Configs de exemplo devem ser genéricas o suficiente para qualquer pessoa copiar e adaptar.

## Convenção de commit

[Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`). Sem `Co-Authored-By` de ferramentas de IA — o commit é seu.

## Onde entender as decisões

O racional por trás dos hooks (contrato de regra, formato de saída, limites conhecidos) está documentado em `.claude/plans/ideia.md` — é uma ideia em avaliação, ainda não implementada neste repo.

## Checklist antes do PR

- [ ] Nenhum dado sensível ou específico de máquina/empresa foi commitado
- [ ] Se mudou `settings.example.json`, validei com `python3 -m json.tool settings.example.json`
- [ ] Referenciei a issue relacionada no PR (`closes #XXXX`)
