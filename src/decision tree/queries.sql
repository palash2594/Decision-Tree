
select distinct iris_type from iris_dataset

select count(*) from iris_dataset where iris_type = "Iris-Virginica"

select iris_type, count(iris_type) from iris_dataset group by iris_type



select avg(sepal_length), avg(sepal_width), avg(petal_length), avg(petal_width)
from iris_dataset

select iris_type, count(iris_type) from iris_dataset
where sepal_length < 5.84
group by iris_type


