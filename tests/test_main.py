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
