# Architecture Plan: Chapter 6 - NLP for HRI

## 1. Scope and Dependencies

### In Scope
- Speech recognition integration
- Intent classification and slot filling
- Dialogue management
- Speech synthesis
- Vision-language models
- LLM integration

### Out of Scope
- Low-level audio processing (refer to libraries)
- Hardware integration (Chapter 8)
- Multi-robot coordination (Chapter 7)

### External Dependencies
- Whisper (OpenAI)
- Vosk (for edge deployment)
- transformers (HuggingFace)
- LangChain (LLM integration)

## 2. Key Decisions and Rationale

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| ASR Engine | Whisper vs Vosk | Both | Whisper for accuracy, Vosk for edge |
| NLU Framework | Rasa vs custom | Custom | Educational value, simplicity |
| LLM Integration | LangChain vs direct | LangChain | Abstraction, flexibility |
| TTS Engine | Coqui vs Edge | Edge TTS | No本地部署需求 |

## 3. Interfaces and API Contracts

### Speech Recognition
```python
class SpeechRecognizer:
    def __init__(self, model: str = "base")
    def transcribe(self, audio: np.ndarray) -> str
```

### Intent Classifier
```python
class IntentClassifier:
    def __init__(self, model_path: str)
    def classify(self, text: str) -> IntentPrediction
```

### Dialogue Manager
```python
class DialogueManager:
    def __init__(self, states: List[DialogueState], policies: List[Policy])
    def predict(self, state: DialogueState) -> DialogueAction
```

## 4. Chapter Structure

1. Introduction to NLP for HRI
2. Automatic Speech Recognition
3. Intent Recognition and NLU
4. Dialogue Systems
5. Speech Synthesis
6. Vision-Language Models
7. LLM for Robot Control
