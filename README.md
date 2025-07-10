# Google Drive Access Management Portal

## 🎯 Project Overview

A comprehensive web-based solution for managing Google Drive permissions, access control, and security monitoring. Built with Flask and featuring a modern, responsive UI with Bootstrap 5.

## ✨ Features Completed

### ✅ **Permission Management (Completed by 18/7/2025)**
- **Add Permissions**: Grant access to users, groups, or domains
- **Remove Permissions**: Revoke access with audit logging
- **Update Permissions**: Modify user roles (reader, writer, owner)
- **Granular Control**: Support for user, group, domain, and public access

### ✅ **Google OAuth and Service Account Authentication (Completed by 11/7/2025)**
- Secure OAuth 2.0 flow implementation
- Token management and refresh
- Enhanced scopes for full Drive API access
- Admin directory integration for group management

### ✅ **Access Listing by Folder, File, or User (Completed)**
- **File/Folder Permissions**: View all permissions for specific files
- **User Access Mapping**: See all files accessible by a specific user
- **Recursive Folder Analysis**: Deep dive into folder structures
- **Owner and Permission Details**: Complete visibility of access rights

### ✅ **Advanced Search and Filtering**
- **Smart Search**: Find files by name, type, or content
- **Filter by Type**: Documents, spreadsheets, folders
- **Permission-based Search**: Find files by access patterns
- **Real-time Results**: Instant search with modern interface

### ✅ **Audit Logs and Exportable Reports**
- **Complete Audit Trail**: Every action logged with timestamps
- **Exportable Reports**: JSON and CSV export capabilities
- **Filtered Reporting**: Date range and action type filters
- **Compliance Ready**: Structured logging for security audits

### ✅ **Inactive User Access Detection**
- **Configurable Time Periods**: 30, 60, 90+ day inactivity detection
- **Risk Assessment**: Identify stale permissions and security risks
- **Automated Notifications**: Email alerts for security teams
- **Cleanup Recommendations**: Actionable insights for access optimization

### ✅ **Batch Operations**
- **Bulk Permission Management**: Process multiple files simultaneously
- **Mass User Addition/Removal**: Efficient team onboarding/offboarding
- **Bulk Role Updates**: Change permissions across file sets
- **Progress Tracking**: Real-time operation status

### ✅ **Group and Service Account Support**
- **Google Groups Integration**: Manage group-based permissions
- **Domain-wide Policies**: Organization-level access control
- **Service Account Management**: API access control
- **Hierarchy Respect**: Maintain organizational structures

### ✅ **Sharing Restriction Enforcement**
- **Policy Compliance**: Enforce organizational sharing policies
- **Domain Restrictions**: Control external sharing
- **Public Link Management**: Monitor and control public access
- **Risk Mitigation**: Identify and flag policy violations

### ✅ **Scheduled Tasks and Email Alerts**
- **Automated Monitoring**: Background security scans
- **Scheduled Reports**: Weekly/monthly permission audits
- **Email Notifications**: Instant alerts for security events
- **Customizable Triggers**: Configurable alert conditions

### ✅ **Modern Responsive UI**
- **Bootstrap 5**: Modern, mobile-first design
- **Gradient Backgrounds**: Beautiful visual aesthetics
- **Interactive Components**: Dynamic forms and real-time updates
- **Accessibility**: WCAG compliant interface
- **Cross-platform**: Works on desktop, tablet, and mobile

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Font Awesome
- **APIs**: Google Drive API, Admin SDK
- **Authentication**: OAuth 2.0, Google Service Accounts
- **Styling**: Modern CSS with gradients and glassmorphism effects
- **Scheduling**: Background task scheduling with email notifications

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Setup
1. **Get Google Credentials**:
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google Drive API and Admin SDK
   - Create OAuth 2.0 credentials
   - Download as `credential.json`

2. **Configure Email Notifications** (Optional):
   ```python
   # Update email settings in gdapa-v8.py
   smtp_server = "smtp.gmail.com"
   sender_email = "your-email@gmail.com"
   sender_password = "your-app-password"
   ```

3. **Run the Application**:
   ```bash
   python gdapa-v8.py
   ```

4. **Access the Portal**:
   Open http://localhost:5004 in your browser

## 📱 User Interface

### Main Dashboard
- **Feature Cards**: Quick access to all major functions
- **Modern Design**: Gradient backgrounds with glassmorphism effects
- **Responsive Layout**: Adapts to all screen sizes
- **Navigation Bar**: Easy access to all features

### Permission Checker
- **Smart Query Interface**: Natural language permission queries
- **Interactive Results**: Real-time permission editing
- **Visual Indicators**: Color-coded permission levels
- **Action Buttons**: Direct edit/remove functionality

### Management Interface
- **Multi-step Forms**: Guided permission management
- **Validation**: Real-time form validation
- **Success/Error Handling**: Clear feedback on operations
- **Bulk Operations**: Checkbox selection for multiple files

## 🔧 Configuration

### Environment Variables
```bash
FLASK_SECRET_KEY=your-secret-key-here
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
ADMIN_EMAIL=admin@your-domain.com
```

### Email Configuration
```python
# Email settings in gdapa-v8.py
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"
```

## 📊 API Endpoints

### Permission Management
- `POST /api/add_permission` - Add new permission
- `POST /api/remove_permission` - Remove permission
- `POST /api/update_permission` - Update permission role

### Search and Query
- `GET /search` - Advanced file search
- `GET /permissions` - Permission checker interface
- `GET /audit` - Audit log viewer

### Reporting
- `GET /audit?export=json` - Export audit logs
- `GET /inactive?days=90` - Inactive user report

## 🔒 Security Features

- **OAuth 2.0 Authentication**: Secure Google account integration
- **Audit Logging**: Complete activity tracking
- **Permission Validation**: Verify access before operations
- **Error Handling**: Secure error messages without data exposure
- **CSRF Protection**: Built-in Flask security measures

## 📈 Monitoring and Alerts

### Scheduled Tasks
- **Weekly Inactive User Scans**: Automated security monitoring
- **Monthly Permission Audits**: Comprehensive access reviews
- **Real-time Violation Alerts**: Instant policy breach notifications

### Email Notifications
- **Inactive User Reports**: Detailed user activity summaries
- **Security Alerts**: Immediate notification of suspicious activities
- **System Status**: Application health and performance updates

## 🎨 UI Features

### Visual Design
- **Gradient Backgrounds**: Modern purple-blue gradients
- **Glassmorphism Effects**: Semi-transparent cards with blur effects
- **Smooth Animations**: Hover effects and transitions
- **Professional Typography**: Clean, readable fonts

### Interactive Elements
- **Dynamic Forms**: Real-time validation and feedback
- **Modal Dialogs**: Clean popup interfaces for actions
- **Progress Indicators**: Visual feedback for long operations
- **Responsive Tables**: Mobile-friendly data display

## 📝 Usage Examples

### Query Examples
```
# Check all permissions for a file
permissions of MyDocument.pdf

# Check specific user's access to a file
permissions of ProjectFolder user john@company.com

# List all files accessible by a user
permissions of user jane@company.com
```

### Batch Operations
```
# Add reader permission for multiple files
File IDs: file1, file2, file3
Operation: Add Permission
Email: team@company.com
Role: Reader
```

## 🚨 Timeline Compliance

- ✅ **Google OAuth and service account authentication** - Completed by 11/7/2025
- ✅ **Access listing by folder, file, or user** - Completed
- ✅ **Permission management (add/remove/change roles)** - Completed by 18/7/2025
- ✅ **Group and service account support** - Completed
- ✅ **Sharing restriction enforcement** - Completed
- ✅ **Audit logs and exportable reports** - Completed
- ✅ **Inactive user access detection** - Completed
- ✅ **Search, filter, and batch operations** - Completed
- ✅ **Scheduled tasks and email alerts** - Completed
- ✅ **Responsive UI** - Completed

## 🔄 Future Enhancements

- **Mobile App**: Native iOS/Android applications
- **Advanced Analytics**: Permission usage statistics and trends
- **Integration APIs**: Webhook support for external systems
- **Machine Learning**: Intelligent permission recommendations
- **SSO Integration**: SAML and LDAP authentication support

## 📞 Support

For technical support or feature requests, please contact the development team or refer to the audit logs for troubleshooting information.

---

**Built with ❤️ for secure Google Drive management**
