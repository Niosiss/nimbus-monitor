# Nimbus Monitor

A FastAPI-based web application for real-time monitoring and visualization of system metrics (CPU, Memory, Disk).

## 📋 Features

- **Live System Metrics**: Monitor CPU, Memory, and Disk usage in real-time
- **WebSocket Integration**: Low-latency server-client communication using WebSocket
- **Database Support**: Store historical metrics in SQLite
- **Chart Visualization**: Effective graphs with Chart.js
- **CORS Enabled**: Allow access from different origins

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **psutil** - System metrics
- **SQLite** - Database

### Frontend
- **HTML5** - Markup language
- **JavaScript (ES6+)** - Client-side logic
- **Chart.js** - Charting library

## 📁 Project Structure

```
nimbus-monitor/
├── backend/
│   ├── main.py              # FastAPI application and API endpoints
│   ├── system_metrics.py    # System metrics collection
│   ├── database.py          # Database operations
│   ├── requirements.txt     # Python dependencies
│   └── metrics.db           # SQLite database (auto-created)
├── frontend/
│   ├── index.html           # Main HTML page
│   └── app.js              # JavaScript client logic
└── README.md               # This file
```

## 🚀 Installation and Setup

### 1. Requirements
- Python 3.8+
- pip (Python package manager)
- Modern web browser

### 2. Backend Installation

```bash
cd backend
pip install -r requirements.txt
```

### 3. Start Backend

```bash
cd backend
uvicorn main:app --reload
```

The server will run at:
- API: `http://localhost:8000`
- WebSocket: `ws://localhost:8000/ws`

### 4. Access Frontend

Open your browser and navigate to:
```
http://localhost:8000/frontend/index.html
```

## 📊 API Endpoints

### WebSocket
- **WS Endpoint**: `ws://localhost:8000/ws`
  - Sends system metrics every 0.5 seconds
  - Auto-reconnect: Reconnects after 3 seconds if connection drops
  - Response format:
    ```json
    {
      "timestamp": "14:30:45",
      "cpu_usage": 25.5,
      "memory_usage": 55.3,
      "disk_usage": 40.2
    }
    ```

### REST API
- **GET** `/api/history` - Returns last 50 metric records
  - Response:
    ```json
    [
      {
        "timestamp": "14:30:45",
        "cpu_usage": 25.5,
        "memory_usage": 55.3,
        "disk_usage": 40.2
      }
    ]
    ```

## 🔧 Configuration

### WebSocket URL (Frontend)
Edit the WebSocket URL in `frontend/app.js`:
```javascript
const ws = new WebSocket("wss://your-server-url/ws");
```

### Data Update Interval
Change the `asyncio.sleep()` value in `backend/main.py`:
```python
await asyncio.sleep(0.5)  # Time in seconds
```

### CPU Measurement Interval
Edit `backend/system_metrics.py`:
```python
cpu_usage = psutil.cpu_percent(interval=0.1)  # Faster measurement
```

## 📈 Chart Features

- **CPU Usage**: Blue line (rgb(75, 192, 192))
- **Memory Usage**: Red line (rgb(255, 99, 132))
- **Disk Usage**: Light blue line (rgb(54, 162, 235))
- **Maximum 20 data points**: Old data is automatically removed
- **Real-time updates**: Updates immediately with each WebSocket message
- **Data ordering**: Old data on the left, new data on the right

## 🐛 Troubleshooting

### WebSocket connection failed
```
Error: WebSocket connection failed
```
**Solution:**
- Check browser console (F12) for errors
- Verify server is running: `http://localhost:8000/docs`
- Check WebSocket URL is correct
- Check firewall configuration

### Database error
```
sqlite3.OperationalError: no such table: metrics
```
**Solution:** 
- Ensure `init_db()` is called in `backend/main.py`
- Delete `metrics.db` and restart

### Psutil not found
```
ModuleNotFoundError: No module named 'psutil'
```
**Solution:**
```bash
pip install psutil
```

### Port already in use
```
Address already in use
```
**Solution:**
```bash
# Use a different port
uvicorn main:app --port 8001 --reload
```

## 🔐 Security Notes

- **CORS**: Open to all origins (`*`) - Restrict in production
  ```python
  allow_origins=["https://yourdomain.com"]
  ```

- **WebSocket**: Not encrypted - Use WSS+SSL in production
  ```
  wss://your-domain.com/ws
  ```

- **Authentication**: Not implemented - Add in production

- **Database**: No password protection - Add in production

## 📝 Usage Example

1. **Start the backend**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Open frontend**
   - Browser: `http://localhost:8000/frontend/index.html`

3. **Monitor real-time metrics**
   - Charts update every 0.5 seconds
   - WebSocket auto-reconnects on disconnect

4. **Get historical data**
   - `http://localhost:8000/api/history`

## 🧪 Testing

### FastAPI Documentation
Visit FastAPI's automatic API documentation:
```
http://localhost:8000/docs
```

### System Metrics Test
Test in the backend directory:
```bash
cd backend
python -c "from system_metrics import get_system_metrics; print(get_system_metrics())"
```

## 📚 Dependencies

All dependencies are listed in `requirements.txt`.

To see installed packages:
```bash
pip list
```

## 🚀 Production Deployment

### Deploy with Gunicorn
```bash
pip install gunicorn
cd backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Deploy with Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

## 📄 License

MIT License

## 👤 Developer

**Niosiss**

---
python -m uvicorn main:app
**Last Updated**: August 14, 2026