from playwright.sync_api import Page, expect
import time
import re

def test_homepage_title(page: Page):
    page.goto("https://quickpizza.grafana.com/browser.php")
    expect(page).to_have_title("")

def test_geolocation(page: Page, context):
    context.set_geolocation({"latitude": 37.77, "longitude": -122.42}) # San Francisco

    page.goto("https://quickpizza.grafana.com/browser.php")
    # find a button with "Get geolocation" text
    page.get_by_role("button", name="Get geolocation").click()
    
    expect(page.locator("#geolocation-info-display")).to_contain_text("37.77")
    expect(page.locator("#geolocation-info-display")).to_contain_text("-122.42")

# 2 - Locale-info-display
def test_locale(page: Page):
    page.goto("https://quickpizza.grafana.com/browser.php")

    #redundant inding it by text "id-ID" then checking if it has text "id-ID". That's circular logic.
    # expect(page.get_by_text("id-ID")).to_have_text("id-ID")

    expect(page.get_by_text("id-ID")).to_be_visible()
    # expect(page.locator("#locale-info-display")).to_have_text("id-ID")

def test_network_online(page: Page):
    page.goto("https://quickpizza.grafana.com/browser.php")

    page.get_by_role("button", name="Refresh network status").click()
    expect(page.get_by_text("Network Status: true")).to_be_visible()

# emulate offline netwrok
def test_network_offline(page: Page, context):
    page.goto("https://quickpizza.grafana.com/browser.php")

    # offline
    context.set_offline(True)
    
    page.get_by_role("button", name="Refresh network status").click()
    expect(page.get_by_text("Network Status: false")).to_be_visible()

# timezone
def test_timezone(browser):
    context = browser.new_context(timezone_id="Asia/Jakarta")
    page = context.new_page()
    
    page.goto("https://quickpizza.grafana.com/browser.php")
    expect(page.locator("#timezone-info-display")).to_have_text("Timezone: Asia/Jakarta")
    
    context.close()

# User Agent
def test_user_agent(browser):
    context = browser.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
    page =  context.new_page()

    page.goto('https://quickpizza.grafana.com/browser.php')
    expect(page.locator('#useragent-info-display')).to_have_text('Your UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')

    context.close()