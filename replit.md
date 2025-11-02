# Call Bot for Service Businesses

## Overview

This is an inbound call bot system designed for service businesses (garage doors, appliance repair, HVAC, etc.) that automatically handles customer calls through an AI-powered conversational interface. The system can answer calls with branded voice, qualify leads, book appointments, and send follow-up communications. It uses a turn-based conversation flow with Twilio for telephony, OpenAI for conversation processing, ElevenLabs for text-to-speech, and n8n for automation workflows.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Framework
- **Backend**: Flask web application with SQLAlchemy ORM for database operations
- **Database**: SQLite by default (configurable via DATABASE_URL environment variable)
- **Session Management**: Flask sessions with configurable secret key
- **Proxy Handling**: Werkzeug ProxyFix for proper HTTPS URL generation

### Call Flow Architecture
- **Turn-based Conversation**: Non-duplex conversation flow for stability and reliability
- **Call Handling**: Twilio webhook endpoints process incoming calls and speech input
- **Speech Processing**: Twilio's built-in speech-to-text via `<Gather input="speech">`
- **Response Generation**: OpenAI processes conversation context and generates structured responses
- **Audio Synthesis**: ElevenLabs converts AI responses to natural-sounding speech
- **Audio Hosting**: Static file serving for MP3 audio clips that Twilio can play

### Data Models
- **BusinessProfile**: Stores business configuration, service areas, hours, pricing, calendar settings, and AI prompts
- **CallLog**: Tracks individual calls with metadata, conversation history, lead capture, and appointment booking status
- **CallTurn**: Detailed conversation turns with user input, AI responses, and action tracking

### API Integration Pattern
- **Conversation Processing**: OpenAI GPT-5 with structured JSON responses and function calling
- **Voice Synthesis**: ElevenLabs API with configurable voice models and settings
- **Automation**: n8n webhooks for calendar booking and CRM integration
- **Communication**: Twilio for both voice handling and SMS notifications

### Admin Interface
- **Dashboard**: Bootstrap-based dark theme admin interface
- **Business Management**: CRUD operations for business profiles and configuration
- **Call Monitoring**: Real-time call logs and conversation tracking
- **Analytics**: Basic metrics on calls, appointments, and lead conversion

## External Dependencies

### Communication Services
- **Twilio**: Programmable Voice API for call handling, speech-to-text, and SMS
- **ElevenLabs**: Text-to-speech API for natural voice generation

### AI and Processing
- **OpenAI**: GPT-5 model for conversation processing and lead qualification
- **n8n**: Webhook automation platform for calendar booking and CRM integration

### Infrastructure
- **SMTP Server**: Email service (Gmail by default) for call summaries and notifications
- **Static File Storage**: Local file system for audio file hosting (configurable for S3)

### Frontend Dependencies
- **Bootstrap**: Dark theme UI framework with Font Awesome icons
- **JavaScript**: Form validation, phone number formatting, and UI enhancements

### Environment Configuration
- Database: SQLite (default) or PostgreSQL via DATABASE_URL
- Audio Storage: Local static files with configurable base URL for public access
- Session Security: Configurable secret key for Flask sessions
- API Keys: Environment variables for all third-party service authentication