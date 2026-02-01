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

# Cookies
def test_cookie(page: Page, context):
    context.add_cookies([{
        "name": "test_cookie_id_001",
        "value": "1234value1234",
        "domain": ".grafana.com",
        "path": "/browser.php"
    }])

    page.goto('https://quickpizza.grafana.com/browser.php')

    page.get_by_role("button", name="Refresh cookies").click()
    #assert cookie for name=value
    expect(page.locator("#cookies-info-display")).to_contain_text("test_cookie_id_001=1234value1234")

# Checkbox
def test_checkbox(page: Page):
    page.goto('https://quickpizza.grafana.com/browser.php')

    btn_checkbox = page.get_by_role("checkbox", name="Checkbox test 1")
    checkbox_text = page.locator("#checkbox-info-display")

    # before clicking the checkbox
    expect(checkbox_text).to_have_text("No interaction")

    # 1st click - checked
    btn_checkbox.check()
    expect(checkbox_text).to_have_text("Thanks for checking the box")

    # 2nd click - unchecked
    btn_checkbox.uncheck()
    expect(checkbox_text).to_have_text("You've just unchecked the box")

# Number increment
def test_increment(page:Page):
    page.goto('https://quickpizza.grafana.com/browser.php')
    
    counter_display = page.locator("#counter-info-display")

    # assert default value
    expect(counter_display).to_have_text("Counter: 0")
    
    btn_increment = page.get_by_role("button", name="Increment")

    # click and assert 5 times, 1 to 5
    for i in range(1,6):
        btn_increment.click()
        expect(counter_display).to_have_text(f"Counter: {i}")

def test_normal_input_text_field(page: Page):
    page.goto('https://quickpizza.grafana.com/browser.php')

    input_text_field = page.locator("#text1")
    text_info = page.locator("#text-info-display")

    expect(text_info).to_have_text("No interaction")

    # focus on field
    input_text_field.focus()
    expect(text_info).to_have_text("focused on input text field")
    
    # focus on out of field
    input_text_field.blur()
    expect(text_info).to_have_text("focused out off input text field")

    # fill in the text field
    input_text_field.fill("Hai") # data type not yet tested.
    expect(text_info).to_have_text("Thanks for filling in the input text field")

    input_text_field.clear()
    expect(text_info).to_have_text("You've just removed everything from the input text field")

def test_disabled_field_text(page:Page):
    page.goto('https://quickpizza.grafana.com/browser.php')

    expect(page.locator("#input-text-disabled")).to_be_disabled()

def test_hidden_field_text(page:Page):
    page.goto('https://quickpizza.grafana.com/browser.php')

    expect(page.locator("#input-text-hidden")).to_be_hidden()

def test_select_number(page:Page):
    page.goto('https://quickpizza.grafana.com/browser.php')

    select_number_area = page.locator("#numbers-options")
    select_info_display = page.locator("#select-multiple-info-display")

    select_labels = ["Zero","One","Two","Three","Four","Five"]
    select_values = ["zero","one","two","three","four","five"]

    # select & assert each number one by one
    for select_label, select_value in zip(select_labels, select_values):
        select_number_area.select_option(label=select_label)
        expect(select_info_display).to_have_text(f"Selected: {select_value}")

    # select all numbers & assert them
    select_number_area.select_option(select_labels)
    expect(select_info_display).to_have_text("Selected: " + " ".join(select_values))