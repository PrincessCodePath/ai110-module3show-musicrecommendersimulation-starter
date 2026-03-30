from __future__ import annotations

from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv
import math

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k songs ranked for this user."""
        scored: List[Tuple[Song, float]] = []
        for song in self.songs:
            score, _reasons = score_song(
                {
                    "favorite_genre": user.favorite_genre,
                    "favorite_mood": user.favorite_mood,
                    "target_energy": user.target_energy,
                    "likes_acoustic": user.likes_acoustic,
                },
                {
                    "id": song.id,
                    "title": song.title,
                    "artist": song.artist,
                    "genre": song.genre,
                    "mood": song.mood,
                    "energy": song.energy,
                    "tempo_bpm": song.tempo_bpm,
                    "valence": song.valence,
                    "danceability": song.danceability,
                    "acousticness": song.acousticness,
                },
            )
            scored.append((song, score))

        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a song was recommended."""
        _score, reasons = score_song(
            {
                "favorite_genre": user.favorite_genre,
                "favorite_mood": user.favorite_mood,
                "target_energy": user.target_energy,
                "likes_acoustic": user.likes_acoustic,
            },
            {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "tempo_bpm": song.tempo_bpm,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            },
        )
        return "; ".join(reasons) if reasons else "No strong matches; included based on overall similarity."

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dictionaries."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = dict(row)

            if "id" in song and song["id"] is not None:
                song["id"] = int(song["id"])

            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                if key in song and song[key] is not None:
                    song[key] = float(song[key])

            songs.append(song)

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song and return (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    user_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    user_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))

    if user_genre is not None and song.get("genre") == user_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if user_mood is not None and song.get("mood") == user_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    if target_energy is not None and song.get("energy") is not None:
        diff = abs(float(song["energy"]) - float(target_energy))
        energy_points = 2.0 * max(0.0, 1.0 - diff)
        score += energy_points
        reasons.append(f"energy close to target (+{energy_points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None and song.get("acousticness") is not None:
        a = float(song["acousticness"])
        if bool(likes_acoustic):
            acoustic_points = 1.0 * a
            reasons.append(f"acoustic preference (+{acoustic_points:.2f})")
        else:
            acoustic_points = 1.0 * (1.0 - a)
            reasons.append(f"non-acoustic preference (+{acoustic_points:.2f})")
        score += acoustic_points

    if math.isfinite(score) is False:
        return 0.0, ["invalid score reset to 0.0"]

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank songs by score and return top-k with explanations."""
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
