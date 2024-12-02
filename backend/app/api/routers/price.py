from fastapi import FastAPI, HTTPException
import boto3
import json

app = FastAPI()

# Define your lookup_price function
def lookup_price(name: str) -> dict:
    """Useful for looking up the price of a service."""
    print(f"Looking up price for {name} service")
    client = boto3.client('pricing', region_name='us-east-1')
    response = client.get_products(
        ServiceCode=name,
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'ServiceCode',
                'Value': name,
            },
        ],
        MaxResults=1
    )

    price_items = response.get('PriceList', [])
    if not price_items:
        return None

    price_item = price_items[0]
    price_json = json.loads(price_item)
    terms = price_json.get('terms', {})
    on_demand_terms = terms.get('OnDemand', {})
    for term_key, term_value in on_demand_terms.items():
        price_dimensions = term_value.get('priceDimensions', {})
        for pd_key, pd_value in price_dimensions.items():
            price_per_unit = pd_value.get('pricePerUnit', {})
            unit = pd_value.get('unit', 'Unknown unit')
            price_usd = price_per_unit.get('USD', '0')
            # Return price info
            return {'service': name, 'price_usd': price_usd, 'unit': unit}
    return 'task complete'

# Create an API endpoint
@app.post("/get-price/")
async def get_price(service_name: str):
    price_info = lookup_price(service_name)
    
    if not price_info:
        raise HTTPException(status_code=404, detail="Service not found or no price available")
    
    return price_info