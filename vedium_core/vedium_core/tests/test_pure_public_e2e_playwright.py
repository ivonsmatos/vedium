"""E2E público opcional para o funil de marketing.

Não roda no CI por padrão. Para executar localmente:
VEDIUM_RUN_PUBLIC_E2E=1 pytest vedium_core/vedium_core/tests/test_pure_public_e2e_playwright.py
"""
import os

import pytest


pytestmark = pytest.mark.skipif(
    os.getenv("VEDIUM_RUN_PUBLIC_E2E") != "1",
    reason="E2E público opcional; habilite com VEDIUM_RUN_PUBLIC_E2E=1.",
)


def test_public_level_test_to_diagnostic_and_plans_flow():
    sync_api = pytest.importorskip("playwright.sync_api")
    playwright_errors = pytest.importorskip("playwright._impl._errors")
    base_url = os.getenv("VEDIUM_PUBLIC_E2E_URL", "https://vediums.com").rstrip("/")

    with sync_api.sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(headless=True)
        except playwright_errors.Error as exc:
            pytest.skip(f"Playwright browser not installed: {exc}")
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(f"{base_url}/teste-de-nivel", wait_until="domcontentloaded")
        assert "Teste de Nível" in page.title() or "Teste de Nível" in page.content()

        page.goto(f"{base_url}/aula-diagnostica", wait_until="domcontentloaded")
        assert page.locator("text=Aula diagnóstica").first.is_visible()
        assert page.locator("[data-vd-diagnostic='english']").first.get_attribute("href").startswith(
            "https://wa.me/5511911293075"
        )

        page.goto(f"{base_url}/planos", wait_until="domcontentloaded")
        assert page.locator("text=Planos").first.is_visible()
        assert page.locator("a[href='/teste-de-nivel']").first.is_visible()

        page.goto(f"{base_url}/matricula", wait_until="domcontentloaded")
        assert page.locator("text=Matrícula").first.is_visible()
        assert page.locator("#vd-platform-link").first.get_attribute("href").startswith(
            "https://app.vediums.com/lms/courses/"
        )

        page.goto(f"{base_url}/certificado", wait_until="domcontentloaded")
        assert page.locator("text=Verificar certificado").first.is_visible()
        browser.close()
