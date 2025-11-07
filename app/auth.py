from flask import Blueprint, request, jsonify, g, current_app
from supabase import Client
import jwt
from functools import wraps
from app.supabase_client import get_supabase, get_supabase_admin

auth_bp = Blueprint('auth', __name__)

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format. Use: Bearer <token>'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Verify token with Supabase
            supabase = get_supabase()
            user_response = supabase.auth.get_user(token)
            
            if user_response.user is None:
                return jsonify({'message': 'Invalid token!'}), 401
            
            g.user = user_response.user
            g.user_id = user_response.user.id
            g.token = token
            
        except Exception as e:
            return jsonify({'message': 'Token verification failed!', 'error': str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated

# Get current user info
@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    try:
        supabase = get_supabase()
        
        # Get user profile from profiles table
        profile_response = supabase.table('profiles') \
            .select('*') \
            .eq('id', g.user_id) \
            .execute()
        
        if profile_response.data:
            profile = profile_response.data[0]
            return jsonify({
                'user': {
                    'id': g.user_id,
                    'email': g.user.email,
                    'full_name': profile.get('full_name', ''),
                    'employee_id': profile.get('employee_id', ''),
                    'role': profile.get('role', 'employee'),
                    'department': profile.get('department', '')
                }
            }), 200
        else:
            return jsonify({
                'message': 'Profile not found',
                'user': {
                    'id': g.user_id,
                    'email': g.user.email
                }
            }), 404
            
    except Exception as e:
        return jsonify({'message': 'Error fetching user data', 'error': str(e)}), 500

# User registration
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        print("Headers:", request.headers)
        print("JSON:", request.get_json())
        print("Form:", request.form)

        data = request.get_json() or request.form  # <-- add this line
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        employee_id = data.get('employee_id')
        department = data.get('department', '')

        if not email or not password:
            return jsonify({'message': 'Email and password are required!'}), 400

        
        # Create user in Supabase Auth
        supabase = get_supabase()
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        
        if auth_response.user is None:
            return jsonify({'message': 'Error creating user in authentication'}), 400
        
        user = auth_response.userP
        
        # Create user profile in profiles table
        profile_data = {
            'id': user.id,
            'employee_id': employee_id,
            'full_name': full_name,
            'department': department,
            'role': 'employee'  # Default role
        }
        
        profile_response = supabase.table('profiles') \
            .insert(profile_data) \
            .execute()
        
        if profile_response.data:
            return jsonify({
                'message': 'User registered successfully!',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': full_name,
                    'employee_id': employee_id
                }
            }), 201
        else:
            # If profile creation fails, we should delete the auth user
            # For now, we'll just return an error
            return jsonify({'message': 'User created in auth but profile creation failed'}), 500
        
    except Exception as e:
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 400

# Protected route example
@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected_route():
    return jsonify({
        'message': f'Hello {g.user.email}! This is a protected route.',
        'user_id': g.user_id
    })

# Get all users (admin only)
@auth_bp.route('/users', methods=['GET'])
@token_required
def get_all_users():
    try:
        # Check if user is admin
        supabase = get_supabase()
        profile_response = supabase.table('profiles') \
            .select('role') \
            .eq('id', g.user_id) \
            .execute()
        
        if not profile_response.data or profile_response.data[0]['role'] not in ['admin', 'manager']:
            return jsonify({'message': 'Insufficient permissions'}), 403
        
        # Get all users with profiles
        users_response = supabase.table('profiles') \
            .select('*') \
            .execute()
        
        return jsonify({'users': users_response.data}), 200
        
    except Exception as e:
        return jsonify({'message': 'Error fetching users', 'error': str(e)}), 500