"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        ("High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False}),
        ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.40, "likes_acoustic": True}),
        ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.90, "likes_acoustic": False}),
        ("Edge Case: conflicting prefs", {"genre": "lofi", "mood": "happy", "energy": 0.95, "likes_acoustic": True}),
    ]

    for name, user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== {name} ===")
        print(f"Prefs: {user_prefs}\n")
        for song, score, explanation in recommendations:
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
