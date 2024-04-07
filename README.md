# AWS Resource Management Portal

This is a web portal developed to manage resources in AWS, such as RDS, EKS, and EC2. The portal uses technologies like AJAX for dynamic filtering, Python with Flask as the web framework, and Boto3 to interact with AWS services.

## Project Structure

The project is structured as follows:

- **app.py**: This is the main file of the Flask application. It contains all the routing logic and handling of HTTP requests.

- **templates/index.html**: This file contains the HTML structure of the portal's homepage. It is dynamically rendered by Flask and includes AJAX scripts for resource filtering.

## Technologies Used

- **Flask**: Flask is a lightweight and flexible web framework for Python. It is used to build the web application and handle HTTP requests.

- **Boto3**: Boto3 is the official AWS library for Python. It allows interacting with AWS services programmatically and is used in this project to list and manage resources such as RDS, EKS, and EC2.

- **AJAX**: AJAX (Asynchronous JavaScript and XML) is a web development technique used to create interactive pages. In the context of this portal, it is used to perform asynchronous queries to the server and dynamically update the page content without reloading the entire page.

## Key Features

- **Resource Listing**: The portal allows listing resources such as EC2 instances, RDS databases, and EKS clusters.

- **Dynamic Filtering**: Resources can be dynamically filtered through AJAX queries, providing a smoother user experience.

- **AWS Integration**: Integration with AWS is achieved through the Boto3 library, enabling listing and manipulation of resources directly from the platform.

## Running the Project

1. Make sure you have Python installed on your machine.

2. Clone this repository.

3. Install the project dependencies by running `pip install -r requirements.txt`.

4. Export your AWS credentials as environment variables or configure the `~/.aws/credentials` file.

5. Run the Flask application with the command `python app.py`.

6. Access the portal in your web browser through the address `http://localhost:5000`.

## Configuring AWS Profiles

Before running the application, make sure to configure your AWS profiles in the app.py file. You can add your AWS profile configurations directly in the app.py script. Locate the section where AWS profiles are defined and replace them with your own AWS profiles.

Example:

```python
profiles = {
    "profile_name_1": "profile_name_1",
    "profile_name_2": "profile_name_2",
    ...
}
