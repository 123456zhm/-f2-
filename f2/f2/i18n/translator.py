def _(text):
    return text

class TranslationManager:
    def __init__(self, language='zh'):
        self.language = language
    
    def translate(self, text):
        return text