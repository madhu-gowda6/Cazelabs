DIAGNOSE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Permission Diagnostics - Drive Access Portal</title>
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
        
        .diagnostic-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: none;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            padding: 2rem;
            margin-bottom: 2rem;
        }
        
        .permission-item {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 4px solid #007bff;
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
                    <li class="nav-item"><a class="nav-link" href="/manage">Back to Manage</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="main-content">
        <div class="container">
            <div class="diagnostic-card">
                <h3 class="mb-4">
                    <i class="fas fa-search text-primary me-2"></i>
                    Permission Diagnostics
                </h3>
                
                <form method="POST">
                    <div class="row">
                        <div class="col-md-8">
                            <label for="file_name" class="form-label">File/Folder Name:</label>
                            <input type="text" name="file_name" id="file_name" class="form-control" required 
                                   placeholder="Enter file or folder name to diagnose">
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">&nbsp;</label>
                            <button type="submit" class="btn btn-primary d-block">
                                <i class="fas fa-search me-2"></i>Diagnose
                            </button>
                        </div>
                    </div>
                </form>
                
                {% if error %}
                    <div class="alert alert-danger mt-4">
                        <i class="fas fa-exclamation-triangle me-2"></i>{{ error }}
                    </div>
                {% endif %}
                
                {% if data %}
                    <div class="mt-4">
                        <h4>File Information:</h4>
                        <div class="permission-item">
                            <strong>Name:</strong> {{ data.file_name }}<br>
                            <strong>File ID:</strong> <code>{{ data.file_id }}</code><br>
                            <strong>Type:</strong> {{ data.mime_type }}
                        </div>
                        
                        <h4 class="mt-4">All Permissions ({{ data.permissions|length }} total):</h4>
                        {% if data.permissions %}
                            {% for permission in data.permissions %}
                                <div class="permission-item">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <strong>Type:</strong> {{ permission.type }}<br>
                                            <strong>Role:</strong> 
                                            <span class="badge bg-primary">{{ permission.role }}</span>
                                        </div>
                                        <div class="col-md-6">
                                            {% if permission.emailAddress %}
                                                <strong>Email:</strong> {{ permission.emailAddress }}<br>
                                            {% else %}
                                                <strong>Email:</strong> <span class="text-muted">Not Available</span><br>
                                            {% endif %}
                                            {% if permission.displayName %}
                                                <strong>Display Name:</strong> {{ permission.displayName }}<br>
                                            {% endif %}
                                            {% if permission.photoLink %}
                                                <strong>Has Photo:</strong> Yes<br>
                                            {% endif %}
                                            <strong>Permission ID:</strong> <code>{{ permission.id }}</code>
                                        </div>
                                    </div>
                                </div>
                            {% endfor %}
                        {% else %}
                            <div class="alert alert-info">
                                No permissions found (only owners have access)
                            </div>
                        {% endif %}
                    </div>
                {% endif %}
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
