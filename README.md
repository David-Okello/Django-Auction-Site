# Django Auction Site

Welcome to the Django Auction Site, a web application where users can create auction listings, place bids, and interact with other users through comments. This project follows the specifications provided, allowing users to perform various actions such as creating listings, managing a watchlist, exploring categories, and participating in auctions.

## Features

- **Create Listing:**
  - Users can create new auction listings with a title, description, starting bid, image, and category.
  
- **Active Listings Page:**
  - Displays all currently active auction listings with details such as title, description, current price, and image.

- **Listing Page:**
  - Users can view detailed information about a specific listing.
  - Users can add/remove items from their watchlist.
  - Users can place bids (if signed in), and the bidding system enforces the necessary constraints.
  - The creator of the listing can close the auction, declaring the highest bidder as the winner.

- **Watchlist:**
  - Users can view a dedicated Watchlist page displaying all the listings they have added.

- **Categories:**
  - Users can explore listings based on categories, viewing active listings in each category.

- **Django Admin Interface:**
  - Site administrators have access to the Django admin interface to manage listings, comments, and bids.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/django-auction-site.git 
   ```
2. Install the dependancies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. Access the applications at your locolhost port 8000


## Usage
 1. Create a new auction listing by visiting the "New Listing" page.
 1. Explore active listings on the home page.
 3. Click on a listing to view details, place bids, add to your watchlist, and more.

##  Contributing
If you'd like to contribute to the development of this project, please follow the standard GitHub Fork & Pull Request workflow.
