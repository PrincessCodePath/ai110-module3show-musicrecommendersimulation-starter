# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

VibeBaseRank CLI 1.0

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration

This system recommends the top 5 songs from a small CSV catalog based on a user’s stated preferences. It assumes the user can describe their taste with simple labels (genre, mood) and a target energy number. This is more intended for classroom exploration and demos, rather than real users since the dataset is small and the scoring system cannot capture the full complexity of actual listening behavior.

---

## 3. How the Model Works

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Each song has labels (genre and mood) and numeric features like energy and acousticness. The user gives preferences for genre, mood, and a target energy and can also say if they like acoustic songs. For each song, the model adds points for a matching genre and a matching mood. It also adds more points when the song’s energy is close to the target energy. A small bonus is added if the song matches the acoustic preference. After scoring every song, it sorts all songs by score and returns the top results with short reasonings.  

---

## 4. Data

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset

The catalog has 18 songs in `data/songs.csv`. Each song includes: genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. A few genres are hip hop, pop sofi, synthwave, rock, etc. I added 8 songs to increase genre and mood variety. The dataset is still small and does not include language or listening history.  

---

## 5. Strengths

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition

The system works best when the user has a clear and simple sound in mind, such as “chill lofi” or “intense rock,” because those kinds of preferences are easier for the scoring system to match using genre, mood, and energy. It also performs well when energy level is a major part of the user’s taste, such as choosing music for studying versus working out, since the numeric similarity helps separate calmer songs from more intense ones. Another strength is that the explanations make the recommendations easier to understand because they show why a song scored highly, especially when there is a strong match in category and closeness in energy.

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users

One limitation I noticed is that the dataset is very small, so the same few high-energy songs can appear near the top for very different users. The scoring also assumes that genre and mood labels are perfectly accurate, which can push songs down if they were tagged differently even when they feel like the right genre. If genre match is weighted strongly, the recommender keeps suggesting the same genre instead of mixing in similar songs from other genres.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

For evaluation, I tested multiple user profiles, such as “High-Energy Pop” profile, a “Chill Lofi” profile, a “Deep Intense Rock” profile, and checked whether the top 5 songs made sense based on genre/mood matches and how close the energy value was to the target. One surprise was that songs like “Gym Hero” can show up for different profiles when the user wants high energy, because it has very high energy and low acousticness so it scores well even without a genre match.

---

## 8. Future Work

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes

One useful change would be allowing the user to choose multiple moods or multiple favorite genres instead of being limited to just one, since people’s taste is usually more mixed than a single label can capture. The system could also be improved by adding a simple diversity rule so the top results are not all too similar, such as preventing all five recommendations from coming from the same genre.

---

## 9. Personal Reflection

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps

Working on this project helped me better understand that a recommender system mainly works by scoring everything and then sorting the results. One thing I learned is that even small changes in the weights can completely change which songs rise to the top, which made me realize how much influence design choices have on recommendations. Copilot was helpful for brainstorming possible user profiles and edge cases, but I still had to check the math carefully and make sure the CSV data types actually matched what the scoring logic expected. I find that I have a better understanding of how music recommendation apps work because this project showed me that what feels like a intuitive suggestion is often the result of a series of simple scoring decisions.