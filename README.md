# Recipe Management API

## Project Overview
A Recipe Management API built with Django and Django REST Framework to enable users to manage recipes (CRUD operations), view by category or ingredient, and search recipes efficiently. The API also supports user management, authentication, and deployment on platforms like Heroku.

## Features
- **Recipe Management**: Create, Read, Update, Delete recipes with attributes like Title, Ingredients, Instructions, Category, and more.
- **User Management**: CRUD operations for users with authentication and permissions.
- **Search & Filter**: Search by title, category, ingredient, or time, with optional filters for cooking time and servings.
- **Pagination & Sorting**: Efficient pagination and sorting for large recipe datasets.

## Technical Stack
- **Backend**: Django, Django REST Framework
- **Database**: Django ORM
- **Authentication**: Django authentication (JWT optional)
- **Deployment**: Heroku or PythonAnywhere

## Stretch Goals (Optional)
- Recipe ratings & reviews
- Favorite recipes
- Recipe images
- Meal planner & shopping list
- Nutritional information integration

# Getting Started

Follow these steps to set up the Recipe Management API locally using a virtual environment:

## Prerequisites
- Python 3.x
- Django
- Django REST Framework

## 1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

## 2. Set up a virtual environment
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 3. Install Dependencies
```
pip install django djangorestframework
```

## 4. Setup the Database
```
python manage.py makemigrations
python manage.py migrate
```

## 5. Create a superuser
```
python manage.py createsuperuser
```

## 6. Run the development Server
```
python manage.py runserver
```

## 7. You can also opt to test with Postman on the deployed url:
```
https://jamnjeri.pythonanywhere.com/
```
/api/recipes for recipes
/api/ingredients  for ingredients 
/api/categories for categories
