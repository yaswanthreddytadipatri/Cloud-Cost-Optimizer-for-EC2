
# Project Title

A brief description of what this project does and who it's for

# CloudWatch EC2 Details with Average Utilization

This Python script, named `CloudWatch_EC2_details_Average.py`, uses Boto3 and the AWS CloudWatch service to retrieve CloudWatch metrics data for Amazon EC2 instances. It provides information about the metrics and their average utilization values.

## Prerequisites

Before running the script, make sure you have the following in place:

- [Boto3](https://aws.amazon.com/sdk-for-python/): The AWS SDK for Python (Boto3) should be installed.
- AWS credentials: Ensure that your AWS credentials are correctly configured. You can use the AWS CLI or set environment variables to configure your credentials.

1. Install python 3.0

2. Install boto3
   ```sh
   pip install boto3

3. Install JSON
    ```sh
    pip install json

4. Install pandas
    ```sh
    pip install pandas

5. Install scikit-learn
    ```sh
    pip install scikit-learn

## Usage

1. Clone the repository to your local machine:

   ```sh
   git clone https://github.com/yaswanthreddytadipatri/Cloud-Cost-Optimizer-for-EC2.git

2. Edit the script (CloudWatch_EC2_details_Average.py) to customize the following parameters:

Region: Replace 'eu-north-1' with your desired AWS region.
EC2 namespace: If you want to retrieve metrics for specific namespaces other than AWS/EC2, modify the ec2_namespace variable.
Time range: Adjust the start_time and end_time variables to specify your desired time range.

3. Run the Script: 

    ```sh
    python CloudWatch_EC2_details_Average.py

4. The script will list the EC2-related CloudWatch metrics and compute the average utilization for each metric within the specified time range.

5. The metric details and average utilization data will be saved to a JSON file named "ec2_cloudwatch_metrics_average_data.json"




