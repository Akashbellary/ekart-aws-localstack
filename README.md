# EKart Store - Complete E-Commerce Platform

A modern, cloud-native e-commerce platform built with Next.js, FastAPI, and AWS services (emulated via LocalStack). Features include separate seller and buyer workflows, real-time inventory management, 3D product visualization, secure authentication, and comprehensive order processing.

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Three.js, Framer Motion
- **Backend**: Python FastAPI, Pydantic, boto3
- **Database**: DynamoDB (via LocalStack)
- **Authentication**: AWS Cognito
- **File Storage**: S3 (via LocalStack)
- **Event Processing**: Lambda, SQS, EventBridge
- **Email**: SES (via LocalStack)
- **Infrastructure**: CloudFormation, Docker

### AWS Services Used
- API Gateway - RESTful API endpoints
- Lambda - Serverless compute for order processing
- DynamoDB - NoSQL database for all entities
- S3 - Product images and file storage
- Cognito - User authentication and authorization
- SQS - Asynchronous message processing
- EventBridge - Event-driven architecture
- SES - Transactional email delivery
- CloudWatch - Monitoring and logging
- IAM - Access control and permissions
- CloudFormation - Infrastructure as Code

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.9+
- AWS CLI (configured for LocalStack)

### One-Command Setup
```
git clone <repository-url>
cd ekart-store
chmod +x scripts/*.sh
./scripts/setup-local.sh
make start
```

### Manual Setup
```
# 1. Install dependencies
make install

# 2. Start LocalStack
docker-compose up -d localstack

# 3. Deploy infrastructure
make deploy-infra

# 4. Seed sample data
make seed-data

# 5. Start all services
make start
```

## 🎯 Features

### For Buyers
- **Product Discovery**: Advanced search with filters, categories, and 3D product visualization
- **Shopping Cart**: Persistent cart with real-time inventory validation
- **Secure Checkout**: Multiple payment methods with order tracking
- **Order Management**: Real-time order status, shipping notifications
- **User Profile**: Order history, addresses, preferences

### For Sellers
- **Seller Dashboard**: Comprehensive analytics and order management
- **Product Management**: Easy product listing with image uploads and 3D model support
- **Inventory Control**: Real-time stock tracking with low-stock alerts
- **Order Fulfillment**: Order processing, shipping integration
- **Analytics**: Sales reports, customer insights, revenue tracking

### For Admins
- **System Administration**: User management, seller verification
- **Platform Analytics**: System-wide metrics, performance monitoring
- **Content Management**: Category management, featured products
- **Order Oversight**: Platform-wide order monitoring and support

## 🛠️ Development

### Available Commands
```
make help              # Show all available commands
make install           # Install all dependencies
make start             # Start all services
make stop              # Stop all services
make test              # Run all tests
make build             # Build all components
make clean             # Clean up containers and artifacts
```

### Project Structure
```
ekart-store/
├── backend/           # FastAPI backend service
├── frontend/          # Next.js frontend application
├── lambda-functions/  # AWS Lambda functions
├── infrastructure/    # CloudFormation templates
├── scripts/           # Setup and utility scripts
├── docs/             # Documentation
└── docker-compose.yml # Local development environment
```

### API Documentation
Once running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Testing
```
# Run all tests
make test

# Run specific test suites
cd backend && python -m pytest tests/test_products.py -v
cd frontend && npm test -- --testPathPattern=components
```

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```
# Backend Configuration
ENV=development
LOCALSTACK_ENDPOINT=http://localhost:4566
AWS_REGION=us-east-1

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_AWS_REGION=us-east-1
```

### LocalStack Configuration
LocalStack runs with the following services:
- DynamoDB (port 4566)
- S3 (port 4566)
- Lambda (port 4566)
- API Gateway (port 4566)
- Cognito (port 4566)
- SES (port 4566)
- SQS (port 4566)
- EventBridge (port 4566)

## 📊 Monitoring & Observability

### LocalStack Dashboard
- **URL**: http://localhost:4566/_localstack/cockpit
- **Features**: Resource browser, logs, metrics

### Application Logs
```
make logs              # View all service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Health Checks
```
make ready             # Check all service health
curl http://localhost:8000/health
curl http://localhost:4566/_localstack/health
```

## 🚢 Deployment

### Local Development
```
make dev-setup         # Complete dev environment setup
make start             # Start development servers
```

### Production Deployment
```
make build             # Build production images
make production        # Deploy to production environment
```

## 🤝 Contributing to LocalStack

This project is designed as a comprehensive sample for the LocalStack community. It demonstrates:

1. **Multi-service AWS architecture** using 10+ AWS services
2. **Event-driven patterns** with SQS, Lambda, and EventBridge
3. **Real-world e-commerce workflows** with proper error handling
4. **Modern frontend techniques** including 3D visualization
5. **Production-ready practices** with monitoring, testing, and documentation

### Key LocalStack Features Showcased
- **Service Integration**: Complex workflows across multiple AWS services
- **Event-Driven Architecture**: Async processing with queues and events
- **File Management**: S3 integration for product images and assets
- **Authentication**: Cognito user pools with JWT validation
- **Database Operations**: DynamoDB with GSI queries and streams
- **Email Services**: SES for transactional emails
- **Infrastructure as Code**: CloudFormation deployment automation

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- LocalStack team for providing excellent AWS emulation
- Next.js team for the amazing React framework
- FastAPI team for the high-performance Python web framework
- Three.js community for 3D web graphics capabilities

---

**Built with ❤️ for the LocalStack community**
