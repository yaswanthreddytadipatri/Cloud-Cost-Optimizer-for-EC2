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

# Initialize lists to store metric details and utilization data
ec2_metrics_data = []
cpu_utilization_data = []


# Iterate through EC2 metrics
for metric in response['Metrics']:
    # Retrieve the metric data for the metric
    metric_data = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': metric,
                    'Period': 6000,  # Half year period
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
    highest_utilization = max(utilization_data) if utilization_data else None

    # Append metric details and average utilization data to the list
    ec2_metrics_data.append({
        'MetricName': metric['MetricName'],
        'Namespace': metric['Namespace'],
        'Dimensions': metric['Dimensions'],
        'AverageUtilization': average_utilization,
        'HighestUtilization': highest_utilization,
    })

    

    # Check if the metric is CPUUtilization
    if metric['MetricName'] == 'CPUUtilization':
        # Append only CPUUtilization details to the CPU utilization data list
        cpu_utilization_data.append({
            'MetricName': metric['MetricName'],
            'Namespace': metric['Namespace'],
            'Dimensions': metric['Dimensions'],
            'AverageUtilization': average_utilization,
            'HighestUtilization': highest_utilization,
        })

# Save the EC2 metric details and average utilization data to a JSON file
with open('ec2_cloudwatch_metrics_average_data.json', 'w') as json_file:
    json.dump(ec2_metrics_data, json_file, indent=4)
print("File is saved as ec2_cloudwatch_metrics_average_data.json")

# Save only CPUUtilization details to a separate JSON file
with open('cpu_utilization_metrics_data.json', 'w') as cpu_json_file:
    json.dump(cpu_utilization_data, cpu_json_file, indent=4)
print("File is saved as cpu_utilization_metrics_data.json")



'''
----------------- Machine Learing ---------------------
'''


import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn import metrics
import matplotlib.pyplot as plt


data = cpu_utilization_data

# Extract relevant information and filter rows with empty 'InstanceId'
rows = []
for item in data:
    dimensions = item.get('Dimensions', [])
    instance_id = next((d.get('Value') for d in dimensions if d.get('Name') == 'InstanceId'), '')
    if instance_id:
        row = {
            'MetricName': item.get('MetricName', ''),
            'Namespace': item.get('Namespace', ''),
            'InstanceID': instance_id,
            'AverageUtilization': item.get('AverageUtilization', ''),
            'HighestUtilization': item.get('HighestUtilization', ''),
        }
        rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

print(df.to_string())

CPU_To_Be_Reduced = (df['AverageUtilization'] < 40) & (df['HighestUtilization'] < 40)

CPU_To_Be_Same = ((df['AverageUtilization'] > 40) & (df['AverageUtilization'] < 80)) & ((df['HighestUtilization'] > 40) & (df['HighestUtilization'] < 80))

CPU_To_Be_Increased = (df['AverageUtilization'] > 90)


Increase = df[CPU_To_Be_Increased]

Same = df[CPU_To_Be_Same]

Decrease = df[CPU_To_Be_Reduced]

if Increase.empty:
    print("\n\n\t CPU's to be Increase\n\n There is nothing to be increased\n\n")
else:
    print("\n\n\t CPU's to be Increase\n\n",Increase)

if Same.empty:
    print("\n\n\t CPU's to be Same\n\n There is nothing to be Same\n\n")
else:
    print("\n\n\t CPU's to be Increase\n\n",Same)

if Decrease.empty:
    print("\n\n\t CPU's to be Decrease\n\n There is nothing to be Decrease\n\n")
else:
    print("\n\n\t CPU's to be Decrease\n\n",Decrease)

print("\n\n")






# # Your provided JSON data
# json_data = cpu_utilization_data


# # Load JSON data into a Python object
# # data = json.loads(json_data)

# # Create a DataFrame from the JSON data
# df = pd.DataFrame(json_data)

# # Extracting Dimensions into separate columns
# for dim in df['Dimensions']:
#     if dim:
#         for d in dim:
#             df[d['Name'] + '_' + d['Value']] = 1

# # Drop the original 'Dimensions' column
# df.drop('Dimensions', axis=1, inplace=True)



# # Split the data into features (X) and target variable (y)
# X = df.drop(['MetricName', 'Namespace', 'AverageUtilization', 'HighestUtilization'], axis=1)
# y = df['AverageUtilization']

# # plt.plot(X,y)
# # plt.show()

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Define new_instance_df and align columns
# new_instance_data = {
#     'InstanceId_i-xyz': 1,
#     'InstanceType_t3.micro': 1,
#     'ImageId_ami-xyz': 1,
#     '': 1
# }

# new_instance_df = pd.DataFrame([new_instance_data])
# new_instance_df = new_instance_df.reindex(columns=X_train.columns, fill_value=0)

# # Train a linear regression model
# model = LinearRegression()
# model.fit(X_train, y_train)

# # Make predictions on the test set
# y_pred = model.predict(X_test)

# # Evaluate the model
# mse = metrics.mean_squared_error(y_test, y_pred)
# print(f'Mean Squared Error: {mse}')

# # Threshold for deciding whether to increase or decrease CPU
# threshold = 80

# # Predicted CPU Utilization for new instance
# new_instance_prediction = model.predict(new_instance_df)[0]

# print(f'Predicted CPU Utilization for new instance: {new_instance_prediction}')

# # Decision based on the threshold
# if new_instance_prediction > threshold:
#     print('Consider increasing CPU.')
# else:
#     print('Consider decreasing CPU.')


