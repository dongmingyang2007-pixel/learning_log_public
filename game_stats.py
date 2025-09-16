class GameStats:
    def __init__(x,tht_game):
        x.settings = tht_game.settings
        x.reset_stats()

    def reset_stats(x):
        x.life_left = x.settings.life_limit