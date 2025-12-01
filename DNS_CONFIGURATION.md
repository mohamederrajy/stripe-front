# 🌐 DNS Configuration Guide

## Your Details
- **Server IP:** `5.78.152.132`
- **Frontend Domain:** `stripech.dev`
- **Backend API Domain:** `api.stripech.dev`

---

## Required DNS Records

Go to your domain registrar (where you bought `stripech.dev`) and add these DNS records:

### ✅ DNS Records to Add:

| Type | Name/Host | Value/Points To | TTL |
|------|-----------|-----------------|-----|
| **A** | `@` or `stripech.dev` | `5.78.152.132` | 3600 |
| **A** | `www` | `5.78.152.132` | 3600 |
| **A** | `api` | `5.78.152.132` | 3600 |

---

## Step-by-Step Instructions

### 1. Log into Your Domain Registrar

Common registrars:
- **Namecheap:** namecheap.com → Domain List → Manage → Advanced DNS
- **GoDaddy:** godaddy.com → My Domains → DNS
- **Cloudflare:** cloudflare.com → DNS
- **Google Domains:** domains.google.com → DNS
- **OVH:** ovh.com → Web Cloud → Domains → DNS Zone

### 2. Add DNS Records

#### Record 1: Main Domain (stripech.dev)
```
Type: A Record
Host: @ (or leave blank, or type "stripech.dev")
Value: 5.78.152.132
TTL: 3600 (or Auto)
```

#### Record 2: WWW Subdomain (www.stripech.dev)
```
Type: A Record
Host: www
Value: 5.78.152.132
TTL: 3600 (or Auto)
```

#### Record 3: API Subdomain (api.stripech.dev)
```
Type: A Record
Host: api
Value: 5.78.152.132
TTL: 3600 (or Auto)
```

---

## 📸 Visual Example (Common DNS Panel)

```
┌─────────────────────────────────────────────────────┐
│ DNS Records for stripech.dev                        │
├──────┬──────────┬───────────────┬─────────┬────────┤
│ Type │ Host     │ Value         │ TTL     │ Action │
├──────┼──────────┼───────────────┼─────────┼────────┤
│ A    │ @        │ 5.78.152.132  │ 3600    │ [Edit] │
│ A    │ www      │ 5.78.152.132  │ 3600    │ [Edit] │
│ A    │ api      │ 5.78.152.132  │ 3600    │ [Edit] │
└──────┴──────────┴───────────────┴─────────┴────────┘
```

---

## 🔍 Verify DNS Configuration

After adding records, wait 5-60 minutes for DNS propagation, then check:

### Method 1: Online Tools
Visit these sites and check your domains:
- https://dnschecker.org/#A/stripech.dev
- https://dnschecker.org/#A/www.stripech.dev
- https://dnschecker.org/#A/api.stripech.dev

All should show IP: **5.78.152.132** ✅

### Method 2: Command Line
```bash
# Check main domain
nslookup stripech.dev
# Should return: 5.78.152.132

# Check www subdomain
nslookup www.stripech.dev
# Should return: 5.78.152.132

# Check API subdomain
nslookup api.stripech.dev
# Should return: 5.78.152.132
```

### Method 3: Ping Test
```bash
ping stripech.dev
ping www.stripech.dev
ping api.stripech.dev
```
All should ping to **5.78.152.132**

---

## ⏱️ DNS Propagation Time

- **Minimum:** 5 minutes
- **Average:** 30-60 minutes
- **Maximum:** 24-48 hours (rare)

Don't worry if it doesn't work immediately!

---

## 🚫 Common Mistakes to Avoid

❌ **DON'T** add `http://` or `https://` in the Value field  
✅ **DO** use just the IP: `5.78.152.132`

❌ **DON'T** use CNAME for root domain (@)  
✅ **DO** use A Record for root domain

❌ **DON'T** forget the `api` subdomain  
✅ **DO** add all three records (@ , www, api)

---

## 🎯 Quick Test After DNS Setup

### Test 1: Can you reach the server?
```bash
ping stripech.dev
```
Should see responses from 5.78.152.132

### Test 2: Are the ports open?
```bash
telnet stripech.dev 80
telnet api.stripech.dev 80
```
Should connect successfully

### Test 3: Does HTTP work?
```bash
curl http://stripech.dev
curl http://api.stripech.dev/health
```
Should return HTML or JSON responses

---

## 🔐 After DNS Works

Once DNS is working (all three domains resolve to 5.78.152.132):

1. **Deploy the application** (use QUICK_DEPLOY.sh)
2. **Setup SSL certificates:**
   ```bash
   certbot --nginx -d api.stripech.dev
   certbot --nginx -d stripech.dev -d www.stripech.dev
   ```
3. **Visit your site:** https://stripech.dev

---

## 📋 DNS Configuration Checklist

- [ ] Logged into domain registrar
- [ ] Added A record for `@` or `stripech.dev` → `5.78.152.132`
- [ ] Added A record for `www` → `5.78.152.132`
- [ ] Added A record for `api` → `5.78.152.132`
- [ ] Saved/Published DNS changes
- [ ] Waited 5-60 minutes for propagation
- [ ] Verified with dnschecker.org
- [ ] Tested with `nslookup` or `ping`
- [ ] Ready to deploy application!

---

## 🆘 Troubleshooting DNS

### Issue: "DNS not resolving"
**Solution:** Wait longer, DNS can take up to 24 hours

### Issue: "Only some locations see the new DNS"
**Solution:** Normal during propagation, wait

### Issue: "Getting old IP address"
**Solution:** Clear your DNS cache:
```bash
# macOS
sudo dscacheutil -flushcache

# Windows
ipconfig /flushdns

# Linux
sudo systemd-resolve --flush-caches
```

### Issue: "Can't add @ record"
**Solution:** Try:
- Leave Host field empty
- Use your domain name: `stripech.dev`
- Contact your registrar support

---

## 📞 Need Help?

If you're stuck:
1. Contact your domain registrar support
2. Send them this: "I need to add A records pointing to 5.78.152.132"
3. Show them the table from this guide

---

## ✅ Summary

You need to add **3 DNS A Records**:
1. `stripech.dev` → `5.78.152.132` (main site)
2. `www.stripech.dev` → `5.78.152.132` (www version)
3. `api.stripech.dev` → `5.78.152.132` (backend API)

**That's it!** Once DNS propagates, you can deploy! 🚀

