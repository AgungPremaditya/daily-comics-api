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
  blueprint_id      = "amazon_linux_2"
  bundle_id         = var.instance_bundle_id
  
  tags = {
    Name        = var.instance_name
    Environment = var.environment
    Application = "daily-comics"
  }

  user_data = <<-EOF
    #!/bin/bash
    # Update system packages
    sudo yum update -y
    
    # Install Python and pip
    sudo yum install -y python3 python3-pip git
    
    # Install Docker
    sudo amazon-linux-extras install docker -y
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -a -G docker ec2-user
    
    # Clone the application repository
    git clone ${var.repository_url} /home/ec2-user/daily-comics
    cd /home/ec2-user/daily-comics
    
    # Set up Python virtual environment
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Create .env file with Supabase credentials
    cat > /home/ec2-user/daily-comics/.env << 'ENVFILE'
    SUPABASE_URL=${var.supabase_url}
    SUPABASE_KEY=${var.supabase_key}
    ENVFILE
    
    # Set up systemd service for the application
    cat > /etc/systemd/system/daily-comics.service << 'SERVICE'
    [Unit]
    Description=Daily Comics FastAPI Application
    After=network.target
    
    [Service]
    User=ec2-user
    WorkingDirectory=/home/ec2-user/daily-comics
    ExecStart=/home/ec2-user/daily-comics/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000
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