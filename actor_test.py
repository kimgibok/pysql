# CRUD
# actor table

import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

class CountyCRUD:
    def __init__(self):
        self.conn_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT')
        }
        self.conn = None
        self.connect()

    # 데이터베이스 연결관리
    def connect(self):
        """데이터베이스에 연결합니다."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("데이터베이스에 성공적으로 연결되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")

    def create_actor(self, first_name, last_name):
        """actor 테이블에 새로운 나라를 추가합니다."""
        print(first_name, last_name)
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO actor (first_name, last_name)
                VALUES (%s, %s) RETURNING actor_id;
            """, (first_name,last_name))
            actor_id = cur.fetchone()[0]
            self.conn.commit()
            print(f"배우 '{first_name, last_name}'이(가) actor_id {actor_id}로 추가되었습니다.")
            return actor_id
        
    def read_actor(self, actor_id):
        """actor_id 기반으로 배우 정보를 조회합니다."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM actor WHERE actor_id = %s;",(actor_id,))
            actor = cur.fetchone()
            if actor:
                print(actor)
                return actor
            else:
                print("배우를 찾을 수 없습니다.")
                return None


    def read_all_actor(self):
        """배우 정보를 전체 조회합니다."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM actor;")
            actors = cur.fetchall()
            for actor in actors:
                print(actor)

    def update_actor(self, actor_id, first_name, last_name):
        """actor 정보를 업데이트합니다."""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE actor
                SET (first_name, last_name) = (%s, %s)
                WHERE actor_id = %s;
            """, (first_name, last_name, actor_id))
            self.conn.commit()
            print(f"배우 {actor_id}의 정보가 업데이트되었습니다.")
            
    def delete_actor(self,actor_id):
        """배우 정보를 삭제합니다."""
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM actor WHERE actor_id = %s;", (actor_id,))
            self.conn.commit()
            print(f"actor {actor_id}의 정보가 삭제되었습니다.")
    def close(self):
        self.conn.close()

country_crud = CountyCRUD()
actor_id = country_crud.create_actor("kim","Lion")
country_crud.read_actor(actor_id)
country_crud.read_all_actor()
country_crud.update_actor(actor_id=actor_id, first_name="kim", last_name="gibok")
country_crud.read_actor(actor_id)
country_crud.delete_actor(actor_id)
country_crud.close()
    