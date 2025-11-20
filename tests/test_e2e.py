from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:5000"   


def test_add_book_and_verify_in_catalog():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Add book
        page.goto(f"{BASE_URL}/add_book")
 
        page.fill("input[name='title']", "E2E Test Book")
        page.fill("input[name='author']", "Test Author")
        page.fill("input[name='isbn']", "0987654321098")
        page.fill("input[name='total_copies']", "10")

        page.click("button[type='submit']")

        # check book was added to catalog
        page.goto(f"{BASE_URL}/catalog")
        
        book = page.locator("tr", has_text="E2E Test Book")
        
        assert book.locator("text=E2E Test Book").is_visible()
        assert book.locator("text=Test Author").is_visible()
        assert book.locator("text=0987654321098").is_visible()
        assert book.locator("text=10/10").is_visible()

        browser.close()

def test_borrow_book_and_get_patron_report():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Borrow book from catalog
        page.goto(f"{BASE_URL}/catalog")
        
        book_to_borrow = page.locator("tr", has_text="E2E Test Book")
        book_to_borrow.locator("input[name='patron_id']").fill("777000")
        book_to_borrow.locator("button[type='submit']").click()
        
        assert page.locator('text=Successfully borrowed "E2E Test Book"').is_visible()
        
        # get patron report
        page.goto(f"{BASE_URL}/patron")
        
        page.fill("input[name='patron_id']", "777000")
        page.click("button[type='submit']")
        
        assert page.locator('text=E2E Test Book').is_visible()
        
        browser.close()

def test_return_book():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Get book ID
        page.goto(f"{BASE_URL}/catalog")
        book = page.locator("tr", has_text="E2E Test Book")
        
        book_id = book.locator("td").nth(0).inner_text().strip()

        # Return Book
        page.goto(f"{BASE_URL}/return")
        
        page.fill("input[name='patron_id']", "777000")
        page.fill("input[name='book_id']", book_id)
        
        page.click("button[type='submit']")
        
        # Assertions
        
        assert page.locator('text=Book "E2E Test Book" has been returned').is_visible()
        
        browser.close()
