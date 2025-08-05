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

### Technical Details of Vulnerabilities

For instructors, here are the specific technical vulnerabilities implemented in this application:

1. **API Endpoint Vulnerabilities**:
   - `/api/users` returns all users including their emails, even when users have set emails to private
   - `/api/posts` returns all posts including private ones that should only be visible to their authors
   - `/api/posts/all` returns "deleted" posts that should no longer be accessible

2. **Implementation Issues**:
   - The API doesn't validate authentication tokens for certain endpoints
   - Privacy settings are enforced in the UI but not consistently in the API
   - Soft-deleted data remains in the database and is accessible through certain endpoints
   - No rate limiting on API endpoints allows unrestricted data harvesting

3. **Demonstration Points**:
   - The scraper simulation shows how a third party can easily collect sensitive data
   - Access logs highlight when private data is accessed inappropriately
   - The demo mode visually flags privacy violations as they occur

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

### Instructor Demonstration Guide

Follow these steps to conduct an effective privacy demonstration:

1. **Setup and Login**:
   - Start the application using `docker-compose up --build`
   - Access the application at http://localhost:12000
   - Login with the admin account:
     - Username: `admin`
     - Password: `adminpass`

2. **Explore the User Interface**:
   - Show the admin dashboard at `/admin`
   - Demonstrate how user privacy settings are respected in the UI
   - Create a new post and set it to "private"

3. **Demonstrate Privacy Leaks**:
   - Navigate to the "Data Scraper Simulation" at `/scraper`
   - Click "Start Data Scraper" to begin the simulation
   - Point out how the scraper accesses:
     - Private emails that users marked as non-public
     - Private posts that should only be visible to their authors
     - "Deleted" posts that are still accessible through the API

4. **Access Logs and Visualization**:
   - Show the access logs at `/admin/logs`
   - Highlight the entries marked as "PRIVACY LEAK"
   - Explain how the application flags unauthorized data access

5. **User Perspective**:
   - Log out and log in as a regular user:
     - Username: `alice`
     - Password: `alicepass`
   - Show how the user interface respects privacy settings
   - Demonstrate that the user cannot see the privacy leaks occurring

6. **Discussion Points**:
   - Ask participants to identify the privacy vulnerabilities
   - Discuss how these issues could be fixed
   - Highlight real-world examples of similar privacy breaches
   - Emphasize the importance of privacy by design

## Educational Value

This demonstration highlights:

1. **Privacy by Design**: The importance of incorporating privacy considerations from the beginning of the development process
2. **Data Minimization**: Why applications should only collect and process the minimum amount of data necessary
3. **Transparency**: How making data flows visible helps users understand where their information goes
4. **User Control**: The importance of giving users meaningful control over their personal information

### Addressing the Vulnerabilities

For discussion purposes, here are ways these privacy issues could be fixed:

1. **Proper API Authentication and Authorization**:
   - Implement consistent token validation across all API endpoints
   - Add middleware that checks user permissions before returning data
   - Apply privacy settings filters at the database query level, not just in the UI

2. **Data Protection Measures**:
   - Implement proper data deletion practices (not just soft deletion)
   - Add field-level access controls based on user privacy settings
   - Use data masking for sensitive information like email addresses

3. **API Security Improvements**:
   - Implement rate limiting to prevent mass data harvesting
   - Add detailed logging and alerting for suspicious access patterns
   - Use proper HTTP status codes (401, 403) when access is denied

4. **Architectural Changes**:
   - Separate public and private data into different endpoints
   - Implement a proper authorization layer that's consistent across the application
   - Use a formal access control model (RBAC, ABAC) for all data access

## Disclaimer

This application intentionally contains privacy vulnerabilities for educational purposes. It should only be used in a controlled environment for demonstration and learning. Do not use any real personal information when testing this application.