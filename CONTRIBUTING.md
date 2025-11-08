# Contributing Guide

Vielen Dank für Ihr Interesse, zum Rüsselsheim Chatbot beizutragen!

## Entwicklungsumgebung einrichten

1. **Repository forken und klonen**
   ```bash
   git clone https://github.com/your-username/r-sselsheim-chatbot.git
   cd r-sselsheim-chatbot
   ```

2. **Entwicklungsumgebung starten**
   ```bash
   cp .env.example .env
   # API Keys in .env eintragen
   make install
   ```

## Code-Stil

### Python (Backend)

- **Formatter**: Black
- **Linter**: Flake8
- **Type Hints**: Verwenden Sie Type Hints wo möglich
- **Docstrings**: Google-Style Docstrings

```python
def example_function(param: str) -> dict:
    """Short description.

    Args:
        param: Parameter description

    Returns:
        Return value description
    """
    pass
```

Vor dem Commit:
```bash
black app/
flake8 app/
mypy app/
```

### JavaScript/React (Frontend)

- **Formatter**: Prettier (optional)
- **Linter**: ESLint
- **Komponenten**: Functional Components mit Hooks

## Git Workflow

1. **Feature Branch erstellen**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Commits**
   - Kleine, fokussierte Commits
   - Aussagekräftige Commit-Messages
   - Conventional Commits Format (optional)

   ```
   feat: Add new feature
   fix: Fix bug in chat service
   docs: Update README
   refactor: Refactor RAG service
   test: Add tests for chat API
   ```

3. **Tests ausführen**
   ```bash
   # Backend
   pytest

   # Frontend
   npm test
   ```

4. **Pull Request erstellen**
   - Beschreiben Sie Ihre Änderungen
   - Verlinken Sie zugehörige Issues
   - Fügen Sie Screenshots hinzu (bei UI-Änderungen)

## Tests schreiben

### Backend Tests

```python
# tests/test_chat_service.py
import pytest
from app.services import ChatService

def test_chat_response(db_session):
    service = ChatService(db_session)
    result = service.chat("Test message", "session-id")
    assert result["message"] is not None
```

### Frontend Tests

```javascript
// src/components/__tests__/ChatInput.test.jsx
import { render, screen } from '@testing-library/react';
import ChatInput from '../ChatInput';

test('renders input field', () => {
  render(<ChatInput onSend={() => {}} />);
  const inputElement = screen.getByPlaceholderText(/Stellen Sie Ihre Frage/i);
  expect(inputElement).toBeInTheDocument();
});
```

## Neue Features hinzufügen

1. **Issue erstellen** oder kommentieren
2. **Feature entwickeln** auf einem Branch
3. **Tests schreiben**
4. **Dokumentation aktualisieren**
5. **Pull Request erstellen**

## Fragen?

Öffnen Sie ein Issue oder kontaktieren Sie die Maintainer.

Vielen Dank für Ihren Beitrag! 🎉
