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