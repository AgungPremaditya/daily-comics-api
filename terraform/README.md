# Daily Comics AWS Lightsail Terraform Configuration

This Terraform configuration deploys the Daily Comics application to AWS Lightsail.

## Prerequisites

1. [Terraform](https://www.terraform.io/downloads.html) installed (version >= 1.0.0)
2. AWS CLI configured with appropriate credentials
3. Your application code in a Git repository

## Configuration

1. Update the Git repository URL in `main.tf` (search for `git clone your-repo-url`)
2. (Optional) Modify variables in `variables.tf` to change:
   - AWS region
   - Environment name

## Deployment Steps

1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Review the deployment plan:
   ```bash
   terraform plan
   ```

3. Apply the configuration:
   ```bash
   terraform apply
   ```

4. After deployment, Terraform will output:
   - Instance IP address
   - Instance name
   - SSH command to connect to the instance

## Access the Application

The FastAPI application will be available at:
```
http://<instance_ip>:8000
```

## Cleanup

To destroy the infrastructure:
```bash
terraform destroy
```

## Security Notes

1. The instance uses Ubuntu 22.04 LTS
2. Python 3.8 is installed with all required dependencies
3. The application runs as a systemd service
4. Remember to configure your security group to allow only necessary ports (8000 for API) 