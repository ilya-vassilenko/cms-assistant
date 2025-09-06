#!/usr/bin/env python3
"""
Test script for GoogleDocReader class.
Reads Google Doc link from environment variable and tests the reader functionality.
"""

import os
from datetime import date
from google_doc_reader import GoogleDocReader

def main():
    """Test the GoogleDocReader functionality."""
    
    # Get Google Doc link from environment variable
    google_doc_link = os.getenv('GOOGLE_DOC_LINK')
    
    if not google_doc_link:
        print("Error: GOOGLE_DOC_LINK environment variable not set")
        print("Please set it to your Google Sheets URL")
        return
    
    print(f"Using Google Doc link: {google_doc_link}")
    
    # Set target month (you can modify this as needed)
    target_month = date(2025, 8, 1)  
    sheet_name = "AlpineAI"
    
    print(f"Target month: {target_month.strftime('%B %Y')}")
    print(f"Target sheet: {sheet_name}")
    
    # Create GoogleDocReader instance
    reader = GoogleDocReader(google_doc_link, sheet_name, target_month)
    
    # Connect to the sheet
    print("\nConnecting to Google Sheet...")
    if not reader.connect():
        print("Failed to connect to Google Sheet")
        return
    
    # Retrieve work items
    print("\nRetrieving work items...")
    work_items = reader.retrieve_work_items()
    
    if not work_items:
        print("No work items found for the specified month and sheet")
        return
    
    # Print all items
    reader.print_all_items()
    
    # Compute and display total hours
    total_hours = reader.compute_total_hours()
    print(f"\nTotal hours worked: {total_hours:.2f}")
    
    # Additional statistics
    print(f"\nStatistics:")
    print(f"- Number of work items: {len(work_items)}")
    print(f"- Average hours per item: {total_hours/len(work_items):.2f}" if work_items else "- No items to calculate average")
    
    # Show unique topics
    topics = set(item['topic'] for item in work_items if item['topic'])
    if topics:
        print(f"- Unique topics: {', '.join(sorted(topics))}")

if __name__ == "__main__":
    main()
