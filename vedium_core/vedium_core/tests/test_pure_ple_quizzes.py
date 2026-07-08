import importlib
import pathlib
import sys
import types


def _throw(message):
    raise AssertionError(message)


APP_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(APP_ROOT))
sys.modules.setdefault("frappe", types.SimpleNamespace(throw=_throw))


PLE_ACTIVITY_MODULES = [
    "vedium_core.scripts.migrations.oneshot.seed_ple_basico_activities",
    "vedium_core.scripts.migrations.oneshot.seed_ple_intermediario_activities",
    "vedium_core.scripts.migrations.oneshot.seed_ple_avancado_activities",
]


def test_ple_quiz_banks_have_expected_shape():
    for module_name in PLE_ACTIVITY_MODULES:
        module = importlib.import_module(module_name)

        assert len(module.EXAM_QUESTIONS) == 80
        assert len(module.MODULE_FIXATION) == 3

        for questions in module.MODULE_FIXATION.values():
            assert len(questions) == 10

        all_questions = module.EXAM_QUESTIONS + [
            question
            for questions in module.MODULE_FIXATION.values()
            for question in questions
        ]
        for question_text, options, correct_idx in all_questions:
            assert question_text
            assert len(options) == 4
            assert correct_idx in range(4)


def test_ple_quiz_rollout_script_imports():
    module = importlib.import_module(
        "vedium_core.scripts.migrations.oneshot.setup_ple_quizzes"
    )

    assert callable(module.run)
