import requests
from lxml import html

# Define the URLs of the two websites
website1_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=laptop&_sacat=0&rt=nc&LH_ItemCondition=1000'
website2_url = 'https://www.walmart.com/search?q=laptop'

# Define XPath expressions for both websites
xpath_data = {
    'website1': {
        'title': '//div[@class="srp-river-results clearfix"]//div[@class="s-item__title"]//span/text()',
        'price': '//div[@class="srp-river-results clearfix"]//span[@class="s-item__price"]/text()',
    },
    'website2': {
        'title': '//span[@data-automation-id="product-title"]/text()',
        'price': '//div[@data-automation-id="product-price"]//span[@class="w_iUH7"][1]/text()',
    }
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

# function to scrape the data from a website
def scrape_website(url, xpath_expr):
    print(f'Getting response from {url}\n')
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        page_content = html.fromstring(response.text)

        titles = page_content.xpath(xpath_expr['title'])
        prices = page_content.xpath(xpath_expr['price'])

        product_data = []
        for title, price in zip(titles, prices):
            title_text = title.strip()
            price_text = price.strip().replace(',', '').replace('$', '').replace('current price Now ','').replace('current price ','')  # removing characters and special characters
            product_data.append({
                'title': title_text,
                'price': float(price_text),
            })

        return product_data
    else:
        print(f'Failed to fetch the page. Status code: {response.status_code}')
        exit()


# scrape data from both websites
website1_data = scrape_website(website1_url, xpath_data['website1'])
website2_data = scrape_website(website2_url, xpath_data['website2'])


# Function to calculate statistics
def calculate_statistics(data):
    print(f'{len(data)}\n')
    prices = [product['price'] for product in data]
    print(prices)
    average_price = round(sum(prices) / len(prices),2)
    lowest_price = min(prices)
    highest_price = max(prices)

    return {
        'average_price': average_price,
        'lowest_price': lowest_price,
        'highest_price': highest_price,
    }


# Calculate statistics for each website
website1_stats = calculate_statistics(website1_data)
website2_stats = calculate_statistics(website2_data)

# Checking which website has the most affordable prices
cheapest_website = 'eBay' if website1_stats['average_price'] - website2_stats['average_price'] < website2_stats['average_price'] - website1_stats['average_price'] else 'Walmart'

# Print the results
print(f'eBay statistics: \n\t{website1_stats}\n')
print(f'Walmart statistics: \n\t{website2_stats}\n')
print(f'The website with the most affordable prices is: {cheapest_website}')
