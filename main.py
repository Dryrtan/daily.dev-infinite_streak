from playwright.sync_api import sync_playwright, TimeoutError
import os
import time
import datetime

def check_if_read(page):
    """Verifica se o ícone de streak indica que um artigo foi lido hoje."""
    print(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] 🔍 Verificando se o streak já foi contado hoje...")
    try:
        streak_button_selector = 'button[aria-label="Current streak"]'
        # Espera um pouco menos no "re check"
        page.wait_for_selector(streak_button_selector, timeout=5000)

        # O seletor para o path do SVG preenchido (artigo lido)
        path_selector = f'{streak_button_selector} svg path[d^="M12 24c6.627"]'

        if page.locator(path_selector).count() > 0:
            print(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] ✅ Streak já atualizado hoje.")
            return True
    except TimeoutError:
        print(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] ❌ Não foi possível encontrar o botão de streak durante a verificação.")
    print(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] ❌ Streak não foi contado ainda.")
    return False

def login_dailydev(email, password):
    """Faz login no Daily.dev e verifica/atualiza o streak de leitura."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Acessa o site
        page.goto("https://app.daily.dev/onboarding")

        # Aguarda e clica no botão de "login"
        page.wait_for_selector('button:has-text("Log in")')
        page.click('button:has-text("Log in")')

        # Preenche credenciais (ajuste os seletores conforme necessário)
        page.fill('input[type="email"]', email)
        page.fill('input[type="password"]', password)
        page.click('button[type="submit"]')

        # Aguarda o login
        page.wait_for_load_state('domcontentloaded')

        has_read_today = check_if_read(page)

        if not has_read_today:
            print("Nenhum artigo lido hoje. Tentando ler um artigo para atualizar o streak...")
            articles = page.locator("article")
            articles_count = articles.count()

            if articles_count == 0:
                print("Nenhum artigo encontrado na página.")
            else:
                # Tenta ler até 5 artigos para garantir
                for i in range(min(articles_count, 5)):
                    try:
                        print(f"Tentando ler o artigo {i + 1}...")
                        articles.nth(i).click()

                        # Aguarda o modal do artigo abrir e o botão de fechar aparecer
                        close_button_selector = 'button[data-state="closed"][aria-label="Close"]'
                        page.wait_for_selector(close_button_selector, timeout=10000)
                        page.click(close_button_selector)

                        # Aguarda um momento para a UI atualizar
                        page.wait_for_timeout(3000)

                        # Verifica novamente se o artigo foi contabilizado
                        if check_if_read(page):
                            has_read_today = True
                            print("Streak atualizado com sucesso!")
                            break # Sai do "loop" se o streak foi atualizado
                    except Exception as e:
                        print(f"Ocorreu um erro ao tentar ler o artigo {i + 1}: {e}")
                        # Se o modal não fechar, tenta recarregar a página para não ficar preso
                        page.reload()
                        page.wait_for_load_state('networkidle')

        browser.close()
        return has_read_today

if __name__ == "__main__":
    email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')
    interval_hours = int(os.environ.get('INTERVAL_HOURS', 24))

    if not email or not password:
        print(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] ❌ Erro: As variáveis de ambiente EMAIL e PASSWORD devem ser definidas.")
        exit(1)

    print(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] 🚀 Iniciando script com intervalo de {interval_hours} hora{'s' if interval_hours > 1 else ''}.")
    execution_count = 0

    while True:
        execution_count += 1
        print(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] 🔄 Iniciando execução #{execution_count}...")
        has_read = login_dailydev(email, password)
        if has_read:
            print(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] ✅ Já existem artigos lidos hoje; o streak está atualizado.")
        else:
            print(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] ⚠️ Nenhum artigo lido hoje; o streak ainda não foi contado.")
        print(f"[{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] ⏳ Aguardando {interval_hours} hora{'s' if interval_hours > 1 else ''} para a próxima execução, prevista para {(datetime.datetime.now() + datetime.timedelta(hours=interval_hours)).strftime('%d-%m-%Y %H:%M:%S')}...")
        time.sleep(interval_hours * 3600)
