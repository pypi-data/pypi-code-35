from rb.core.lang import Lang

import numpy as np

class TextElement:
    def __init__(self, lang: Lang, text: str, container: 'TextElement' = None):
        self.text = text
        self.lang = lang
        self.container = container
        self.vectors = {}
        self.components = []
        self.vectors_initialized = False
        self.indices = {}
        
    def get_vector(self, model: 'VectorModel') -> np.array:
        return self.vectors[model]

    