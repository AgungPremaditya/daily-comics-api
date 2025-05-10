variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "instance_name" {
  description = "Name of the Lightsail instance"
  type        = string
  default     = "daily-comics-app"
}

variable "instance_bundle_id" {
  description = "The bundle ID for the Lightsail instance (size/plan)"
  type        = string
  default     = "nano_2_0"  # Smallest instance, 1 vCPU, 512 MB RAM
}

variable "environment" {
  description = "Environment (e.g., development, production)"
  type        = string
  default     = "development"
}

variable "repository_url" {
  description = "URL of the Git repository to clone"
  type        = string
  default     = "https://github.com/yourusername/daily-comics.git"
}

variable "supabase_url" {
  description = "Supabase URL for the application"
  type        = string
  sensitive   = true
}

variable "supabase_key" {
  description = "Supabase API key for the application"
  type        = string
  sensitive   = true
}