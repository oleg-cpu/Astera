variable "my_ip" {
  type        = string
  description = "IP address for secure SSH access"
}

variable "db_username" {
  type        = string
  description = "Username for PostgreSQL"
}

variable "db_password" {
  type        = string
  description = "Password for PostgreSQL"
  sensitive   = true
}

variable "db_name" {
  type        = string
  description = "The name of the PostgreSQL database to create"
}

variable "ssh_public_key" {
  type        = string
  description = "Public SSH key for EC2 instance access"
}
