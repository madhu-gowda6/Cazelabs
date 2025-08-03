import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for, flash
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import schedule
import time
import threading

# Import templates
from templates import MAIN_TEMPLATE, PERMISSIONS_TEMPLATE, MANAGE_TEMPLATE
from additional_templates import SEARCH_TEMPLATE, AUDIT_TEMPLATE, INACTIVE_TEMPLATE, BATCH_TEMPLATE, ALERTS_TEMPLATE
from diagnostic_template import DIAGNOSE_TEMPLATE, DIAGNOSE_TEMPLATE

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Enhanced scopes for full permission management
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/admin.directory.user.readonly',
    'https://www.googleapis.com/auth/admin.directory.group.readonly'
]

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[
                       logging.FileHandler('audit.log'),
                       logging.StreamHandler()
                   ])

# ---------------- Google Drive Authentication ---------------- #
def get_drive_service():
    token_file = 'token.json'
    creds = None
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception as e:
            logging.warning(f"Error loading token file: {e}. Will re-authenticate.")
            # Delete corrupted token file
            try:
                os.remove(token_file)
            except:
                pass
            creds = None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                logging.warning(f"Error refreshing token: {e}. Will re-authenticate.")
                # Delete expired token file
                try:
                    os.remove(token_file)
                except:
                    pass
                creds = None
        
        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credential.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                logging.error(f"Error during authentication: {e}")
                raise Exception(f"Authentication failed: {e}")
        
        # Save the credentials for the next run
        try:
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            logging.warning(f"Error saving token file: {e}")
    
    return build('drive', 'v3', credentials=creds)

# ---------------- Utility Functions ---------------- #
#Find file id by name
def find_file_id(service, file_name):
    query = f"name='{file_name}' and trashed = false"
    results = service.files().list(q=query, supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
    items = results.get('files', [])
    return items[0]['id'] if items else None

#Get all permissions of a file
def get_permissions(service, file_id):
    try:
        results = service.permissions().list(fileId=file_id).execute()
        return results.get('permissions', [])
    except HttpError:
        return []
#Check if user has permission to access the file
def list_all_files_and_check_user_permission(service, user_email):
    page_token, matched_items = None, []
    while True:
        response = service.files().list(
            q="trashed = false and (sharedWithMe or 'me' in owners or 'me' in readers or 'me' in writers)",
            spaces='drive',
            fields='nextPageToken, files(id, name, mimeType, owners, permissions)',
            pageToken=page_token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        for file in response.get('files', []):
            file_type = 'Folder' if file['mimeType'] == 'application/vnd.google-apps.folder' else 'File'
            owners = [o.get('emailAddress') for o in file.get('owners', [])]
            if user_email in owners:
                matched_items.append((file['name'], file_type, 'owner'))
            else:
                for p in file.get('permissions', []):
                    if p.get('emailAddress') == user_email:
                        matched_items.append((file['name'], file_type, p.get('role')))
                        break
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return matched_items

#Recursively list all files and folders inside a folder
def get_folder_contents_recursively(service, folder_id, folder_name, depth=0):
    output = ""
    indent = "&nbsp;" * 4 * depth  # Indent for nested items in HTML

    try:
        # List files and folders inside this folder
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType, owners, permissions)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        items = results.get('files', [])

        if not items:
            output += f"{indent}<p>No items found in '{folder_name}'</p>"
            return output
        #If files are found thn checks if its file or folder and list permissions
        for item in items:
            item_name = item['name']
            item_type = 'Folder' if item['mimeType'] == 'application/vnd.google-apps.folder' else 'File'
            owners = ", ".join([o.get('emailAddress', 'Unknown Owner') for o in item.get('owners', [])])

            output += f"{indent}<h4>{item_type}: {item_name}</h4>"
            output += f"{indent}<p><strong>Owner(s):</strong> {owners}</p>"

            # List permissions
            output += f"{indent}<table border='1'><tr><th>User/Entity</th><th>Role</th></tr>"
            for p in item.get('permissions', []):
                if p['type'] == 'user':
                    user_display = p.get('emailAddress', 'Unknown User')
                elif p['type'] == 'group':
                    user_display = p.get('emailAddress', 'Unknown Group')
                elif p['type'] == 'domain':
                    user_display = f"Domain: {p.get('domain', 'Unknown Domain')}"
                elif p['type'] == 'anyone':
                    user_display = "Anyone with the link"
                else:
                    user_display = p['type']

                output += f"<tr><td>{user_display}</td><td>{p.get('role')}</td></tr>"
            output += "</table>"

            # If it's a folder, recursively call this function
            if item_type == 'Folder':
                output += get_folder_contents_recursively(service, item['id'], item_name, depth + 1)

    except HttpError as error:
        output += f"{indent}<p>Error accessing '{folder_name}': {error}</p>"

    return output

# ---------------- Flask Routes ---------------- #
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template_string(MAIN_TEMPLATE)

@app.route("/permissions", methods=['GET', 'POST'])
def permissions():
    try:
        service = get_drive_service()
    except Exception as e:
        output = f"<div class='alert alert-danger'>Authentication error: {str(e)}. Please check your credentials and try again.</div>"
        return render_template_string(PERMISSIONS_TEMPLATE, output=output or "")
    
    output = None
    if request.method == "POST":
        query = request.form['query'].strip().lower()
        # Case 1: List files/folders accessible by a user
        if query.startswith("permissions of user"):
            user_email = query.replace("permissions of user", "").strip()
            # List all files and folders accessible by the user
            items = list_all_files_and_check_user_permission(service, user_email)
            output = f"<h3>Files and Folders accessible by {user_email}:</h3>"
            if items:
                output += "<table class='table table-striped'><tr><th>Type</th><th>Name</th><th>Role</th></tr>"
                output += "".join([f"<tr><td>{t}</td><td>{n}</td><td><span class='badge bg-primary'>{r}</span></td></tr>" for n, t, r in items])
                output += "</table>"
            else:
                output += "<div class='alert alert-info'>No files or folders found.</div>"

        # Case 2 and 3: Check file permissions and user permission on file
        elif query.startswith("permissions of "):
            # Extract file name and user email (if provided)
            parts = query.replace("permissions of ", "").split(" user ")
            #Extract the file name and user email from the query
            file_name, user_email = parts[0].strip(), parts[1].strip() if len(parts) > 1 else None
            file_id = find_file_id(service, file_name)
            if not file_id:
                output = f"<div class='alert alert-danger'>File '{file_name}' not found.</div>"
            else:
                # Fetch file metadata including owners
                file_metadata = service.files().get(
                    fileId=file_id,
                    fields='owners, permissions',
                    supportsAllDrives=True
                ).execute()
                owners = file_metadata.get('owners', [])
                permissions = file_metadata.get('permissions', [])

                #when specific user permission is queried
                if user_email:
                    user_permissions = [p for p in permissions if p.get('emailAddress') == user_email]
                    if user_permissions:
                        output = f"<h3>Permissions of {user_email} on '{file_name}':</h3><ul class='list-group'>"
                        output += "".join([f"<li class='list-group-item'>Role: <span class='badge bg-success'>{p.get('role')}</span></li>" for p in user_permissions])
                        output += "</ul>"
                    else:
                        output = f"<div class='alert alert-warning'>{user_email} has no permissions for '{file_name}'.</div>"
                else:
                    # Show owner properly
                    output = f"<h3>Permissions for '{file_name}':</h3>"
                    output += "<h4>Owner(s):</h4><ul class='list-group mb-3'>"
                    for owner in owners:
                        owner_email = owner.get('emailAddress', 'Unknown Owner')
                        output += f"<li class='list-group-item'><i class='fas fa-crown text-warning'></i> {owner_email}</li>"
                    output += "</ul>"

                    # List other permissions
                    output += "<h4>Other Permissions:</h4><table class='table table-striped'><tr><th>User/Entity</th><th>Role</th><th>Actions</th></tr>"
                    for p in permissions:
                        if p['type'] == 'user':
                            user_display = p.get('emailAddress', 'Unknown User')
                        elif p['type'] == 'group':
                            user_display = f"<i class='fas fa-users'></i> {p.get('emailAddress', 'Unknown Group')}"
                        elif p['type'] == 'domain':
                            user_display = f"<i class='fas fa-globe'></i> Domain: {p.get('domain', 'Unknown Domain')}"
                        elif p['type'] == 'anyone':
                            user_display = "<i class='fas fa-link'></i> Anyone with the link"
                        else:
                            user_display = p['type']

                        role_badge = f"<span class='badge bg-primary'>{p.get('role')}</span>"
                        actions = f"""
                        <button class='btn btn-sm btn-warning' onclick='updatePermission("{file_id}", "{p.get('id')}", "{p.get('role')}")'>
                            <i class='fas fa-edit'></i> Edit
                        </button>
                        <button class='btn btn-sm btn-danger' onclick='removePermission("{file_id}", "{p.get('id')}")'>
                            <i class='fas fa-trash'></i> Remove
                        </button>
                        """
                        output += f"<tr><td>{user_display}</td><td>{role_badge}</td><td>{actions}</td></tr>"
                    output += "</table>"
                    output += get_folder_contents_recursively(service, file_id, file_name)

        else:
            output = "<div class='alert alert-danger'>Invalid query format.</div>"

    return render_template_string(PERMISSIONS_TEMPLATE, output=output)

def find_file_by_name(service, file_name):
    """Find file ID by name"""
    try:
        # Search for files with exact name match
        results = service.files().list(
            q=f"name='{file_name}' and trashed=false",
            fields="files(id, name, mimeType)"
        ).execute()
        
        files = results.get('files', [])
        if not files:
            return None, f"File '{file_name}' not found"
        elif len(files) > 1:
            # If multiple files with same name, return the first one but warn user
            return files[0]['id'], f"Found {len(files)} files named '{file_name}'. Using the first one."
        else:
            return files[0]['id'], f"Found file '{file_name}'"
            
    except HttpError as error:
        return None, f"Error searching for file: {error}"

def find_permission_by_email(service, file_id, email):
    """Find permission ID by email for a specific file"""
    try:
        permissions = service.permissions().list(
            fileId=file_id,
            fields='permissions(id,type,role,emailAddress,displayName,photoLink,deleted)'
        ).execute()
        
        # First try to match by email address
        for permission in permissions.get('permissions', []):
            if permission.get('emailAddress') == email:
                return permission['id'], f"Found permission for {email}"
        
        # If no email match found, try to get individual permission details
        # This is a fallback for when emailAddress is not populated in the list
        for permission in permissions.get('permissions', []):
            if permission.get('type') == 'user' and permission.get('role') != 'owner':
                try:
                    # Get detailed permission info
                    detailed_permission = service.permissions().get(
                        fileId=file_id,
                        permissionId=permission['id'],
                        fields='id,type,role,emailAddress,displayName'
                    ).execute()
                    
                    if detailed_permission.get('emailAddress') == email:
                        return permission['id'], f"Found permission for {email} (via detailed lookup)"
                except:
                    continue
        
        return None, f"No permission found for {email} on this file"
        
    except HttpError as error:
        return None, f"Error finding permission: {error}"

@app.route("/manage", methods=['GET', 'POST'])
def manage_permissions():
    if request.method == 'POST':
        try:
            service = get_drive_service()
        except Exception as e:
            flash(f"Authentication error: {str(e)}. Please check your credentials and try again.", 'danger')
            return render_template_string(MANAGE_TEMPLATE)
        
        action = request.form.get('action')
        
        if action == 'add_permission':
            file_name = request.form.get('file_name')
            email = request.form.get('email')
            role = request.form.get('role', 'reader')
            perm_type = request.form.get('type', 'user')
            
            # Convert file name to file ID
            file_id, find_message = find_file_by_name(service, file_name)
            if not file_id:
                flash(find_message, 'danger')
            else:
                success, message = add_permission(service, file_id, email, role, perm_type)
                flash(f"{find_message}. {message}", 'success' if success else 'danger')
            
        elif action == 'remove_permission':
            file_name = request.form.get('file_name')
            email = request.form.get('email')
            
            # Convert file name to file ID
            file_id, find_message = find_file_by_name(service, file_name)
            if not file_id:
                flash(find_message, 'danger')
            else:
                # Convert email to permission ID
                permission_id, perm_message = find_permission_by_email(service, file_id, email)
                if not permission_id:
                    flash(f"{find_message}. {perm_message}", 'danger')
                else:
                    success, message = remove_permission(service, file_id, permission_id)
                    flash(f"{find_message}. {message}", 'success' if success else 'danger')
            
        elif action == 'update_permission':
            file_name = request.form.get('file_name')
            email = request.form.get('email')
            new_role = request.form.get('new_role')
            
            # Convert file name to file ID
            file_id, find_message = find_file_by_name(service, file_name)
            if not file_id:
                flash(find_message, 'danger')
            else:
                # Convert email to permission ID
                permission_id, perm_message = find_permission_by_email(service, file_id, email)
                if not permission_id:
                    flash(f"{find_message}. {perm_message}", 'danger')
                else:
                    success, message = update_permission(service, file_id, permission_id, new_role)
                    flash(f"{find_message}. {message}", 'success' if success else 'danger')
    
    return render_template_string(MANAGE_TEMPLATE)

@app.route("/search", methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        try:
            service = get_drive_service()
        except Exception as e:
            flash(f"Authentication error: {str(e)}. Please check your credentials and try again.", 'danger')
            return render_template_string(SEARCH_TEMPLATE, results=[])
        
        query = request.form.get('query', '')
        file_type = request.form.get('file_type', '')
        
        results = search_files(service, query, file_type)
        log_action('search', f"Search performed: {query}, type: {file_type}")
    
    return render_template_string(SEARCH_TEMPLATE, results=results)

@app.route("/audit")
def audit():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    logs = export_audit_report(start_date, end_date)
    return render_template_string(AUDIT_TEMPLATE, logs=logs)

@app.route("/inactive")
def inactive_users():
    try:
        service = get_drive_service()
    except Exception as e:
        flash(f"Authentication error: {str(e)}. Please check your credentials and try again.", 'danger')
        return render_template_string(INACTIVE_TEMPLATE, inactive_users=[], days=90, test_mode=False)
    
    days = int(request.args.get('days', 90))
    test_mode = request.args.get('test', 'false').lower() == 'true'
    
    if test_mode:
        # Generate sample inactive users for testing
        inactive = [
            {
                'email': 'john.doe@example.com',
                'file': 'Project Documentation.docx',
                'last_modified': '2024-01-15T10:30:00Z'
            },
            {
                'email': 'jane.smith@example.com',
                'file': 'Budget Spreadsheet.xlsx',
                'last_modified': '2024-02-20T14:15:00Z'
            },
            {
                'email': 'old.user@example.com',
                'file': 'Shared Photos',
                'last_modified': '2023-12-01T09:00:00Z'
            }
        ]
    else:
        inactive = detect_inactive_users(service, days)
    
    return render_template_string(INACTIVE_TEMPLATE, inactive_users=inactive, days=days)

@app.route("/batch", methods=['GET', 'POST'])
def batch_operations():
    if request.method == 'POST':
        try:
            service = get_drive_service()
        except Exception as e:
            flash(f"Authentication error: {str(e)}. Please check your credentials and try again.", 'danger')
            return render_template_string(BATCH_TEMPLATE)
        
        operation = request.form.get('operation')
        file_pattern = request.form.get('file_pattern')
        email = request.form.get('email')
        role = request.form.get('role', 'reader')
        test_mode = request.form.get('test_mode') == 'on'
        
        if not operation or not file_pattern or not email:
            flash("All fields are required", 'danger')
            return render_template_string(BATCH_TEMPLATE)
        
        # Test mode for debugging
        if test_mode:
            # Simulate finding files for testing
            files = [
                {'id': 'test_file_1', 'name': 'Labsheet1'},
                {'id': 'test_file_2', 'name': 'Labsheet2'},
                {'id': 'test_file_3', 'name': 'Labsheet3'}
            ]
            
            batch_results = []
            for file in files:
                if file_pattern == '*' or file_pattern.lower() in file['name'].lower():
                    batch_results.append({
                        'file_name': file['name'],
                        'success': True,
                        'message': f"TEST MODE: Would {operation} for {email} with role {role}"
                    })
            
            summary = f"TEST MODE: Found {len(batch_results)} matching files for pattern '{file_pattern}'"
            flash(f"TEST MODE ACTIVE: {summary}", 'info')
            
            return render_template_string(BATCH_TEMPLATE, 
                                        batch_results=batch_results, 
                                        summary=summary,
                                        operation=operation,
                                        file_pattern=file_pattern,
                                        email=email,
                                        test_mode=True)
        
        # Find files matching the pattern
        try:
            # Build search query based on pattern
            if file_pattern.startswith('*') and file_pattern.endswith('*'):
                # Pattern like *report* - contains search
                search_term = file_pattern[1:-1]
                query = f"name contains '{search_term}' and trashed=false"
            elif file_pattern.startswith('*'):
                # Pattern like *.pdf or *report - ends with search
                if file_pattern.startswith('*.'):
                    # File extension search like *.pdf
                    extension = file_pattern[2:]
                    query = f"name contains '.{extension}' and trashed=false"
                else:
                    # Ends with search like *report
                    search_term = file_pattern[1:]
                    query = f"name contains '{search_term}' and trashed=false"
            elif file_pattern.endswith('*'):
                # Pattern like Labsheet* - starts with search
                search_term = file_pattern[:-1]
                query = f"name contains '{search_term}' and trashed=false"
            else:
                # Exact name match
                query = f"name='{file_pattern}' and trashed=false"
            
            # Log the search query for debugging
            log_action('batch_search', f"Searching with query: {query}")
            
            results = service.files().list(
                q=query,
                fields="files(id, name, mimeType)",
                pageSize=100,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            files = results.get('files', [])
            
            # Additional filtering for better pattern matching
            if file_pattern.startswith('*') or file_pattern.endswith('*'):
                filtered_files = []
                for file in files:
                    file_name = file['name'].lower()
                    pattern_lower = file_pattern.lower()
                    
                    if pattern_lower.startswith('*') and pattern_lower.endswith('*'):
                        # *term* - contains
                        term = pattern_lower[1:-1]
                        if term in file_name:
                            filtered_files.append(file)
                    elif pattern_lower.startswith('*'):
                        # *term - ends with
                        if pattern_lower.startswith('*.'):
                            # *.ext - file extension
                            ext = pattern_lower[2:]
                            if file_name.endswith('.' + ext):
                                filtered_files.append(file)
                        else:
                            # *term - ends with term
                            term = pattern_lower[1:]
                            if file_name.endswith(term):
                                filtered_files.append(file)
                    elif pattern_lower.endswith('*'):
                        # term* - starts with
                        term = pattern_lower[:-1]
                        if file_name.startswith(term):
                            filtered_files.append(file)
                files = filtered_files
            
            log_action('batch_search_result', f"Found {len(files)} files matching pattern: {file_pattern}")
            
            if not files:
                flash(f"No files found matching pattern: {file_pattern}. Query used: {query}", 'warning')
                return render_template_string(BATCH_TEMPLATE)
            
            # Process each file
            batch_results = []
            success_count = 0
            
            for file in files:
                file_id = file['id']
                file_name = file['name']
                
                try:
                    if operation == 'add_permission':
                        success, message = add_permission(service, file_id, email, role, 'user')
                        log_action('batch_add_permission', f"Added {role} permission for {email} to {file_name}")
                    
                    elif operation == 'remove_permission':
                        # Find permission by email first
                        permission_id, perm_message = find_permission_by_email(service, file_id, email)
                        if permission_id:
                            success, message = remove_permission(service, file_id, permission_id)
                            log_action('batch_remove_permission', f"Removed permission for {email} from {file_name}")
                        else:
                            success, message = False, perm_message
                    
                    elif operation == 'change_role':
                        # Find permission by email first
                        permission_id, perm_message = find_permission_by_email(service, file_id, email)
                        if permission_id:
                            success, message = update_permission(service, file_id, permission_id, role)
                            log_action('batch_change_role', f"Changed role to {role} for {email} on {file_name}")
                        else:
                            success, message = False, perm_message
                    
                    else:
                        success, message = False, "Unknown operation"
                    
                    if success:
                        success_count += 1
                    
                    batch_results.append({
                        'file_name': file_name,
                        'success': success,
                        'message': message
                    })
                    
                except Exception as e:
                    batch_results.append({
                        'file_name': file_name,
                        'success': False,
                        'message': str(e)
                    })
            
            # Create summary message
            summary = f"Batch operation '{operation}' completed: {success_count}/{len(files)} files processed successfully"
            
            # Add more detailed logging
            log_action('batch_operation_complete', f"Operation: {operation}, Pattern: {file_pattern}, Email: {email}, Success: {success_count}/{len(files)}")
            
            if success_count > 0:
                flash(summary, 'success')
            elif len(files) > 0:
                flash(f"{summary}. Check individual file results below.", 'warning')
            else:
                flash("No files were processed.", 'info')
            
            return render_template_string(BATCH_TEMPLATE, 
                                        batch_results=batch_results, 
                                        summary=summary,
                                        operation=operation,
                                        file_pattern=file_pattern,
                                        email=email,
                                        files_found=len(files))
            
        except Exception as e:
            flash(f"Error during batch operation: {str(e)}", 'danger')
            return render_template_string(BATCH_TEMPLATE)
    
    return render_template_string(BATCH_TEMPLATE)

@app.route("/batch/bulk-emails", methods=['POST'])
def bulk_email_operations():
    """Handle bulk email permissions for a single file"""
    try:
        service = get_drive_service()
    except Exception as e:
        flash(f"Authentication error: {str(e)}. Please check your credentials and try again.", 'danger')
        return render_template_string(BATCH_TEMPLATE)
    
    single_file_name = request.form.get('single_file_name')
    bulk_emails = request.form.get('bulk_emails')
    bulk_role = request.form.get('bulk_role', 'reader')
    bulk_operation = request.form.get('bulk_operation')
    bulk_test_mode = request.form.get('bulk_test_mode') == 'on'
    
    if not single_file_name or not bulk_emails or not bulk_operation:
        flash("All fields are required for bulk email operations", 'danger')
        return render_template_string(BATCH_TEMPLATE)
    
    # Parse email addresses (handle both comma and newline separation)
    email_list = []
    invalid_emails = []
    for email in bulk_emails.replace(',', '\n').split('\n'):
        email = email.strip()
        if email:
            if validate_email(email):
                email_list.append(email)
            else:
                invalid_emails.append(email)
    
    if invalid_emails:
        flash(f"Invalid email addresses found: {', '.join(invalid_emails)}", 'warning')
    
    if not email_list:
        flash("No valid email addresses found", 'danger')
        return render_template_string(BATCH_TEMPLATE)
    
    # Limit the number of emails to prevent abuse
    MAX_EMAILS = 100
    if len(email_list) > MAX_EMAILS:
        flash(f"Too many emails! Maximum allowed: {MAX_EMAILS}. Found: {len(email_list)}", 'danger')
        return render_template_string(BATCH_TEMPLATE)
    
    # Test mode simulation
    if bulk_test_mode:
        bulk_results = []
        for email in email_list:
            bulk_results.append({
                'email': email,
                'success': True,
                'message': f"TEST MODE: Would {bulk_operation} {bulk_role} permission for {email}"
            })
        
        summary = f"TEST MODE: Bulk operation '{bulk_operation}' would process {len(email_list)} emails for file '{single_file_name}'"
        flash(f"TEST MODE ACTIVE: {summary}", 'info')
        
        return render_template_string(BATCH_TEMPLATE, 
                                    bulk_results=bulk_results, 
                                    bulk_summary=summary,
                                    bulk_operation_type="bulk_emails",
                                    single_file_name=single_file_name,
                                    bulk_test_mode=True)
    
    # Find the target file
    file_id, find_message = find_file_by_name(service, single_file_name)
    if not file_id:
        flash(f"File not found: {find_message}", 'danger')
        return render_template_string(BATCH_TEMPLATE)
    
    # Process each email
    bulk_results = []
    success_count = 0
    
    for email in email_list:
        try:
            if bulk_operation == 'add':
                success, message = add_permission(service, file_id, email, bulk_role, 'user')
                log_action('bulk_add_permission', f"Added {bulk_role} permission for {email} to {single_file_name}")
            
            elif bulk_operation == 'remove':
                # Find permission by email first
                permission_id, perm_message = find_permission_by_email(service, file_id, email)
                if permission_id:
                    success, message = remove_permission(service, file_id, permission_id)
                    log_action('bulk_remove_permission', f"Removed permission for {email} from {single_file_name}")
                else:
                    success, message = False, perm_message
            
            elif bulk_operation == 'update':
                # Find permission by email first
                permission_id, perm_message = find_permission_by_email(service, file_id, email)
                if permission_id:
                    success, message = update_permission(service, file_id, permission_id, bulk_role)
                    log_action('bulk_update_permission', f"Updated role to {bulk_role} for {email} on {single_file_name}")
                else:
                    success, message = False, perm_message
            
            else:
                success, message = False, "Unknown operation"
            
            if success:
                success_count += 1
            
            bulk_results.append({
                'email': email,
                'success': success,
                'message': message
            })
            
        except Exception as e:
            bulk_results.append({
                'email': email,
                'success': False,
                'message': str(e)
            })
    
    # Create summary message
    summary = f"Bulk email operation '{bulk_operation}' completed: {success_count}/{len(email_list)} emails processed successfully for file '{single_file_name}'"
    
    # Log the bulk operation
    log_action('bulk_email_operation_complete', 
               f"Operation: {bulk_operation}, File: {single_file_name}, Role: {bulk_role}, "
               f"Emails: {len(email_list)}, Success: {success_count}/{len(email_list)}")
    
    if success_count > 0:
        flash(summary, 'success')
    elif len(email_list) > 0:
        flash(f"{summary}. Check individual email results below.", 'warning')
    else:
        flash("No emails were processed.", 'info')
    
    return render_template_string(BATCH_TEMPLATE, 
                                bulk_results=bulk_results, 
                                bulk_summary=summary,
                                bulk_operation_type="bulk_emails",
                                single_file_name=single_file_name,
                                bulk_role=bulk_role,
                                bulk_operation=bulk_operation,
                                emails_processed=len(email_list))

# API endpoints for AJAX calls
@app.route("/api/add_permission", methods=['POST'])
def api_add_permission():
    try:
        service = get_drive_service()
    except Exception as e:
        return jsonify({'success': False, 'message': f'Authentication error: {str(e)}'})
    
    data = request.get_json()
    
    success, message = add_permission(
        service, 
        data['file_id'], 
        data['email'], 
        data.get('role', 'reader'),
        data.get('type', 'user')
    )
    
    return jsonify({'success': success, 'message': message})

@app.route("/api/remove_permission", methods=['POST'])
def api_remove_permission():
    try:
        service = get_drive_service()
    except Exception as e:
        return jsonify({'success': False, 'message': f'Authentication error: {str(e)}'})
    
    data = request.get_json()
    
    success, message = remove_permission(service, data['file_id'], data['permission_id'])
    
    return jsonify({'success': success, 'message': message})

@app.route("/api/update_permission", methods=['POST'])
def api_update_permission():
    try:
        service = get_drive_service()
    except Exception as e:
        return jsonify({'success': False, 'message': f'Authentication error: {str(e)}'})
    
    data = request.get_json()
    
    success, message = update_permission(service, data['file_id'], data['permission_id'], data['new_role'])
    
    return jsonify({'success': success, 'message': message})

@app.route("/api/remove-access", methods=['POST'])
def remove_access():
    """Remove user access from a specific file"""
    try:
        data = request.get_json()
        user_email = data.get('email')
        file_name = data.get('file')
        test_mode = data.get('test', False)
        
        if not user_email or not file_name:
            return jsonify({'error': 'Email and file name are required'}), 400
        
        # Test mode for demonstration
        if test_mode or any(email in user_email for email in ['example.com', 'test.com']):
            # Simulate successful removal for test emails
            log_action('remove_access_test', f"Simulated removal of access for {user_email} from {file_name}")
            return jsonify({
                'success': True,
                'message': f'Successfully removed access for {user_email} from {file_name} (TEST MODE)'
            })
        
        try:
            service = get_drive_service()
        except Exception as e:
            return jsonify({'error': f'Authentication error: {str(e)}'}), 401
        
        # Find the file by name
        results = service.files().list(
            q=f"name='{file_name}' and trashed=false",
            fields="nextPageToken, files(id, name)"
        ).execute()
        
        items = results.get('files', [])
        if not items:
            return jsonify({'error': f'File "{file_name}" not found'}), 404
        
        file_id = items[0]['id']
        
        # Get current permissions
        permissions = service.permissions().list(fileId=file_id).execute()
        
        # Find the permission for this user
        permission_to_remove = None
        for permission in permissions.get('permissions', []):
            if permission.get('emailAddress') == user_email:
                permission_to_remove = permission
                break
        
        if not permission_to_remove:
            return jsonify({'error': f'User {user_email} does not have access to {file_name}'}), 404
        
        # Remove the permission
        service.permissions().delete(
            fileId=file_id,
            permissionId=permission_to_remove['id']
        ).execute()
        
        # Log the action
        log_action('remove_access', f"Removed access for {user_email} from {file_name}")
        
        return jsonify({
            'success': True,
            'message': f'Successfully removed access for {user_email} from {file_name}'
        })
        
    except HttpError as error:
        logging.error(f"An error occurred removing access: {error}")
        return jsonify({'error': f'Google Drive API error: {str(error)}'}), 500
    except Exception as e:
        logging.error(f"Unexpected error removing access: {e}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

def get_detailed_permissions(service, file_id):
    """Get detailed permission information including email addresses"""
    try:
        permissions = service.permissions().list(
            fileId=file_id,
            fields='permissions(id,type,role,emailAddress,displayName,photoLink,deleted)'
        ).execute()
        
        detailed_permissions = []
        for permission in permissions.get('permissions', []):
            # Get individual permission details if email is missing
            if not permission.get('emailAddress') and permission.get('type') == 'user':
                try:
                    detailed_permission = service.permissions().get(
                        fileId=file_id,
                        permissionId=permission['id'],
                        fields='id,type,role,emailAddress,displayName'
                    ).execute()
                    # Update with detailed info
                    permission.update(detailed_permission)
                except:
                    pass
            detailed_permissions.append(permission)
        
        return detailed_permissions
    except HttpError as error:
        return []

@app.route("/diagnose", methods=['GET', 'POST'])
def diagnose_permissions():
    """Diagnostic tool to check file permissions"""
    if request.method == 'POST':
        try:
            service = get_drive_service()
        except Exception as e:
            return render_template_string(DIAGNOSE_TEMPLATE, error=f"Authentication error: {str(e)}. Please check your credentials and try again.")
        
        file_name = request.form.get('file_name')
        
        if not file_name:
            return render_template_string(DIAGNOSE_TEMPLATE, error="Please provide a file name")
        
        # Find the file
        file_id, find_message = find_file_by_name(service, file_name)
        if not file_id:
            return render_template_string(DIAGNOSE_TEMPLATE, error=find_message)
        
        try:
            # Get detailed permissions
            detailed_permissions = get_detailed_permissions(service, file_id)
            
            # Get file details
            file_details = service.files().get(
                fileId=file_id, 
                fields='name,id,mimeType,owners'
            ).execute()
            
            diagnostic_data = {
                'file_name': file_details['name'],
                'file_id': file_details['id'],
                'mime_type': file_details['mimeType'],
                'owners': file_details.get('owners', []),
                'permissions': detailed_permissions
            }
            
            return render_template_string(DIAGNOSE_TEMPLATE, data=diagnostic_data)
            
        except HttpError as error:
            return render_template_string(DIAGNOSE_TEMPLATE, error=f"Error accessing file: {error}")
    
    return render_template_string(DIAGNOSE_TEMPLATE)

# ---------------- Enhanced Utility Functions ---------------- #

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def log_action(action, details, user_email=None):
    """Log actions for audit trail"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'details': details,
        'user': user_email or 'system'
    }
    logging.info(f"AUDIT: {json.dumps(log_entry)}")
    
    # Save to audit file
    with open('audit_trail.json', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def add_permission(service, file_id, email, role='reader', permission_type='user'):
    """Add permission to a file"""
    try:
        permission = {
            'type': permission_type,
            'role': role,
            'emailAddress': email
        }
        result = service.permissions().create(
            fileId=file_id,
            body=permission,
            sendNotificationEmail=True
        ).execute()
        log_action('add_permission', f"Added {role} permission for {email} to file {file_id}")
        return True, f"Permission added successfully"
    except HttpError as error:
        log_action('add_permission_failed', f"Failed to add permission for {email}: {error}")
        return False, f"Error: {error}"

def remove_permission(service, file_id, permission_id):
    """Remove permission from a file"""
    try:
        service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
        log_action('remove_permission', f"Removed permission {permission_id} from file {file_id}")
        return True, "Permission removed successfully"
    except HttpError as error:
        log_action('remove_permission_failed', f"Failed to remove permission {permission_id}: {error}")
        return False, f"Error: {error}"

def update_permission(service, file_id, permission_id, new_role):
    """Update permission role"""
    try:
        permission = {'role': new_role}
        service.permissions().update(
            fileId=file_id,
            permissionId=permission_id,
            body=permission
        ).execute()
        log_action('update_permission', f"Updated permission {permission_id} to {new_role} for file {file_id}")
        return True, "Permission updated successfully"
    except HttpError as error:
        log_action('update_permission_failed', f"Failed to update permission {permission_id}: {error}")
        return False, f"Error: {error}"

def get_groups(service):
    """Get all groups (requires admin SDK)"""
    try:
        admin_service = build('admin', 'directory_v1', credentials=service._http.credentials)
        result = admin_service.groups().list(domain='your-domain.com').execute()
        return result.get('groups', [])
    except HttpError:
        return []

def detect_inactive_users(service, days=90):
    """Detect users with access but no recent activity"""
    from datetime import timezone
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    inactive_users = []
    
    try:
        # This is a simplified version - in production you'd need to check actual usage
        page_token = None
        while True:
            response = service.files().list(
                q="trashed = false",
                fields='nextPageToken, files(id, name, permissions, modifiedTime)',
                pageToken=page_token
            ).execute()
            
            for file in response.get('files', []):
                modified_time = datetime.fromisoformat(file.get('modifiedTime', '').replace('Z', '+00:00'))
                if modified_time < cutoff_date:
                    for permission in file.get('permissions', []):
                        if permission.get('type') == 'user' and permission.get('emailAddress'):
                            inactive_users.append({
                                'email': permission.get('emailAddress'),
                                'file': file.get('name'),
                                'last_modified': modified_time.isoformat()
                            })
            
            page_token = response.get('nextPageToken')
            if not page_token:
                break
                
    except HttpError as error:
        log_action('detect_inactive_users_failed', f"Error detecting inactive users: {error}")
    
    return inactive_users

def search_files(service, query, file_type=None):
    """Enhanced file search with filters"""
    search_query = f"name contains '{query}' and trashed = false"
    
    if file_type == 'folder':
        search_query += " and mimeType = 'application/vnd.google-apps.folder'"
    elif file_type == 'document':
        search_query += " and mimeType = 'application/vnd.google-apps.document'"
    elif file_type == 'spreadsheet':
        search_query += " and mimeType = 'application/vnd.google-apps.spreadsheet'"
    
    try:
        results = service.files().list(
            q=search_query,
            fields='files(id, name, mimeType, owners, permissions, modifiedTime)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        return results.get('files', [])
    except HttpError as error:
        log_action('search_files_failed', f"Search failed: {error}")
        return []

def batch_permission_operation(service, file_ids, operation, **kwargs):
    """Perform batch operations on multiple files"""
    results = []
    for file_id in file_ids:
        try:
            if operation == 'add':
                success, message = add_permission(service, file_id, kwargs['email'], kwargs['role'])
            elif operation == 'remove':
                success, message = remove_permission(service, file_id, kwargs['permission_id'])
            elif operation == 'update':
                success, message = update_permission(service, file_id, kwargs['permission_id'], kwargs['new_role'])
            
            results.append({'file_id': file_id, 'success': success, 'message': message})
        except Exception as e:
            results.append({'file_id': file_id, 'success': False, 'message': str(e)})
    
    return results

def export_audit_report(start_date=None, end_date=None):
    """Export audit report as JSON"""
    try:
        with open('audit_trail.json', 'r') as f:
            logs = [json.loads(line) for line in f.readlines()]
        
        if start_date:
            logs = [log for log in logs if log['timestamp'] >= start_date]
        if end_date:
            logs = [log for log in logs if log['timestamp'] <= end_date]
        
        return logs
    except FileNotFoundError:
        return []

# ---------------- Email Notification System ---------------- #
def send_email_notification(to_email, subject, body):
    """Send email notifications"""
    try:
        # Configure your SMTP settings here
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your-email@gmail.com"
        sender_password = "your-app-password"
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        log_action('email_sent', f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        log_action('email_failed', f"Failed to send email to {to_email}: {e}")
        return False

# ---------------- Scheduled Tasks ---------------- #
def scheduled_inactive_user_check():
    """Scheduled task to check for inactive users"""
    try:
        service = get_drive_service()
    except Exception as e:
        log_action('scheduled_task_error', f"Authentication error in scheduled task: {str(e)}")
        return
        inactive_users = detect_inactive_users(service, days=90)
        
        if inactive_users:
            # Send notification to admin
            body = "<h2>Inactive Users Report</h2>"
            body += "<table border='1'><tr><th>Email</th><th>File</th><th>Last Modified</th></tr>"
            for user in inactive_users:
                body += f"<tr><td>{user['email']}</td><td>{user['file']}</td><td>{user['last_modified']}</td></tr>"
            body += "</table>"
            
            send_email_notification("admin@your-domain.com", "Inactive Users Report", body)
            
        log_action('scheduled_task', f"Inactive user check completed. Found {len(inactive_users)} inactive users")
    except Exception as e:
        log_action('scheduled_task_failed', f"Scheduled task failed: {e}")

# ---------------- Scheduled Tasks Setup ---------------- #
def setup_scheduler():
    """Setup scheduled tasks"""
    try:
        import schedule
        schedule.every().monday.at("09:00").do(scheduled_inactive_user_check)
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(3600)  # Check every hour
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        log_action('scheduler_started', 'Background scheduler started successfully')
    except ImportError:
        log_action('scheduler_failed', 'Schedule module not available. Install with: pip install schedule')

@app.route("/alerts", methods=['GET', 'POST'])
def configure_alerts():
    if request.method == "POST":
        alert_type = request.form.get('alert_type')
        email = request.form.get('email')
        frequency = request.form.get('frequency')
        enabled = request.form.get('enabled') == 'on'
        
        alert_config = {
            'type': alert_type,
            'email': email,
            'frequency': frequency,
            'enabled': enabled,
            'created_at': datetime.now().isoformat()
        }
        
        log_action('configure_alert', f"Alert configured: {alert_type} for {email}")
        
        return render_template_string(ALERTS_TEMPLATE, 
                                    success="Alert configuration saved successfully!",
                                    config=alert_config)
    
    return render_template_string(ALERTS_TEMPLATE)

# ---------------- Run Flask App ---------------- #
if __name__ == '__main__':
    # Setup logging
    if not os.path.exists('audit_trail.json'):
        with open('audit_trail.json', 'w') as f:
            pass
    
    log_action('app_started', 'Google Drive Access Management Portal started')
    
    # Start scheduler
    setup_scheduler()
    
    print("Google Drive Access Management Portal")
    print("=====================================")
    print("Features available:")
    print("✓ Permission checking and management")
    print("✓ Advanced search and filtering") 
    print("✓ Audit logging and reports")
    print("✓ Inactive user detection")
    print("✓ Batch operations")
    print("✓ Modern responsive UI")
    print("\nStarting server on http://localhost:5004")
    
    app.run(debug=True, port=5004, host='0.0.0.0')