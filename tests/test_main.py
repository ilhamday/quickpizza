from playwright.sync_api import Page, expect
import time
import re

def test_homepage_title(page: Page):
    page.goto("https://quickpizza.grafana.com/browser.php")
    expect(page).to_have_title("")

def test_geolocation(page: Page, context):
    context.grant_permissions(["geolocation"])
    page.goto("https://quickpizza.grafana.com/browser.php")
    # find a button with "Get geolocation" text
    page.get_by_role("button", name="Get geolocation").click()

    expect(page.get_by_text("Lat: ? Long: ?")).not_to_be_visible()

    lat_long_text = page.locator("text=Lat:").text_content()
    assert "?" not in lat_long_text

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
