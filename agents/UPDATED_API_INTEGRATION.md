# 🔄 Updated Google Trends API Integration

## 📋 **API Changes**

The Google Trends API has been updated to use new endpoints at `http://localhost:3010`:

### **New API Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/trends/daily` | Daily trending searches |
| `GET` | `/api/trends/realtime` | Realtime trends |
| `GET` | `/api/trends/interest-over-time` | Interest over time for keyword |
| `GET` | `/api/trends/interest-by-region` | Interest by region for keyword |
| `GET` | `/api/trends/related-topics` | Related topics for keyword |
| `GET` | `/api/trends/related-queries` | Related queries for keyword |

### **Updated Parameters**

All endpoints now use `startTime` and `endTime` parameters in `YYYY-MM-DD` format:

```bash
# Example API calls
curl "http://localhost:3010/api/trends/interest-over-time?keyword=AI&startTime=2024-01-01&endTime=2024-12-31"
curl "http://localhost:3010/api/trends/related-queries?keyword=project+management&startTime=2024-01-01&endTime=2024-12-31"
```

## 🔧 **Updated Configuration**

### **1. Environment Variables**

```bash
# Update your .env file
GOOGLE_TRENDS_API_URL=http://localhost:3010
ANTHROPIC_API_KEY=your-anthropic-key
```

### **2. Start the Google Trends API Server**

You need to start the Google Trends API server at `localhost:3010`. The server should provide these endpoints:

```bash
# Start your Google Trends API server
# (This should be running on port 3010)
```

### **3. Test the API**

```bash
# Test health
curl http://localhost:3010/api/health

# Test daily trends
curl http://localhost:3010/api/trends/daily

# Test interest over time
curl "http://localhost:3010/api/trends/interest-over-time?keyword=AI&startTime=2024-01-01&endTime=2024-12-31"
```

## 🚀 **Updated SaaS Validator Integration**

### **1. Updated MCP Client**

The `mcp_client.py` has been updated to work with the new API structure:

- ✅ Updated endpoint URLs to use `/api/` prefix
- ✅ Updated parameter handling for `startTime`/`endTime`
- ✅ Added new endpoints (realtime, interest-by-region)
- ✅ Improved error handling and logging

### **2. Updated NestJS Integration**

The `nestjs_integration.py` has been updated with new endpoints:

```python
# New endpoints available
@app.get("/trends/daily")           # Daily trends
@app.get("/trends/realtime")        # Realtime trends
@app.get("/trends/related-topics")  # Related topics
@app.get("/trends/interest-by-region") # Interest by region
```

### **3. Test the Updated Integration**

```bash
# Test the updated SaaS Validator API
curl http://localhost:8001/health

# Test with a SaaS validation query
curl -X POST http://localhost:8001/validate \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I build a SaaS for AI project management?"}'
```

## 🧪 **Testing the Updated API**

### **1. Run the Test Script**

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY=your-key-here

# Run the updated test
python test_new_api.py
```

### **2. Expected Test Results**

When the Google Trends API server is running:

```
✅ Health Check: PASS
✅ Daily Trends: PASS - Found X trends
✅ Related Queries: PASS - Found X queries
✅ Related Topics: PASS - Found X topics
✅ Interest Over Time: PASS
✅ Interest By Region: PASS
✅ Realtime Trends: PASS - Found X trends
```

## 🔄 **Migration Guide**

### **From Old API to New API**

| Old Endpoint | New Endpoint | Changes |
|--------------|--------------|---------|
| `/health` | `/api/health` | Added `/api/` prefix |
| `/trending` | `/api/trends/daily` | Renamed and moved |
| `/related-queries` | `/api/trends/related-queries` | Added date parameters |
| `/interest-over-time` | `/api/trends/interest-over-time` | Added date parameters |
| N/A | `/api/trends/realtime` | New endpoint |
| N/A | `/api/trends/related-topics` | New endpoint |
| N/A | `/api/trends/interest-by-region` | New endpoint |

### **Parameter Changes**

| Old Parameter | New Parameter | Format |
|---------------|---------------|--------|
| `timeframe` | `startTime`, `endTime` | `YYYY-MM-DD` |
| `country` | `country` | Same |
| `limit` | `limit` | Same |

## 🚀 **Quick Start**

### **1. Start the Google Trends API Server**

```bash
# Start your Google Trends API server on port 3010
# (This should be running and providing the new endpoints)
```

### **2. Start the SaaS Validator API**

```bash
# Set environment variables
export ANTHROPIC_API_KEY=your-key-here
export GOOGLE_TRENDS_API_URL=http://localhost:3010

# Start the SaaS Validator API
python nestjs_integration.py
```

### **3. Test the Integration**

```bash
# Test health
curl http://localhost:8001/health

# Test validation
curl -X POST http://localhost:8001/validate \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I build a SaaS for AI project management?"}'
```

## 🔍 **Troubleshooting**

### **Common Issues**

1. **Google Trends API not responding**
   ```bash
   # Check if the server is running
   curl http://localhost:3010/api/health
   ```

2. **Missing Anthropic API key**
   ```bash
   # Set the environment variable
   export ANTHROPIC_API_KEY=your-key-here
   ```

3. **Wrong API endpoints**
   - Ensure you're using the new `/api/` prefix
   - Check that date parameters are in `YYYY-MM-DD` format

### **Debug Commands**

```bash
# Check Google Trends API
curl http://localhost:3010/api/health

# Check SaaS Validator API
curl http://localhost:8001/health

# Test daily trends
curl http://localhost:3010/api/trends/daily

# Test interest over time
curl "http://localhost:3010/api/trends/interest-over-time?keyword=AI&startTime=2024-01-01&endTime=2024-12-31"
```

## 📚 **Updated Documentation**

- **README.md** - Main project documentation
- **NESTJS_INTEGRATION.md** - NestJS integration guide
- **INTEGRATION_SUMMARY.md** - Complete integration summary

## 🎯 **Next Steps**

1. ✅ **Start your Google Trends API server** on port 3010
2. ✅ **Set your Anthropic API key** in environment variables
3. ✅ **Test the updated integration** with the new endpoints
4. ✅ **Integrate with your NestJS backend** using the updated API

The SaaS Validator agent is now ready to work with the new Google Trends API structure! 