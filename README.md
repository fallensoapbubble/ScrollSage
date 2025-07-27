# ScrollSage 🔮

**Decode Your Media Culture Clusters**

ScrollSage is a beautiful web application that analyzes your digital taste preferences using Qloo APIs and AI to uncover hidden cultural narratives, biases, and media consumption patterns. Discover how your favorite influencers, brands, and media shape your worldview.

## ✨ Features

- **🎯 Taste Analysis**: Upload 2-5 influencers, brands, or media you engage with
- **🔍 Cultural Decoding**: AI-powered analysis of your taste clusters and cultural positioning
- **🔄 Opposite Bubble Recommendations**: Discover contrasting content from different taste cultures
- **🧠 Bias Detection**: Uncover cultural biases and ideologies in your media consumption
- **💫 Beautiful UI**: Glass-morphism design with neon pastel aesthetics and smooth animations
- **📊 Identity Critique**: Understand how corporate interests and media narratives shape identity

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Qloo API key
- Gemini key

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

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your API keys:
   ```env
   QLOO_API_KEY=your-qloo-api-key-here
   OPENAI_API_KEY=your-openai-api-key-here
   SECRET_KEY=your-secret-key-here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t scrollsage .
docker run -p 5000:5000 --env-file .env scrollsage
```

## 🏗️ Architecture

### Backend (Flask)

- **`/`** - Main page with taste input form
- **`/insights`** - POST endpoint for processing user inputs and returning insights

### Frontend (HTML + Tailwind CSS)

- **Glass-morphism UI**: Translucent cards with neon borders and smooth animations
- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Form**: Dynamic entity input with type categorization
- **Animated Results**: Staggered card animations for insight display

### API Integration

#### Qloo API
- **Search Endpoint**: Resolves user entities to Qloo URNs
- **Insights Endpoint**: Analyzes taste clusters and affinities
- **Entity Types**: Supports person, brand, movie, tv_show, podcast, book, artist, video_game, destination, place

#### OpenAI API
- **Cultural Analysis**: Processes Qloo data to generate insights
- **Structured Output**: Returns narratives, biases, recommendations, and critiques

## 📋 API Documentation

### POST /insights

**Request Body:**
```json
{
  "entities": [
    {
      "name": "@username",
      "type": "person"
    },
    {
      "name": "Brand Name",
      "type": "brand"
    }
  ]
}
```

**Response:**
```json
{
  "user_entities": [...],
  "qloo_data": {...},
  "insights": {
    "narratives": "Analysis of cultural narratives...",
    "taste_alignment": "Analysis of shared taste traits...",
    "cultural_biases": "Analysis of cultural biases...",
    "opposite_recommendations": ["Contrasting content 1", "Contrasting content 2"],
    "interpretation_contrast": "Analysis of media interpretation...",
    "identity_critique": "Analysis of corporate interests..."
  },
  "clusters": [...],
  "affinities": [...],
  "recommendations": [...]
}
```

## 🎨 UI Components

### Glass-Morphism Cards
- Translucent backgrounds with backdrop blur
- Neon border effects with glow animations
- Smooth hover transitions and scaling effects

### Animations
- **Floating Bubbles**: Background decorative elements
- **Fade-in Effects**: Smooth entrance animations
- **Staggered Cards**: Sequential insight card reveals
- **Hover Effects**: Interactive feedback on user interaction

### Color Scheme
- **Neon Pink**: `#ff6b9d`
- **Neon Blue**: `#4ecdc4`
- **Neon Purple**: `#a855f7`
- **Neon Green**: `#10b981`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `QLOO_API_KEY` | Your Qloo API key | Yes |
| `QLOO_API_URL` | Qloo API base URL | No (default: https://api.qloo.com) |
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `SECRET_KEY` | Flask secret key | No (auto-generated) |

### Supported Entity Types

- `person` / `influencer` → `urn:entity:person`
- `brand` → `urn:entity:brand`
- `movie` → `urn:entity:movie`
- `tv_show` → `urn:entity:tv_show`
- `podcast` → `urn:entity:podcast`
- `book` → `urn:entity:book`
- `artist` → `urn:entity:artist`
- `video_game` → `urn:entity:video_game`
- `destination` → `urn:entity:destination`
- `place` → `urn:entity:place`

## 🧪 Development

### Project Structure
```
ScrollSage/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Main UI template
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── env.example          # Environment variables template
└── README.md           # This file
```

### Running Tests
```bash
# Install test dependencies
pip install pytest

# Run tests
pytest
```

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

## 🙏 Acknowledgments

- **Qloo**: For providing cultural intelligence APIs
- **OpenAI**: For AI-powered analysis capabilities
- **Tailwind CSS**: For the beautiful UI framework
- **Flask**: For the robust web framework

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Include your environment details and error messages

---

**Built with ❤️ for cultural exploration and media literacy** 