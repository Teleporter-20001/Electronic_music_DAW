import os

class Settings:
    '''
    A param server for managing audio software settings.
    '''

    default_speed: int = 120
    default_beat_num_per_bar: int = 4
    default_beat_unit: int = 4
    default_sample_rate: int = 44100
    
    config_path = os.path.join('../cache', 'settings.json')
    
    def __init__(self):
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)