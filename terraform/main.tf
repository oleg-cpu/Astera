terraform {
    required_providers {
        aws = {

            source  = "hashicorp/aws"
            version = "~> 6.53.0"

            }

        }

        required_version = ">= 1.5.0"
    }

provider "aws" {
    region = "eu-north-1"
    }

resource "aws_vpc" "astera_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "astera-app-vpc"
  }
}

resource "aws_internet_gateway" "astera_igw" {
  vpc_id = aws_vpc.astera_vpc.id

  tags = {
    Name = "astera-app-igw"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.astera_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-north-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "astera-public-subnet"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.astera_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-north-1a"

  tags = {
    Name = "astera-private-subnet"
  }
}

resource "aws_subnet" "private_subnet_b" {
  vpc_id            = aws_vpc.astera_vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "eu-north-1b"

  tags = {
    Name = "astera-private-subnet-b"
  }
}

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "astera-rds-subnet-group"
  subnet_ids = [aws_subnet.private_subnet.id, aws_subnet.private_subnet_b.id]

  tags = {
    Name = "astera-db-subnet-group"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.astera_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.astera_igw.id
  }

  tags = {
    Name = "astera-public-route-table"
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_security_group" "ec2_sg" {
  name        = "astera-ec2-sg"
  description = "Allow web and SSH traffic to EC2"
  vpc_id      = aws_vpc.astera_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "astera-ec2-security-group"
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "astera-rds-sg"
  description = "Allow database traffic ONLY from EC2"
  vpc_id      = aws_vpc.astera_vpc.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2_sg.id]
  }
}

resource "aws_key_pair" "astera_ssh_key" {
  key_name   = "astera-deployed-key"
  public_key = var.ssh_public_key
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }
}

resource "aws_instance" "app_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  subnet_id = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  key_name = aws_key_pair.astera_ssh_key.key_name

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    delete_on_termination = true
  }
  tags = {
    Name = "astera-app-server"
  }
}

resource "aws_db_instance" "postgres_db" {
  allocated_storage      = 20
  max_allocated_storage  = 100
  engine                 = "postgres"
  engine_version         = "18.4"
  instance_class         = "db.t3.micro"

  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  skip_final_snapshot    = true
  publicly_accessible    = false

  tags = {
    Name = "astera-postgres-db"
  }
}
