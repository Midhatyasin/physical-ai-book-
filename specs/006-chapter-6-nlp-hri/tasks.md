# Testable Tasks: Chapter 6 - NLP for HRI

## Task 1: Whisper Integration

**Status**: pending | **Priority**: P1

### Description
Integrate OpenAI Whisper for speech recognition on robot.

### Test Cases
- [ ] Whisper transcribes speech with < 5% WER
- [ ] Real-time transcription achieves < 500ms latency
- [ ] Noise robustness tested (SNR > 10dB)

### Code Reference
```python
import whisper

class SpeechRecognizer:
    def __init__(self, model="base", device="cuda"):
        self.model = load_whisper(model, device=device)

    def transcribe(self, audio_path):
        result = self.model.transcribe(audio_path)
        return result["text"]
```

---

## Task 2: Intent Classification

**Status**: pending | **Priority**: P1

### Description
Implement intent classifier for robot commands.

### Test Cases
- [ ] Intent accuracy > 90% on test set
- [ ] Slot filling correctly extracts entities
- [ ] Handles out-of-vocabulary gracefully

### Code Reference
```python
class IntentClassifier(nn.Module):
    def __init__(self, vocab_size, num_intents, num_slots, embed_dim=128):
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.intent_head = nn.Linear(embed_dim, num_intents)
        self.slot_head = nn.Linear(embed_dim, num_slots)
```

---

## Task 3: Dialogue Manager

**Status**: pending | **Priority**: P1

### Description
Implement rule-based and neural dialogue management.

### Test Cases
- [ ] Multi-turn dialogue maintains context
- [ ] Slot filling persists across turns
- [ ] Error handling for misunderstood commands

---

## Task 4: TTS Integration

**Status**: pending | **Priority**: P2

### Description
Integrate speech synthesis for robot responses.

### Test Cases
- [ ] TTS produces natural-sounding speech
- [ ] Latency < 200ms for short responses
- [ ] Multiple voices/languages supported

---

## Task 5: LLM Integration

**Status**: pending | **Priority**: P2

### Description
Integrate LLM for natural language robot control.

### Test Cases
- [ ] LLM generates valid robot commands
- [ ] Safety filter prevents dangerous commands
- [ ] Context window maintains conversation history
