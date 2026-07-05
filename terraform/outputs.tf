output "ec2_public_ip" {
  value       = aws_instance.app_server.public_ip
  description = "Public IP address of our EC2 app server"
}

output "rds_endpoint" {
  value       = aws_db_instance.postgres_db.endpoint
  description = "The connection endpoint for the PostgreSQL database"
}
