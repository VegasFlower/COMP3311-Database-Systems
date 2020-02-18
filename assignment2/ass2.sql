-- COMP3311 19T3 Assignment 2
-- Written by <<Tong Zheng>>
-- z5142003

-- Q1 Which movies are more than 6 hours long? 

create or replace view Q1(title)
as
select main_title as title from titles
where format = 'movie'
and runtime > 360
;


-- Q2 What different formats are there in Titles, and how many of each?

create or replace view Q2(format, ntitles)
as
select format, count(*) as ntitles from titles
group by format
;


-- Q3 What are the top 10 movies that received more than 1000 votes?

create or replace view Q3(title, rating, nvotes)
as
select main_title as title, rating, nvotes from titles
where format = 'movie'
and nvotes > 1000
order by rating desc, main_title asc
LIMIT 10
;


-- Q4 What are the top-rating TV series and how many episodes did each have?

create or replace view Q4(title, nepisodes)
as
select a.main_title as title, count(*) as nepisodes
from titles a left join Episodes b on (a.id = b.parent_id)
where (a.format = 'tvSeries' or a.format = 'tvMiniSeries')
and a.rating=(select max(rating) from titles where format = 'tvSeries' or format = 'tvMiniSeries')
group by b.parent_id, a.id
order by a.main_title
;


-- Q5 Which movie was released in the most languages?

create or replace view Q5(title, nlanguages)
as
select a.main_title as title, max(languages) as nlanguages
from titles as a join (select title_id, count(distinct language) as languages from aliases group by title_id order by count(distinct language) desc limit 1) as b on (a.id=b.title_id)
where a.format = 'movie'
group by a.id
order by max(languages) desc
;


-- Q6 Which actor has the highest average rating in movies that they're known for?

create or replace view Q6(name)
as
select b.name as name
from worked_as as a join names as b on (a.name_id=b.id)
join known_for as c on (b.id = c.name_id)
join titles as d on (c.title_id=d.id)
where 
;

-- Q7 For each movie with more than 3 genres, show the movie title and a comma-separated list of the genres


create or replace view Q7(title,genres)
as
select a.main_title as title, b.genres as genres from titles a join (select title_id, count(*), string_agg(genre,',') as genres from title_genres group by title_id having count(*) > 3) as b on (a.id=b.title_id)
group by a.id, b.genres
having a.format = 'movie'
order by a.main_title
;

-- Q8 Get the names of all people who had both actor and crew roles on the same movie

create or replace view Q8(name)
as
select c.name as name from actor_roles as a join
(select title_id, name_id from crew_roles as x join titles as y on (x.title_id=y.id) where y.format = 'movie')
as b on (a.title_id = b.title_id) and (a.name_id = b.name_id)
join names as c on(a.name_id = c.id)
group by c.id
order by c.name
;

-- Q9 Who was the youngest person to have an acting role in a movie, and how old were they when the movie started?

create or replace view Q9(name,age)
as
select a.name as name, min(c.start_year-a.birth_year) as age from names a join actor_roles b on(a.id=b.name_id) join titles c on(b.title_id=c.id) 
where c.format='movie' 
group by a.name 
order by age 
limit 1
;

-- Q10 Write a PLpgSQL function that, given part of a title, shows the full title and the total size of the cast and crew

create or replace function
	Q10(partial_title text) returns setof text
as $$
...
$$ language plpgsql;

