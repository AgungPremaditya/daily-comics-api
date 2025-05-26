output "instance_ip" {
  description = "Public IP address of the Lightsail instance"
  value       = aws_lightsail_instance.daily_comics.public_ip_address
}

output "instance_name" {
  description = "Name of the Lightsail instance"
  value       = aws_lightsail_instance.daily_comics.name
}

output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh ubuntu@${aws_lightsail_instance.daily_comics.public_ip_address}"
} 