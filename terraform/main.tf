terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_lightsail_instance" "daily_comics" {
  name              = "daily-comics-instance"
  availability_zone = "${var.aws_region}a"
  blueprint_id      = "ubuntu_22_04"
  bundle_id         = "medium_2_0" # 2GB RAM, 2 vCPUs
  
  user_data = <<-EOF
              #!/bin/bash
              # Update system
              sudo apt-get update
              sudo apt-get upgrade -y

              # Install Python 3.8 and pip
              sudo apt-get install -y python3.8 python3.8-venv python3-pip

              # Create app directory
              mkdir -p /opt/daily-comics
              cd /opt/daily-comics

              # Clone the application (you'll need to replace with your actual repo URL)
              # git clone your-repo-url .

              # Setup Python virtual environment
              python3.8 -m venv venv
              source venv/bin/activate

              # Install dependencies
              pip install -r requirements.txt

              # Setup systemd service
              cat > /etc/systemd/system/daily-comics.service <<EOL
              [Unit]
              Description=Daily Comics FastAPI Application
              After=network.target

              [Service]
              User=ubuntu
              WorkingDirectory=/opt/daily-comics
              Environment="PATH=/opt/daily-comics/venv/bin"
              ExecStart=/opt/daily-comics/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000

              [Install]
              WantedBy=multi-user.target
              EOL

              # Start and enable the service
              sudo systemctl start daily-comics
              sudo systemctl enable daily-comics
              EOF

  tags = {
    Name = "daily-comics"
    Environment = var.environment
  }
} 