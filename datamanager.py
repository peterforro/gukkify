from db_connection import connection_handler
from psycopg2 import sql
import bcrypt, uuid



def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')



def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)



def create_random_filename(filename):
    filename = filename.split('.')
    filename[0] = str(uuid.uuid4())
    return '.'.join(filename)



@connection_handler
def verify_session(cursor,user_id):
    query = """ SELECT id FROM users 
                WHERE id=%(user_id)s  """
    params = {'user_id':user_id}
    cursor.execute(query,params)
    return 1 == len(cursor.fetchall())



@connection_handler
def add_user_to_db(cursor, user_data):
    user_data['password'] = hash_password(user_data['password'])
    query = """ INSERT INTO users (user_name,email,password)
                VALUES (%(user_name)s,%(email)s,%(password)s)   """
    cursor.execute(query, user_data)



@connection_handler
def get_user_by_email(cursor,email):
    query = ''' SELECT * from users
                WHERE email=%(email)s   '''
    params = {"email":email}
    cursor.execute(query,params)
    return cursor.fetchone()



@connection_handler
def confirm_account(cursor,user_name):
    query = ''' UPDATE users
                SET confirmed=true
                WHERE user_name=%(user_name)s   '''
    params = {'user_name':user_name}
    cursor.execute(query,params)



@connection_handler
def add_file_to_db(cursor, data):
    query = ''' INSERT INTO files (post_id,user_id,category,filename)
                VALUES (%(post_id)s,%(user_id)s,%(category)s,%(filename)s)'''
    cursor.execute(query,data)



@connection_handler
def add_post_to_db(cursor,data):
    query = ''' INSERT INTO posts (submission_time,story,user_id,title)
                VALUES (%(submission_time)s,%(story)s,%(user_id)s,%(title)s);
                SELECT MAX(id) AS id FROM posts;'''
    cursor.execute(query,data)
    return cursor.fetchone()['id']



@connection_handler
def remove_file_from_db(cursor, filename):
    query = ''' DELETE FROM files    
                where filename=%(filename)s'''
    params = {'filename':filename}
    cursor.execute(query,params)



@connection_handler
def get_filename_by_id(cursor,picture_id):
    query = ''' SELECT filename FROM files
                WHERE id=%(picture_id)s '''
    params = {'picture_id':picture_id}
    cursor.execute(query,params)
    return cursor.fetchone()['filename']



@connection_handler
def get_files(cursor):
    query = ''' SELECT filename FROM files'''
    cursor.execute(query)
    return cursor.fetchall()



@connection_handler
def get_posts(cursor):
    query = ''' SELECT * FROM posts'''
    cursor.execute(query)
    return cursor.fetchall()



@connection_handler
def get_post(cursor,post_id):
    query = ''' SELECT * FROM posts
                WHERE id=%(post_id)s'''
    params = {'post_id':post_id}
    cursor.execute(query,params)
    return cursor.fetchone()



@connection_handler
def get_post_files(cursor,post_id):
    query = ''' SELECT * FROM files
                WHERE post_id=%(post_id)s'''
    params = {'post_id':post_id}
    cursor.execute(query,params)
    return cursor.fetchall()


@connection_handler
def delete_records(cursor,table):
    query = sql.SQL('DELETE FROM {}').format(sql.Identifier(table))
    cursor.execute(query)
