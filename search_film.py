# 상속
# .env : 정보보호
# CRUD를 부모클래스로 


import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

class BaseCRUD:
    def __init__(self, table_name, record_field, primary_key):
        self.conn_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }
        self.table_name = table_name
        self.record_field = record_field
        self.primary_key = primary_key
        self.conn = None
        self.connect()

    def connect(self):
        """데이터베이스에 연결합니다."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("데이터베이스에 성공적으로 연결되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")

    # def create_record(self, record):
    #     """테이블에 새로운 레코드를 추가합니다."""
    #     with self.conn.cursor() as cur:
    #         cur.execute(f"""
    #             INSERT INTO {self.table_name} ({self.record_field})
    #             VALUES (%s) RETURNING {self.primary_key};
    #         """, (record,))
    #         record_id = cur.fetchone()[0]
    #         self.conn.commit()
    #         print(f"레코드 '{record}'이(가) {self.table_name} {record_id}로 추가되었습니다.")
    #         return record_id
        
    def close(self):
        self.conn.close()


class FilmCRUD(BaseCRUD):
    def __init__(self):
        super().__init__('film', 'title', 'film_id')


    def search_films(self, title=None, genre=None, actor_id=None, actor=None):
        """다양한 조건으로 영화를 검색합니다."""
        query = """SELECT f.film_id, f.title, a.actor_id, a.first_name||' '||a.last_name, c."name" 
        FROM film f
        join film_actor fa using(film_id)
        join actor a using(actor_id)
        join film_category fc using(film_id)
        join category c using(category_id)
        WHERE TRUE"""
        parameters = []

        if title:
            query += " AND f.title ILIKE %s" # 대소문자 구분X
            parameters.append(f"%{title}%")

        if genre:
            query += " AND c.name ILIKE %s"
            parameters.append(f"%{genre}%")

        if actor_id:
            query += " AND a.actor_id = %s"
            parameters.append(actor_id)
            
        if actor:
            first_name, last_name = actor.split(" ")
            query += " AND a.first_name ILIKE %s and a.last_name ILIKE %s"
            parameters.append(f"%{first_name}%")
            parameters.append(f"%{last_name}%")

        with self.conn.cursor() as cur:
            cur.execute(query, tuple(parameters))
            movies = cur.fetchall()
            if movies:
                for movie in movies:
                    print(f"Film_ID:{movie[0]}, Title: {movie[1]}, Actor_ID: {movie[2]}, Actor: {movie[3]}, Genre: {movie[4]}")
            else:
                print('검색된 정보가 없습니다.')




# movie_crud.create_record("The Godfather")
# film_crud.search_films(title="Chamber Italian")
# film_crud.search_films(genre="comedy")
# film_crud.search_films(actor_id=1)
# film_crud.search_films(actor="Penelope ")

# 데이터베이스 연결을 닫습니다.
film_crud = FilmCRUD()
print("="*50)
print("안녕하세요 멋사레코드입니다")
while True:
    user_select = input('''찾으시는 영화가 있으신가요? 어떤 방식으로 찾길 원하시나요?
          1. 영화제목으로 찾기
          2. 영화장르로 찾기
          3. 배우이름으로 찾기
          4. 배우번호로 찾기
          q: 프로그램 종료하기 
          :''')
    if user_select == '1' :
        print('영화 제목으로 찾기를 원하시는군요')
        title=input("영화 제목을 입력해주세요:")
        film_crud.search_films(title=title)
    elif user_select == '2' :
        print('영화 장르으로 찾기를 원하시는군요')
        genre=input("영화 장르를 입력해주세요:")
        film_crud.search_films(genre=genre)
    elif user_select == '3' :
        print('배우 이름으로 찾기를 원하시는군요')
        actor_name=input("배우 이름을 입력해주세요:")
        film_crud.search_films(actor=actor_name)
    elif user_select == '4' :
        print('배우 번호로 찾기를 원하시는군요')
        actor_id=input("배우 번호를 입력해주세요:")
        film_crud.search_films(actor_id=actor_id)
    elif user_select =='q':
        print('프로그램이 종료되었습니다')
        break
    
    
film_crud.close()