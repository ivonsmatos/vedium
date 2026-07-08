## Geração Automática de Schemas OpenAPI

Para endpoints críticos (pagamentos, inscrições), recomenda-se uso de ferramentas como [frappe-openapi](https://github.com/alyf-de/frappe-openapi) para gerar e manter schemas OpenAPI atualizados.

# Documentação da API do Vedium Core

## Visão Geral

Este documento descreve os endpoints de API personalizados disponíveis na aplicação `vedium_core`. Esses endpoints foram projetados para suportar o site público e o catálogo de cursos.

## Endpoints

### 1. Obter Cursos Publicados

Recupera uma lista de cursos publicados do LMS.

- **Endpoint**: `vedium_core.vedium_core.api.get_published_courses`
- **Método**: `GET`
- **Acesso**: Público (`allow_guest=True`)
- **Parâmetros**:
  - `category` (opcional): Filtrar por categoria de curso.
  - `limit` (opcional, padrão=10): Número de cursos para retornar.

- **Resposta**: Lista de objetos de curso contendo:
  - `name`: ID do Curso
  - `title`: Título do Curso
  - `short_introduction`: Breve descrição
  - `image`: Miniatura do curso
  - `paid_course`: Booleano indicando se é pago
  - `course_price`: Preço
  - `currency`: Moeda
  - `instructor_name`: Nome do instrutor principal
  - `lesson_count`: Número total de lições
  - `url`: URL direto para o curso

### 2. Obter Categorias de Cursos

Recupera todas as categorias de cursos disponíveis.

- **Endpoint**: `vedium_core.vedium_core.api.get_course_categories`
- **Método**: `GET`
- **Acesso**: Público (`allow_guest=True`)
- **Resposta**: Lista de categorias com `name`, `category_name` e `description`.

### 3. Obter Cursos em Destaque

Recupera uma lista de cursos populares baseada na contagem de matrículas.

- **Endpoint**: `vedium_core.vedium_core.api.get_featured_courses`
- **Método**: `GET`
- **Acesso**: Público (`allow_guest=True`)
- **Parâmetros**:
  - `limit` (opcional, padrão=6): Número de cursos para retornar.

### 4. Criar Sessão de Checkout

Inicia uma sessão de pagamento para um curso.

- **Endpoint**: `vedium_core.vedium_core.api.create_checkout_session`
- **Método**: `POST`
- **Acesso**: Apenas Usuários Autenticados
- **Parâmetros**:
  - `course_name`: O ID do curso para comprar.
- **Resposta**:
  - `checkout_url`: URL para redirecionar o usuário para pagamento.

### 5. Chat com Tutor IA

Interage com a persona de Tutor IA (Llama 3 via Groq).

> Estado atual: endpoint parcial. Antes de tratar como API de produção, criar
> e migrar os DocTypes `AI Persona`, `AI Interaction Log` e `Vedium Settings`,
> além do fluxo de sessão descrito em
> `docs/plataforma/14-atendimento-e-tutor-ia.md`.

- **Endpoint**: `vedium_core.vedium_core.controllers.ai_controller.chat_with_tutor`
- **Método**: `POST`
- **Acesso**: Apenas Usuários Autenticados
- **Parâmetros**:
  - `message`: A pergunta do usuário.
  - `persona_id`: ID da `AI Persona`.
  - `context` (opcional): Contexto adicional para a pergunta.
- **Resposta**: String contendo a resposta da IA.
- **Limite de Taxa**: 50 mensagens/hora por usuário.
- **Erros**:
  - `PermissionError`: Se o usuário for Convidado ou o limite for excedido.

### 6. Suporte e Observabilidade

- **Abrir chamado de suporte**
  - **Endpoint**: `vedium_core.vedium_core.api.open_support_ticket`
  - **Método**: `POST`
  - **Acesso**: Usuário autenticado
  - **Parâmetros**: `subject`, `description`, `category` (opcional)
  - **Resposta**: `{ ticket_id }`

- **Listar meus chamados**
  - **Endpoint**: `vedium_core.vedium_core.api.get_my_tickets`
  - **Método**: `GET`
  - **Acesso**: Usuário autenticado
  - **Resposta**: Lista de chamados

- **Dashboard de monitoramento**
  - **Endpoint**: `vedium_core.vedium_core.api.get_monitoring_dashboard`
  - **Método**: `GET`
  - **Acesso**: Usuário autenticado
  - **Resposta**: Status de containers, disco, memória, alertas

### 7. Gamificação, Comunidade e Internacionalização

- **Emblemas do usuário**
  - **Endpoint**: `vedium_core.vedium_core.api.get_user_badges`
  - **Método**: `GET`
  - **Acesso**: Usuário autenticado
  - **Resposta**: Lista de emblemas e níveis

- **Leaderboard do curso**
  - **Endpoint**: `vedium_core.vedium_core.api.get_leaderboard`
  - **Método**: `GET`
  - **Parâmetros**: `course_name`
  - **Acesso**: Público
  - **Resposta**: Ranking de alunos

- **Tópicos do fórum**
  - **Endpoint**: `vedium_core.vedium_core.api.get_forum_topics`
  - **Método**: `GET`
  - **Parâmetros**: `course_name`
  - **Acesso**: Público
  - **Resposta**: Lista de tópicos

- **Links de comunidade**
  - **Endpoint**: `vedium_core.vedium_core.api.get_community_links`
  - **Método**: `GET`
  - **Parâmetros**: `course_name`
  - **Acesso**: Público
  - **Resposta**: Lista de links

- **Idiomas do curso**
  - **Endpoint**: `vedium_core.vedium_core.api.get_course_languages`
  - **Método**: `GET`
  - **Parâmetros**: `course_name`
  - **Acesso**: Público
  - **Resposta**: Lista de idiomas

- **Acessibilidade do curso**
  - **Endpoint**: `vedium_core.vedium_core.api.get_accessibility_features`
  - **Método**: `GET`
  - **Parâmetros**: `course_name`
  - **Acesso**: Público
  - **Resposta**: Lista de recursos

### 8. Sessões, Flashcards e Exercícios

- **Sessões do curso**
  - **Endpoint**: `vedium_core.vedium_core.api.get_course_sessions`
  - **Método**: `GET`
  - **Parâmetros**: `course_name`
  - **Acesso**: Público
  - **Resposta**: Lista de sessões

- **Flashcards do curso**
  - **Endpoint**: `vedium_core.vedium_core.api.get_flashcards`
  - **Método**: `GET`
  - **Parâmetros**: `course_name`
  - **Acesso**: Público
  - **Resposta**: Lista de flashcards

- **Exercício de escuta ativa**
  - **Endpoint**: `vedium_core.vedium_core.api.submit_listening_exercise`
  - **Método**: `POST`
  - **Parâmetros**: `course_name`, `audio_url`
  - **Acesso**: Usuário autenticado
  - **Resposta**: Status e resultado da análise

- **Exercício de fala**
  - **Endpoint**: `vedium_core.vedium_core.api.submit_speaking_exercise`
  - **Método**: `POST`
  - **Parâmetros**: `course_name`, `audio_url`
  - **Acesso**: Usuário autenticado
  - **Resposta**: Status e resultado da análise

### 9. Quiz e Certificados

- **Submeter tentativa de quiz**
  - **Endpoint**: `vedium_core.vedium_core.api.submit_quiz_attempt`
  - **Método**: `POST`
  - **Parâmetros**: `course_name`, `answers` (dict)
  - **Acesso**: Usuário autenticado
  - **Resposta**: Score, feedbacks

- **Emitir certificado**
  - **Endpoint**: `vedium_core.vedium_core.api.issue_certificate`
  - **Método**: `POST`
  - **Parâmetros**: `enrollment_name`
  - **Acesso**: Usuário autenticado
  - **Resposta**: Dados do certificado

- **Verificar certificado**
  - **Endpoint**: `vedium_core.vedium_core.api.verify_certificate`
  - **Método**: `GET`
  - **Parâmetros**: `code`
  - **Acesso**: Público
  - **Resposta**: Dados do certificado

## Notas de Implantação

Esses endpoints dependem do `frappe.whitelist` e devem ser acessados via `/api/method/<caminho_do_endpoint>`.
Exemplo: `https://app.vediums.com/api/method/vedium_core.vedium_core.api.get_published_courses`
