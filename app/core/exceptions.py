class HighMalePercent(Exception):
    def __init__(self):
        super().__init__("Hay demasiados machos capturados")

class ApplyProduct(Exception):
    def __init__(self):
        super().__init__("Aplicar producto preventivo")