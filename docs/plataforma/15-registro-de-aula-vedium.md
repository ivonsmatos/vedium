# Registro de Aula Vedium

Este pacote cria o fluxo pedagógico para professores registrarem aulas, chamada,
conteúdo aplicado, observações individuais e alertas para coordenação.

## DocTypes

### Registro de Aula Vedium

DocType principal, não público, com histórico de alterações ativo.

Campos principais:

- `curso`: Link para `LMS Course`.
- `turma`: Link para `LMS Batch`.
- `professor`: Link para `User`.
- `data_aula`: Date.
- `horario_inicio`: Time.
- `horario_termino`: Time.
- `link_google_meet`: Data/URL.
- `tema_aula`: Data.
- `objetivo_aula`: Small Text.
- `conteudo_aplicado`: Text Editor.
- `atividade_realizada`: Text Editor.
- `material_utilizado`: Small Text.
- `tarefa_indicada`: Small Text.
- `resumo_aula`: Text Editor.
- `problemas_tecnicos`: Small Text.
- `observacoes_gerais`: Text Editor.
- `status_registro`: Select com `Rascunho`, `Enviado`,
  `Revisado pela coordenação`, `Pendente de ajuste`, `Concluído`.
- `alunos`: tabela de `Aluno da Aula Vedium`.

### Aluno da Aula Vedium

Child Table usada dentro do registro de aula.

Campos:

- `aluno`: Link para `User`.
- `status_presenca`: Select com presença/falta/atraso.
- `horario_entrada` e `horario_saida`: Time.
- `justificativa`: Small Text.
- `participacao`, `compreensao`, `producao_oral`, `producao_escrita`,
  `pronuncia`: Select com `Não avaliado nesta aula`, `Baixa`, `Média`, `Alta`.
- `dificuldade_observada`, `evolucao_observada`, `observacao_individual`.
- `precisa_reforco`, `recomenda_mudanca_nivel`.
- `criar_alerta_coordenacao`, `tipo_alerta`, `prioridade`,
  `encaminhar_para_coordenacao`.

## Papéis

O setup cria dois papéis:

- `Vedium Professor`
- `Vedium Coordenacao Pedagogica`

Professor pode criar registros e editar os próprios registros enquanto estão em
`Rascunho` ou `Pendente de ajuste`. Coordenação e `System Manager` podem ver e
gerenciar todos.

## Workflow

Workflow criado: `Fluxo Registro de Aula Vedium`.

Transições:

- `Rascunho` -> `Enviado`: professor.
- `Enviado` -> `Revisado pela coordenação`: coordenação.
- `Enviado` -> `Pendente de ajuste`: coordenação.
- `Pendente de ajuste` -> `Enviado`: professor.
- `Revisado pela coordenação` -> `Concluído`: coordenação.

## Relatórios

Relatórios criados como Query Report:

- `Vedium - Frequencia por aluno`
- `Vedium - Frequencia por turma`
- `Vedium - Aulas por professor`
- `Vedium - Alertas de coordenacao`
- `Vedium - Alunos que precisam de reforco`
- `Vedium - Registros pendentes de revisao`

Relatórios ainda recomendados para uma segunda etapa:

- evolução por aluno com série temporal;
- conteúdo aplicado por turma;
- recomendação de mudança de nível;
- alunos com três faltas consecutivas.

## Automações

Implementado:

- registros com alerta na child table geram `ToDo` para usuários com papel de
  coordenação pedagógica;
- status `Pendente de ajuste` gera `ToDo` para o professor;
- registro em `Rascunho` por mais de 24h gera lembrete diário para o professor.

Recomendado para segunda etapa:

- alerta automático de três faltas consecutivas;
- dashboard visual da coordenação no Desk;
- regra de retenção/anonimização para observações sensíveis.

## Privacidade

Os dados deste fluxo são internos. O DocType não deve ser publicado no website.
Observações individuais ficam no Desk e devem ser acessadas apenas por professor
responsável, coordenação e administradores.

Boas práticas:

- atribuir `Vedium Professor` apenas a professores ativos;
- atribuir `Vedium Coordenacao Pedagogica` apenas à coordenação;
- evitar dados médicos, familiares ou sensíveis sem necessidade pedagógica real;
- usar o campo de alerta para encaminhamento, não para expor detalhes excessivos;
- revisar periodicamente quem tem acesso aos relatórios.
