import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """Initialize Supabase client"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    if not url or not key:
        print("Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.")
        return None
    return create_client(url, key)

def test_user_roles():
    """Test get_user_roles function for specific user"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            print("❌ Could not connect to Supabase")
            return
        
        # First, find the user by email
        print("🔍 Looking for user with email: sw@ftfacil.com")
        user_response = supabase.table('users').select('*').eq('email', 'sw@ftfacil.com').execute()
        
        if not user_response.data:
            print("❌ User not found with email: sw@ftfacil.com")
            return
        
        user = user_response.data[0]
        print(f"✅ User found:")
        print(f"   ID: {user['id']}")
        print(f"   Name: {user['name']}")
        print(f"   Email: {user['email']}")
        
        # Now get user roles
        print(f"\n🔍 Getting roles for user ID: {user['id']}")
        roles_response = supabase.table('user_roles').select('*').eq('user_id', user['id']).execute()
        
        print(f"📊 Roles query response:")
        print(f"   Response data: {roles_response.data}")
        print(f"   Response count: {len(roles_response.data) if roles_response.data else 0}")
        
        if roles_response.data:
            roles = [role['role'] for role in roles_response.data]
            print(f"✅ Extracted roles: {roles}")
        else:
            print("❌ No roles found for this user")
        
        # Let's also check all user_roles in the database
        print(f"\n🔍 Checking all user_roles in database:")
        all_roles_response = supabase.table('user_roles').select('*').execute()
        print(f"   All user_roles: {all_roles_response.data}")
        
        # Check if there are any user_roles with different user IDs
        print(f"\n🔍 Checking for any user_roles records:")
        if all_roles_response.data:
            for role_record in all_roles_response.data:
                print(f"   User ID: {role_record['user_id']}, Role: {role_record['role']}")
        else:
            print("   No user_roles records found in database")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_user_roles()
