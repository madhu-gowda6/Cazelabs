# HTML Templates for the Google Drive Access Management Portal

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Drive Access Management Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #4285f4;
            --secondary-color: #34a853;
            --danger-color: #ea4335;
            --warning-color: #fbbc04;
        }
        
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
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .btn-custom {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            color: white;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .btn-custom:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(66, 133, 244, 0.3);
            color: white;
        }
        
        .hero-section {
            padding: 4rem 0;
            text-align: center;
            color: white;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .hero-subtitle {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        .features-grid {
            margin-top: 4rem;
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
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/permissions">Permissions</a></li>
                    <li class="nav-item"><a class="nav-link" href="/manage">Manage</a></li>
                    <li class="nav-item"><a class="nav-link" href="/search">Search</a></li>
                    <li class="nav-item"><a class="nav-link" href="/audit">Audit</a></li>
                    <li class="nav-item"><a class="nav-link" href="/inactive">Inactive Users</a></li>
                    <li class="nav-item"><a class="nav-link" href="/batch">Batch Operations</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="hero-section">
        <div class="container">
            <h1 class="hero-title">Google Drive Access Management</h1>
            <p class="hero-subtitle">Comprehensive permission management and security monitoring for your Google Drive</p>
            <a href="/permissions" class="btn btn-custom btn-lg me-3">
                <i class="fas fa-search me-2"></i>Check Permissions
            </a>
            <a href="/manage" class="btn btn-outline-light btn-lg">
                <i class="fas fa-cog me-2"></i>Manage Access
            </a>
        </div>
    </div>

    <div class="container features-grid">
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="card h-100 text-center p-4">
                    <i class="fas fa-shield-alt feature-icon"></i>
                    <h4>Permission Management</h4>
                    <p class="text-muted">Add, remove, and modify user permissions with granular control over file and folder access.</p>
                    <a href="/manage" class="btn btn-custom mt-auto">Manage Permissions</a>
                </div>
            </div>
            
            <div class="col-md-4 mb-4">
                <div class="card h-100 text-center p-4">
                    <i class="fas fa-search feature-icon"></i>
                    <h4>Advanced Search</h4>
                    <p class="text-muted">Search and filter files, folders, and permissions with powerful query capabilities.</p>
                    <a href="/search" class="btn btn-custom mt-auto">Search Files</a>
                </div>
            </div>
            
            <div class="col-md-4 mb-4">
                <div class="card h-100 text-center p-4">
                    <i class="fas fa-clipboard-list feature-icon"></i>
                    <h4>Audit & Reports</h4>
                    <p class="text-muted">Comprehensive audit trails and exportable reports for compliance and security monitoring.</p>
                    <a href="/audit" class="btn btn-custom mt-auto">View Audit Logs</a>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="card h-100 text-center p-4">
                    <i class="fas fa-users-slash feature-icon"></i>
                    <h4>Inactive User Detection</h4>
                    <p class="text-muted">Identify users with access but no recent activity to optimize security and licensing.</p>
                    <a href="/inactive" class="btn btn-custom mt-auto">Check Inactive Users</a>
                </div>
            </div>
            
            <div class="col-md-4 mb-4">
                <div class="card h-100 text-center p-4">
                    <i class="fas fa-tasks feature-icon"></i>
                    <h4>Batch Operations</h4>
                    <p class="text-muted">Perform bulk permission changes across multiple files and folders efficiently.</p>
                    <a href="/batch" class="btn btn-custom mt-auto">Batch Operations</a>
                </div>
            </div>
            
            <div class="col-md-4 mb-4">
                <div class="card h-100 text-center p-4">
                    <i class="fas fa-bell feature-icon"></i>
                    <h4>Automated Alerts</h4>
                    <p class="text-muted">Scheduled monitoring with email notifications for security events and policy violations.</p>
                    <a href="/alerts" class="btn btn-custom mt-auto">Configure Alerts</a>
                </div>
            </div>
        </div>
    </div>

    <footer class="text-center text-white py-4 mt-5">
        <div class="container">
            <p>&copy; 2025 Google Drive Access Management Portal. All rights reserved.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

PERMISSIONS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Permission Checker - Drive Access Portal</title>
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
        
        .results-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            padding: 2rem;
        }
        
        .search-input {
            border-radius: 25px;
            border: 2px solid #e0e0e0;
            padding: 15px 20px;
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }
        
        .search-input:focus {
            border-color: #4285f4;
            box-shadow: 0 0 0 0.2rem rgba(66, 133, 244, 0.25);
        }
        
        .search-btn {
            border-radius: 25px;
            padding: 15px 30px;
            background: linear-gradient(135deg, #4285f4, #34a853);
            border: none;
            font-weight: 600;
        }
        
        .example-queries {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin-top: 1rem;
        }
        
        .query-example {
            background: #fff;
            border-radius: 8px;
            padding: 0.8rem;
            margin: 0.5rem 0;
            border-left: 4px solid #4285f4;
            font-family: monospace;
            font-size: 0.9rem;
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
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link active" href="/permissions">Permissions</a></li>
                    <li class="nav-item"><a class="nav-link" href="/manage">Manage</a></li>
                    <li class="nav-item"><a class="nav-link" href="/search">Search</a></li>
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
                    Permission Checker
                </h2>
                
                <form method="POST" class="mb-4">
                    <div class="row align-items-end">
                        <div class="col-md-8">
                            <label for="query" class="form-label fw-bold">Enter your query:</label>
                            <input type="text" 
                                   name="query" 
                                   id="query"
                                   class="form-control search-input" 
                                   placeholder="e.g., permissions of MyDocument.pdf user john@example.com" 
                                   required>
                        </div>
                        <div class="col-md-4">
                            <button type="submit" class="btn search-btn text-white w-100">
                                <i class="fas fa-search me-2"></i>Check Permissions
                            </button>
                        </div>
                    </div>
                </form>
                
                <div class="example-queries">
                    <h5 class="mb-3"><i class="fas fa-lightbulb text-warning me-2"></i>Query Examples:</h5>
                    <div class="query-example">
                        <strong>File/Folder Permissions:</strong><br>
                        permissions of MyDocument.pdf
                    </div>
                    <div class="query-example">
                        <strong>User-Specific Permissions:</strong><br>
                        permissions of ProjectFolder user john@example.com
                    </div>
                    <div class="query-example">
                        <strong>All User Access:</strong><br>
                        permissions of user jane@example.com
                    </div>
                </div>
            </div>
            
            {% if output %}
            <div class="results-card">
                <h3 class="mb-4">
                    <i class="fas fa-list-alt text-success me-2"></i>
                    Results
                </h3>
                {{ output|safe }}
            </div>
            {% endif %}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function updatePermission(fileId, permissionId, currentRole) {
            const newRole = prompt('Enter new role (owner, writer, commenter, reader):', currentRole);
            if (newRole && newRole !== currentRole) {
                fetch('/api/update_permission', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        file_id: fileId,
                        permission_id: permissionId,
                        new_role: newRole
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Permission updated successfully!');
                        location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                });
            }
        }
        
        function removePermission(fileId, permissionId) {
            if (confirm('Are you sure you want to remove this permission?')) {
                fetch('/api/remove_permission', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        file_id: fileId,
                        permission_id: permissionId
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Permission removed successfully!');
                        location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                });
            }
        }
    </script>
</body>
</html>
"""

MANAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manage Permissions - Drive Access Portal</title>
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
        
        .management-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            padding: 2rem;
            margin-bottom: 2rem;
        }
        
        .action-btn {
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        
        .btn-add {
            background: linear-gradient(135deg, #34a853, #4caf50);
            color: white;
        }
        
        .btn-remove {
            background: linear-gradient(135deg, #ea4335, #f44336);
            color: white;
        }
        
        .btn-update {
            background: linear-gradient(135deg, #fbbc04, #ff9800);
            color: white;
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
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="/permissions">Permissions</a></li>
                    <li class="nav-item"><a class="nav-link active" href="/manage">Manage</a></li>
                    <li class="nav-item"><a class="nav-link" href="/search">Search</a></li>
                    <li class="nav-item"><a class="nav-link" href="/audit">Audit</a></li>
                    <li class="nav-item"><a class="nav-link" href="/inactive">Inactive Users</a></li>
                    <li class="nav-item"><a class="nav-link" href="/batch">Batch Operations</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="main-content">
        <div class="container">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <!-- Help Information -->
            <div class="alert alert-info mb-4">
                <h5 class="alert-heading"><i class="fas fa-info-circle me-2"></i>How to Use This Interface</h5>
                <p class="mb-2">This user-friendly interface allows you to manage Google Drive permissions using simple file names and email addresses:</p>
                <ul class="mb-0">
                    <li><strong>File/Folder Name:</strong> Enter the exact name as it appears in Google Drive (e.g., "Project Report.docx", "Photos Folder")</li>
                    <li><strong>Email Address:</strong> Enter the user's email address (e.g., "user@example.com")</li>
                    <li><strong>Multiple Files:</strong> If multiple files have the same name, the system will use the first one found</li>
                </ul>
            </div>
            
            <!-- Add Permission -->
            <div class="management-card">
                <h3 class="mb-4">
                    <i class="fas fa-plus-circle text-success me-2"></i>
                    Add Permission
                </h3>
                <form method="POST">
                    <input type="hidden" name="action" value="add_permission">
                    <div class="row">
                        <div class="col-md-6">
                            <label for="file_name_add" class="form-label">File/Folder Name:</label>
                            <input type="text" name="file_name" id="file_name_add" class="form-control" required 
                                   placeholder="Enter file or folder name (e.g., 'Project Report.docx')">
                            <div class="form-text">Enter the exact name of the file or folder as it appears in Google Drive</div>
                        </div>
                        <div class="col-md-6">
                            <label for="email_add" class="form-label">Email Address:</label>
                            <input type="email" name="email" id="email_add" class="form-control" required 
                                   placeholder="user@example.com">
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col-md-6">
                            <label for="role_add" class="form-label">Role:</label>
                            <select name="role" id="role_add" class="form-select">
                                <option value="reader">Reader</option>
                                <option value="commenter">Commenter</option>
                                <option value="writer">Writer</option>
                                <option value="owner">Owner</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label for="type_add" class="form-label">Type:</label>
                            <select name="type" id="type_add" class="form-select">
                                <option value="user">User</option>
                                <option value="group">Group</option>
                                <option value="domain">Domain</option>
                                <option value="anyone">Anyone</option>
                            </select>
                        </div>
                    </div>
                    <button type="submit" class="btn action-btn btn-add mt-3">
                        <i class="fas fa-plus me-2"></i>Add Permission
                    </button>
                </form>
            </div>
            
            <!-- Remove Permission -->
            <div class="management-card">
                <h3 class="mb-4">
                    <i class="fas fa-minus-circle text-danger me-2"></i>
                    Remove Permission
                </h3>
                <form method="POST">
                    <input type="hidden" name="action" value="remove_permission">
                    <div class="row">
                        <div class="col-md-6">
                            <label for="file_name_remove" class="form-label">File/Folder Name:</label>
                            <input type="text" name="file_name" id="file_name_remove" class="form-control" required 
                                   placeholder="Enter file or folder name (e.g., 'Budget.xlsx')">
                            <div class="form-text">Enter the exact name of the file or folder</div>
                        </div>
                        <div class="col-md-6">
                            <label for="email_remove" class="form-label">User Email:</label>
                            <input type="email" name="email" id="email_remove" class="form-control" required 
                                   placeholder="user@example.com to remove access from">
                            <div class="form-text">Email of the user whose access you want to remove</div>
                        </div>
                    </div>
                    <button type="submit" class="btn action-btn btn-remove mt-3">
                        <i class="fas fa-trash me-2"></i>Remove Permission
                    </button>
                </form>
            </div>
            
            <!-- Update Permission -->
            <div class="management-card">
                <h3 class="mb-4">
                    <i class="fas fa-edit text-warning me-2"></i>
                    Update Permission
                </h3>
                <form method="POST">
                    <input type="hidden" name="action" value="update_permission">
                    <div class="row">
                        <div class="col-md-4">
                            <label for="file_name_update" class="form-label">File/Folder Name:</label>
                            <input type="text" name="file_name" id="file_name_update" class="form-control" required 
                                   placeholder="Enter file or folder name">
                            <div class="form-text">Name of the file/folder to update</div>
                        </div>
                        <div class="col-md-4">
                            <label for="email_update" class="form-label">User Email:</label>
                            <input type="email" name="email" id="email_update" class="form-control" required 
                                   placeholder="user@example.com">
                            <div class="form-text">Email of user to update permissions for</div>
                        </div>
                        <div class="col-md-4">
                            <label for="new_role" class="form-label">New Role:</label>
                            <select name="new_role" id="new_role" class="form-select">
                                <option value="reader">Reader</option>
                                <option value="commenter">Commenter</option>
                                <option value="writer">Writer</option>
                                <option value="owner">Owner</option>
                            </select>
                        </div>
                    </div>
                    <button type="submit" class="btn action-btn btn-update mt-3">
                        <i class="fas fa-edit me-2"></i>Update Permission
                    </button>
                </form>
            </div>
            
            <div class="management-card">
                <h4 class="mb-3">
                    <i class="fas fa-info-circle text-info me-2"></i>
                    How to Find File/Permission IDs
                </h4>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">
                        <strong>File ID:</strong> Use the <a href="/permissions" class="text-primary">Permission Checker</a> 
                        to find file information, or extract from Google Drive URL
                    </li>
                    <li class="list-group-item">
                        <strong>Permission ID:</strong> Available in the permission details when checking file permissions
                    </li>
                    <li class="list-group-item">
                        <strong>Batch Operations:</strong> For multiple files, use the 
                        <a href="/batch" class="text-primary">Batch Operations</a> page
                    </li>
                </ul>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
