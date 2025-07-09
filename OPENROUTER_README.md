# OpenRouter API Integration

## Overview

This project now includes AI-enhanced TRIZ analysis using OpenRouter API with the deepseek-r1t2-chimera model. The integration provides more intelligent parameter detection and solution enhancement.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the project root or set the following environment variables:

```bash
# Required: OpenRouter API Key
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# Optional: Site information for OpenRouter
OPENROUTER_SITE_URL=https://your-domain.com
OPENROUTER_SITE_NAME=InnovateTRIZ
```

### 3. Test the Integration

Run the test script to verify the OpenRouter API connection:

```bash
python test_openrouter.py
```

## Features

### AI-Enhanced Analysis

When the "AI Smart Enhancement" toggle is enabled:

1. **Problem Analysis**: AI automatically identifies technical parameters and contradictions
2. **Parameter Detection**: Automatically detects improving and worsening parameters
3. **Solution Enhancement**: AI provides contextual application suggestions for TRIZ principles
4. **Enhanced Descriptions**: More detailed and problem-specific solution descriptions

### API Endpoints

- `POST /api/ai-analyze` - AI-enhanced TRIZ analysis
- `POST /api/analyze` - Standard TRIZ analysis (fallback)

## Usage

### Frontend Integration

The AI enhancement is controlled by a toggle switch in the analysis form:

```html
<div class="ai-toggle-section">
    <label class="ai-toggle-label">
        <input type="checkbox" id="ai-enhanced" checked>
        <span class="ai-toggle-switch"></span>
        <span class="ai-toggle-text">
            <i class="fas fa-magic"></i> AI Smart Enhancement
        </span>
    </label>
</div>
```

### Backend Processing

The AI analysis follows this workflow:

1. **AI Problem Analysis**: Extract technical parameters and contradictions
2. **TRIZ Analysis**: Apply traditional TRIZ methodology
3. **AI Solution Enhancement**: Provide contextual application guidance
4. **Response Generation**: Return enhanced solutions with AI insights

## Model Information

- **Provider**: OpenRouter
- **Model**: tngtech/deepseek-r1t2-chimera:free
- **Temperature**: 0.3 (balanced creativity/consistency)
- **Max Tokens**: 500-1000 depending on task

## Cost Considerations

The integration uses a free model tier, but be aware of:
- Rate limits may apply
- Response time may vary
- Quality depends on model availability

## Error Handling

The system gracefully degrades:
- If OpenRouter API is unavailable → Falls back to standard TRIZ analysis
- If AI analysis fails → Uses user-provided parameters
- If solution enhancement fails → Returns original TRIZ solutions

## Deployment Notes

### Vercel Deployment

Set environment variables in Vercel dashboard:
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `OPENROUTER_SITE_URL`: Your deployed site URL
- `OPENROUTER_SITE_NAME`: Your site name

### Local Development

```bash
export OPENROUTER_API_KEY="your-api-key-here"
python triz_web_app/backend/app.py
```

## Monitoring

Check the health endpoint for system status:

```bash
curl http://localhost:5001/api/health
```

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Ensure `OPENROUTER_API_KEY` is set
   - Check environment variable spelling

2. **Rate Limiting**
   - OpenRouter free tier has usage limits
   - Consider upgrading to paid tier for production

3. **Model Unavailable**
   - deepseek-r1t2-chimera model may have availability issues
   - System will fall back to standard TRIZ analysis

4. **JSON Parsing Errors**
   - AI responses may not always be valid JSON
   - Error handling extracts usable information when possible

### Debug Mode

Enable debug logging by setting:

```bash
export FLASK_ENV=development
```

This will provide detailed error messages and API response information.

## Future Enhancements

- Multiple model support
- Response caching
- Advanced prompt engineering
- Custom model fine-tuning
- Usage analytics and monitoring