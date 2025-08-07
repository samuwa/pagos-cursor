#!/usr/bin/env python3
"""
Find Supabase Project Reference
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_project_ref():
    """Get project reference from access token"""
    
    access_token = os.getenv("SUPABASE_ACCESS_TOKEN")
    if not access_token:
        print("❌ SUPABASE_ACCESS_TOKEN not found")
        return None
    
    # Try to get project info from Supabase API
    url = "https://api.supabase.com/v1/projects"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            projects = response.json()
            if projects:
                print("📋 Found Supabase projects:")
                for project in projects:
                    print(f"   • {project['name']}: {project['ref']}")
                    print(f"     URL: https://{project['ref']}.supabase.co")
                return projects[0]['ref']  # Return first project
            else:
                print("❌ No projects found")
                return None
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def main():
    """Main function"""
    print("🔍 Finding Supabase Project Reference")
    print("=" * 40)
    
    project_ref = get_project_ref()
    
    if project_ref:
        print(f"\n✅ Project Reference: {project_ref}")
        print(f"📝 Set it as:")
        print(f"   export SUPABASE_PROJECT_REF='{project_ref}'")
        
        # Set it automatically
        os.environ["SUPABASE_PROJECT_REF"] = project_ref
        print(f"\n🚀 Project reference set automatically!")
        
        # Now run the OTP configuration
        print("\n🔄 Running OTP configuration...")
        import configure_supabase_otp
        configure_supabase_otp.main()
    else:
        print("\n❌ Could not find project reference")
        print("📝 Please manually set SUPABASE_PROJECT_REF")

if __name__ == "__main__":
    main()
