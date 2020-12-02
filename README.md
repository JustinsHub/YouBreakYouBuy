# https://youbreakyoubuy.herokuapp.com/
Capstone 1 Proposal (Mini-Ecommerce)
Goal: Build a database-driven website from an API of my choice

# Website Goal
Users who are in need of the products/services presented to the users (yet to find out). 

# User Demographics
*User Demographics*
- Users who are willing to pay for services/product

# Project creation plan
Database Models
> `User`
- Id (primary key)
- username (required, unique)
- password (required)
- first_name (required)
- last_name (required)
- email (required) ```very important to email market for future products```

> `Product`
- Id (primary key)
- product (required)
- product_img 
- inventory 

> `Purchases`
- Id (primary key)
- product_id (ForeignKey required)
- user_id (ForeignKey required)
- purchase date/time
- current_inventory

# API
  - Stripe `for payment`
  
# Potential Issues with API
> Possible issues include:

- Exceeding the limits of the API token quota
- There may be other issues I haven't foreseen

# Sensitive Information
- Users will need to log in. Therefore, passwords will need to be secured.
- Confirming purchases.

# App functionality
- Users can register, login, and logout.
- Users have to login to purchase anything.
- Users are able to see the product/services provided without logging in.

# User workflow
1. Place the product for the user to see right away to create interest and have a call to action (ex: 20% discount off right now (set a timer for discount?).
2. Once signed up, can purchase the product/service.
3. Add to cart. (Set up to have a min/max add on to cart)
4. `optional` Redirect them to product before finalizing a sale to create potential add on to cart.
5. Sale -> send email 

# CRUD features
- Create account
- Make purchases
- Update account/purchases
- Delete account/purchases

# Stretch Goals
- Once the email has been captured. Optimize email marketing.
