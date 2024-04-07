from flask import Flask, render_template, request, jsonify, Response
import boto3
import csv
from io import StringIO
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

app = Flask(__name__)

profiles = {
    "account1": "Account 1",
    "account2": "Account 2",
    "account3": "Account 3",
    "account4": "Account 4",
    "account5": "Account 5",
    "account6": "Account 6",
    "account7": "Account 7",
    "account8": "Account 8",
    "account9": "Account 9",
    "account10": "Account 10",
    "account11": "Account 11",
    "account12": "Account 12",
    "account13": "Account 13",
    "account14": "Account 14",
    "account15": "Account 15",
    "account16": "Account 16",
    "account17": "Account 17",
    "account18": "Account 18",
    "account19": "Account 19",
    "account20": "Account 20",
    "account21": "Account 21",
    "account22": "Account 22",
    "account23": "Account 23",
    "account24": "Account 24",
    "account25": "Account 25"
}
def generate_csv(selected_account):
    all_resources = []
    if selected_account == 'all':
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_profile = {executor.submit(get_resources_for_account, boto3.Session(profile_name=profile_name)): profile_name for profile_name in profiles.values()}
            for future in concurrent.futures.as_completed(future_to_profile):
                profile_name = future_to_profile[future]
                try:
                    all_resources.extend(future.result())
                except Exception as exc:
                    print(f'Error fetching resources for profile {profile_name}: {exc}')
    elif selected_account:
        session = boto3.Session(profile_name=selected_account)
        all_resources.extend(get_resources_for_account(session))
    return all_resources

@app.route('/')
def index():
    return render_template('index.html', profiles=profiles)

@app.route('/instances', methods=['GET'])
def list_instances():
    selected_account = request.args.get('account')

    all_resources = []

    if selected_account == 'all':
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_profile = {executor.submit(get_resources_for_account, boto3.Session(profile_name=profile_name)): profile_name for profile_name in profiles.values()}
            for future in concurrent.futures.as_completed(future_to_profile):
                profile_name = future_to_profile[future]
                try:
                    all_resources.extend(future.result())
                except Exception as exc:
                    print(f'Error fetching resources for profile {profile_name}: {exc}')
    elif selected_account in profiles:
        session = boto3.Session(profile_name=selected_account)
        all_resources.extend(get_resources_for_account(session))

    return jsonify(all_resources)


def get_resources_for_account(session):
    resources = []

    # List EC2 instances
    for region_name in ['us-east-1', 'sa-east-1']:
        ec2 = session.resource('ec2', region_name=region_name)
        for instance in ec2.instances.all():
            tags = {tag['Key']: tag['Value'] for tag in instance.tags or []}
            launch_time = instance.launch_time.strftime("%Y-%m-%d %H:%M:%S")
            state = instance.state['Name']
            if state != 'terminated':  # Avoid adding 'terminated' resources
                resources.append({
                    'id': instance.id,
                    'type': 'EC2',
                    'name': tags.get('Name', ''),
                    'region': region_name,
                    'state': state,
                    'version': '',
                    'launch_time': launch_time,
                    'account': session.profile_name
                })

    # List RDS instances including read replicas
    for region_name in ['us-east-1', 'sa-east-1']:
        rds = session.client('rds', region_name=region_name)
        rds_instances = rds.describe_db_instances()['DBInstances']
        for db_instance in rds_instances:
            launch_time = db_instance['InstanceCreateTime'].strftime("%Y-%m-%d %H:%M:%S")
            state = db_instance['DBInstanceStatus']
            resources.append({
                'id': db_instance['DBInstanceIdentifier'],
                'type': 'RDS',
                'name': db_instance['DBInstanceIdentifier'],
                'region': region_name,
                'state': state,
                'version': db_instance['EngineVersion'],
                'launch_time': launch_time,
                'account': session.profile_name
            })
            # Check if it has read replicas
            if 'ReadReplicaDBInstanceIdentifiers' in db_instance:
                for replica_id in db_instance['ReadReplicaDBInstanceIdentifiers']:
                    resources.append({
                        'id': replica_id,
                        'type': 'RDS Replica',
                        'name': replica_id,
                        'region': region_name,
                        'state': state,
                        'version': db_instance['EngineVersion'],
                        'launch_time': launch_time,
                        'account': session.profile_name
                    })

    # List EKS clusters
    for region_name in ['us-east-1', 'sa-east-1']:
        eks = session.client('eks', region_name=region_name)
        clusters = eks.list_clusters()['clusters']
        for cluster_name in clusters:
            cluster_info = eks.describe_cluster(name=cluster_name)
            region = cluster_info['cluster'].get('region', 'N/A')
            resources.append({
                'id': cluster_info['cluster']['arn'],
                'type': 'EKS',
                'name': cluster_info['cluster']['name'],
                'region': region,
                'state': cluster_info['cluster']['status'],
                'version': cluster_info['cluster']['version'],
                'launch_time': cluster_info['cluster']['createdAt'],
                'account': session.profile_name
            })

    return resources

@app.route('/export_csv', methods=['GET'])
def export_csv():
    selected_account = request.args.get('account')
    if selected_account:
        all_resources = generate_csv(selected_account)
        if all_resources:
            csv_data = StringIO()
            csv_writer = csv.DictWriter(csv_data, fieldnames=all_resources[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(all_resources)
            csv_data.seek(0)
            return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=resource_data.csv'})
        else:
            return 'No resources found for the selected account.'
    else:
        return 'No account selected.'

if __name__ == '__main__':
    app.run(debug=True)
