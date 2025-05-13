terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "daily-comics"  # Add this line to specify the profile
}

# Create a Lightsail instance
resource "aws_lightsail_instance" "daily_comics_app" {
  name              = var.instance_name
  availability_zone = "${var.aws_region}a"
  blueprint_id      = "ubuntu_24_04"
  bundle_id         = var.instance_bundle_id
  
  tags = {
    Name        = var.instance_name
    Environment = var.environment
    Application = "daily-comics"
  }

  user_data = <<-EOF
    #!/bin/bash
    # Update system packages
    sudo apt update -y
    sudo apt upgrade -y
    
    # Install Python and pip
    sudo apt install -y python3 python3-pip python3-venv git
    
    # Install Docker
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -a -G docker ubuntu
    
    # Create application directory with proper permissions
    sudo mkdir -p /home/ubuntu/daily-comics
    sudo chown -R ubuntu:ubuntu /home/ubuntu/daily-comics
    
    # Clone the application repository
    cd /home/ubuntu/daily-comics
    git clone ${var.repository_url} .
    
    # Set up Python virtual environment with correct permissions
    sudo -u ubuntu python3 -m venv /home/ubuntu/daily-comics/venv
    sudo -u ubuntu bash -c "source /home/ubuntu/daily-comics/venv/bin/activate && pip install -r requirements.txt"
    
    # Create .env file with Supabase credentials
    sudo -u ubuntu bash -c "cat > /home/ubuntu/daily-comics/.env << 'ENVFILE'
    SUPABASE_URL=${var.supabase_url}
    SUPABASE_KEY=${var.supabase_key}
    ENVFILE"
    
    # Set up systemd service for the application
    cat > /etc/systemd/system/daily-comics.service << 'SERVICE'
    [Unit]
    Description=Daily Comics FastAPI Application
    After=network.target
    
    [Service]
    User=ubuntu
    WorkingDirectory=/home/ubuntu/daily-comics
    ExecStart=/home/ubuntu/daily-comics/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    SERVICE
    
    # Enable and start the service
    sudo systemctl daemon-reload
    sudo systemctl enable daily-comics
    sudo systemctl start daily-comics
  EOF
}

# Open ports for the Lightsail instance
resource "aws_lightsail_instance_public_ports" "daily_comics_ports" {
  instance_name = aws_lightsail_instance.daily_comics_app.name

  port_info {
    protocol  = "tcp"
    from_port = 22
    to_port   = 22
  }

  port_info {
    protocol  = "tcp"
    from_port = 80
    to_port   = 80
  }

  port_info {
    protocol  = "tcp"
    from_port = 8000
    to_port   = 8000
  }
}

# Create a static IP for the Lightsail instance
resource "aws_lightsail_static_ip" "daily_comics_static_ip" {
  name = "${var.instance_name}_static_ip"
}

# Attach the static IP to the Lightsail instance
resource "aws_lightsail_static_ip_attachment" "daily_comics_static_ip_attachment" {
  static_ip_name = aws_lightsail_static_ip.daily_comics_static_ip.name
  instance_name  = aws_lightsail_instance.daily_comics_app.name
}