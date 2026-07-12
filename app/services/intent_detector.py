from app.domain.intents import Intent


class IntentDetector:
    def detect(self, text: str) -> Intent:
        text = text.lower()

        if "remind" in text:
            return Intent.REMINDER

        return Intent.CHAT
