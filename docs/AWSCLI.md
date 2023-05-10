# Installing AWS CLI

AWS CLI is a command-line tool that enables you to interact with AWS services and manage your resources. Here are the steps to install AWS CLI on your computer.

## Prerequisites

Before you begin, make sure you have the following prerequisites:

- Python 3.9 installed on your computer. You can download Python 3 from the official website: https://www.python.org/downloads/
- A user account in AWS with the necessary permissions to access the AWS services you want to manage.

## Installation Steps

1. Open your terminal or command prompt.
2. Install AWS CLI using pip, which is a package manager for Python. Enter the following command:

    ```bash
    pip install awscli
    ```

3. Verify that AWS CLI is installed by entering the following command:

    ```bash
    aws --version
    ```

    This should display the version of AWS CLI that you just installed. If you get a "command not found" error, try adding the following directory to your `PATH` environment variable:

    ```bash
    export PATH=~/.local/bin:$PATH
    ```

    You can add this line to your `.bashrc` file to make it persistent across terminal sessions.

4. Configure AWS CLI by entering the following command:

    ```bash
    aws configure
    ```

    This command will prompt you for your AWS Access Key ID, Secret Access Key, default region name, and default output format. You can find your Access Key ID and Secret Access Key in the AWS Management Console under "My Security Credentials".

    Once you have entered your credentials and configuration settings, you're ready to start using AWS CLI!