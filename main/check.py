
import boto3
import json
def get_ec2_pricing(region, instance_type):
    # Create a pricing client
    pricing_client = boto3.client('pricing', region_name=region)
 
    # Define the product and filter parameters
    product = 'AmazonEC2'
    filters = [
        {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
        {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
    ]
 
    # Get the pricing data
    response = pricing_client.get_products(
        ServiceCode=product,
        Filters=filters,
    )
 
    # Extract the price from the response
    price_list = response['PriceList']
    price_data = json.loads(price_list)
    price_dimensions = price_data['terms']['OnDemand'][list(price_data['terms']['OnDemand'].keys())[0]]['priceDimensions']
    price = next(iter(price_dimensions.values()))['pricePerUnit']['USD']
 
    return price
 
# Example usage
region = 'us-east-1'
instance_type = 't3.micro'
 
price = get_ec2_pricing(region=region, instance_type=instance_type)
print(f'The price for {instance_type} in {region} is ${price} per hour.')

# has context menu
# Compose