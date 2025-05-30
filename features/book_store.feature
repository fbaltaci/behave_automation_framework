@book_store
Feature: Book Store API functionality

  @positive
  Scenario: Retrieve all books from the catalog
    When I send a GET request to fetch all books
    Then the response status code should be 200
    And the response should contain a non-empty list of books

  @positive
  Scenario: Retrieve a specific book by ISBN
    When I send a GET request to fetch book with ISBN "9781449325862"
    Then the response status code should be 200
    And the response should contain the book title "Git Pocket Guide"

  @positive
  Scenario: Add a book to the user's collection
    Given I have a valid user and token
    When I send a POST request to add book with ISBN "9781449325862" to the user's account
    Then the response status code should be 201

  @positive
  Scenario: Update a book in the user's collection
    Given I have a valid user and a book with ISBN "9781449325862" in their collection
    When I send a PUT request to replace book with ISBN "9781449325862" with "9781449331818"
    Then the response status code should be 200

  @positive
  Scenario: Delete a book from the user's collection
    Given I have a valid user and a book with ISBN "9781449331818" in their collection
    When I send a DELETE request to remove book with ISBN "9781449331818"
    Then the response status code should be 204