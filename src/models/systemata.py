'''
Classes to represent different ancient musical systemata.



'''

class GreaterPerfectSystem:


    def __init__(self, mese_frequency: float, genus: str, chroa: str) -> None:
        self.mese_frequency: float = mese_frequency
        self.genus: str = genus
        self.chroa: str = chroa

        
        self.proslambanomenos: float

        # Tetrachords hypaton and meson
        self.hypate_hypaton: float
        self.parhypate_hypaton: float
        self.lichanos_hypaton: float
        self.hypate_meson: float
        self.parhypate_meson: float
        self.lichanos_meson: float
        self.mese: float

        # Tetrachords diezeugmenon and hyperbolaion
        self.paramese: float
        self.trite_diezeugmenon: float
        self.paranete_diezeugmenon: float
        self.nete_diezeugmenon: float
        self.trite_hyperbolaion: float
        self.paranete_hyperbolaion: float
        self.nete_hyperbolaion: float





    
