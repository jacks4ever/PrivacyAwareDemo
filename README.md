# Privacy Aware Demo

A sandboxed demonstration web app that simulates a small social platform to highlight privacy concerns in modern applications.

## Purpose

This application serves as an educational tool to demonstrate how personal data can be leaked through poor API design, insufficient access controls, and inadequate data governance practices. It visually illustrates the importance of "privacy by design" principles in software development.

## Features

- User registration with name, email, and bio
- Public and private post creation
- Admin dashboard for user management
- Simulated third-party data scraper
- Demo mode that visually flags privacy leaks
- Docker containerization for safe demonstration
- Comprehensive logging of all data access

## Privacy Risks Demonstrated

This application intentionally demonstrates several common privacy vulnerabilities:

1. **Unprotected API Endpoints**: Shows how APIs without proper authentication can leak user data
2. **Overfetching**: Demonstrates how APIs that return more data than necessary can expose sensitive information
3. **Insufficient Access Controls**: Illustrates how poor authorization mechanisms can allow unauthorized access to private data
4. **Data Persistence Issues**: Shows how deleted data might still be accessible through certain interfaces

## Running the Demo

```bash
# Build and run the Docker container
docker-compose up --build

# Access the application at http://localhost:12000
```

## Demo Scenario

The application includes a pre-configured demo scenario with:
- Several user accounts with varying privacy settings
- A simulated third-party scraper that attempts to collect user data
- Visual indicators when privacy leaks occur

## Educational Value

This demonstration highlights:

1. **Privacy by Design**: The importance of incorporating privacy considerations from the beginning of the development process
2. **Data Minimization**: Why applications should only collect and process the minimum amount of data necessary
3. **Transparency**: How making data flows visible helps users understand where their information goes
4. **User Control**: The importance of giving users meaningful control over their personal information

## Disclaimer

This application intentionally contains privacy vulnerabilities for educational purposes. It should only be used in a controlled environment for demonstration and learning. Do not use any real personal information when testing this application.