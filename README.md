# py-memory-rag
py-memory-rag

# database

CREATE TABLE IF NOT EXISTS MEMORY (
            id serial PRIMARY KEY,
            user_id varchar(10),
            message text,
            vector_data vector(1024)
);

--- hi, my name is Eliezer Antunes
@set vector_data1='[-0.06538654,0.016056776.....,-0.016389577]'

-- My name Eliezer Ribeiro Antunes Junior and I work at Dock 
@set vector_data2='[-0.09992789,0.04000856,....,0.025501434,0.01616083,-0.04475922,0.037032798,-0.07503439]'

-- I work at Dock as an architect and I am Eliezer Antunes
@set vector_data3='[-0.07451753,0.048712887,-....,0.016055588,-0.070429035]'
 
select :vector_data3
SELECT id, user_id ,message,
       1 - (vector_data <=> :vector_data2::vector) AS cosine_similarity,
       ROW_NUMBER() OVER (
               PARTITION BY message 
               ORDER BY 1 - (vector_data <=> :vector_data2::vector) DESC
       ) as rn
FROM MEMORY
WHERE 1 - (vector_data <=> :vector_data2::vector) >= 0.75

# create venv
python3 -m venv .venv

# activate
source .venv/bin/activate

# install requirements
pip install -r requirements.txt

# run
gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app --bind 127.0.0.1:8000
