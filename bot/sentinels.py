import requests
from bs4 import BeautifulSoup


class N64SwitchControllerSentinel():

    def __init__(self, url):
        self.url = url
        self.html = None
        self.status = None


    def load_html(self) -> None:
        """Attempt GET request on url and set text with page contents"""
        # Attempt HTTP request
        try:
            # Excecute GET request
            response = requests.get(self.url)
            # Raise error if status is not OK
            response.raise_for_status() 

            # Set self.html as page contents
            self.html = response.text
        # Print exception and exit if request fails
        except requests.exceptions.RequestException as e:
            print(e)
            raise RuntimeError("Unable to load HTML. Exiting.")
            sys.exit(1)

    def update_status(self):
        """Sets self.status according to status in self.html"""
        
        # Exit if HTML was not loaded properly
        if self.html is None:
            raise RuntimeError("HTML was not loaded properly. Exiting.")
            sys.exit(1)
        
        # Initialize BeautifulSoup parser
        soup = BeautifulSoup(self.html, 'html.parser')

        # Find status in HTML
        stock_info = soup.find("div", {"class": "product-info-stock-sku"})
        availability = stock_info.find("div", {"title": "Availability"})
        status = availability['class'][1]

        # Set status
        self.status = status

    def clear_html(self):
        """Set html to None as a safety net"""
        self.html = None
