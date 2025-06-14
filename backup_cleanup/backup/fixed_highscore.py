#!/usr/bin/env python3
import json
import os
import time

class HighScoreManager:
    def __init__(self, filename="highscores.json"):
        self.filename = filename
        self.highscores = {
            "endless": [],
            "time_attack": [],
            "missions": []
        }
        self.load_highscores()
    
    def load_highscores(self):
        """Load high scores from file if it exists"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.highscores = json.load(f)
        except Exception as e:
            print(f"Error loading high scores: {e}")
            # If there's an error, we'll use the default empty high scores
    
    def save_highscores(self):
        """Save high scores to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.highscores, f)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    def add_score(self, game_mode, player_name, score, distance=0, coins=0):
        """Add a new score to the appropriate game mode list only if it's higher than the current maximum"""
        mode_key = self._get_mode_key(game_mode)
        
        # Check if this is a new high score
        current_scores = self.highscores[mode_key]
        
        # If there are no scores yet, or if this score is higher than the highest score
        if not current_scores or score > max([s["score"] for s in current_scores], default=0):
            print(f"New highest score: {score}!")
            
            # Create score entry with timestamp
            score_entry = {
                "name": player_name,
                "score": score,
                "distance": distance,
                "coins": coins,
                "date": time.strftime("%Y-%m-%d %H:%M")
            }
            
            # Add to appropriate list
            self.highscores[mode_key].append(score_entry)
            
            # Sort by score (descending)
            self.highscores[mode_key].sort(key=lambda x: x["score"], reverse=True)
            
            # Keep only top 10 scores
            self.highscores[mode_key] = self.highscores[mode_key][:10]
            
            # Save to file
            self.save_highscores()
            return True
        else:
            print(f"Score {score} is not higher than the current highest score.")
            return False
    
    def get_highscores(self, game_mode):
        """Get high scores for the specified game mode"""
        mode_key = self._get_mode_key(game_mode)
        return self.highscores[mode_key]
    
    def is_high_score(self, game_mode, score):
        """Check if the score qualifies as a high score (only if it's the highest)"""
        mode_key = self._get_mode_key(game_mode)
        scores = self.highscores[mode_key]
        
        # If there are no scores yet, it's automatically a high score
        if not scores:
            return True
        
        # Otherwise, check if it's higher than the highest score
        return score > max([s["score"] for s in scores])
    
    def _get_mode_key(self, game_mode):
        """Convert game mode constant to string key"""
        if game_mode == 0:  # GAME_MODE_ENDLESS
            return "endless"
        elif game_mode == 1:  # GAME_MODE_TIME_ATTACK
            return "time_attack"
        elif game_mode == 2:  # GAME_MODE_MISSIONS
            return "missions"
        else:
            return "endless"  # Default
