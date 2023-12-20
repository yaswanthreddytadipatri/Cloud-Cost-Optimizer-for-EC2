import boto3
import csv

def get_all_instance_types():
    # Create a Boto3 EC2 client
    ec2_client = boto3.client('ec2')

    # Describe instance types using the describe_instance_types method
    response = ec2_client.describe_instance_types()

    # Extract and format instance type details
    instance_types = []
    for instance_type_info in response['InstanceTypes']:
        instance_storage_info = instance_type_info.get('InstanceStorageInfo', [])

        instance_type = {
            'Type': instance_type_info['InstanceType'],
            'VCPU': instance_type_info['VCpuInfo']['DefaultVCpus'],
            'Memory': instance_type_info['MemoryInfo']['SizeInMiB'] / 1024.0,
            'Storage (GB)': sum([block_device['SizeInGB'] for block_device in instance_storage_info]) if isinstance(instance_storage_info, list) else 0,
            'Network Performance': instance_type_info['NetworkInfo']['NetworkPerformance'],
            'EBS-Optimized': instance_type_info.get('EbsInfo', {}).get('EbsOptimizedInfo', {}).get('BaselineBandwidthInMbps'),
            'Price (USD)': get_pricing_info(instance_type_info['InstanceType'])  # Replace with actual pricing logic
        }
        instance_types.append(instance_type)

    return instance_types

def get_pricing_info(instance_type):
    # Placeholder for pricing logic
    # Implement your logic to retrieve pricing information for the given instance type
    # This may involve using the AWS Pricing API, Pricing Calculator, or Price List API
    return 'N/A'

def save_to_csv(data, filename='aws_instance_types_with_pricing.csv'):
    # Save the data to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    all_instance_types = get_all_instance_types()

    # Save instance types to CSV file
    save_to_csv(all_instance_types)
    print("Instance types with pricing saved to 'aws_instance_types_with_pricing.csv'")
