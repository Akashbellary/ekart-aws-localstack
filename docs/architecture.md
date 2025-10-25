# EKart Store Architecture

## Overview
This document describes the architecture of the EKart Store e-commerce platform.

## Components

### Frontend (Next.js)
- Server-side rendered React application
- TypeScript for type safety
- Tailwind CSS for styling
- Three.js for 3D product visualization

### Backend (FastAPI)
- RESTful API built with Python FastAPI
- Pydantic models for data validation
- JWT authentication via AWS Cognito
- Integration with AWS services via boto3

### Infrastructure (AWS via LocalStack)
- **DynamoDB**: NoSQL database for all entities
- **S3**: Object storage for product images
- **Cognito**: User authentication and authorization
- **Lambda**: Serverless functions for async processing
- **API Gateway**: RESTful API endpoints
- **SQS**: Message queues for order processing
- **EventBridge**: Event-driven architecture
- **SES**: Transactional email delivery

## Data Flow

1. User interacts with Next.js frontend
2. Frontend calls FastAPI backend
3. Backend validates requests and interacts with AWS services
4. DynamoDB stores all data
5. Lambda functions process async tasks
6. SES sends email notifications

## Security

- All API endpoints require JWT authentication
- S3 buckets have private access control
- Cognito manages user credentials
- HTTPS enforced in production
