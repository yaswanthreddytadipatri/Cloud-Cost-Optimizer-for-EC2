import boto3
import datetime
import json

# Initialize the CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name='eu-north-1')

# Define the namespace for EC2 metrics
ec2_namespace = 'AWS/EC2'

# Define the time range (e.g., past 24 hours)
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(hours=24)  # Adjust the time range as needed

# List EC2-related CloudWatch metrics
response = cloudwatch.list_metrics(Namespace=ec2_namespace)

# Initialize a list to store metric details and utilization data
ec2_metrics_data = []

# Iterate through EC2 metrics
for metric in response['Metrics']:
    # Retrieve the metric data for the metric
    metric_data = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': metric,
                    'Period': 300,  # 5-minute period
                    'Stat': 'Average',
                },
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )

    # Get the utilization values from the metric data
    utilization_data = metric_data['MetricDataResults'][0]['Values'] if 'Values' in metric_data['MetricDataResults'][0] else []

    # Calculate the average utilization
    average_utilization = sum(utilization_data) / len(utilization_data) if utilization_data else None

    # Append metric details and average utilization data to the list
    ec2_metrics_data.append({
        'MetricName': metric['MetricName'],
        'Namespace': metric['Namespace'],
        'Dimensions': metric['Dimensions'],
        'AverageUtilization': average_utilization,
    })

# Save the EC2 metric details and average utilization data to a JSON file
with open('ec2_cloudwatch_metrics_average_data.json', 'w') as json_file:
    json.dump(ec2_metrics_data, json_file, indent=4)
print("File is saved as ec2_cloudwatch_metrics_average_data.json")
