"""
IMPORTANT: This selfbot requires your Discord USER token (not a bot token)

To get your Discord USER token:
1. Open Discord in your browser
2. Press F12 to open Developer Tools
3. Go to the Network tab
4. Click on the 'Filter' icon and type '/api'
5. Click on any request (like /api/v9/users/@me)
6. In the request headers, find 'authorization'
7. Copy the ENTIRE token

SECURITY WARNINGS:
- NEVER share your token with anyone
- Keep this file secure
- If compromised, change your password immediately (this invalidates the token)
- Using selfbots is against Discord's Terms of Service - use at your own risk

Example token format:
mfa.VkO_2G4Qv3T--NO--lWetW_tjND--TOKEN--QFTm6YGtzq9PH--4U--tG0
"""

# Replace with your actual Discord user token (keep the quotes)
TOKEN = "YOUR_USER_TOKEN_HERE"

# Additional configuration
BOT_PREFIX = "."
SAFE_MODE = True  # Enable additional security features 