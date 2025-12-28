from typing import Optional, Any
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


class UIUtils:
    """Application specific helper utilities for Playwright Page interactions.
    This is just a skeleton and should be extended for the AUT.
    """

    DEFAULT_TIMEOUT = 5000

    @staticmethod
    def wait_for_selector(page: Page, selector: str, timeout: Optional[int] = None, visible: bool = True):
        """Wait for selector to appear. Returns the element handle or None."""
        timeout = timeout if timeout is not None else UIUtils.DEFAULT_TIMEOUT
        state = "visible" if visible else "attached"
        try:
            return page.wait_for_selector(selector, state=state, timeout=timeout)
        except PlaywrightTimeoutError:
            return None

    @staticmethod
    def click(page: Page, selector: str, timeout: Optional[int] = None, force: bool = False):
        """Waits for selector and clicks it."""
        timeout = timeout if timeout is not None else UIUtils.DEFAULT_TIMEOUT
        el = UIUtils.wait_for_selector(page, selector, timeout=timeout, visible=True)
        if not el:
            raise PlaywrightTimeoutError(f"Could not find element to click: {selector}")
        return page.click(selector, timeout=timeout, force=force)

    @staticmethod
    def fill(page: Page, selector: str, text: str, timeout: Optional[int] = None):
        """Waits for selector and fills it with text (replaces existing)."""
        timeout = timeout if timeout is not None else UIUtils.DEFAULT_TIMEOUT
        el = UIUtils.wait_for_selector(page, selector, timeout=timeout, visible=True)
        if not el:
            raise PlaywrightTimeoutError(f"Could not find element to fill: {selector}")
        return page.fill(selector, text, timeout=timeout)

    @staticmethod
    def type_text(page: Page, selector: str, text: str, timeout: Optional[int] = None, delay: Optional[float] = 0):
        """Types text into an input, character by character (useful when fill doesn't work)."""
        timeout = timeout if timeout is not None else UIUtils.DEFAULT_TIMEOUT
        el = UIUtils.wait_for_selector(page, selector, timeout=timeout, visible=True)
        if not el:
            raise PlaywrightTimeoutError(f"Could not find element to type into: {selector}")
        return page.type(selector, text, delay=delay)

    @staticmethod
    def is_visible(page: Page, selector: str, timeout: Optional[int] = None) -> bool:
        """Returns True if selector is visible within timeout, else False."""
        timeout = timeout if timeout is not None else UIUtils.DEFAULT_TIMEOUT
        try:
            el = UIUtils.wait_for_selector(page, selector, timeout=timeout, visible=True)
            return el is not None and page.is_visible(selector)
        except Exception:
            return False

    @staticmethod
    def get_text(page: Page, selector: str, timeout: Optional[int] = None) -> Optional[str]:
        """Gets text content of the selector or None if not found."""
        timeout = timeout if timeout is not None else UIUtils.DEFAULT_TIMEOUT
        el = UIUtils.wait_for_selector(page, selector, timeout=timeout, visible=False)
        if not el:
            return None
        return page.text_content(selector)

    @staticmethod
    def get_attribute(page: Page, selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """Gets an attribute value from an element."""
        timeout = timeout if timeout is not None else UIUtils.DEFAULT_TIMEOUT
        el = UIUtils.wait_for_selector(page, selector, timeout=timeout, visible=False)
        if not el:
            return None
        return page.get_attribute(selector, attribute)

    @staticmethod
    def goto(page: Page, url: str, timeout: Optional[int] = None, wait_until: str = "load"):
        """Navigate to a URL with a sensible default timeout."""
        timeout = timeout if timeout is not None else UIUtils.DEFAULT_TIMEOUT
        return page.goto(url, timeout=timeout, wait_until=wait_until)

    @staticmethod
    def wait_for_navigation(page: Page, timeout: Optional[int] = None, wait_until: str = "load"):
        """Waits for page to reach given load state."""
        timeout = timeout if timeout is not None else UIUtils.DEFAULT_TIMEOUT
        return page.wait_for_load_state(wait_until, timeout=timeout)

    @staticmethod
    def take_screenshot(page: Page, path: str, full_page: bool = False):
        """Takes a screenshot and saves to path."""
        return page.screenshot(path=path, full_page=full_page)