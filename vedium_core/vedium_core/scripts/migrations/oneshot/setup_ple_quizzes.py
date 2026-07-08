# -*- coding: utf-8 -*-
"""Seed and expose PLE exercise quizzes and final exams.

This is the operational entry point for the PLE quiz rollout:

1. Upsert final exams and module fixation quizzes for Básico/Intermediário/Avançado.
2. Embed each module fixation quiz in a visible lesson.
3. Embed each final exam in the "Avaliação Final" chapter.
4. Sync native LMS navigation child tables and lesson counters.

Run:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.setup_ple_quizzes.run
"""

from vedium_core.scripts.migrations.oneshot import (
    fix_ple_chapter_lesson_references,
    fix_ple_quiz_lesson_content,
    seed_ple_avancado_activities,
    seed_ple_basico_activities,
    seed_ple_intermediario_activities,
)


def run():
    print("\n=== PLE Básico: quizzes e prova final ===")
    seed_ple_basico_activities.run()

    print("\n=== PLE Intermediário: quizzes e prova final ===")
    seed_ple_intermediario_activities.run()

    print("\n=== PLE Avançado: quizzes e prova final ===")
    seed_ple_avancado_activities.run()

    print("\n=== PLE: lições visíveis com blocos de quiz ===")
    fix_ple_quiz_lesson_content.run()

    print("\n=== PLE: navegação nativa do LMS ===")
    fix_ple_chapter_lesson_references.run()

    print("\nConcluído. Quizzes de exercícios e provas finais PLE configurados.")
