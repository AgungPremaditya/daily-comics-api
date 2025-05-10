output "instance_ip" {
  description = "Public IP address of the Lightsail instance"
  value       = aws_lightsail_instance.daily_comics_app.public_ip_address
}

output "static_ip" {
  description = "Static IP address assigned to the Lightsail instance"
  value       = aws_lightsail_static_ip.daily_comics_static_ip.ip_address
}

output "instance_username" {
  description = "Username to SSH into the instance"
  value       = "ec2-user"
}

output "application_url" {
  description = "URL to access the FastAPI application"
  value       = "http://${aws_lightsail_static_ip.daily_comics_static_ip.ip_address}:8000"
}

output "api_docs_url" {
  description = "URL to access the FastAPI documentation"
  value       = "http://${aws_lightsail_static_ip.daily_comics_static_ip.ip_address}:8000/docs"
}