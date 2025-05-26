# Daily Comics

A FastAPI application that serves daily comics with AI-powered features.

## Local Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd daily-comics
```

2. Create and activate a virtual environment:
```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your configuration:
# - SUPABASE_URL=your_supabase_url
# - SUPABASE_KEY=your_supabase_key
# - OPENAI_API_KEY=your_openai_api_key
```

### Running the Application

1. Start the FastAPI server:
```bash
uvicorn api.main:app --reload
```

The application will be available at `http://localhost:8000`

API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Project Structure

```
daily-comics/
├── api/
│   ├── routes/        # API route handlers
│   ├── services/      # Business logic
│   └── integrations/  # External service integrations
├── db/
│   ├── repositories/  # Database repositories
│   └── exceptions/    # Custom database exceptions
├── models/           # Data models
├── scripts/
│   ├── commands/     # CLI commands
│   └── utils/        # Utility functions
└── terraform/        # Infrastructure as Code
```

### Database Management

1. Check database status:
```bash
python scripts/check_db.py
```

2. Setup database tables:
```bash
python scripts/setup_supabase.py
```

## Deployment

### AWS Lightsail Deployment

For deploying to AWS Lightsail, refer to the [Terraform deployment instructions](terraform/README.md).

The Terraform configuration includes:
- Ubuntu 22.04 LTS instance with 2GB RAM
- Automatic Python 3.8 installation
- SystemD service setup
- Security group configuration

### Manual Deployment

1. Ensure Python 3.8+ is installed on your server
2. Clone the repository and follow the local setup steps
3. Set up a process manager (e.g., systemd) to run the application
4. Configure your web server (e.g., Nginx) to proxy requests to the application

## Development

### Adding New Features

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Run tests (if available)
4. Submit a pull request

### Scripts

The `scripts/` directory contains various utility scripts:
- `check_db.py`: Verify database connection and status
- `setup_supabase.py`: Initialize database tables and schema

## Environment Variables

Required environment variables:
```
# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
APP_ENV=development
APP_DEBUG=true
APP_PORT=8000
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

Copyright (c) 2024 Daily Comics

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 