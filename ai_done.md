# SSL Certificate Installation with Let's Encrypt

## Date: April 30, 2025

## Summary
Successfully installed and configured SSL certificates for rauma24h.com using Let's Encrypt and Certbot with Nginx.

## Steps Performed

1. **Verified Certbot Installation**
   - Confirmed Certbot was already installed at `/usr/bin/certbot`

2. **Installed Certbot Nginx Plugin**
   - Installed the Nginx plugin for Certbot: `apt-get install -y python3-certbot-nginx`

3. **Examined Existing Nginx Configuration**
   - Found existing configuration at `/etc/nginx/sites-available/rauma24h.com`
   - Identified that the actual active configuration was at `/etc/nginx/sites-enabled/raovat`

4. **Obtained SSL Certificates**
   - Ran `certbot --nginx -d rauma24h.com -d www.rauma24h.com`
   - Successfully obtained certificates for both domains

5. **Verified Nginx Configuration**
   - Certbot automatically updated the Nginx configuration to:
     - Serve HTTPS on port 443 using the new SSL certificates
     - Redirect all HTTP traffic to HTTPS
     - Apply recommended SSL security parameters
   - Validated configuration with `nginx -t`
   - Restarted Nginx to apply changes

6. **Confirmed Automatic Renewal**
   - Verified that the Certbot timer service is active and running twice daily
   - Successfully tested the renewal process with a dry run

## Certificate Details
- **Certificate Location**: `/etc/letsencrypt/live/rauma24h.com/fullchain.pem`
- **Private Key Location**: `/etc/letsencrypt/live/rauma24h.com/privkey.pem`
- **Expiration Date**: July 29, 2025 (90 days from issuance)
- **Domains Covered**: rauma24h.com, www.rauma24h.com

## Automatic Renewal
- Certificates will automatically renew approximately 30 days before expiration
- Renewal is handled by a systemd timer that runs twice daily
