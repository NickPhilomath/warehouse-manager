finished project task by @NickPhilomath

# Set up project
- install poetry `pip install poetry`
- install dependencies using poetry `poetry install`
- migrate `poetry run python manage.py migrate`
- and finally run the server `poetry run python manage.py runserver`

you can visit localhost on port 8000
main api urls:
- `/api/product-info`
- `/api/products/products`
- `/api/products/materials`
- `/api/products/product-materials`
- `/api/products/partial-warehouse`

you can configure database in `.env` file


to create postgres server using docker
run `docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=pwd -d postgres`
