SEARCH_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Files - Drive Access Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .navbar {
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }
        .main-content {
            margin-top: 100px;
            padding: 2rem 0;
        }
        .search-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            padding: 2rem;
            margin-bottom: 2rem;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light fixed-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fab fa-google-drive text-primary me-2"></i>
                Drive Access Portal
            </a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/permissions">Permissions</a></li>
                    <li class="nav-item"><a class="nav-link" href="/manage">Manage</a></li>
                    <li class="nav-item"><a class="nav-link active" href="/search">Search</a></li>
                    <li class="nav-item"><a class="nav-link" href="/audit">Audit</a></li>
                    <li class="nav-item"><a class="nav-link" href="/inactive">Inactive Users</a></li>
                    <li class="nav-item"><a class="nav-link" href="/batch">Batch Operations</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="main-content">
        <div class="container">
            <div class="search-card">
                <h2 class="mb-4 text-center">
                    <i class="fas fa-search text-primary me-2"></i>
                    Advanced File Search
                </h2>
                
                <form method="POST">
                    <div class="row">
                        <div class="col-md-8">
                            <label for="query" class="form-label">Search Query:</label>
                            <input type="text" name="query" id="query" class="form-control" 
                                   placeholder="Enter filename or keyword" required>
                        </div>
                        <div class="col-md-4">
                            <label for="file_type" class="form-label">File Type:</label>
                            <select name="file_type" id="file_type" class="form-select">
                                <option value="">All Types</option>
                                <option value="folder">Folders</option>
                                <option value="document">Documents</option>
                                <option value="spreadsheet">Spreadsheets</option>
                            </select>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary mt-3">
                        <i class="fas fa-search me-2"></i>Search
                    </button>
                </form>
            </div>
            
            {% if results %}
            <div class="search-card">
                <h3>Search Results ({{ results|length }} found)</h3>
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Type</th>
                                <th>Owner</th>
                                <th>Modified</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for file in results %}
                            <tr>
                                <td>{{ file.name }}</td>
                                <td>
                                    {% if file.mimeType == 'application/vnd.google-apps.folder' %}
                                        <i class="fas fa-folder text-warning"></i> Folder
                                    {% else %}
                                        <i class="fas fa-file text-primary"></i> File
                                    {% endif %}
                                </td>
                                <td>
                                    {% for owner in file.owners %}
                                        {{ owner.emailAddress }}
                                    {% endfor %}
                                </td>
                                <td>{{ file.modifiedTime }}</td>
                                <td>
                                    <a href="/permissions?file_id={{ file.id }}" class="btn btn-sm btn-outline-primary">
                                        <i class="fas fa-eye"></i> View Permissions
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

AUDIT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audit Logs - Drive Access Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .navbar {
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }
        .main-content {
            margin-top: 100px;
            padding: 2rem 0;
        }
        .audit-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            padding: 2rem;
            margin-bottom: 2rem;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light fixed-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fab fa-google-drive text-primary me-2"></i>
                Drive Access Portal
            </a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/permissions">Permissions</a></li>
                    <li class="nav-item"><a class="nav-link" href="/manage">Manage</a></li>
                    <li class="nav-item"><a class="nav-link" href="/search">Search</a></li>
                    <li class="nav-item"><a class="nav-link active" href="/audit">Audit</a></li>
                    <li class="nav-item"><a class="nav-link" href="/inactive">Inactive Users</a></li>
                    <li class="nav-item"><a class="nav-link" href="/batch">Batch Operations</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="main-content">
        <div class="container">
            <div class="audit-card">
                <h2 class="mb-4 text-center">
                    <i class="fas fa-clipboard-list text-primary me-2"></i>
                    Audit Trail
                </h2>
                
                <div class="row mb-4">
                    <div class="col-md-4">
                        <label for="start_date" class="form-label">Start Date:</label>
                        <input type="date" id="start_date" class="form-control">
                    </div>
                    <div class="col-md-4">
                        <label for="end_date" class="form-label">End Date:</label>
                        <input type="date" id="end_date" class="form-control">
                    </div>
                    <div class="col-md-4">
                        <label class="form-label">&nbsp;</label>
                        <button onclick="filterLogs()" class="btn btn-primary d-block w-100">
                            <i class="fas fa-filter me-2"></i>Filter
                        </button>
                    </div>
                </div>
                
                <button onclick="exportLogs()" class="btn btn-success mb-3">
                    <i class="fas fa-download me-2"></i>Export Report
                </button>
            </div>
            
            <div class="audit-card">
                <h3>Audit Logs ({{ logs|length }} entries)</h3>
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Action</th>
                                <th>User</th>
                                <th>Details</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for log in logs %}
                            <tr>
                                <td>{{ log.timestamp }}</td>
                                <td>
                                    <span class="badge 
                                        {% if 'failed' in log.action %}bg-danger
                                        {% elif 'add' in log.action %}bg-success
                                        {% elif 'remove' in log.action %}bg-warning
                                        {% else %}bg-primary{% endif %}">
                                        {{ log.action }}
                                    </span>
                                </td>
                                <td>{{ log.user }}</td>
                                <td>{{ log.details }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function filterLogs() {
            const startDate = document.getElementById('start_date').value;
            const endDate = document.getElementById('end_date').value;
            
            let url = '/audit?';
            if (startDate) url += 'start_date=' + startDate + '&';
            if (endDate) url += 'end_date=' + endDate;
            
            window.location.href = url;
        }
        
        function exportLogs() {
            const startDate = document.getElementById('start_date').value;
            const endDate = document.getElementById('end_date').value;
            
            let url = '/audit?export=true&';
            if (startDate) url += 'start_date=' + startDate + '&';
            if (endDate) url += 'end_date=' + endDate;
            
            window.open(url, '_blank');
        }
    </script>
</body>
</html>
"""

INACTIVE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inactive Users - Drive Access Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg glass-card mb-4">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/"><i class="fab fa-google-drive text-primary me-2"></i>Drive Access Portal</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/permissions">Permissions</a>
                <a class="nav-link" href="/manage">Manage</a>
                <a class="nav-link" href="/search">Search</a>
                <a class="nav-link" href="/audit">Audit</a>
                <a class="nav-link active" href="/inactive">Inactive</a>
                <a class="nav-link" href="/batch">Batch</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="glass-card p-4">
                    <h2 class="text-center mb-4 text-white">
                        <i class="fas fa-user-clock text-warning me-2"></i>Inactive Users Detection
                    </h2>
                    
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <form method="GET" class="d-flex">
                                <input type="number" name="days" value="{{ days }}" class="form-control me-2" placeholder="Days">
                                <button type="submit" class="btn btn-primary">
                                    <i class="fas fa-search"></i> Check
                                </button>
                            </form>
                        </div>
                    </div>

                    {% if inactive_users %}
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Found {{ inactive_users|length }} inactive users (no activity for {{ days }} days)
                    </div>
                    
                    <div class="table-responsive">
                        <table class="table table-hover bg-white rounded">
                            <thead class="table-dark">
                                <tr>
                                    <th><i class="fas fa-user"></i> User Email</th>
                                    <th><i class="fas fa-file"></i> File Name</th>
                                    <th><i class="fas fa-calendar"></i> Last Modified</th>
                                    <th><i class="fas fa-cogs"></i> Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for user in inactive_users %}
                                <tr>
                                    <td>{{ user.email }}</td>
                                    <td>{{ user.file }}</td>
                                    <td>{{ user.last_modified }}</td>
                                    <td>
                                        <button class="btn btn-sm btn-danger" onclick="removeAccess('{{ user.email }}', '{{ user.file }}', this)">
                                            <i class="fas fa-user-times"></i> Remove Access
                                        </button>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% else %}
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle me-2"></i>
                        No inactive users found for the specified period.
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function removeAccess(email, file, buttonElement) {
            if (confirm(`Remove access for ${email} from ${file}?`)) {
                // Show loading state using the passed button element
                const originalHTML = buttonElement.innerHTML;
                buttonElement.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Removing...';
                buttonElement.disabled = true;
                
                // Make API call to remove access
                fetch('/api/remove-access', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        file: file,
                        test: true  // Enable test mode for demo emails
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Show success message
                        showAlert('success', data.message);
                        // Remove the row from the table
                        removeTableRow(email, file);
                    } else {
                        showAlert('danger', data.error || 'Failed to remove access');
                        // Restore button state on error
                        buttonElement.innerHTML = originalHTML;
                        buttonElement.disabled = false;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('danger', 'Network error occurred while removing access');
                    // Restore button state on error
                    buttonElement.innerHTML = originalHTML;
                    buttonElement.disabled = false;
                });
            }
        }
        
        function showAlert(type, message) {
            // Create alert element
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
            alertDiv.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            // Insert at the top of the container
            const container = document.querySelector('.container-fluid');
            container.insertBefore(alertDiv, container.firstChild);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 5000);
        }
        
        function removeTableRow(email, file) {
            // Find and remove the table row
            const rows = document.querySelectorAll('tbody tr');
            rows.forEach(row => {
                const emailCell = row.cells[0].textContent;
                const fileCell = row.cells[1].textContent;
                if (emailCell === email && fileCell === file) {
                    // Add a fade-out effect
                    row.style.transition = 'opacity 0.5s';
                    row.style.opacity = '0';
                    setTimeout(() => {
                        row.remove();
                        
                        // Check if table is now empty
                        const tbody = document.querySelector('tbody');
                        if (tbody.children.length === 0) {
                            // Replace table with success message
                            const tableContainer = document.querySelector('.table-responsive').parentNode;
                            tableContainer.innerHTML = `
                                <div class="alert alert-success">
                                    <i class="fas fa-check-circle me-2"></i>
                                    No inactive users found for the specified period.
                                </div>
                            `;
                        }
                    }, 500);
                }
            });
        }
    </script>
</body>
</html>
"""

BATCH_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Batch Operations - Drive Access Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg glass-card mb-4">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/"><i class="fab fa-google-drive text-primary me-2"></i>Drive Access Portal</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/permissions">Permissions</a>
                <a class="nav-link" href="/manage">Manage</a>
                <a class="nav-link" href="/search">Search</a>
                <a class="nav-link" href="/audit">Audit</a>
                <a class="nav-link" href="/inactive">Inactive</a>
                <a class="nav-link active" href="/batch">Batch</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="glass-card p-4">
                    <h2 class="text-center mb-4 text-white">
                        <i class="fas fa-tasks text-info me-2"></i>Batch Operations
                    </h2>

                    <form method="POST" class="mb-4">
                        <div class="row">
                            <div class="col-md-4">
                                <select name="operation" class="form-select" required>
                                    <option value="">Select Operation</option>
                                    <option value="add_permission">Add Permission</option>
                                    <option value="remove_permission">Remove Permission</option>
                                    <option value="change_role">Change Role</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                                <input type="text" name="file_pattern" class="form-control" placeholder="File pattern (e.g., *.pdf)" required>
                            </div>
                            <div class="col-md-4">
                                <input type="email" name="email" class="form-control" placeholder="User email" required>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-4">
                                <select name="role" class="form-select">
                                    <option value="reader">Reader</option>
                                    <option value="writer">Writer</option>
                                    <option value="owner">Owner</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                                <button type="submit" class="btn btn-primary w-100">
                                    <i class="fas fa-play"></i> Execute Batch Operation
                                </button>
                            </div>
                        </div>
                    </form>

                    {% if output %}
                    <div class="alert alert-info">
                        <h5><i class="fas fa-info-circle"></i> Operation Results:</h5>
                        {{ output|safe }}
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

ALERTS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configure Alerts - Drive Access Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        .alert-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        .alert-card:hover {
            transform: translateY(-5px);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg glass-card mb-4">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/"><i class="fab fa-google-drive text-primary me-2"></i>Drive Access Portal</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/permissions">Permissions</a>
                <a class="nav-link" href="/manage">Manage</a>
                <a class="nav-link" href="/search">Search</a>
                <a class="nav-link" href="/audit">Audit</a>
                <a class="nav-link" href="/inactive">Inactive</a>
                <a class="nav-link" href="/batch">Batch</a>
                <a class="nav-link active" href="/alerts">Alerts</a>
            </div>
        </div>
    </nav>

    <div class="container">
        {% if success %}
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            <i class="fas fa-check-circle me-2"></i>{{ success }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endif %}

        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="glass-card p-4">
                    <h2 class="text-center mb-4 text-white">
                        <i class="fas fa-bell text-warning me-2"></i>Configure Automated Alerts
                    </h2>
                    
                    <div class="row">
                        <!-- Alert Configuration Form -->
                        <div class="col-md-6">
                            <div class="alert-card p-4 mb-4">
                                <h4 class="text-white mb-3"><i class="fas fa-cog me-2"></i>New Alert</h4>
                                <form method="POST">
                                    <div class="mb-3">
                                        <label for="alert_type" class="form-label text-white">Alert Type</label>
                                        <select class="form-select" id="alert_type" name="alert_type" required>
                                            <option value="">Select Alert Type</option>
                                            <option value="permission_change">Permission Changes</option>
                                            <option value="new_file_shared">New Files Shared</option>
                                            <option value="external_sharing">External Sharing</option>
                                            <option value="inactive_users">Inactive Users</option>
                                            <option value="large_file_access">Large File Access</option>
                                            <option value="suspicious_activity">Suspicious Activity</option>
                                        </select>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="email" class="form-label text-white">Notification Email</label>
                                        <input type="email" class="form-control" id="email" name="email" required>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="frequency" class="form-label text-white">Frequency</label>
                                        <select class="form-select" id="frequency" name="frequency" required>
                                            <option value="immediate">Immediate</option>
                                            <option value="hourly">Hourly</option>
                                            <option value="daily">Daily</option>
                                            <option value="weekly">Weekly</option>
                                        </select>
                                    </div>
                                    
                                    <div class="mb-3 form-check">
                                        <input type="checkbox" class="form-check-input" id="enabled" name="enabled" checked>
                                        <label class="form-check-label text-white" for="enabled">
                                            Enable this alert
                                        </label>
                                    </div>
                                    
                                    <button type="submit" class="btn btn-warning w-100">
                                        <i class="fas fa-save me-2"></i>Save Alert Configuration
                                    </button>
                                </form>
                            </div>
                        </div>
                        
                        <!-- Alert Types Information -->
                        <div class="col-md-6">
                            <div class="alert-card p-4">
                                <h4 class="text-white mb-3"><i class="fas fa-info-circle me-2"></i>Alert Types</h4>
                                <div class="text-white">
                                    <div class="mb-3">
                                        <strong><i class="fas fa-user-lock text-warning me-2"></i>Permission Changes</strong>
                                        <p class="mb-2 small">Notifies when file or folder permissions are modified</p>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <strong><i class="fas fa-share text-info me-2"></i>New Files Shared</strong>
                                        <p class="mb-2 small">Alerts when new files are shared with external users</p>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <strong><i class="fas fa-external-link-alt text-danger me-2"></i>External Sharing</strong>
                                        <p class="mb-2 small">Monitors files shared outside the organization</p>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <strong><i class="fas fa-user-clock text-secondary me-2"></i>Inactive Users</strong>
                                        <p class="mb-2 small">Detects users with file access but no recent activity</p>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <strong><i class="fas fa-file-download text-success me-2"></i>Large File Access</strong>
                                        <p class="mb-2 small">Alerts on access to files larger than specified size</p>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <strong><i class="fas fa-shield-alt text-warning me-2"></i>Suspicious Activity</strong>
                                        <p class="mb-2 small">Detects unusual access patterns or bulk operations</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    {% if config %}
                    <div class="alert-card p-4 mt-4">
                        <h4 class="text-white mb-3"><i class="fas fa-check-circle text-success me-2"></i>Last Configuration</h4>
                        <div class="row text-white">
                            <div class="col-md-3">
                                <strong>Type:</strong><br>
                                <span class="badge bg-primary">{{ config.type }}</span>
                            </div>
                            <div class="col-md-3">
                                <strong>Email:</strong><br>
                                {{ config.email }}
                            </div>
                            <div class="col-md-3">
                                <strong>Frequency:</strong><br>
                                <span class="badge bg-info">{{ config.frequency }}</span>
                            </div>
                            <div class="col-md-3">
                                <strong>Status:</strong><br>
                                <span class="badge bg-{{ 'success' if config.enabled else 'secondary' }}">
                                    {{ 'Enabled' if config.enabled else 'Disabled' }}
                                </span>
                            </div>
                        </div>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
