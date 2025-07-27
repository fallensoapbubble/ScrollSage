# ScrollSage 🔮

**Decode Your Media Culture Clusters**

ScrollSage is a web application that helps you analyze your digital taste preferences and media culture clusters. It features a beautiful glass-morphism UI and a Flask backend that processes your favorite influencers, brands, or media picks.

## ✨ Features

- **Taste Analysis**: Upload 2-5 influencers, brands, or media you engage with
- **Cultural Decoding**: Backend parses your taste seeds and can call external APIs for insights
- **Beautiful UI**: Glass-morphism design with pastel neon aesthetics and smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.9+

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ScrollSage
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   > **Note:** The requirements.txt is auto-generated and may include extra packages from development. You may trim it if you want a minimal install.

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 🛠️ Troubleshooting

### Flask/Watchdog ImportError: cannot import name 'EVENT_TYPE_OPENED'

If you see an error like this when running `python app.py`:

```
ImportError: cannot import name 'EVENT_TYPE_OPENED' from 'watchdog.events' (.../site-packages/watchdog/events.py)
```

**How to fix:**

- Open `app.py` in a text editor.
- Find the last line (it looks like this):
  ```python
  app.run(debug=True, host='0.0.0.0', port=5000)
  ```
- Change it to:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
  ```
- Save the file and run `python app.py` again.

This disables Flask's auto-reloader, which avoids the watchdog import error. You can still develop and debug as usual, but you'll need to restart the server manually after code changes.

Alternatively, you can run without debug mode:
```python
app.run(host='0.0.0.0', port=5000)
```

Or install a compatible watchdog version:
```bash
pip install watchdog==2.1.9
```

## 🏗️ Architecture

### Backend (Flask)

- **`app.py`** - Main Flask application
  - **`/`** (GET): Renders the main form (template: `page.html`)
  - **`/`** (POST): Receives form data, parses entities, returns JSON
  - **`/insights`** (POST): Receives JSON `{entities: [...]}` and calls `calltoAPI` from `func.py` to process and return insights
  - **`/add/<a>/<b>`**: Example endpoint for testing
- **`func.py`** - Contains the `calltoAPI` function for external API calls or mock analysis

### Frontend (HTML + Tailwind CSS)

- **`templates/page.html`**: Main UI template (not `index.html`)
- **Glass-morphism UI**: Translucent cards, neon borders, smooth animations
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Form**: Dynamic entity input with type categorization

## 📋 API Documentation

### POST /

**Request:** (form submission)
- Fields: `entity_0_name`, `entity_0_type`, `entity_1_name`, `entity_1_type`, ...

**Response:**
```json
{
  "status": "success",
  "message": "Received N entities",
  "entities": [
    {"name": "...", "type": "..."},
    ...
  ]
}
```

### POST /insights

**Request:**
```json
{
  "entities": [
    {"name": "...", "type": "..."},
    ...
  ]
}
```

**Response:**
- Returns the result of `calltoAPI(entities)` (see `func.py` for details)

## 🧪 Development

### Project Structure
```
ScrollSage/
├── app.py                 # Main Flask application
├── func.py                # API call/analysis logic
├── templates/
│   └── page.html          # Main UI template
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

### Running Tests
- No formal tests included yet. You can use the `/add/<a>/<b>` endpoint for basic checks.

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for all functions
- Handle exceptions gracefully

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the Issues page
2. Create a new issue with detailed information
3. Include your environment details and error messages

---

**Built with ❤️ for cultural exploration and media literacy** 