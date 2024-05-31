from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()
rotten = []
fresh = []
movies = {}

class Body(BaseModel):
   link: str

def read_files():
   file_movies = pd.read_csv('rotten_tomatoes_movies.csv', header=0)
   temp_movies = {}
   
   for index, x in file_movies.iterrows():
      temp_movies[str(x['rotten_tomatoes_link'])] = {
            'title': str(x['movie_title']),
            'info': str(x['movie_info']),
            'critics_consensus': str(x['critics_consensus']),
            'content_rating': str(x['content_rating']),
            'genres': str(x['genres']),
            'directors': str(x['directors']),
            'authors': str(x['authors']),
            'actors': str(x['actors']),
            'original_release_date': str(x['original_release_date']),
            'streaming_release_date': str(x['streaming_release_date']),
            'runtime': str(x['runtime']),
            'production_company': str(x['production_company']),
            'tomatometer_status': str(x['tomatometer_status']),
            'tomatometer_rating': str(x['tomatometer_rating']),
            'tomatometer_count': str(x['tomatometer_count']),
            'audience_status': str(x['audience_status']),
            'audience_rating': str(x['audience_rating']),
            'audience_count': str(x['audience_count']),
            'tomatometer_top_critics_count': str(x['tomatometer_top_critics_count']),
            'tomatometer_fresh_critics_count': str(x['tomatometer_fresh_critics_count']),
            'tomatometer_rotten_critics_count': str(x['tomatometer_rotten_critics_count']),
            'reviews': []
         }
      
   file_reviews = pd.read_csv('rotten_tomatoes_critic_reviews.csv', header=0)

   for index, y in file_reviews.iterrows():
      # create object
      review = {
         'rotten_tomatoes_link': str(y['rotten_tomatoes_link']),
         'critic_name': str(y['critic_name']),
         'top_critic': str(y['top_critic']),
         'publisher_name': str(y['publisher_name']),
         'review_type': str(y['review_type']),
         'review_score': str(y['review_score']),
         'review_date': str(y['review_date']),
         'review_content': str(y['review_content'])
      }

      # get rotten and fresh reviews
      if review['review_type'] == 'Fresh':
         fresh.append(review)
      elif review['review_type'] == 'Rotten':
         rotten.append(review)

      # add reviews to current data
      if str(y['rotten_tomatoes_link']) not in temp_movies.keys():
         new_movie = {
            'title': '',
            'info': '',
            'critics_consensus': '',
            'content_rating': '',
            'genres': '',
            'directors': '',
            'authors': '',
            'actors': '',
            'original_release_date': '',
            'streaming_release_date': '',
            'runtime': '',
            'production_company': '',
            'tomatometer_status': '',
            'tomatometer_rating': '',
            'tomatometer_count': '',
            'audience_status': '',
            'audience_rating': '',
            'audience_count': '',
            'tomatometer_top_critics_count': '',
            'tomatometer_fresh_critics_count': '',
            'tomatometer_rotten_critics_count': '',
            'reviews': [review]
         }
         temp_movies[y['rotten_tomatoes_link']] = new_movie
      else:
         temp_movies[review['rotten_tomatoes_link']]['reviews'].append(review)
         
   return temp_movies

movies = read_files()

@app.get('/get-movie')
async def get_movie(payload: Body):
   if f"m/{payload.link}" not in movies.keys():
      return {
         'error': 'No movies with that code'
      }
   return movies[f'm/{payload.link}']

@app.get('/hello-world')
def read_root():
  return { 'Hello': 'World' }

if __name__ == '__main__':
   uvicorn.run('main:app', port=8000)