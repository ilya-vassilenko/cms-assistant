#!/usr/bin/env python3
"""
Google Docs Reader Class
Reads work items from Google Sheets based on specified month and sheet name.
"""

import os
import re
from datetime import datetime, date
from typing import List, Dict, Optional
import gspread
from google.oauth2.service_account import Credentials

class GoogleDocReader:
    """
    A class to read work items from Google Sheets.
    
    Attributes:
        url (str): URL to the Google document
        sheet_name (str): Name of the target sheet
        target_month (date): First day of the target month (e.g., 2025-08-01)
        work_items (List[Dict]): List of work items found
    """
    
    def __init__(self, url: str, sheet_name: str, target_month: date):
        """
        Initialize the GoogleDocReader.
        
        Args:
            url (str): URL to the Google document
            sheet_name (str): Name of the target sheet
            target_month (date): First day of the target month (e.g., 2025-08-01)
        """
        self.url = url
        self.sheet_name = sheet_name
        self.target_month = target_month
        self.work_items = []
        self._sheet = None
        self._setup_credentials()
    
    def _setup_credentials(self):
        """Setup Google Sheets credentials."""
        try:
            # Try OAuth2 authentication with custom credentials file
            credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
            if not credentials_path:
                # Try to find the credentials file in common locations
                possible_paths = [
                    '/Users/vasilenkoilya/Documents/7 GitHub Cursor/cms-assistant/.vscode/client_secret_1049835516666-5v9s988evv40904gof6p0i7l93f57go7.apps.googleusercontent.com.json',
                    'credentials.json',
                    'client_secret.json',
                    os.path.expanduser('~/.config/gspread/credentials.json')
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        credentials_path = path
                        break
            
            if credentials_path and os.path.exists(credentials_path):
                print(f"Using credentials file: {credentials_path}")
                try:
                    # Look for authorized_user.json in common locations
                    authorized_user_paths = [
                        '.vscode/authorized_user.json',
                        'authorized_user.json',
                        os.path.expanduser('~/.config/gspread/authorized_user.json')
                    ]
                    
                    authorized_user_path = None
                    for path in authorized_user_paths:
                        if os.path.exists(path):
                            authorized_user_path = path
                            break
                    
                    # Use OAuth2 with custom credentials file
                    self._gc = gspread.oauth(
                        credentials_filename=credentials_path,
                        authorized_user_filename=authorized_user_path
                    )
                    print("Successfully authenticated using OAuth2")
                    return
                except Exception as oauth_error:
                    print(f"OAuth2 authentication failed: {oauth_error}")
                    print("Trying service account authentication...")
                    
                    # Fallback to service account credentials
                    try:
                        scope = ['https://spreadsheets.google.com/feeds',
                                'https://www.googleapis.com/auth/drive']
                        creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
                        self._gc = gspread.authorize(creds)
                        print("Successfully authenticated using service account")
                        return
                    except Exception as sa_error:
                        print(f"Service account authentication also failed: {sa_error}")
            
            # Try default OAuth2 authentication
            try:
                self._gc = gspread.oauth()
                print("Successfully authenticated using default OAuth2")
                return
            except Exception as oauth_error:
                print(f"Default OAuth2 authentication failed: {oauth_error}")
            
            print("No authentication method available.")
            print("Please either:")
            print("1. Set GOOGLE_CREDENTIALS_PATH environment variable to your credentials JSON file")
            print("2. Place your credentials file as 'credentials.json' in the project directory")
            print("3. Run 'gspread auth' to set up OAuth2 authentication")
            self._gc = None
            
        except Exception as e:
            print(f"Error setting up credentials: {e}")
            self._gc = None
    
    def _extract_sheet_id(self, url: str) -> Optional[str]:
        """
        Extract sheet ID from Google Sheets URL.
        
        Args:
            url (str): Google Sheets URL
            
        Returns:
            Optional[str]: Sheet ID if found, None otherwise
        """
        # Pattern to match Google Sheets URL and extract sheet ID
        pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
        match = re.search(pattern, url)
        return match.group(1) if match else None
    
    def _parse_date(self, date_str: str) -> Optional[date]:
        """
        Parse date string into date object.
        
        Args:
            date_str (str): Date string in various formats
            
        Returns:
            Optional[date]: Parsed date or None if parsing fails
        """
        if not date_str or date_str.strip() == '':
            return None
            
        date_str = date_str.strip()
        
        # Try different date formats
        date_formats = [
            '%Y-%m-%d',      # 2025-08-01
            '%m/%d/%Y',      # 08/01/2025
            '%d/%m/%Y',      # 01/08/2025
            '%Y-%m-%d %H:%M:%S',  # 2025-08-01 10:30:00
            '%m/%d/%Y %H:%M:%S',  # 08/01/2025 10:30:00
        ]
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt).date()
                return parsed_date
            except ValueError:
                continue
        
        return None
    
    def _parse_hours(self, hours_str: str) -> float:
        """
        Parse hours string into float.
        
        Args:
            hours_str (str): Hours string
            
        Returns:
            float: Parsed hours or 0.0 if parsing fails
        """
        if not hours_str or hours_str.strip() == '':
            return 0.0
            
        try:
            # Remove any non-numeric characters except decimal point
            cleaned = re.sub(r'[^\d.]', '', str(hours_str))
            return float(cleaned) if cleaned else 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def _is_in_target_month(self, item_date: date) -> bool:
        """
        Check if the item date is within the target month.
        
        Args:
            item_date (date): Date to check
            
        Returns:
            bool: True if date is in target month, False otherwise
        """
        return (item_date.year == self.target_month.year and 
                item_date.month == self.target_month.month)
    
    def connect(self) -> bool:
        """
        Connect to the Google Sheet.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        if not self._gc:
            print("Error: No Google Sheets credentials available")
            return False
        
        try:
            sheet_id = self._extract_sheet_id(self.url)
            if not sheet_id:
                print(f"Error: Could not extract sheet ID from URL: {self.url}")
                return False
            
            # Open the spreadsheet
            spreadsheet = self._gc.open_by_key(sheet_id)
            
            # Get the specific worksheet
            try:
                self._sheet = spreadsheet.worksheet(self.sheet_name)
            except gspread.WorksheetNotFound:
                print(f"Error: Worksheet '{self.sheet_name}' not found")
                return False
            
            print(f"Successfully connected to sheet: {self.sheet_name}")
            return True
            
        except Exception as e:
            print(f"Error connecting to Google Sheet: {e}")
            return False
    
    def retrieve_work_items(self) -> List[Dict]:
        """
        Retrieve all work items from the specified sheet for the target month.
        
        Returns:
            List[Dict]: List of work items with keys: date, topic, working_item, hours
        """
        if not self._sheet:
            print("Error: Not connected to sheet. Call connect() first.")
            return []
        
        self.work_items = []
        
        try:
            # Get all values from the sheet
            all_values = self._sheet.get_all_values()
            
            if not all_values:
                print("No data found in the sheet")
                return []
            
            # Process each row (skip header if present)
            for row_idx, row in enumerate(all_values):
                if len(row) < 4:  # Need at least 4 columns
                    continue
                
                # Parse date from column A
                date_str = row[0] if len(row) > 0 else ''
                item_date = self._parse_date(date_str)
                
                if not item_date:
                    continue  # Skip rows without valid dates
                
                # Check if date is in target month
                if not self._is_in_target_month(item_date):
                    continue
                
                # Extract work item data
                topic = row[1] if len(row) > 1 else ''
                working_item = row[2] if len(row) > 2 else ''
                hours_str = row[3] if len(row) > 3 else ''
                hours = self._parse_hours(hours_str)
                
                work_item = {
                    'date': item_date,
                    'topic': topic.strip(),
                    'working_item': working_item.strip(),
                    'hours': hours
                }
                
                self.work_items.append(work_item)
            
            print(f"Found {len(self.work_items)} work items for {self.target_month.strftime('%B %Y')}")
            return self.work_items
            
        except Exception as e:
            print(f"Error retrieving work items: {e}")
            return []
    
    def print_all_items(self):
        """Print all work items found."""
        if not self.work_items:
            print("No work items found.")
            return
        
        print(f"\nWork Items for {self.target_month.strftime('%B %Y')}:")
        print("-" * 80)
        print(f"{'Date':<12} {'Topic':<20} {'Working Item':<30} {'Hours':<8}")
        print("-" * 80)
        
        for item in self.work_items:
            date_str = item['date'].strftime('%Y-%m-%d')
            print(f"{date_str:<12} {item['topic']:<20} {item['working_item']:<30} {item['hours']:<8.2f}")
        
        print("-" * 80)
    
    def compute_total_hours(self) -> float:
        """
        Compute the sum of hours worked for all items.
        
        Returns:
            float: Total hours worked
        """
        return sum(item['hours'] for item in self.work_items)
    
    def get_work_items(self) -> List[Dict]:
        """
        Get the list of work items.
        
        Returns:
            List[Dict]: List of work items
        """
        return self.work_items
    
    def read_currency_and_hourly_rate(self) -> tuple:
        """
        Read currency and hourly rate from the Google Sheet.
        
        Returns:
            tuple: (currency, hourly_rate) where currency is str and hourly_rate is float
            
        Raises:
            ValueError: If cells are empty or contain invalid data
        """
        if not self._sheet:
            raise ValueError("Not connected to sheet. Call connect() first.")
        
        try:
            # Read currency from cell E1 (row 1, column 5 in 1-based indexing)
            currency = self._sheet.cell(1, 5).value  # E1
            if not currency:
                raise ValueError("Cell E1 (currency) is empty in Google Sheet!")
            
            # Read hourly rate from cell E2 (row 2, column 5 in 1-based indexing)
            hourly_rate_str = self._sheet.cell(2, 5).value  # E2
            if not hourly_rate_str:
                raise ValueError("Cell E2 (hourly rate) is empty in Google Sheet!")
            
            try:
                hourly_rate = float(hourly_rate_str)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid hourly rate in cell E2: '{hourly_rate_str}'")
            
            return (currency, hourly_rate)
            
        except Exception as e:
            raise ValueError(f"Error reading currency and hourly rate from Google Sheet: {e}")
