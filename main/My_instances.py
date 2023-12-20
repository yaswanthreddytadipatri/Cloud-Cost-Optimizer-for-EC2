import boto3
import psutil
import json
import csv

def get_ec2_instances_data():
    ec2 = boto3.resource('ec2')

    # Get all instances in the region
    instances = ec2.instances.all()

    # Store instance data
    instance_data = []

    for instance in instances:
        instance_id = instance.id
        instance_type = instance.instance_type

        # Get RAM and CPU utilization
        ram_utilization = psutil.virtual_memory().percent
        cpu_utilization = psutil.cpu_percent(interval=1)

        # Get highest RAM and CPU utilization
        ram_usage_stats = psutil.virtual_memory()
        highest_ram_usage = ram_usage_stats.percent
        highest_cpu_usage = psutil.cpu_percent(interval=1)

        # Estimate price (replace 'us-east-1' with your region)
        price = estimate_instance_price(instance_type, 'us-east-1')

        # Append data to the list
        instance_data.append({
            'instance_id': instance_id,
            'instance_type': instance_type,
            'ram_utilization_avg': ram_utilization,
            'cpu_utilization_avg': cpu_utilization,
            'highest_ram_utilization': highest_ram_usage,
            'highest_cpu_utilization': highest_cpu_usage,
            'price': price
        })

    return instance_data

def estimate_instance_price(instance_type, region):
    pricing_client = boto3.client('pricing', region_name=region)

    response = pricing_client.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region},
            {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': 'Linux'},
            {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'shared'},
        ]
    )

    price_list = response['PriceList']
    if price_list:
        on_demand_price = price_list[0]['terms']['OnDemand']
        price_dimensions = on_demand_price[list(on_demand_price.keys())[0]]['priceDimensions']
        price = list(price_dimensions.values())[0]['pricePerUnit']['USD']
        return price
    else:
        return None

if __name__ == "__main__":
    instances_data = get_ec2_instances_data()

    # Print the results
    for instance_data in instances_data:
        print("Instance ID:", instance_data['instance_id'])
        print("Instance Type:", instance_data['instance_type'])
        print("Avg RAM Utilization:", instance_data['ram_utilization_avg'], "%")
        print("Avg CPU Utilization:", instance_data['cpu_utilization_avg'], "%")
        print("Highest RAM Utilization:", instance_data['highest_ram_utilization'], "%")
        print("Highest CPU Utilization:", instance_data['highest_cpu_utilization'], "%")
        print("Estimated Price:", instance_data['price'], "USD")
        print("-----------------------------")

    # Save data to JSON file
    with open('ec2_instances_data.json', 'w') as json_file:
        json.dump(instances_data, json_file, indent=2)

    # Save data to CSV file
    csv_columns = instances_data[0].keys()
    csv_file_path = 'ec2_instances_data.csv'
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for data in instances_data:
            writer.writerow(data)

    print(f"Data saved to {json_file.name} and {csv_file_path}")